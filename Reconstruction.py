import numpy as np
from scipy.fft import fft, ifft, fftfreq
from scipy.interpolate import CubicSpline

def whittaker_shannon(original_time_points, sampled_points, sampling_frequency):
    """
    Perform Whittaker-Shannon reconstruction of a signal from uniformly taken samples.
    """
    sampling_interval = (1 / sampling_frequency)
    time_points = original_time_points
    sampled_times = sampled_points[0]
    sampled_amplitudes = sampled_points[1]

    reconstructed_amplitudes = np.zeros_like(time_points)

    for i, t in enumerate(time_points):
        sinc_terms = np.sinc((t - sampled_times) / sampling_interval)
        reconstructed_amplitudes[i] = np.sum(sampled_amplitudes * sinc_terms)
    reconstructed_signal = np.array([time_points, reconstructed_amplitudes])
    return reconstructed_signal

def fourier(sampled_points, sampling_frequency):
    
    sampled_amplitudes = sampled_points[1]
    time = sampled_points[0]

    N = len(sampled_amplitudes)
    signal_fft = fft(sampled_amplitudes)
    if ((time[1] - time[0]) > 0.0):
        freq = fftfreq(N, d=(time[1] - time[0]))
    else:
        freq = fftfreq(N, d=(0.1))
    cutoff_freq = sampling_frequency/2
    signal_fft[np.abs(freq) > cutoff_freq] = 0
    reconstructed_signal = np.real(ifft(signal_fft))

    new_time = np.linspace(time[0], time[-1], len(reconstructed_signal))
    return np.array([new_time, reconstructed_signal])

def spline(sampled_points):
    signal = sampled_points[1]
    time = np.linspace(0, 2, len(signal))

    spline = CubicSpline(time, signal, bc_type='natural')
    new_time = np.linspace(time[0], time[-1], 4 * len(time))  
    reconstructed_signal = spline(new_time)
    
    return np.array([new_time, reconstructed_signal])
