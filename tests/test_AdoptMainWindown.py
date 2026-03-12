from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.Adopt.AdoptMainWindowEx import AdoptMainWindowEx

app = QApplication([])
mainWindow = QMainWindow()
ui = AdoptMainWindowEx()
ui.setupUi(mainWindow)
mainWindow.show()
app.exec()
