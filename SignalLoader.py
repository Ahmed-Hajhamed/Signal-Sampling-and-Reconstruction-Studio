import numpy as np
import pandas as pd
import SignalMixer


class SignalLoader:
    def __init__(self):
        self.load_signal_from_file('file_of_signal/ECG Signal (Lead AVR).csv')
        # self.signal_data = pd.read_csv('file_of_signal/ECG Signal (Lead AVR).csv')
        # time_data = self.signal_data.iloc[:, 0].values
        # amplitude_data = self.signal_data.iloc[:, 1].values
        # self.signal_data = np.array([time_data, amplitude_data])
        # # Crop the signal
        # first_second_indices = np.where(time_data <= 2)[0]  # Get indices where time is less than or equal to 1 second

        # if first_second_indices.size > 0:  # Check if there are any indices found
        #     self.signal_data = self.signal_data[:, first_second_indices]  # Crop the signal data
        # else:
        #     print("Warning: No data points found for the first second of the signal.")

        # self.maximum_freq = 30
        self.noisy_signal = None

    def load_signal_from_file(self, filepath):
        if filepath:
            # Load the signal from the specified file
            self.signal_data = pd.read_csv(filepath)
            time_data = self.signal_data.iloc[:, 0].values
            amplitude_data = self.signal_data.iloc[:, 1].values
            self.signal_data = np.array([time_data, amplitude_data])

            cropped_indices = np.where(time_data <= 2)[0]  # crop the first 2 seconds

            if cropped_indices.size > 0: 
                self.signal_data = self.signal_data[:, cropped_indices]  
            else:
                print("Warning: No data points found for the first 2 seconds of the signal.")

            self.maximum_freq = 1 / (2 * (time_data[1] - time_data[0]))

    def load_signal_from_mixer(self):
        # Load a user-composed signal
        frequencies = []
        time_data = SignalMixer.time
        amplitude_data = SignalMixer.get_composed_signal()
        self.signal_data = np.array([time_data, amplitude_data])

        for component in SignalMixer.components:
            frequencies.append(component["frequency"])
        self.maximum_freq = 2 * np.pi *max(frequencies)

    def get_maximum_frequency(self):
        
        return self.maximum_freq

    def add_noise(self, snr):
        # Add noise to the signal based on SNR
        signal = self.signal_data[1]
        if self.noisy_signal is not None:
            self.signal_data[1] = signal - self.noisy_signal
        signal_power = np.mean(signal ** 2)
        noise_power = signal_power / snr
        random_generator = np.random.default_rng(1)
        self.noisy_signal = np.sqrt(noise_power) * random_generator.normal(size=signal.shape)
        self.signal_data[1] = signal + self.noisy_signal

    def get_loaded_signal(self):
        return self.signal_data
    