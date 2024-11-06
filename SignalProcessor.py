import sys
import numpy as np
from Reconstruction import Reconstruction
from scipy.fft import dct
from scipy.interpolate import interp1d
class  SignalProcessor:
    def __init__(self):
        super().__init__()

    def sample_signal(self, signal, sampling_frequency):
        # This function uses different methods to take samples (uniform, non-uniform, or threshold sampling)
        """
        Creates samples from a signal based on the method chosen; uniform, non-uniform or threshold sampling.
        """
        time_data = signal[0]
        amplitude_data = signal[1]

        if sampling_frequency is None:
            raise ValueError("Sampling frequency must be specified.")
        if sampling_frequency != 0:
            sampling_interval = (1 / sampling_frequency)  # samples per interval
            sampled_points_time = np.arange(0, 2, sampling_interval)

            # Calculate the sampled indices using np.searchsorted
            sampled_indices = np.searchsorted(time_data, sampled_points_time)

            # To ensure we don't go out of bounds, you might want to filter sampled_indices
            # Keep only valid indices
            sampled_indices = sampled_indices[sampled_indices < len(time_data)]

            # Collect the sampled points
            sampled_points = amplitude_data[sampled_indices]
            sampled_points_time = time_data[sampled_indices]
            sampled_signal = np.array([sampled_points_time, sampled_points])
        else:
            sampled_signal = np.array([[], []])

        return sampled_signal

    def recover_signal(self, sampled_points, sampling_frequency, method="Whittaker Shannon"):
        """
        Reconstructs original signal from sampled points based on 3 methods; Niquist-Shannon,...
        """
        recovered_signal = None
        duration = 2
        uniform_time_points = np.arange(0, duration, 1 / sampling_frequency)
        if method == 'Whittaker Shannon':
            recovered_signal = Reconstruction.whittaker_shannon(sampled_points, sampling_frequency)

        elif method == 'Fourier':
            recovered_signal = Reconstruction.fourier(sampled_points , sampling_frequency)

        elif method == 'Spline':
            recovered_signal = Reconstruction.spline(sampled_points)
    
        else:
            raise ValueError("Invalid method. Choose 'whittakerShannon', compressedSensing or levelCrossing")
        
        return recovered_signal

    def calculate_difference(self,signal,  recovered_signal):
        # Calculate the difference between original and recovered signals
        # Outputs signals_difference in a 2D numpy array
        """
        Calculates the error in the recovered signal (difference between original and recovered signal).
        #         """

        original_signal_time = signal[0]
        original_signal_values = signal[1]

        recovered_signal_time = recovered_signal[0]
        recovered_signal_values = recovered_signal[1]
        # Align recovered signal with original signal time
        recovered_signal_values = self.align_signals(original_signal_time, original_signal_values, recovered_signal_time, recovered_signal_values)

        recovered_signal_values = np.pad(recovered_signal_values,
                                         (0, len(original_signal_values) - len(recovered_signal_values)),
                                         "constant")

        magnitude_difference = np.abs(original_signal_values - recovered_signal_values)

        signals_difference = np.array([original_signal_time, magnitude_difference])
        
        return signals_difference

    @staticmethod
    def frequency_domain(recovered_signal, sampling_frequency):
        # Perform Fourier transform to check for aliasing
        """
        Returns the full frequency domain of recovered signal.
        """
        # Extract time and signal values
        signal = recovered_signal[1]
     
        time_intervals = 1 / sampling_frequency  #time interval between samples
        
        # Number of samples
        number_of_samples = len(signal)
        
        # Perform FFT to get frequency components
        freq_spectrum = np.fft.fft(signal)
        
        # Generate the full range of frequency bins
        frequency_components = np.fft.fftfreq(number_of_samples, d=time_intervals)
        magnitude_components = np.abs(freq_spectrum) * 2 / number_of_samples  #Scaled Magnitude

        frequency_domain = np.array([frequency_components, magnitude_components])
        
        return frequency_domain

    @staticmethod
    def align_signals(self, original_time, recovered_time, recovered_values):
        # Create an interpolation function based on the recovered signal
        interp_function = interp1d(recovered_time, recovered_values, bounds_error=False, fill_value="extrapolate")
        # Use it to generate recovered values at the original time points
        aligned_recovered_values = interp_function(original_time)
        return aligned_recovered_values
