import numpy as np
from scipy import linalg
import scipy.interpolate as interp
from sklearn.linear_model import OrthogonalMatchingPursuit
from scipy.fft import dct
import numpy as np
from scipy.fft import fft, ifft, fftfreq
import pyqtgraph as pg
from PyQt5 import QtWidgets
from scipy.interpolate import CubicSpline

class Reconstruction:
    # @staticmethod
    # def whittaker_shannon(sampled_points, sampling_frequency):
    #     # Reconstruct Signal
    #     t = np.arange(sampled_points[0][0], sampled_points[-1][0], 1 / sampling_frequency)
    #     x_vec = sampled_points[0]
    #     y_vec = sampled_points[1]

    #     # Whittaker–Shannon interpolation formula
    #     y_interp = np.zeros_like(t)
    #     for i, t_i in enumerate(t):
    #         y_interp[i] = np.sum(y_vec * np.sinc((x_vec - t_i) * sampling_frequency))
        
    #     reconstructed_time = t
    #     reconstructed_amplitude = y_interp
    #     return np.array([reconstructed_time, reconstructed_amplitude])

    @staticmethod
    def whittaker_shannon(sampled_points, sampling_frequency):
        """
        Perform Whittaker-Shannon reconstruction of a signal from uniformly taken samples.
        """
        # Calculate sampling interval T
        T = (1 / sampling_frequency)

        # Duration of signal based on number of sampled points
        duration = 2

        # Generate uniformly spaced time points for the reconstruction
        time_points = np.arange(0, duration, T)

        # Extract sampled times and amplitudes
        sampled_times = sampled_points[0]
        sampled_amplitudes = sampled_points[1]

        # Initialize array for the reconstructed signal
        reconstructed_amplitudes = np.zeros_like(time_points)

        # Apply the Whittaker-Shannon reconstruction formula
        for i, t in enumerate(time_points):
            # Sum each sampled amplitude scaled by the sinc function
            sinc_terms = np.sinc((t - sampled_times) / T)
            reconstructed_amplitudes[i] = np.sum(sampled_amplitudes * sinc_terms)
        reconstructed_signal = np.array([time_points, reconstructed_amplitudes])
        return reconstructed_signal
    
    @staticmethod
    def fourier(sampled_points, sampling_frequency):

        # Original signal
        signal = sampled_points[1]
        time = np.linspace(0, 2, len(signal))

        # Fourier transform, zero-padding, and inverse transform
        N = len(signal)
        signal_fft = fft(signal)
        # padded_fft = np.pad(signal_fft, (0, N), 'constant')
        # reconstructed_signal = np.real(ifft(padded_fft))

        freq = fftfreq(N, d=(time[1] - time[0]))
        cutoff_freq = sampling_frequency/2 # Adjust based on signal content
        signal_fft[np.abs(freq) > cutoff_freq] = 0
        reconstructed_signal = np.real(ifft(signal_fft))

        # New time points for the reconstructed signal
        new_time = np.linspace(time[0], time[-1], len(reconstructed_signal))
        return np.array([new_time, reconstructed_signal])
        # # spline = CubicSpline(time, signal)
        # # reconstructed_signal = spline(new_time)

    @staticmethod
    def spline (sampled_points, sampling_frequency):
        # time = np.arange(0, 2, 1/sampling_frequency)
        time = np.linspace(0, 2, len(sampled_points))
        N = len(sampled_points)
        signal_fft = fft(sampled_points)

        padded_fft = np.pad(signal_fft, (0, N), 'constant')
        reconstructed_signal = np.real(ifft(padded_fft))

        spline = CubicSpline(time, sampled_points)
        new_time = np.linspace(time[0], time[-1], len(reconstructed_signal))
        reconstructed_signal = spline(time)
        
        return np.array([time, reconstructed_signal])

    @staticmethod
    def compressed_sensing_reconstruct(sampled_points, sampling_matrix, sampled_indices, duration):
        """
        Reconstructs a signal using Compressed Sensing (CS).

        Parameters:
        - sampled_points (np.ndarray): 1D array of sampled values.
        - sampling_matrix (np.ndarray): Measurement matrix, created with random Gaussian or Bernoulli distribution.
        - signal_length (int): Length of the original signal.
        - sparsity_level (int): Number of non-zero elements expected in the sparse representation.

        Returns:
        - reconstructed_signal (np.ndarray): Reconstructed signal in the original domain.
        """

        # Define an empty array for the sparse signal
        sparse_signal = np.zeros(duration)

        # Solve for the sparse signal that best matches the measurements
        sparse_signal = linalg.lstsq(sampling_matrix, sampled_points)[0]
        sampling_matrix_rows = sampling_matrix[sampled_indices, :]
        uniform_time_points = np.arange(0, duration, 100 * duration)

        # # Retain only the top `sparsity_level` largest elements
        # idx = np.argsort(np.abs(sparse_signal))[-sparsity_level:]
        # sparse_signal[~np.isin(np.arange(duration), idx)] = 0
        #
        # # Reconstruct the full signal from the sparse coefficients
        # reconstructed_signal = np.dot(sampling_matrix.T, sparse_signal)
        omp = OrthogonalMatchingPursuit(n_nonzero_coefs=10)
        omp.fit(sampling_matrix_rows, sampled_points)
        recovered_amplitudes = omp.predict(sampling_matrix)

        reconstructed_signal = np.array([uniform_time_points, recovered_amplitudes])

        return reconstructed_signal

    @staticmethod
    def level_crossing_reconstruct(sampled_points, duration, threshold:int):
        """
        Reconstructs a signal using Level-Crossing Sampling (LCS).
        """
        uniform_time_points = np.arange(0, duration, duration * 0.5)
        frequency1 = 5  # Frequency of first sine wave
        frequency2 = 20  # Frequency of second sine wave
        sparse_signal = 0.5 * np.sin(2 * np.pi * frequency1 * uniform_time_points) + \
                        0.3 * np.sin(2 * np.pi * frequency2 * uniform_time_points)
        # Generate uniform time points over the signal duration
        crossings = np.where(np.diff(np.sign(sparse_signal - threshold)))[0]
        crossing_times = uniform_time_points[crossings]
        # sampled_points = sparse_signal[crossings]

        # Use interpolation to reconstruct the signal over uniform time points
        interpolator = interp.interp1d(crossing_times, sampled_points, kind="linear", fill_value="extrapolate")
        reconstructed_amplitudes = interpolator(uniform_time_points)

        reconstructed_signal = np.array([uniform_time_points, reconstructed_amplitudes])

        return reconstructed_signal
