
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
![sampling theory](https://github.com/user-attachments/assets/ff5e6de0-1abf-4df7-8e6e-e13a4c41040b)

### 2. Load & Compose
- **Signal Loading**: Load signals from a file or create them using an integrated signal mixer.
- **Signal Mixer**: Add and combine multiple sinusoidal signals with different frequencies and magnitudes.
- **Editable Components**: Allow removal of individual components while preparing the mixed signal.
- **Default Values**: Ensure the interface is never empty and provides default signals for immediate use.
![load and compase](https://github.com/user-attachments/assets/7e9d5c19-d0a1-44cc-bc42-24e44d4a7313)

### 3. Additive Noise
- **Noise Control**: Add noise to the signal with adjustable Signal-to-Noise Ratio (SNR).
- **Noise Analysis**: Display how noise effects depend on the signal frequency.
![Screen Shot 2024-12-31 at 9 19 51 PM](https://github.com/user-attachments/assets/933e0641-df73-4af7-8c53-662593bd9921)


### 4. Real-time Updates
- Perform sampling and recovery in real time as the user interacts with the application.
- Eliminate the need for manual updates or refresh buttons.

### 5. Multiple Reconstruction Methods
- **Whittaker–Shannon, spline interpolation, and Fourier.**:
  - **Whittaker–Shannon**
    ![Screen Shot 2024-12-31 at 9 34 14 PM](https://github.com/user-attachments/assets/deac92ec-10e5-4d65-935a-beec3402ed76)
  - **spline interpolation**
    ![Screen Shot 2024-12-31 at 9 35 22 PM](https://github.com/user-attachments/assets/8767642a-797d-4391-8855-20c7c32da784)
  - **Fourier interpolation**
    ![Screen Shot 2024-12-31 at 9 36 26 PM](https://github.com/user-attachments/assets/676f8e51-4cd5-4296-8ac4-7d76ba88b3c8)

- **Customization**: Users can select the reconstruction method using a combobox.
- ![Screen Shot 2024-12-31 at 9 33 08 PM](https://github.com/user-attachments/assets/6853db38-f3bd-41d6-92a0-5025204fa837)

## Technologies Used
- **Programming Language**: Python
- **Framework**: PyQt or PySide for GUI development
- **Visualization**: Matplotlib or PyQtGraph for dynamic graphing
- **Signal Processing**: NumPy and SciPy libraries

## Installation
1. Clone this repository.
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
