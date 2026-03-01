


# Radar Object Classification: Football vs. Tennis Ball

This project uses an HB100 Doppler Radar and an ESP32 to distinguish between a football and a tennis ball. The system analyzes the frequency of the radar signal and provides real-time feedback using LEDs.

### Project Demo
https://github.com/user-attachments/assets/560f44b9-72be-4c11-99da-892df91c4005

---

## Hardware Design
The signal from the HB100 radar is very weak, so I built a custom amplification circuit:

* **Two-Stage Amplification:** I used two amplifier stages to keep the signal clean and stable.
* **Filtering:** Capacitors are used to remove DC noise and focus only on the movement (Doppler shift).
* **ESP32 Compatibility:** The circuit adds a 1.65V offset so the ESP32 can read the full signal wave correctly.

<img width="512" height="369" alt="image" src="https://github.com/user-attachments/assets/1a499dc5-28ce-4dc4-82cb-1aff8bad70a5" />


---

## Signal Processing & Machine Learning

### 1. Data Collection
I first recorded many samples of both balls being thrown at the radar. I used a DFT (Discrete Fourier Transform) to look at the signal in the frequency domain.

<img width="1489" height="843" alt="צילום מסך 2026-03-01 174832" src="https://github.com/user-attachments/assets/d5360088-65b7-45d2-82b5-ec032c35aecf" />
Tennis ball
<img width="1457" height="832" alt="צילום מסך 2026-03-01 174802" src="https://github.com/user-attachments/assets/482bdb52-50b4-4ff7-be39-2b9249fd04db" />
Soccer ball

### 2. Choosing the Model
Initially, I tried using K-means clustering to separate the data, but the signatures of the balls were too similar for an unsupervised model. To get better accuracy, I switched to Supervised Learning, which allowed the system to learn the specific patterns of each ball.

### 3. Real-Time Logic
In real-time mode, the system follows these steps:
1. Captures the radar signal.
2. Applies an SNR (Signal-to-Noise Ratio) filter and a threshold to ignore background noise.
3. Processes the data through the ML model.
4. Turns on the LEDs based on the result.

---

##  Results
The classification is indicated by two LEDs:
*  **Red LED:** Tennis Ball detected.
*  **Yellow LED:** Football detected.

---

## Project Structure
* **ESP32-Code:** C++ code for signal acquisition and LED control.
* **ML-Python:** Python scripts for model training and real-time classification.
