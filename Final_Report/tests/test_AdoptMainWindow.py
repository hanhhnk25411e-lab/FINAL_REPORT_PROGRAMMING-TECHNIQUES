import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from Final_Report.ui.Adopt.AdoptMainWindowEx import AdoptMainWindowEx

os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1.5"

def main():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = AdoptMainWindowEx()
    ui.setupUi(MainWindow)
    ui.showWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()