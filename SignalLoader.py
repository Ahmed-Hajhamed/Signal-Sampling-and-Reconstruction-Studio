class SignalLoader:
    def load_signal_from_file(self, filepath):
        # Load the signal from the specified file in a 2D numpy array
        pass

    def load_signal_from_mixer(self, signal):
        # Load a user-composed signal
        pass

    def add_noise(self, signal, snr):
        # Add noise to the signal based on SNR
        pass

    def get_loaded_signal(self):
        # Return the currently loaded signal
        pass
