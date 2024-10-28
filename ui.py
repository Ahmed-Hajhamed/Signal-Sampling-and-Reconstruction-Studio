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

        graph_layout.addWidget(self.original_signal_plot, 0, 0)
        graph_layout.addWidget(self.reconstructed_signal_plot, 0, 1)
        graph_layout.addWidget(self.difference_signal_plot, 1, 0)
        graph_layout.addWidget(self.frequency_domain_plot, 1, 1)

        load_button = QPushButton("Load Signal")
        compose_button = QPushButton("Compose Signal")
        
        signal_list = QLineEdit()

        sampling_label = QLabel("Sampling Frequency:")
        sampling_slider = QSlider(Qt.Horizontal)
        sampling_slider.setMinimum(0)
        sampling_slider.setMaximum(4)
        sampling_slider.setValue(2)

        reconstruction_label = QLabel("Reconstruction Method:")
        reconstruction_combo = QComboBox()
        reconstruction_combo.addItems(["Whittaker-Shannon", "Hussein-method", "Ziyad-Method ","Ahmed-Method","Rashed-Method"])
        noise_label = QLabel("Noise Level (SNR):")
        noise_input = QLineEdit()
        noise_input.setValidator(QIntValidator(1, 1000))  
        noise_input.setText("50")  

        control_layout.addWidget(load_button)
        control_layout.addWidget(compose_button)
        control_layout.addWidget(signal_list)
        control_layout.addWidget(sampling_label)
        control_layout.addWidget(sampling_slider)
        control_layout.addWidget(reconstruction_label)
        control_layout.addWidget(reconstruction_combo)
        control_layout.addWidget(noise_label)
        control_layout.addWidget(noise_input)
        
        main_layout.addLayout(graph_layout)
        main_layout.addLayout(control_layout)

        main_widget.setLayout(main_layout)
        
        load_button.clicked.connect(self.load_signal)
        compose_button.clicked.connect(self.compose_signal)
        sampling_slider.valueChanged.connect(self.update_sampling_frequency)
        # noise_slider.valueChanged.connect(self.update_noise_level)
        noise_input.textChanged.connect(self.update_noise_level)
        reconstruction_combo.currentIndexChanged.connect(self.change_reconstruction_method)
    
    def load_signal(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open CSV File", "", "CSV Files (*.csv)")
        SignalLoader.load_signal_from_file(file_path)

    def compose_signal(self):
        print("Compose Signal functionality goes here")

    def update_sampling_frequency(self, value):
        print(f"Sampling frequency updated to {value}")

    def update_noise_level(self, value):
        print(f"Noise level (SNR) updated to {value}")

    def change_reconstruction_method(self, index):
        print(f"Reconstruction method changed to {index}")

    def update_noise_level(self, value):
        try:
            noise_level = int(value)
            print(f"Noise level (SNR) updated to {noise_level}")
        except ValueError:
            pass
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SamplingTheoryStudio()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    sys.exit(app.exec_())
