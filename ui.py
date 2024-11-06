from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QComboBox, QSlider, QLabel, QMessageBox, QLineEdit, QFileDialog
)
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from PyQt5.QtGui import QIntValidator
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
        v_layout_for_label_of_frequencies = QVBoxLayout()
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
        graph_layout.addWidget(self.reconstructed_signal_plot, 1, 0)
        graph_layout.addWidget(self.difference_signal_plot, 0, 1)
        graph_layout.addWidget(self.frequency_domain_plot, 1, 1)

        self.load_button = QPushButton("Load Signal")
        self.compose_button = QLabel("Compose Signal:")

        self.cos_sin_expression = QLineEdit()
        self.cos_sin_expression.setPlaceholderText("Enter an expression")
        self.cos_sin_expression.setFixedWidth(150)

        self.sampling_label = QLabel("Sampling Frequency:")
        self.sampling_slider = QSlider(Qt.Horizontal)
        self.sampling_slider.setMinimum(10)
        self.sampling_slider.setMaximum(400)
        self.sampling_slider.setValue(200)
        self.sampling_frequency_label= QLabel("")
        self.max_frequency_label = QLabel("")

        self.reconstruction_label = QLabel("Reconstruction Method:")
        self.reconstruction_combo = QComboBox()
        self.reconstruction_combo.addItems(
            ["Whittaker Shannon", "Fourier", "Spline"])
        self.reconstruction_combo.setStyleSheet("QComboBox { color: white; }")

        self.noise_label = QLabel("Noise Level (SNR):")
        self.noise_input = QLineEdit()
        self.noise_input.setPlaceholderText("1-9999")
        self.noise_input.setValidator(QIntValidator(1, 1000))

        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.compose_button)
        control_layout.addWidget(self.cos_sin_expression)
        control_layout.addWidget(self.sampling_label)
        control_layout.addWidget(self.sampling_slider)
        v_layout_for_label_of_frequencies.addWidget(self.max_frequency_label)
        v_layout_for_label_of_frequencies.addWidget(self.sampling_frequency_label)
        control_layout.addLayout(v_layout_for_label_of_frequencies)
        control_layout.addWidget(self.reconstruction_label)
        control_layout.addWidget(self.reconstruction_combo)
        control_layout.addWidget(self.noise_label)
        control_layout.addWidget(self.noise_input)

        main_layout.addLayout(graph_layout)
        main_layout.addLayout(control_layout)

        main_widget.setLayout(main_layout)

        self.load_button.clicked.connect(self.load_signal)
        self.cos_sin_expression.textChanged.connect(self.compose_signal)
        self.noise_input.textChanged.connect(self.update_noise_level)
        self.sampling_slider.valueChanged.connect(self.update_sampling_frequency)
        self.reconstruction_combo.currentIndexChanged.connect(self.change_reconstruction_method)

        self.signal= self.signal_loader.get_loaded_signal()
        self.max_frequency = self.signal_loader.get_maximum_frequency()
        self.sampling_frequency = 2 * self.max_frequency
        self.method = self.reconstruction_combo.currentText()
        self.sampled_points = self.signal_processor.sample_signal(self.signal, self.sampling_frequency)
        self.recovered_signal = self.signal_processor.recover_signal(self.sampled_points, self.sampling_frequency, method = self.method)
        self.difference_signal = self.signal_processor.calculate_difference(self.signal, self.recovered_signal)
        self.frequency_domain = self.signal_processor.frequency_domain(self.recovered_signal, self.sampling_frequency)
        self.update_plot()

        self.compose_line_edit_is_removed = False

    def update_plot(self):
        self.signal = self.signal_loader.get_loaded_signal()
        if self.sampling_frequency == 0:
            print("Error: Sampling frequency is zero. Cannot proceed with plotting.")
            return

        self.method = self.reconstruction_combo.currentText()
        self.sampled_points = self.signal_processor.sample_signal(self.signal, self.sampling_frequency)
        self.recovered_signal = self.signal_processor.recover_signal(self.sampled_points, self.sampling_frequency, method=self.method)
        self.difference_signal = self.signal_processor.calculate_difference(self.signal, self.recovered_signal)
        self.frequency_domain = self.signal_processor.frequency_domain(self.recovered_signal, self.sampling_frequency)

        # Clear existing plots
        self.original_signal_plot.clear()
        self.reconstructed_signal_plot.clear()
        self.difference_signal_plot.clear()
        self.frequency_domain_plot.clear()

        if self.signal.size > 0:
            # self.curve_original_signal_plot.setData(self.signal[0], self.signal[1])
            # self.curve_original_signal_plot.setData(self.sampled_points[0], self.sampled_points[1])
            self.original_signal_plot.plot(self.signal[0], self.signal[1], color ='blue')
            self.original_signal_plot.plot(self.sampled_points[0], self.sampled_points[1], pen=None, symbol='o', symbolSize=5,symbolBrush='b', alpha=0.7)
        if self.recovered_signal.size > 0:
            # self.curve_reconstructed_signal_plot.setData(self.recovered_signal[0], self.recovered_signal[1])
            self.reconstructed_signal_plot.plot(self.recovered_signal[0], self.recovered_signal[1])
        if self.difference_signal.size > 0:
            # self.curve_difference_signal_plot.setData(self.difference_signal[0], self.difference_signal[1])
            self.difference_signal_plot.plot(self.difference_signal[0], self.difference_signal[1])
        if self.frequency_domain.size > 0:
            # self.curve_frequency_domain_plot.setData(self.frequency_domain[0], self.frequency_domain[1])
            self.frequency_domain_plot.plot( self.frequency_domain[0], self.frequency_domain[1])


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
        self.update_plot()
        self.max_frequency_label.setText(f"{value} f_max")
        self.sampling_frequency_label.setText(f"f_sampling={self.sampling_frequency}Hz")

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
        self.recovered_signal = self.signal_processor.recover_signal(self.sampled_points, self.sampling_frequency, self.method)
        self.update_plot()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = SamplingTheoryStudio()
#     apply_stylesheet(app, theme='dark_teal.xml')
#     window.show()
#     sys.exit(app.exec_())
