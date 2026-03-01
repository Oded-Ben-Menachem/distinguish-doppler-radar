import numpy as np
import matplotlib.pyplot as plt



FFT_SIZE = 1024
FREQUENCY_SIZE = 5000
FREQUENCY_ASIX = FREQUENCY_SIZE/FFT_SIZE
EPSILON = 1e-9

np.set_printoptions(suppress=True, precision=5)


#-----step 1 - filter the samples-----

def high_pass_filter(matrix, cut_off):
    matrix[:,:cut_off] = 0
    return matrix

def low_pass_filter(matrix, cut_off):
    matrix[:,-cut_off:] = 0
    return matrix



def smooth_time_axis(matrix):
    padded = np.pad(matrix, ((1, 0), (0, 0)), mode='edge')
    
    smoothed = (padded[:-1, :] + padded[1:, :]) / 2.0
    return smoothed

def smooth_freq_axis(matrix):
    padded = np.pad(matrix, ((0, 0), (2, 2)), mode='edge')
    smoothed = (padded[:, :-4] + padded[:, 1:-3]  + padded[:, 2:-2] + padded[:, 3:-1]+ padded[:, 4:]) / 5.0
    return smoothed

def snr(matrix ,cut_off):
    signal_power = np.max(matrix, axis = 1)
    median = np.median(matrix, axis=1)
    snr_vector = signal_power/(median + EPSILON)
    snr_vector =  10*np.log10(snr_vector + EPSILON)
    zero_under_vector = snr_vector > cut_off
    #print(zero_under_vector.shape, matrix.shape)
    #print(snr_vector)
    without_noise_matrix = matrix[zero_under_vector,:]
    #print(without_noise_matrix.shape)
    return without_noise_matrix


def delete_under_threshold(matrix,thres):
    new_matrix = matrix.copy()
    mean = np.mean(new_matrix, axis =1)
    threshold = mean*thres
    threshold = threshold[:,np.newaxis]
    new_matrix[new_matrix<threshold] = 0
    return new_matrix


def clean_noise(matrix):
    row_max = np.max(matrix, axis = 1)
    without_noise = row_max >1000
    clean_matrix = matrix[without_noise]
    return clean_matrix


#-----part 2 - prosses the data for clustering-----

def calculate_spectral_bandwidth(matrix):
    index_vector = np.arange(matrix.shape[1])            # Create index array (0-511)
    frequency_vector = index_vector*FREQUENCY_ASIX
    Fc = frequency_vector@matrix.T/(np.sum(matrix, axis = 1)+EPSILON)
    bandwidth = (matrix@((frequency_vector)**2))/(np.sum(matrix, axis = 1)+EPSILON)
    bandwidth = np.sqrt(bandwidth-Fc**2)
    return bandwidth.flatten()


def calculate_spectral_kurosis(matrix):
    index_vector = np.arange(matrix.shape[1])
    power = np.sum(matrix, axis =1,keepdims = True) + EPSILON
    center = (matrix@index_vector.reshape(-1,1))/power
    delta = index_vector-center
    m2 = np.sum(matrix * (delta**2), axis=1, keepdims=True) / power # variance
    m4 = np.sum(matrix * (delta**4), axis=1, keepdims=True) / power # the 4'th moment
    #print(m2.shape,m4.shape)

    kurosis = m4/(m2**2 + EPSILON)
    return kurosis

def peak_to_average(matrix):
    peak_to_average = np.max(matrix, axis=1) / (np.mean(matrix, axis=1) + EPSILON)
    return peak_to_average

def calculate_spectral_skewness(matrix):
    index_vector = np.arange(matrix.shape[1])
    power = np.sum(matrix, axis =1,keepdims = True) + EPSILON
    center = (matrix@index_vector.reshape(-1,1))/power
    delta = index_vector-center
    m3 = np.sum(matrix * (delta**3), axis=1, keepdims=True) / power
    m2 = np.sum(matrix * (delta**2), axis=1, keepdims=True) / power # variance
    skewness = m3 / (np.sqrt(m2)**3 + EPSILON)
    return skewness
    
def calculate_spectral_rolloff(matrix, alpha=0.95):
    cumulative_energy = np.cumsum(matrix, axis=1)
    total_energy = cumulative_energy[:, -1:] 
    threshold_mask = cumulative_energy >= (alpha * total_energy)
    rolloff_indices = np.argmax(threshold_mask, axis=1)
    return rolloff_indices



