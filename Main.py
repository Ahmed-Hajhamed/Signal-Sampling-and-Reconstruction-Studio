from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QComboBox, QSlider, QLabel, QMessageBox, QLineEdit, QFileDialog
)
from UI import UI
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from PyQt5.QtGui import QIntValidator
from SignalLoader import SignalLoader
import SignalMixer
from SignalProcessor import SignalProcessor
from qt_material import apply_stylesheet
from PyQt5.QtWidgets import QApplication
import sys

class SamplingTheoryStudio(UI):
    def __init__(self):
        super().__init__()
        self.signal_loader = SignalLoader()
        self.signal_processor = SignalProcessor()

        self.max_frequency = self.signal_loader.maximum_freq
        self.sampling_frequency = 2 * self.max_frequency
        self.sampling_frequency_label.setText(f"F_sampling={self.sampling_frequency}Hz")
        self.max_frequency_label.setText(f"{2} F_max")

        self.load_button.clicked.connect(self.load_signal)
        self.cos_sin_expression.textChanged.connect(self.compose_signal)
        self.noise_input.textChanged.connect(self.update_noise_level)
        self.sampling_slider.valueChanged.connect(self.update_sampling_frequency)
        self.reconstruction_combo.currentIndexChanged.connect(self.change_reconstruction_method)

        self.compose_line_edit_is_removed = False
        self.update_plot()

    def update_plot(self):
        self.signal = self.signal_loader.get_loaded_signal()
        self.max_frequency = self.signal_loader.get_maximum_frequency()
        self.method = self.reconstruction_combo.currentText()
        self.sampled_points = self.signal_processor.sample_signal(self.signal, self.sampling_frequency)
        self.recovered_signal = self.signal_processor.recover_signal(self.signal[0], self.sampled_points,
                                           self.sampling_frequency, method=self.method)
        self.difference_signal = self.signal_processor.calculate_difference(self.signal, self.recovered_signal)
        self.frequency_domain = self.signal_processor.frequency_domain(self.recovered_signal, self.sampling_frequency)

        self.original_signal_plot.clear()
        self.reconstructed_signal_plot.clear()
        self.difference_signal_plot.clear()
        self.frequency_domain_plot.clear()

        offsets = [-self.sampling_frequency, self.sampling_frequency]   
        
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
                original_band_mask = (self.frequency_domain[0] >= -self.sampling_frequency) & (self.frequency_domain[0] <= self.sampling_frequency)
                self.frequency_domain_plot.plot(frequency_components[original_band_mask], 
                                magnitude_components[original_band_mask], 
                            pen=pg.mkPen(color='white', width=2))
                
                for i, offset in enumerate(offsets):
                         repeated_band_mask = (frequency_components + offset >= -self.max_frequency) & (frequency_components + offset <=self.max_frequency)
                         self.frequency_domain_plot.plot(frequency_components[repeated_band_mask] + offset, 
                                   magnitude_components[repeated_band_mask], 
                                   pen=pg.mkPen(color='r'))

                    
    def load_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open CSV File", "", "CSV Files (*.csv)")
        self.signal_loader.load_signal_from_file(file_path)
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

        self.update_plot()

    def update_sampling_frequency(self, value):
        value = value/100
        self.sampling_frequency = int(value * self.max_frequency)
        self.sampled_points = self.signal_processor.sample_signal(self.signal, self.sampling_frequency)
        self.max_frequency_label.setText(f"{value} F_max")
        self.sampling_frequency_label.setText(f"F_sampling={self.sampling_frequency}Hz")
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

    def change_reconstruction_method(self, index):
        self.method = self.reconstruction_combo.currentText()
        self.recovered_signal = self.signal_processor.recover_signal(self.signal[0],self.sampled_points, 
                                                 self.sampling_frequency, self.method)
        self.update_plot()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SamplingTheoryStudio()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    sys.exit(app.exec_())
