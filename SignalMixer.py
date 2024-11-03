import numpy as np
import re

components = []
composed_signal = [[0,0], [0,0]]
# time = np.array([])
sampling_rate =100 
time = np.linspace(0, 1, int(sampling_rate))


def add_components(expression: str):
    pattern = r'([\+\-]?)\s*(\d*)\s*(cos|sin)\((\d+)t\)'

    # Finding all matches
    matches = re.findall(pattern, expression)

    for match in matches:
        sign = match[0] if match[0] else "+"  # Default sign is "+" if not specified
        amplitude = int(match[1]) if match[1] else 1  # Default amplitude is 1 if not specified
        func_type = match[2]
        frequency = int(match[3])

        components.append({'sign': sign, 'type': func_type, 'amplitude': amplitude, 'frequency': frequency})


def create_signal(type_of_signal, frequency, amplitude):
    global time
    
    if type_of_signal == "cos":
        signal = amplitude * np.cos(2 * np.pi * frequency * time)
    elif type_of_signal == "sin":
        signal = amplitude * np.sin(2 * np.pi * frequency * time)
    else:
        raise ValueError ("Invalid Sinusoidal")

    return signal


def set_time(duration = 1):
    global time
    sampling_rate =100 * duration
    time = np.linspace(0, duration, int(sampling_rate))


def add_sinusoidal_component():
    # Add a sinusoidal component to the signal
    global components
    global composed_signal

    for component in components:
        signal = create_signal(component["type"], component["amplitude"], component["frequency"])
        if composed_signal:
            composed_signal = composed_signal + signal if component['sign'] == "+" else composed_signal - signal
        else:
            composed_signal = signal


# def remove_component(index):
#     # Remove a sinusoidal component
#     global components
#     global composed_signal
#
#     signal_component = components.pop(index)
#     signal = create_signal(signal_component["type"], signal_component["amplitude"], signal_component["frequency"])
#     if composed_signal:
#         composed_signal = composed_signal - signal


def get_composed_signal():
    # Return the composed signal
    return composed_signal
