import sys
import numpy as np
from Reconstruction import Reconstruction
from scipy.fft import dct
from scipy.interpolate import interp1d
class  SignalProcessor:
    def __init__(self):
        super().__init__()

    def sample_signal(self, signal, sampling_frequency, method="uniform", threshold=None):
        # This function uses different methods to take samples (uniform, non-uniform, or threshold sampling)
        """
        Creates samples from a signal based on the method chosen; uniform, non-uniform or threshold sampling.
        """
        time_data = signal[0]
        amplitude_data = signal[1]

        if method == "uniform":
            if sampling_frequency is None:
                raise ValueError("Sampling frequency must be specified.")
            
            sampling_interval = (1 / sampling_frequency )  # samples per interval
            sampled_points_time = np.arange(0, 2, sampling_interval)

            # Calculate the sampled indices using np.searchsorted
            sampled_indices = np.searchsorted(time_data, sampled_points_time)
            
            # To ensure we don't go out of bounds, you might want to filter sampled_indices
            # Keep only valid indices
            sampled_indices = sampled_indices[sampled_indices < len(time_data)]

        # Now you can use sampled_indices to get sampled points from amplitude_data
            # sampled_points = amplitude_data[sampled_indices]
            
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
        sampled_points = amplitude_data[sampled_indices]
        sampled_points_time = time_data[sampled_indices]
        sampled_signal = np.array([sampled_points_time, sampled_points])

        return sampled_signal

    def recover_signal(self, sampled_points, sampling_frequency, sampled_indices = [], method = "Whittaker Shannon", threshold = None):
        """
        Reconstructs original signal from sampled points based on 3 methods; Niquist-Shannon,...
        """
        recovered_signal = None
        duration = 2
        uniform_time_points = np.arange(0, duration, 1 / sampling_frequency)
        if method == 'Whittaker Shannon' :
            recovered_signal = Reconstruction.whittaker_shannon(sampled_points, sampling_frequency)

        elif method == 'Compressed Sensing' :
            sampling_matrix = dct(np.eye(len(uniform_time_points)), axis=0, norm='ortho')
            recovered_signal = Reconstruction.fourier(sampled_points , sampling_frequency)
            # recovered_signal = Reconstruction.compressed_sensing_reconstruct(sampled_points, sampling_matrix, sampled_indices, duration)

        elif method == 'Level Crossing' :
            recovered_signal = Reconstruction.level_crossing_reconstruct(sampled_points, duration, threshold)
    
        else:
         raise ValueError("Invalid method. Choose 'whittakerShannon', compressedSensing or levelCrossing")
        
        return recovered_signal
         
    

    def calculate_difference(self,signal,  recovered_signal):
        # Calculate the difference between original and recovered signals
        # Outputs signals_difference in a 2D numpy array
        """
        Calculates the error in the recovered signal (difference between original and recovered signal).
                """
        # Example 2D signals with different lengths in both dimensions
        signal1 = signal   # Shape (3, 2)
        signal2 = recovered_signal   # Shape (2, 3)

        # Step 1: Interpolate along the time dimension to make both signals have the same length
        target_len = max(signal1.shape[0], signal2.shape[0])

        # Interpolate signal1
        interp_signal1 = interp1d(np.linspace(0, 1, signal1.shape[0]), signal1, axis=0, fill_value="extrapolate")
        resized_signal1 = interp_signal1(np.linspace(0, 1, target_len))

        # Interpolate signal2
        interp_signal2 = interp1d(np.linspace(0, 1, signal2.shape[0]), signal2, axis=0, fill_value="extrapolate")
        resized_signal2 = interp_signal2(np.linspace(0, 1, target_len))

        # Step 2: Match the channel/feature dimension
        # Adjust to the same number of channels by truncating or padding with zeros
        target_channels = max(resized_signal1.shape[1], resized_signal2.shape[1])

        # Pad signal1 if needed
        if resized_signal1.shape[1] < target_channels:
            resized_signal1 = np.pad(resized_signal1, ((0, 0), (0, target_channels - resized_signal1.shape[1])), mode='constant')
        else:
            resized_signal1 = resized_signal1[:, :target_channels]

        # Pad signal2 if needed
        if resized_signal2.shape[1] < target_channels:
            resized_signal2 = np.pad(resized_signal2, ((0, 0), (0, target_channels - resized_signal2.shape[1])), mode='constant')
        else:
            resized_signal2 = resized_signal2[:, :target_channels]

        # Step 3: Calculate the pointwise magnitude difference
        difference_signal = resized_signal1 - resized_signal2
        magnitude_difference = np.linalg.norm(difference_signal, axis=1)

        # Output time vs magnitude difference as a 2D array
        output_signal = np.hstack((np.arange(target_len).reshape(-1, 1), magnitude_difference.reshape(-1, 1)))

        return output_signal
            

        # original_signal_time = signal[0]
        # original_signal_values = signal [1]

        # recovered_signal_time = recovered_signal[0]
        # recovered_signal_values = recovered_signal[1]
        # # Align recovered signal with original signal time
        # # recovered_signal_values = self.align_signals(original_signal_time, original_signal_values, recovered_signal_time, recovered_signal_values)
        # if not np.array_equal(original_signal_time, recovered_signal_time):
        #     raise ValueError("Time arrays of both signals must be equal")
        # print(original_signal_values,".....", recovered_signal_values)
        # magnitude_difference = np.abs(original_signal_values - recovered_signal_values)

        # signals_difference = np.array([original_signal_time, magnitude_difference])
        
        # return signals_difference
    

    def frequency_domain(self, recovered_signal, sampling_frequency):
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

    def align_signals(self, original_time, original_values, recovered_time, recovered_values):
        # Create an interpolation function based on the recovered signal
        interp_function = interp1d(recovered_time, recovered_values, bounds_error=False, fill_value="extrapolate")
        # Use it to generate recovered values at the original time points
        aligned_recovered_values = interp_function(original_time)
        return aligned_recovered_values
