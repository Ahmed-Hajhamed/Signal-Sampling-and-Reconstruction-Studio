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
  

Uploading Screen Recording 2024-12-31 at 2.50.44 PM.mov…



### 3. Additive Noise
- **Noise Control**: Add noise to the signal with adjustable Signal-to-Noise Ratio (SNR).
- **Noise Analysis**: Display how noise effects depend on the signal frequency.


Uploading Screen Recording 2024-12-31 at 9.14.55 PM.mov…


### 4. Real-time Updates
- Perform sampling and recovery in real time as the user interacts with the application.
- Eliminate the need for manual updates or refresh buttons.

### 5. Multiple Reconstruction Methods
- **Exploration**: Provide a selection of reconstruction methods beyond Whittaker–Shannon for comparison.
- **Customization**: Let users choose the reconstruction method via a combobox.
- **Educational Examples**: Include signal examples highlighting the advantages and limitations of each method.

### 6. Resizable UI
- Ensure the application layout adjusts seamlessly to window resizing without disrupting usability or aesthetics.

### 7. Different Sampling Scenarios
- Prepare and include at least three synthetic testing signals to demonstrate sampling scenarios. Examples include:
  1. **Mix of 2Hz and 6Hz Sinusoids**:
     - **Scenario**: When sampled at ≥12Hz, the signal recovers accurately.
     - **Alias Check**: When sampled at 4Hz, the two frequencies appear as one.
     - **Intermediate Case**: Sampling at 8Hz.
  2. **Scenario 2**: A signal exploiting aliasing effects with non-integer frequency ratios.
  3. **Scenario 3**: A signal demonstrating frequency-domain noise effects on sampling and recovery.

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

## Future Enhancements
- Expand reconstruction method options.
- Provide support for real-world signal inputs via hardware integration.
- Add advanced noise analysis tools.

## References
- [Nyquist–Shannon Sampling Theorem](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem)
- [Whittaker–Shannon Interpolation Formula](https://en.wikipedia.org/wiki/Whittaker%E2%80%93Shannon_interpolation_formula)
