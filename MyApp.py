from PyQt6.QtWidgets import QApplication, QMainWindow
from MainWindowEx import MainWindowEx

app = QApplication([])

mainWindow = QMainWindow()
ui = MainWindowEx()
ui.setupUi(mainWindow)

mainWindow.show()   # 👈 sửa dòng này

app.exec()
