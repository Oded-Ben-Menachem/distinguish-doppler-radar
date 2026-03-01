import serial
import numpy as np
import matplotlib.pyplot as plt

SAMPLING_INTERVAL = 200e-6
port = 'COM3'
serial_speed = 921600
samples_num = 1024
samples_amount = 20

np.set_printoptions(suppress=True, precision=4)

def fft_for_samples(sample, window_size):
    kernal = np.ones(window_size)/window_size
    
    moving_avarage_filter = np.convolve(sample,kernal,mode='same')
    clean_DC = moving_avarage_filter - np.mean(moving_avarage_filter)
    
    # This reduces spectral leakage
    h_window = np.hanning(len(clean_DC))
    windowed = clean_DC * h_window
    
    fft_signal = np.fft.fft(windowed,samples_num)
   # Keep only the first half (positive frequencies) due to FFT symmetry for real signals
    magnitude = np.abs(fft_signal[:samples_num//2])

    fft_matrix = magnitude
    return fft_matrix

def get_sampels():
    while True:
        if my_data.read(1) == b'\xaa':
            if my_data.read(1) == b'\xbb':
                sample_bytes = my_data.read(samples_num*2)
                if my_data.read(1) == b'\xcc' and my_data.read(1) == b'\xdd':
                    return np.frombuffer(sample_bytes, dtype='<u2')
                else:
                    print('Error')



# Connect to ESP32
my_data = serial.Serial(port, serial_speed, timeout=1)



data_matrix = []
for sample in range(samples_amount):
    data = get_sampels()
    #plt.figure(figsize=(12, 6))
    #plt.plot(data, label='Signal')
    #print(len(data))
    data = fft_for_samples(data,3)
    #print(data)
    data_matrix.append(data)
data_matrix = np.array(data_matrix)

print(data_matrix.shape)


    
def high_pass_filter(matrix, cut_off):
    new_matrix = matrix.copy()
    new_matrix[:,:cut_off]=0
    return new_matrix
    



radar_matrix = np.array(data_matrix)
np.save('radar_matrix.npy',radar_matrix )

#np.save('next_prossing_step.npy', radar_matrix)
#np.save('soccer1.npy', radar_matrix)
#np.save('soccer2.npy', radar_matrix)
#np.save('soccer3.npy', radar_matrix)
#np.save('soccer4.npy', radar_matrix)
#np.save('soccer5.npy', radar_matrix)
#np.save('soccer6.npy', radar_matrix)
#np.save('soccer7.npy', radar_matrix)
#np.save('tennis1.npy', radar_matrix)
#np.save('tennis2.npy', radar_matrix)
#np.save('tennis3.npy', radar_matrix)
#np.save('tennis4.npy', radar_matrix)
#np.save('tennis5.npy', radar_matrix)
#np.save('tennis6.npy', radar_matrix)
#np.save('tennis7.npy', radar_matrix)
#np.save('tennis8.npy', radar_matrix)
#np.save('noise.npy',radar_matrix)


# Create the Spectrogram (Heatmap)
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
plt.ylim(0, 500) # Focus on movement range
plt.colorbar(label='Signal Strength')
plt.show()
