import sys
import numpy as np
from Reconstruction import Reconstruction
from scipy.fft import dct
import SignalLoader
signal = SignalLoader.get_loaded_signal()
class SignalProcessor:
    def __init__(self):
        super().__init__()
        self.signal = SignalLoader.get_loaded_signal()

    def sample_signal(sampling_frequency, method="uniform", threshold=None):
        # This function uses different methods to take samples (uniform, non-uniform, or threshold sampling)
        """
        Creates samples from a signal based on the method chosen; uniform, non-uniform or threshold sampling.
        """
        time_data = signal[0]
        amplitude_data = signal[1]

        if method == "uniform":
            if sampling_frequency is None:
                raise ValueError("For uniform sampling, 'sampling_rate' must be specified.")
            
            # Sample uniformly by picking indices at intervals based on sampling rate
            # sampling_interval = int(1 / sampling_frequency / (time_data[1] - time_data[0]))
            sampling_interval = int(1 / sampling_frequency )   # samples per interval
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
        sampled_points = amplitude_data[sampled_indices]
        sampled_points_time = time_data[sampled_indices]

        return np.array([sampled_points_time, sampled_points])

    def recover_signal(sampled_points, sampling_frequency, sampled_indices = [], method = "whittaker Shannon", threshold = None):
        # Reconstruct the signal using the specified method
        # Outputs a 2D numpy array
        """
        Reconstructs original signal from sampled points based on 3 methods; Niquist-Shannon,...
        """
        recovered_signal = None
        duration = len(signal[0])
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
         
    

    def calculate_difference(recovered_signal):
        # Calculate the difference between original and recovered signals
        # Outputs signals_difference in a 2D numpy array
        """
        Calculates the error in the recovered signal (difference between original and recovered signal).
        """
        original_signal_time = signal[0]
        original_signal_values = signal [1]

        recovered_signal_time = recovered_signal[0]
        recovered_signal_values = recovered_signal[1]

        if not np.array_equal(original_signal_time, recovered_signal_time):
            raise ValueError("Time arrays of both signals must be equal")

        magnitude_difference = np.abs(original_signal_values - recovered_signal_values)

        signals_difference = np.array([original_signal_time, magnitude_difference])
        
        return signals_difference
    

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