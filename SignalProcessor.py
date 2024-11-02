import sys
import numpy as np
from Reconstruction import Reconstruction
from scipy.fft import dct
from SignalLoader import SignalLoader
from scipy.interpolate import interp1d
class  SignalProcessor:
    def __init__(self):
        super().__init__()
        self.signal_loader = SignalLoader()
        self.signal = self.signal_loader.get_loaded_signal()

    def sample_signal(self, sampling_frequency, method="uniform", threshold=None):
        # This function uses different methods to take samples (uniform, non-uniform, or threshold sampling)
        """
        Creates samples from a signal based on the method chosen; uniform, non-uniform or threshold sampling.
        """
        time_data = self.signal[0]
        amplitude_data = self.signal[1]

        if method == "uniform":
            if sampling_frequency is None:
                raise ValueError("Sampling frequency must be specified.")
            
            sampling_interval = 1 / sampling_frequency / (time_data[1] - time_data[0])  # samples per interval
            sampled_points_time = np.arange(0, len(time_data)+1, sampling_interval)

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

        return np.array([sampled_points_time, sampled_points])

    def recover_signal(self, sampled_points, sampling_frequency, sampled_indices = [], method = "whittaker Shannon", threshold = None):
        # Reconstruct the signal using the specified method
        # Outputs a 2D numpy array
        """
        Reconstructs original signal from sampled points based on 3 methods; Niquist-Shannon,...
        """
        recovered_signal = None
        duration = len(self.signal[0])
        uniform_time_points = np.linspace(0, duration, 100 * duration)
        if method == 'Whittaker Shannon' :
            recovered_signal = Reconstruction.whittaker_shannon(sampled_points, sampling_frequency)

        elif method == 'Compressed Sensing' :
            sampling_matrix = dct(np.eye(len(uniform_time_points)), axis=0, norm='ortho')

            recovered_signal = Reconstruction.compressed_sensing_reconstruct(sampled_points, sampling_matrix, sampled_indices, duration,)

        elif method == 'Level Crossing' :
            recovered_signal = Reconstruction.level_crossing_reconstruct(sampled_points, duration, threshold)
    
        else:
         raise ValueError("Invalid method. Choose 'whittakerShannon', compressedSensing or levelCrossing")
        
        return recovered_signal
         
    

    def calculate_difference(self, recovered_signal):
        # Calculate the difference between original and recovered signals
        # Outputs signals_difference in a 2D numpy array
        """
        Calculates the error in the recovered signal (difference between original and recovered signal).
        """
        original_signal_time = self.signal[0]
        original_signal_values = self.signal [1]

        recovered_signal_time = recovered_signal[0]
        recovered_signal_values = recovered_signal[1]
        # Align recovered signal with original signal time
        recovered_signal_values = self.align_signals(original_signal_time, original_signal_values, recovered_signal_time, recovered_signal_values)
        if not np.array_equal(original_signal_time, recovered_signal_time):
            raise ValueError("Time arrays of both signals must be equal")

        magnitude_difference = np.abs(original_signal_values - recovered_signal_values)

        signals_difference = np.array([original_signal_time, magnitude_difference])
        
        return signals_difference
    

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
