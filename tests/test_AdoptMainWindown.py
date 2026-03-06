from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.Adopt.AdoptMainWindowEx import MainWindowEx

app = QApplication([])

mainWindow = QMainWindow()
ui = MainWindowEx()
ui.setupUi(mainWindow)

mainWindow.show()   # 👈 sửa dòng này

app.exec()
