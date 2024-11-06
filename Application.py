from ui import SamplingTheoryStudio
import sys
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

# test of github to fix the problem

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SamplingTheoryStudio()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    sys.exit(app.exec_())
