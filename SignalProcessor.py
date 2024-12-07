import numpy as np
import Reconstruction
from scipy.interpolate import interp1d

def sample_signal(signal, sampling_frequency):
    """
    Creates samples from a signal based on the method chosen; uniform, non-uniform or threshold sampling.
    """
    time_data = signal[0]
    amplitude_data = signal[1]

    if sampling_frequency is None:
        raise ValueError("Sampling frequency must be specified.")
    if sampling_frequency != 0:
        sampling_interval = (1.0 / sampling_frequency)
        sampled_points_time = np.arange(time_data[0], time_data[-1]+sampling_interval, sampling_interval)
        
        sampled_indices = np.searchsorted(time_data, sampled_points_time)

        sampled_indices = sampled_indices[sampled_indices < len(time_data)]

        sampled_points = amplitude_data[sampled_indices]
        sampled_points_time = time_data[sampled_indices]
        sampled_signal = np.array([sampled_points_time, sampled_points])
    else:
        sampled_signal = np.array([[], []])

    return sampled_signal

def recover_signal(original_time_points, sampled_points, sampling_frequency, method="Whittaker Shannon"):
    """
    Reconstructs original signal from sampled points based on 3 methods; Niquist-Shannon,...
    """
    recovered_signal = None
    if method == 'Whittaker Shannon':
        recovered_signal = Reconstruction.whittaker_shannon(original_time_points, sampled_points, sampling_frequency)

    elif method == 'Fourier':
        recovered_signal = Reconstruction.fourier(sampled_points , sampling_frequency)

    elif method == 'Spline':
        recovered_signal = Reconstruction.spline(sampled_points)
    
    return recovered_signal

def calculate_difference(signal, recovered_signal):
    # Example input arrays
    # Array 1: Smaller array (time and values)
    arr1 = signal

    # Array 2: Larger array (time and values)
    arr2 = recovered_signal
    # Extract time and values
    time1, values1 = arr1[0], arr1[1]
    time2, values2 = arr2[0], arr2[1]

    # Interpolate values1 to match time2
    interp_func = interp1d(time1, values1, kind='cubic', fill_value="extrapolate")
    values1_interpolated = interp_func(time2)

    # Compute the difference
    difference = abs(values1_interpolated - values2)

    # Resulting time and difference array
    result = np.array([time2, difference])

    # Output the difference
    # print("Difference shape:", result.shape)
    return result


# def calculate_difference(signal, recovered_signal):
#     """
#     Calculates the error in the recovered signal (difference between original and recovered signal).
#         """
#     original_signal_time = signal[0]
#     original_signal_values = signal[1]
#     recovered_signal_time = recovered_signal[0]
#     recovered_signal_values = recovered_signal[1]

#     recovered_signal_values = align_signals(original_signal_time,
#                                                 recovered_signal_time, recovered_signal_values)

#     recovered_signal_values = np.pad(recovered_signal_values,
#                                         (0, len(original_signal_values) - len(recovered_signal_values)),
#                                         "constant")


#     magnitude_difference = abs(original_signal_values - recovered_signal_values)
#     normalized_error = magnitude_difference / (np.max(original_signal_values) - np.min(original_signal_values))
#     signals_difference = np.array([original_signal_time, magnitude_difference])
#     return signals_difference

def frequency_domain(recovered_signal, sampling_frequency):
    """
    Returns the full frequency domain of recovered signal.
    """
    signal = recovered_signal[1]
    time_intervals = 1 / sampling_frequency 
    number_of_samples = len(signal)

    freq_spectrum = np.fft.fft(signal)

    frequency_components = np.fft.fftfreq(number_of_samples, d=time_intervals)
    magnitude_components = np.abs(freq_spectrum) * 2 / number_of_samples 

    sorted_indices = np.argsort(frequency_components)
    frequency_components = frequency_components[sorted_indices]
    magnitude_components = magnitude_components[sorted_indices]

    frequency_domain = np.array([frequency_components, magnitude_components])
    
    return frequency_domain

def align_signals(original_time, recovered_time, recovered_values):
    interp_function = interp1d(recovered_time, recovered_values, bounds_error=False, fill_value="extrapolate")
    aligned_recovered_values = interp_function(original_time)
    return aligned_recovered_values

def calculate_padding(array_to_pad, reference_array):
    rows_diff = reference_array.shape[0] - array_to_pad.shape[0]
    cols_diff = reference_array.shape[1] - array_to_pad.shape[1]
    return ((0, rows_diff), (0, cols_diff))  # Padding only on the bottom and right