import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QComboBox, QSlider, QLabel, QListWidget, QLineEdit, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
from PyQt5.QtGui import QIntValidator
from qt_material import apply_stylesheet
from SignalLoader import SignalLoader
import SignalMixer
from SignalProcessor import SignalProcessor


class SamplingTheoryStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signal_loader = SignalLoader()
        self.signal_processor = SignalProcessor()
        self.setWindowTitle("Sampling-Theory Studio")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        graph_layout = QGridLayout()
        control_layout = QHBoxLayout()

        self.original_signal_plot = pg.PlotWidget(title="Original Signal")
        self.reconstructed_signal_plot = pg.PlotWidget(title="Reconstructed Signal")
        self.difference_signal_plot = pg.PlotWidget(title="Difference Signal")
        self.frequency_domain_plot = pg.PlotWidget(title="Frequency Domain")

        self.curve_original_signal_plot = self.original_signal_plot.plot()
        self.curve_reconstructed_signal_plot = self.reconstructed_signal_plot.plot()
        self.curve_difference_signal_plot = self.difference_signal_plot.plot()
        self.curve_frequency_domain_plot = self.frequency_domain_plot.plot()

        self.curve_original_signal_plot.show()
        self.original_signal_plot.show()

        graph_layout.addWidget(self.original_signal_plot, 0, 0)
        graph_layout.addWidget(self.reconstructed_signal_plot, 0, 1)
        graph_layout.addWidget(self.difference_signal_plot, 1, 0)
        graph_layout.addWidget(self.frequency_domain_plot, 1, 1)

        self.load_button = QPushButton("Load Signal")
        self.compose_button = QLabel("Compose Signal:")

        self.cos_sin_signal = QLineEdit()
        self.cos_sin_signal.setPlaceholderText("Enter an expression")
        self.cos_sin_signal.setFixedWidth(150)

        self.sampling_label = QLabel("Sampling Frequency:")
        self.sampling_slider = QSlider(Qt.Horizontal)
        self.sampling_slider.setMinimum(0)
        self.sampling_slider.setMaximum(4)
        self.sampling_slider.setValue(2)

        self.reconstruction_label = QLabel("Reconstruction Method:")
        self.reconstruction_combo = QComboBox()
        self.reconstruction_combo.addItems(
            ["Whittaker Shannon", "Compressed Sensing", "Level Crossing"])
        self.noise_label = QLabel("Noise Level (SNR):")
        self.noise_input = QLineEdit()
        self.noise_input.setValidator(QIntValidator(1, 1000))
        self.noise_input.setText("0")

        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.compose_button)
        control_layout.addWidget(self.cos_sin_signal)
        control_layout.addWidget(self.sampling_label)
        control_layout.addWidget(self.sampling_slider)
        control_layout.addWidget(self.reconstruction_label)
        control_layout.addWidget(self.reconstruction_combo)
        control_layout.addWidget(self.noise_label)
        control_layout.addWidget(self.noise_input)

        main_layout.addLayout(graph_layout)
        main_layout.addLayout(control_layout)

        main_widget.setLayout(main_layout)

        self.load_button.clicked.connect(self.load_signal)
        self.cos_sin_signal.textChanged.connect(self.compose_signal)
        self.sampling_slider.valueChanged.connect(self.update_sampling_frequency)
        self.reconstruction_combo.currentIndexChanged.connect(self.change_reconstruction_method)

        self.signal= self.signal_loader.get_loaded_signal()
        self.max_frequency = self.signal_loader.get_maximum_frequency()
        self.sampling_frequency = 2 * self.max_frequency
        self.method = self.reconstruction_combo.currentText()
        self.sampled_points = self.signal_processor.sample_signal(self.sampling_frequency)
        self.recovered_signal = self.signal_processor.recover_signal(self.sampled_points, self.sampling_frequency, method = self.method)
        # self.difference_signal = self.signal_processor.calculate_difference(self.recovered_signal)
        self.frequency_domain = self.signal_processor.frequency_domain(self.recovered_signal, self.sampling_frequency)
        self.update_plot()
        # self.timer = QTimer(self)
        # self.timer.setInterval(100)  # Update every 100ms
        # self.timer.timeout.connect(self.update_plot)

    def update_plot(self):
    # Retrieve signals and calculate necessary components
        self.signal = self.signal_loader.get_loaded_signal()
        self.max_frequency = self.signal_loader.get_maximum_frequency()
        if self.max_frequency == 0:
            print("Error: Maximum frequency is zero. Please load a valid signal.")
            return  # Exit early to avoid further errors

        self.sampling_frequency = 2 * self.max_frequency
        if self.sampling_frequency == 0:
            print("Error: Sampling frequency is zero. Cannot proceed with plotting.")
            return

        self.method = self.reconstruction_combo.currentText()
        print(self.sampling_frequency)
        self.sampled_points = self.signal_processor.sample_signal(self.sampling_frequency)
        self.recovered_signal = self.signal_processor.recover_signal(self.sampled_points, self.sampling_frequency, method=self.method)
        # self.difference_signal = self.signal_processor.calculate_difference(self.recovered_signal)
        self.frequency_domain = self.signal_processor.frequency_domain(self.recovered_signal, self.sampling_frequency)
        print("Time Data:", self.sampled_points[0])
        print("Amplitude Data:", self.sampled_points[1])

        # Clear existing plots and set data as before
        self.original_signal_plot.clear()
        self.reconstructed_signal_plot.clear()
        # self.difference_signal_plot.clear()
        self.frequency_domain_plot.clear()

        if self.signal.size > 0:
            self.curve_original_signal_plot.setData(self.signal[0], self.signal[1])
            self.curve_original_signal_plot.setData(self.sampled_points[0], self.sampled_points[1])
            self.original_signal_plot.plot(self.signal[0], self.signal[1], color ='blue')
            self.original_signal_plot.plot(self.sampled_points[0], self.sampled_points[1], pen=None, symbol='o', symbolSize=10,symbolBrush='b', alpha=0.7)
        if self.recovered_signal.size > 0:
            self.curve_reconstructed_signal_plot.setData(self.recovered_signal[0], self.recovered_signal[1])
            self.reconstructed_signal_plot.plot(self.recovered_signal[0], self.recovered_signal[1])
        # if self.difference_signal.size > 0:
        #     self.curve_difference_signal_plot.setData(self.difference_signal[0], self.difference_signal[1])
        if self.frequency_domain.size > 0:
            self.curve_frequency_domain_plot.setData(self.frequency_domain[0], self.frequency_domain[1])
            self.frequency_domain_plot.plot( self.frequency_domain[0], self.frequency_domain[1])

        self.update_sampling_frequency(self.sampling_slider.value())



    def load_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open CSV File", "", "CSV Files (*.csv)")
        self.signal_loader.load_signal_from_file(file_path)
        # self.update_plot()

    def compose_signal(self, expression):
        SignalMixer.components.clear()
        SignalMixer.add_components(expression)
        if len(SignalMixer.components) > 0:
            # SignalMixer.composed_signal.clear()
            SignalMixer.add_sinusoidal_component()
            self.signal_loader.load_signal_from_mixer()
        print(f"Compose Signal functionality goes here {expression}")
        # self.update_plot()

    def update_sampling_frequency(self, value):
        self.sampling_frequency = self.sampling_slider.value() * self.max_frequency
        # self.sampling_frequency = value * self.max_frequency
        self.sampled_points = self.signal_processor.sample_signal(self.sampling_frequency)
        # self.update_plot()
        print(f"Sampling frequency updated to {value}")
        print(type(value))

    def update_noise_level(self, value):
        self.signal_loader.add_noise(value)
        # self.update_plot()
        print(f"Noise level (SNR) updated to {value}")

    def change_reconstruction_method(self, index):
        self.method = self.reconstruction_combo[index]
        self.recovered_signal = self.signal_processor.recover_signal(self.sampled_points, self.sampling_frequency, mehtod = self.method)
        print(f"Reconstruction method changed to {index}")
        # self.update_plot()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SamplingTheoryStudio()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    sys.exit(app.exec_())