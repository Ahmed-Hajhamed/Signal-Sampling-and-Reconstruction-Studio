from PyQt5.QtWidgets import ( QMessageBox, QFileDialog )
from UI import UI
import pyqtgraph as pg
from SignalLoader import SignalLoader
import SignalMixer
import SignalProcessor
from qt_material import apply_stylesheet
from PyQt5.QtWidgets import QApplication
import sys
import numpy as np

class SamplingTheoryStudio(UI):
    def __init__(self):
        super().__init__()
        self.signal_loader = SignalLoader()
        self.signal =None
        self.method = self.reconstruction_combo.currentText()
        self.current_scenario = None
        self.load_signal()
        self.load_button.clicked.connect(self.load_signal)
        self.cos_sin_expression.textChanged.connect(self.compose_signal)
        self.noise_input.textChanged.connect(self.update_noise_level)
        self.sampling_slider.valueChanged.connect(self.update_sampling_frequency)
        self.reconstruction_combo.currentIndexChanged.connect(self.change_reconstruction_method)
        self.scenarios_combo.currentIndexChanged.connect(self.load_test_scenario)

        self.compose_line_edit_is_removed = False
        self.update_plot()

    def update_plot(self):
        self.recovered_signal = SignalProcessor.recover_signal(self.signal[0], self.sampled_points,
                                           self.sampling_frequency, method=self.method)
        self.difference_signal = SignalProcessor.calculate_difference(self.signal, self.recovered_signal)
        self.frequency_domain = SignalProcessor.frequency_domain(self.recovered_signal, self.sampling_frequency)

        self.original_signal_plot.clear()
        self.reconstructed_signal_plot.clear()
        self.difference_signal_plot.clear()
        self.frequency_domain_plot.clear()

        offsets = [-self.sampling_frequency, self.sampling_frequency]   

        self.max_frequency_label.setText(f"{self.sampling_slider.value()/100} F_max")
        self.sampling_frequency_label.setText(f"F_sampling={int(self.sampling_frequency)}Hz")

        if self.signal.size > 0:
            self.original_signal_plot.plot(self.signal[0], self.signal[1], color ='blue')
            self.original_signal_plot.plot(self.sampled_points[0], self.sampled_points[1],
                                            pen=None, symbol='o', symbolSize=5,symbolBrush='b', alpha=0.7)
        if self.recovered_signal.size > 0:
            self.reconstructed_signal_plot.plot(self.recovered_signal[0], self.recovered_signal[1])
        if self.difference_signal.size > 0:
            self.difference_signal_plot.plot(self.difference_signal[0], self.difference_signal[1])

        if self.frequency_domain.size > 0:
                frequency_components = self.frequency_domain[0]
                magnitude_components = self.frequency_domain[1]
                original_band_mask = (self.frequency_domain[0] >= -self.sampling_frequency)\
                                            & (self.frequency_domain[0] <= self.sampling_frequency)
                self.frequency_domain_plot.plot(frequency_components[original_band_mask], 
                                                magnitude_components[original_band_mask], 
                                                pen=pg.mkPen(color='white', width=2))
                
                for i, offset in enumerate(offsets):
                         repeated_band_mask = (frequency_components + offset >= -self.max_frequency)\
                                             & (frequency_components + offset <=self.max_frequency)
                         self.frequency_domain_plot.plot(frequency_components[repeated_band_mask] + offset, 
                                   magnitude_components[repeated_band_mask], 
                                   pen=pg.mkPen(color='r'))

    def load_signal(self):
        if self.signal is not None:
            file_path, _ = QFileDialog.getOpenFileName(None, "Open CSV File", "", "CSV Files (*.csv)")
            self.signal_loader.load_signal_from_file(file_path)
            self.signal = self.signal_loader.get_loaded_signal()
        else:
            self.signal = self.signal_loader.get_loaded_signal()
        self.restore_placeholder()
        self.max_frequency = self.signal_loader.get_maximum_frequency()
        self.sampling_frequency = 2 * self.max_frequency
        self.sampled_points = SignalProcessor.sample_signal(self.signal, self.sampling_frequency)
        self.cos_sin_expression.setText("")
        self.update_plot()

    def compose_signal(self, expression):
        if len(SignalMixer.components) > 0:
            self.compose_line_edit_is_removed = True

        SignalMixer.components.clear()
        SignalMixer.add_components(expression)

        if len(SignalMixer.components) > 0:
            SignalMixer.add_sinusoidal_component()
            self.signal_loader.load_signal_from_mixer()

        elif self.compose_line_edit_is_removed and len(self.cos_sin_expression.text())==0:
            self.signal_loader = SignalLoader()
            self.compose_line_edit_is_removed = False
        if (expression != self.current_scenario):
            self.restore_placeholder()
        self.signal = self.signal_loader.get_loaded_signal()
        self.max_frequency = self.signal_loader.get_maximum_frequency()
        self.sampling_frequency = 2 * self.max_frequency
        self.sampled_points = SignalProcessor.sample_signal(self.signal, self.sampling_frequency)
        self.update_plot()

    def update_sampling_frequency(self, value):
        value = value/100
        self.sampling_frequency = np.ceil(value * self.max_frequency)
        self.sampled_points = SignalProcessor.sample_signal(self.signal, self.sampling_frequency)
        self.update_plot()

    def update_noise_level(self, value):
        if value != "":
            value = int(value)
            if value == 0:
                QMessageBox.warning(self,  "Invalid Input", "Please enter a number between 1 and 1000, not 0.")
                self.noise_input.clear()
                return
            self.signal_loader.add_noise(value)
        else:
            if self.signal_loader.noisy_signal is not None:
                self.signal_loader.signal_data[1] = self.signal_loader.signal_data[1] - self.signal_loader.noisy_signal
                self.signal_loader.noisy_signal = None

        self.update_plot()

    def change_reconstruction_method(self):
        self.method = self.reconstruction_combo.currentText()
        self.recovered_signal = SignalProcessor.recover_signal(self.signal[0],self.sampled_points, 
                                                 self.sampling_frequency, self.method)
        self.update_plot()
        
    def load_test_scenario(self):
        current_scenario = self.scenarios_combo.currentText()
        if current_scenario == 'Scenario 1':
            current_scenario = 'cos(8t)'
            self.reconstruction_combo.setCurrentIndex(0)

        elif current_scenario == 'Scenario 2':
            self.reconstruction_combo.setCurrentIndex(1)
            current_scenario = 'sin(5t)+sin(15t)'

        elif current_scenario == 'Scenario 3':
            self.reconstruction_combo.setCurrentIndex(2)
            current_scenario = 'sin(2t)+cos(2t)+sin(t)'
        else :
            return
        self.current_scenario = current_scenario
        self.change_reconstruction_method()
        self.cos_sin_expression.setText(self.current_scenario)
        self.compose_signal(self.current_scenario)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SamplingTheoryStudio()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    sys.exit(app.exec_())
