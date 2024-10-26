import numpy as np


class SignalMixer:
    components = []

    def add_sinusoidal_component(self, frequency, amplitude, duration):
        # Add a sinusoidal component to the signal

        SignalMixer.components.append(amplitude * np.cos(2 * np.pi * frequency * duration))

    def remove_component(self, index):
        # Remove a sinusoidal component
        SignalMixer.components.pop(index)

    def get_composed_signal(self):
        # Return the composed signal
        return SignalMixer.components