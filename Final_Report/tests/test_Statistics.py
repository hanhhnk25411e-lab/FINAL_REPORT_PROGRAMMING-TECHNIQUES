import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from Final_Report.ui.Statistics.StatisticsMainWindowEx import StatisticsMainWindowEx

os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1.5"

def main():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = StatisticsMainWindowEx()
    ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()