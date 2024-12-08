from xml.etree.ElementPath import find
import numpy as np
import pandas as pd
import SignalMixer

# def find_maximum_freq(signal):
    # time = signal[0]
    # amplitude = signal[1]
    # time_diff = np.diff(time)
    # sampling_rate = 1 / np.mean(time_diff) #equal 125 for defualt signal

    # n = len(amplitude)
    # fft_result = np.fft.fft(amplitude)
    # frequncies = np.fft.fftfreq(n, d= 1 /sampling_rate)
    # print(frequncies)
    # print(frequncies.shape)

    # positive_freq = frequncies[:n//2]
    # magnitudes = np.abs(fft_result[:n//2])
    # print(max(magnitudes))
    # print(positive_freq)
    # print(np.argmax(magnitudes))
    # max_freq = positive_freq[np.argmax(magnitudes)]
    # print(max_freq)

    # return max_freq


class SignalLoader:
    def __init__(self):
        self.load_signal_from_file('file_of_signal/Pulse Oximeter Signal.csv')
        self.noisy_signal = None

    def load_signal_from_file(self, filepath):
        if filepath:
            self.signal_data = pd.read_csv(filepath, header= None)
            time_data = self.signal_data.iloc[:, 0].values
            amplitude_data = self.signal_data.iloc[:, 1].values
            self.signal_data = np.array([time_data, amplitude_data])

            cropped_indices = np.where(time_data <= 10)[0]  # crop

            if cropped_indices.size > 0: 
                self.signal_data = self.signal_data[:, cropped_indices]  
            else:
                print("Warning: No data points found for the first 2 seconds of the signal.")
            
            self.maximum_freq = 1 / (2 * (time_data[1] - time_data[0]))
            # self.maximum_freq =250
            
            

    def load_signal_from_mixer(self):
        frequencies = []
        amplitude_data = SignalMixer.get_composed_signal()
        time_data = SignalMixer.time

        for component in SignalMixer.components:
            frequencies.append(component["frequency"])
        self.maximum_freq =max(frequencies) 
        # sampling_rate = (2*self.maximum_freq)
        # time_data = np.linspace(0, 2, int(sampling_rate))
        self.signal_data = np.array([time_data, amplitude_data])

    def get_maximum_frequency(self):
        return self.maximum_freq

    def add_noise(self, snr):
        signal = self.signal_data[1]
        if self.noisy_signal is not None:
            self.signal_data[1] = signal - self.noisy_signal
        signal_power = np.mean(signal ** 2)
        # signal_power = 10 * np.log10(signal_power)

        snr = 10**(snr /10)
        noise_power = signal_power / snr
        # noise_power = 10**(noise_power/10)
        random_generator = np.random.default_rng(1)
        self.noisy_signal = np.sqrt(noise_power) * random_generator.normal(size=signal.shape)
        # self.noisy_signal = np.random.normal(0, np.sqrt(noise_power), size=signal.shape)
        self.signal_data[1] = signal + self.noisy_signal

    def get_loaded_signal(self):
        return self.signal_data
    