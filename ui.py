from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QComboBox, QSlider, QLabel, QLineEdit, QFrame
)
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from PyQt5.QtGui import QIntValidator

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sampling-Theory Studio")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.label_style_sheet = "font-size: 15px;"
        main_layout = QVBoxLayout()
        graph_layout = QGridLayout()
        v_layout_for_label_of_frequencies = QVBoxLayout()
        control_layout = QHBoxLayout()

        self.original_signal_plot = pg.PlotWidget(title="Original Signal")
        self.reconstructed_signal_plot = pg.PlotWidget(title="Recovered Signal")
        self.difference_signal_plot = pg.PlotWidget(title="Error")
        self.frequency_domain_plot = pg.PlotWidget(title="Frequency Domain")
        self.original_signal_plot.setBackground('#2E2E2E')
        self.reconstructed_signal_plot.setBackground('#2E2E2E')
        self.difference_signal_plot.setBackground('#2E2E2E')
        self.frequency_domain_plot.setBackground('#2E2E2E')

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
        self.load_button.setStyleSheet(self.label_style_sheet)
        self.compose_button = QLabel("Compose Signal:")
        self.compose_button.setStyleSheet(self.label_style_sheet)
        self.cos_sin_expression = QLineEdit()
        self.cos_sin_expression.setPlaceholderText("Enter an expression")
        self.cos_sin_expression.setStyleSheet("color : 'white'")
        self.cos_sin_expression.setFixedWidth(150)

        self.sampling_label = QLabel("Sampling Frequency:")
        self.sampling_label.setStyleSheet(self.label_style_sheet)
        self.sampling_slider = QSlider(Qt.Horizontal)
        self.sampling_slider.setMinimum(10)
        self.sampling_slider.setMaximum(400)
        self.sampling_slider.setValue(200)
        self.sampling_slider.setMinimumWidth(100)
        self.reconstruction_label = QLabel("Reconstruction Method:")
        self.reconstruction_label.setStyleSheet(self.label_style_sheet)
        self.reconstruction_combo = QComboBox()
        self.reconstruction_combo.addItems(
            ["Spline", "Whittaker Shannon", "Fourier"])
        self.reconstruction_combo.setStyleSheet(""" QComboBox { color: 'white';}
                                                    QComboBox QAbstractItemView {color: 'white'; }""")
        
        self.scenarios_label = QLabel("Test Scenarios:")
        self.scenarios_label.setStyleSheet(self.label_style_sheet)
        self.scenarios_combo = QComboBox()
        self.restore_placeholder()
        self.scenarios_combo.setStyleSheet(""" QComboBox { color: 'white';}
                                                    QComboBox QAbstractItemView {color: 'white'; }""")

        self.noise_label = QLabel("Noise Level (SNR):")
        self.noise_label.setStyleSheet(self.label_style_sheet)
        self.noise_input = QLineEdit()
        self.noise_input.setMaximumWidth(100)
        self.noise_input.setPlaceholderText("1-9999")
        self.noise_input.setStyleSheet("color : 'white'")
        self.noise_input.setFixedWidth(65)
        self.noise_input.setValidator(QIntValidator(1, 1000))

        self.sampling_frequency_label= QLabel(f"F_sampling=4Hz")
        self.sampling_frequency_label.setStyleSheet(self.label_style_sheet)
        self.max_frequency_label = QLabel(f"4 F_max")
        self.max_frequency_label.setStyleSheet(self.label_style_sheet)
        # self.sampling_frequency_label.setFixedWidth(130)
        # self.max_frequency_label.setFixedWidth(130)
        def add_separator():
            separator = QFrame()
            separator.setFrameShape(QFrame.VLine)
            separator.setFrameShadow(QFrame.Sunken)
            separator.setStyleSheet("border: 2px solid gray;") 
            control_layout.addWidget(separator)

        control_layout.addWidget(self.load_button)
        add_separator()
        control_layout.addWidget(self.compose_button)
        control_layout.addWidget(self.cos_sin_expression)
        add_separator()
        control_layout.addWidget(self.sampling_label)
        control_layout.addWidget(self.sampling_slider)
        add_separator()
        control_layout.addLayout(v_layout_for_label_of_frequencies)
        add_separator()
        control_layout.addWidget(self.reconstruction_label)
        control_layout.addWidget(self.reconstruction_combo)
        add_separator()
        control_layout.addWidget(self.noise_label)
        control_layout.addWidget(self.noise_input)
        add_separator()
        control_layout.addWidget(self.scenarios_label)
        control_layout.addWidget(self.scenarios_combo)
        
        v_layout_for_label_of_frequencies.addWidget(self.max_frequency_label)
        v_layout_for_label_of_frequencies.addWidget(self.sampling_frequency_label)
        
        main_layout.addLayout(graph_layout)
        main_layout.addLayout(control_layout)
        main_widget.setLayout(main_layout)

    def restore_placeholder(self):
        self.scenarios_combo.clear()
        self.scenarios_combo.addItem("Select a Scenario")
        self.scenarios_combo.addItems(
            ["Scenario 1", "Scenario 2", "Scenario 3"])
        self.scenarios_combo.setItemData(0, 0, Qt.UserRole - 1)
