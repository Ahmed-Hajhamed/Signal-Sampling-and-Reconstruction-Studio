import numpy as np
import pandas as pd
import SignalMixer

data = None


def load_signal_from_file(filepath):
    # Load the signal from the specified file
    global data
    data = pd.read_csv(filepath)
    x_data = data.iloc[:, 0].values
    y_data = data.iloc[:, 1].values
    data = np.array([x_data, y_data])


def load_signal_from_mixer(signal):
    # Load a user-composed signal
    global data
    y_data = SignalMixer.get_composed_signal()
    x_data = SignalMixer.time
    data = np.array([x_data, y_data])


def add_noise(signal, snr):
    # Add noise to the signal based on SNR
    signal_power = np.mean(signal**2)
    noise_power = signal_power / snr
    noisy_signal = np.sqrt(noise_power) * np.random.normal(size=signal.shape)
    return noisy_signal


def get_loaded_signal():
    return data
