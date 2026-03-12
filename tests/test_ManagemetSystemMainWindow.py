from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.ManagementSystem.ManagementSystemMainWindowEx import ManagementSystemMainWindowEx

app=QApplication([])
gui=ManagementSystemMainWindowEx
gui.setupUi(QMainWindow())
gui.MainWindow.show()
app.exec()