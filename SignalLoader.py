import numpy as np
import pandas as pd
import SignalMixer
from pprint import pprint



class SignalLoader:
    def __init__(self):
        self.load_signal_from_file('Signals\\synthetic_ecg_data.csv')
        self.noise = None

    def load_signal_from_file(self, filepath):
        global max_magnitude
        if filepath:
            self.signal_data = pd.read_csv(filepath, header= None)
            time_data = self.signal_data.iloc[:, 0].values
            amplitude_data = self.signal_data.iloc[:, 1].values
            self.signal_data = np.array([time_data, amplitude_data])
            max_magnitude = None

            cropped_indices = np.where(time_data <= 2)[0]  # crop the first 2 seconds

            if cropped_indices.size > 0: 
                self.signal_data = self.signal_data[:, cropped_indices]  
            else:
                print("Warning: No data points found for the first 2 seconds of the signal.")
            
            self.maximum_freq = 1 / (2 * (time_data[1] - time_data[0]))
            
            

    def load_signal_from_mixer(self):
        global max_magnitude
        frequencies = []
        amplitude_data = SignalMixer.get_composed_signal()
        time_data = SignalMixer.time
        max_magnitude = None

        for component in SignalMixer.components:
            frequencies.append(component["frequency"])
        self.maximum_freq =max(frequencies) 
        self.signal_data = np.array([time_data, amplitude_data])

    def get_maximum_frequency(self):
        return self.maximum_freq

    def add_noise(self, snr_db):
        signal = self.signal_data[1]
        if self.noise is not None:
            self.signal_data[1] = signal - self.noise
        signal_power = np.mean(signal ** 2)
        signal_power_db = 10 * np.log10(signal_power)
        noise_power_db = signal_power_db - snr_db 
        noise_power = 10 **(noise_power_db/10)

        self.noise = np.random.normal(0, np.sqrt(noise_power), size=signal.shape)
        self.signal_data[1] = signal + self.noise

    def get_loaded_signal(self):
        return self.signal_data
