import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QComboBox, QSlider, QLabel, QListWidget, QLineEdit, QFileDialog
)
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from PyQt5.QtGui import QIntValidator
from qt_material import apply_stylesheet

import SignalLoader
import SignalMixer


class SamplingTheoryStudio(QMainWindow):
    def __init__(self):
        super().__init__()
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
            ["Whittaker-Shannon", "Hussein-method", "Ziyad-Method ", "Ahmed-Method", "Rashed-Method"])
        self.noise_label = QLabel("Noise Level (SNR):")
        self.noise_input = QLineEdit()
        self.noise_input.setValidator(QIntValidator(1, 1000))
        self.noise_input.setText("50")

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

    def load_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open CSV File", "", "CSV Files (*.csv)")
        SignalLoader.load_signal_from_file(file_path)

    def compose_signal(self, expression):
        SignalMixer.components.clear()
        SignalMixer.add_components(expression)
        if len(SignalMixer.components) > 0:
            SignalMixer.composed_signal.clear()
            SignalMixer.add_sinusoidal_component()
            SignalLoader.load_signal_from_mixer()
        # print(f"Compose Signal functionality goes here {expression}")

    def update_sampling_frequency(self, value):
        print(f"Sampling frequency updated to {value}")
        print(type(value))

    def update_noise_level(self, value):
        SignalLoader.add_noise(value)
        print(f"Noise level (SNR) updated to {value}")

    def change_reconstruction_method(self, index):
        print(f"Reconstruction method changed to {index}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SamplingTheoryStudio()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    sys.exit(app.exec_())
