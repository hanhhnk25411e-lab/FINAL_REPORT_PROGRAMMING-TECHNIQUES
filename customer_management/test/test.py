import sys
from PyQt6.QtWidgets import QApplication
from MainWindowEx import MainWindowEx

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowEx()
    window.show()
    sys.exit(app.exec())