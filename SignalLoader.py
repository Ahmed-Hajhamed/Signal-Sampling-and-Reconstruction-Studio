import numpy as np
import pandas as pd
import SignalMixer

signal_data = np.array([[1,2], [3,4]])
maximum_freq = 0


def load_signal_from_file(filepath):
    # Load the signal from the specified file
    global signal_data, maximum_freq
    signal_data = pd.read_csv(filepath)
    time_data = signal_data.iloc[:, 0].values
    amplitude_data = signal_data.iloc[:, 1].values
    signal_data = np.array([time_data, amplitude_data])
    maximum_freq = 1 / (2 * (time_data[2] - time_data[1]))


def load_signal_from_mixer():
    # Load a user-composed signal
    global signal_data, maximum_freq
    frequencies = []
    time_data = SignalMixer.time
    amplitude_data = SignalMixer.get_composed_signal()
    signal_data = np.array([time_data, amplitude_data])

    for component in SignalMixer.components:
        frequencies.append(component["frequency"])
    maximum_freq = max(frequencies)

def get_maximum_frequency():
    time = signal_data[0]
    maximum_freq = 1/(2*(time[1]-time[0]))

    return maximum_freq


def add_noise(signal, snr):
    # Add noise to the signal based on SNR
    signal_power = np.mean(signal**2)
    noise_power = signal_power / snr
    random_generator = np.random.default_rng(1)
    noisy_signal = np.sqrt(noise_power) * random_generator.normal(size=signal.shape)
    return noisy_signal


def get_loaded_signal():
    return signal_data