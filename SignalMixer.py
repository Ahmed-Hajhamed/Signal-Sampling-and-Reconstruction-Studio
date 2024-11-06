import numpy as np
import re

components = []
composed_signal = np.array([])
time = np.array([])


def add_components(expression: str):
    expression.lower()
    pattern = r'([\+\-]?)\s*(\d*)\s*(cos|sin)\s*\(\s*(\d*)\s*t\s*\)'

    # Finding all matches
    matches = re.findall(pattern, expression)
    for match in matches:
        sign = match[0] if match[0] else "+"  
        amplitude = int(match[1]) if match[1] else 1  
        func_type = match[2]
        frequency = int(match[3]) if match[3] else 1

        components.append({'sign': sign, 'type': func_type, 'amplitude': amplitude, 'frequency': frequency})

def create_signal(type_of_signal, amplitude, frequency):
    global time
    
    if type_of_signal == "cos":
        signal = amplitude * np.cos(2 * np.pi * frequency * time)
    elif type_of_signal == "sin":
        signal = amplitude * np.sin(2 * np.pi * frequency * time)
    else:
        raise ValueError ("Invalid Sinusoidal")

    return signal


def set_time(duration):
    global time
    sampling_rate =100 * duration
    time = np.linspace(0, duration, int(sampling_rate))


def add_sinusoidal_component():
    # Add a sinusoidal component to the signal
    global components
    global composed_signal
    set_time(2)
    composed_signal = np.array([])

    if components:
        check_line_edit_is_removed = True
    for component in components:
        signal = create_signal(component["type"], component["amplitude"], component["frequency"])
        if composed_signal.size != 0:
            composed_signal = composed_signal + signal if component['sign'] == "+" else composed_signal - signal
        else:
            composed_signal = signal

def get_composed_signal():
    # Return the composed signal
    return composed_signal
