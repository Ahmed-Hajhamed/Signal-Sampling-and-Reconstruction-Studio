
# Signal Sampling and Recovery Desktop Application

## Introduction
Sampling an analog signal is a crucial step in any digital signal processing system. The Nyquist–Shannon sampling theorem guarantees full recovery of the signal when sampling at a frequency greater than or equal to the signal's bandwidth (or double the maximum frequency for real signals). This project demonstrates the principles of signal sampling and recovery while validating the Nyquist rate.

## Features

### 1. Sample & Recover
- **Visualization**: Load and visualize a mid-length signal (approximately 1000 points).
- **Sampling**: Sample the signal at different frequencies, displayed either as actual frequency values or normalized values (e.g., ranging from 0×fmax to 4×fmax).
- **Recovery**: Reconstruct the original signal using the Whittaker–Shannon interpolation formula.
- **Graphical Outputs**: Four graphs to display:
  1. Original signal with sampled points marked.
  2. Reconstructed signal.
  3. Difference between the original and reconstructed signals.
  4. Frequency domain visualization to detect aliasing.
- **User Interface**: Arrange the graphs conveniently to ensure ease of use.
![Screenshot 2025-01-06 192614](https://github.com/user-attachments/assets/3206ae0e-d280-4ed5-babf-faf39cddf3b9)

### 2. Load & Compose
- **Signal Loading**: Load signals from a file or create them using an integrated signal mixer.
- **Signal Mixer**: Add and combine multiple sinusoidal signals with different frequencies and magnitudes.
- **Editable Components**: Allow removal of individual components while preparing the mixed signal.
- **Default Values**: Ensure the interface is never empty and provides default signals for immediate use.
![Screenshot 2025-01-06 192756](https://github.com/user-attachments/assets/9e4f5416-9e4c-43fd-9356-a0fb1dc2b834)

### 3. Additive Noise
- **Noise Control**: Add noise to the signal with adjustable Signal-to-Noise Ratio (SNR).
- **Noise Analysis**: Display how noise effects depend on the signal frequency.
![Screenshot 2025-01-06 193045](https://github.com/user-attachments/assets/aac93362-83cd-4c52-b7a0-77f929582992)

### 4. Real-time Updates
- Perform sampling and recovery in real time as the user interacts with the application.
- Eliminate the need for manual updates or refresh buttons.

### 5. Multiple Reconstruction Methods
- **Whittaker–Shannon, spline interpolation, and Fourier.**:
  - **Whittaker–Shannon**
  - ![Screenshot 2025-01-06 192756](https://github.com/user-attachments/assets/2bdbd2ee-6f3e-4ed0-a514-f6b79f03a6a9)
  - **Cubic Spline i Interpolation**
  - ![Screenshot 2025-01-06 192614](https://github.com/user-attachments/assets/1f94132c-b473-4ec4-bf57-907c7673b12b)
  - **Low-Pass Filter**
  - ![Screenshot 2025-01-06 192647](https://github.com/user-attachments/assets/446b4413-d480-47ac-a342-9386ebbcb7df)

- **Customization**: Users can select the reconstruction method using a combobox.
![re](https://github.com/user-attachments/assets/9c8ca41e-f1dd-4a91-8825-3f6e7747ab56)

## Technologies Used
- **Programming Language**: Python
- **Framework**: PyQt or PySide for GUI development
- **Visualization**: Matplotlib or PyQtGraph for dynamic graphing
- **Signal Processing**: NumPy and SciPy libraries

## Installation
1. Clone this repository:
  ```bash
  git clone https://github.com/Ahmed-Hajhamed/Signal-Sampling-and-Reconstruction-Studio
  ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. Launch the application.
2. Load or compose a signal using the interface.
3. Adjust sampling frequency and observe real-time changes in recovery and aliasing.
4. Add noise and experiment with different SNR values.
5. Compare reconstruction methods to explore their pros and cons.

## References
- [Nyquist–Shannon Sampling Theorem](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem)
- [Whittaker–Shannon Interpolation Formula](https://en.wikipedia.org/wiki/Whittaker%E2%80%93Shannon_interpolation_formula)