def create_clustering_matrix(radar_matrix, HP_cutoff, noise,threshold,file_name):
    #radar_matrix = low_pass_filter(radar_matrix,LP_cutoff)
    radar_matrix = high_pass_filter(radar_matrix,HP_cutoff)
    radar_matrix = smooth_freq_axis(radar_matrix)
    #radar_matrix = smooth_time_axis(radar_matrix)
    radar_matrix = snr(radar_matrix,noise)
    radar_matrix = delete_under_threshold(radar_matrix,threshold)
    radar_matrix = clean_noise(radar_matrix)

    CSB = calculate_spectral_bandwidth(radar_matrix).flatten()
    CSK = calculate_spectral_kurosis(radar_matrix).flatten()
    PTA = peak_to_average(radar_matrix).flatten()
    CSS = calculate_spectral_skewness(radar_matrix).flatten()
    CSKK = calculate_spectral_rolloff(radar_matrix).flatten()
    Total_Power = np.sum(radar_matrix, axis=1).flatten()
    clustering_matrix = np.column_stack([CSB,CSK,PTA,CSS,CSKK,Total_Power])
    np.save(file_name ,clustering_matrix)
    
def create_clustering_matrix_real_time(radar_matrix, HP_cutoff, noise,threshold):
    radar_matrix = high_pass_filter(radar_matrix,HP_cutoff)
    radar_matrix = smooth_freq_axis(radar_matrix)
    radar_matrix = snr(radar_matrix,noise)
    radar_matrix = delete_under_threshold(radar_matrix,threshold)
    radar_matrix = clean_noise(radar_matrix)

    CSB = calculate_spectral_bandwidth(radar_matrix).flatten()
    CSK = calculate_spectral_kurosis(radar_matrix).flatten()
    PTA = peak_to_average(radar_matrix).flatten()
    CSS = calculate_spectral_skewness(radar_matrix).flatten()
    CSR = calculate_spectral_rolloff(radar_matrix).flatten()
    TP = np.sum(radar_matrix, axis=1).flatten()
    clustering_matrix = np.column_stack([CSB,CSK,PTA,CSS,CSR,TP])
    
    return clustering_matrix

if __name__ == "__main__":
    radar_matrix = np.load('radar_matrix.npy')
    radar_matrix = high_pass_filter(radar_matrix,10)
    #radar_matrix = low_pass_filter(radar_matrix,1)
    radar_matrix = smooth_freq_axis(radar_matrix)
    #radar_matrix = smooth_time_axis(radar_matrix)
    radar_matrix = snr(radar_matrix,8)
    radar_matrix = delete_under_threshold(radar_matrix,4)
    radar_matrix = clean_noise(radar_matrix)

    
    #radar_matrix = clean_noise(radar_matrix)


   
    soccer1 = np.load('soccer1.npy')
    soccer2 = np.load('soccer2.npy')
    soccer3 = np.load('soccer3.npy')
    soccer4 = np.load('soccer4.npy')
    soccer5 = np.load('soccer5.npy')
    soccer6 = np.load('soccer6.npy')
    soccer7 = np.load('soccer7.npy')
    soccer = np.vstack((soccer1,soccer2,soccer3,soccer4,soccer5,soccer6,soccer7))
    create_clustering_matrix(soccer,10,8,3,'soccer1_for_forest.npy')
   

    tennis1 = np.load('tennis1.npy')
    tennis2 = np.load('tennis2.npy')
    tennis3 = np.load('tennis3.npy')
    tennis4 = np.load('tennis4.npy')
    tennis5 = np.load('tennis5.npy')
    tennis6 = np.load('radar_matrix.npy')
    tennis7 = np.load('tennis7.npy')
    tennis8 = np.load('tennis8.npy')


    tennis = np.vstack((tennis1,tennis2,tennis3,tennis4,tennis5,tennis6,tennis7,tennis8))
    create_clustering_matrix(tennis,10,8,3,'tennis1_for_forest.npy')

    


    #radar_matrix = clean_noise(radar_matrix)
    
    plt.figure(figsize=(12, 6))
    fs = 5000
    # Transpose the matrix so time is on the X axis
    # We use vmin/vmax to ignore the low noise and highlight the movement
    plt.imshow(radar_matrix.T, aspect='auto', origin='lower', 
            cmap='jet', extent=[0, len(radar_matrix), 0, fs/2],
            vmin=500, vmax=5000) # Adjust vmax to see the jump clearly

    plt.title('Radar Movement Over Time (Spectrogram)')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time (Block Index)')
    plt.ylim(0, 2500) # Focus on movement range
    plt.colorbar(label='Signal Strength')
    plt.show()
    


    

