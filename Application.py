import SignalMixer
from SignalProcessor import SignalProcessor
import SignalLoader
from UIManager import UIManager
class Application:
    def __init__(self):
        self.signal_loader = SignalLoader()
        self.signal_mixer = SignalMixer()
        self.signal_processor = SignalProcessor()
        self.ui_manager = UIManager()

    def run(self):
        self.ui_manager.setup_main_window()
        # Event loop to handle real-time updates
