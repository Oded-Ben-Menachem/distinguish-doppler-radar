
import serial
import numpy as np
from secendary_sample_prosess import create_clustering_matrix_real_time
import matplotlib.pyplot as plt
import joblib



model = joblib.load('radar_recognize_ball_model.pkl')




# Settings
SAMPLING_INTERVAL = 200e-6
port = 'COM3'
serial_speed = 921600
samples_num = 1024


# Connect to ESP32
my_data = serial.Serial(port, serial_speed, timeout=1)

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

                   
try:
    i = 0
    while i<100:
        data = get_sampels()
       
        if data is not None:
            fft_data = fft_for_samples(data,3)
            fft_data = fft_data.reshape(1,-1)
            ready_for_forest = create_clustering_matrix_real_time(fft_data,10,8,4)
            
            if len(ready_for_forest) > 0:
                prediction = model.predict(ready_for_forest)
                if prediction[0] == 'T':
                    print('Tennis ball')
                    my_data.write(b'T')
                if prediction[0] == 'S':
                    print('Soccer ball')
                    my_data.write(b'S')
            i+=1
except KeyboardInterrupt:
    print("Stopping")
    my_data.close()



