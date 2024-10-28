import sys
import numpy as np
import matplotlib.pyplot as plt
from Reconstruction import Reconstruction
class SignalProcessor:

    def sample_signal(self, signal, sampling_frequency=None, method="uniform", threshold=None):
        # This function uses different methods to take samples (uniform, non-uniform, or threshold sampling)
        """
        Creates samples from a signal based on the method chosen; uniform, non-uniform or threshold sampling.
        """
        time_data = signal[:, 0]
        amplitude_data = signal[:, 1]

        if method == "uniform":
            if sampling_frequency is None:
                raise ValueError("For uniform sampling, 'sampling_rate' must be specified.")
            
            # Sample uniformly by picking indices at intervals based on sampling rate
            sampling_interval = int(1 / sampling_frequency / (time_data[1] - time_data[0]))  # samples per interval
            sampled_indices = np.arange(0, len(time_data), sampling_interval)
        
        elif method == "non-uniform":
            # Non-uniform sampling example (here, random selection)
            random_generator = np.random.default_rng(0)  # Set seed for reproducibility
            sampled_indices = np.sort(random_generator.choice(len(time_data), int(len(time_data) * 0.5), replace=False))
        
        elif method == "threshold":
            if threshold is None:
                raise ValueError("For threshold-based sampling, 'threshold' must be specified.")
            
            # Sample based on signal crossing the threshold level
            sampled_indices = np.nonzero(np.abs(np.diff(np.sign(amplitude_data - threshold))) == 2)[0] #checks if there's a value is crossing the threshold
        
        else:
            raise ValueError("Invalid method. Choose 'uniform', 'non-uniform', or 'threshold'.")

        # Collect the sampled points
        sampled_points = signal[sampled_indices, :]
        return sampled_points


    def recover_signal(self, sampled_points, sampling_frequency, method = "whittakerShannon"):
        # Reconstruct the signal using the specified method
        # Outputs a 2D numpy array
        """
        Reconstructs original signal from sampled points based on 3 methods; Niquist-Shannon,...
        """
        if method == 'whittakerShannon' :
            recoverd_signal = Reconstruction.whittaker_shannon(self, sampled_points, sampling_frequency)

        elif method == 'compressedSensing' :
            pass
        elif method == 'levelCrossing' :
            pass
    
        else:
         raise ValueError("Invalid method. Choose 'whittakerShannon', compressedSensing or levelCrossing")
        
        return recoverd_signal
         
    

    def calculate_difference(self, original_signal, recovered_signal):
        # Calculate the difference between original and recovered signals
        # Outputs signals_difference in a 2D numpy array
        """
        Calculates the error in the recovered signal (difference between original and recovered signal).
        """
        original_signal_time = original_signal[:, 0]
        original_signal_values = original_signal [:, 1]

        recovered_signal_time = recovered_signal[:, 0]
        recovered_signal_values = recovered_signal[:, 1]

        if not np.array_equal(original_signal_time, recovered_signal_time):
            raise ValueError("Time arrays of both signals must be equal")

        magnitude_difference = np.abs(original_signal_values - recovered_signal_values)

        signals_difference = np.column_stack(original_signal_time, magnitude_difference)
        
        return signals_difference
    

    def frequency_domain(self, recovered_signal, sampling_frequency):
        # Perform Fourier transform to check for aliasing
        """
        Returns the full frequency domain of recovered signal.
        """
        # Extract time and signal values
        signal = recovered_signal[:, 1]
     
        time_intervals = 1 / sampling_frequency  #time interval between samples
        
        # Number of samples
        number_of_samples = len(signal)
        
        # Perform FFT to get frequency components
        freq_spectrum = np.fft.fft(signal)
        
        # Generate the full range of frequency bins
        frequency_components = np.fft.fftfreq(number_of_samples, d=time_intervals)
        magnitude_components = np.abs(freq_spectrum) * 2 / number_of_samples  #Scaled Magnitude

        frequency_domain = np.column_stack(frequency_components, magnitude_components)
        
        return frequency_domain