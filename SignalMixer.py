import numpy as np

components = []
composed_signal = None
time = 0


def create_signal(frequency, amplitude):
    global time
    signal = amplitude * np.cos(2 * np.pi * frequency * time)
    return signal


def set_time(duration):
    global time
    sampling =100
    time = np.linspace(0, duration, int(sampling * duration))


def add_sinusoidal_component(frequency, amplitude):
    # Add a sinusoidal component to the signal
    global components
    global composed_signal

    components.append((frequency, amplitude))
    signal = create_signal(frequency, amplitude)
    if composed_signal:
        composed_signal = composed_signal + signal
    else:
        composed_signal = signal


def remove_component(index):
    # Remove a sinusoidal component
    global components
    global composed_signal

    signal_component = components.pop(index)
    frequency, amplitude = signal_component[0], signal_component[1]
    signal = create_signal(frequency, amplitude)
    if composed_signal:
        composed_signal = composed_signal - signal


def get_composed_signal():
    # Return the composed signal
    return composed_signal
