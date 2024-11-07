import numpy as np
from scipy.fft import dct
import numpy as np
from scipy.fft import fft, ifft, fftfreq
from scipy.interpolate import CubicSpline

class Reconstruction:
    @staticmethod
    def whittaker_shannon(original_time_points, sampled_points, sampling_frequency):
        """
        Perform Whittaker-Shannon reconstruction of a signal from uniformly taken samples.
        """
        # Calculate sampling interval T
        sampling_interval = (1 / sampling_frequency)

        time_points = original_time_points

        sampled_times = sampled_points[0]
        sampled_amplitudes = sampled_points[1]

        # Initialize array for the reconstructed signal
        reconstructed_amplitudes = np.zeros_like(time_points)

        # Apply the Whittaker-Shannon reconstruction formula
        for i, t in enumerate(time_points):
            sinc_terms = np.sinc((t - sampled_times) / sampling_interval)
            reconstructed_amplitudes[i] = np.sum(sampled_amplitudes * sinc_terms)
        reconstructed_signal = np.array([time_points, reconstructed_amplitudes])
        return reconstructed_signal
    
    @staticmethod
    def fourier(sampled_points, maximum_frequency):
        
        sampled_amplitudes = sampled_points[1]
        # time = np.linspace(0, 2, len(sampled_amplitudes))
        time = sampled_points[0]

        N = len(sampled_amplitudes)
        signal_fft = fft(sampled_amplitudes)

        freq = fftfreq(N, d=(time[1] - time[0]))
        cutoff_freq = maximum_frequency/2 
        signal_fft[np.abs(freq) > cutoff_freq] = 0
        reconstructed_signal = np.real(ifft(signal_fft))

        # New time points for the reconstructed signal
        new_time = np.linspace(time[0], time[-1], len(reconstructed_signal))
        return np.array([new_time, reconstructed_signal])
    
    @staticmethod
    def spline(sampled_points):
        signal = sampled_points[1]
        time = np.linspace(0, 2, len(signal))
        
        # Fit a 3rd-degree spline using CubicSpline
        spline = CubicSpline(time, signal, bc_type='natural')
        
        # Generate new time points for a smooth curve
        new_time = np.linspace(time[0], time[-1], 4 * len(time))  # Increase points for a smoother output
        
        # Evaluate the spline at the new time points
        reconstructed_signal = spline(new_time)
        
        return np.array([new_time, reconstructed_signal])
