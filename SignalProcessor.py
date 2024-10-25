class SignalProcessor:
    def sample_signal(self, signal, sampling_frequency):
        # Sample the signal at the given frequency
        pass

    def recover_signal(self, sampled_signal, method):
        # Reconstruct the signal using the specified method
        # Outputs a 2D numpy array
        pass

    def calculate_difference(self, original_signal, recovered_signal):
        # Calculate the difference between original and recovered signals
        # Outputs signals_difference in a 2D numpy array
        pass

    def fourier_transform(self, signal):
        # Perform Fourier transform to check for aliasing
        pass
