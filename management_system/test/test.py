from PyQt6.QtWidgets import QApplication, QMainWindow

from management_system.ui.ManagementSystemEx import ManagementSystemEx

app=QApplication([])
gui=ManagementSystemEx()
gui.setupUi(QMainWindow())
gui.MainWindow.show()
app.exec()