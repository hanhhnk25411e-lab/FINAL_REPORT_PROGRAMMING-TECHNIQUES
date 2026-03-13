from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.PetManagementMainWindowEx import PetManagementMainWindowEx

app=QApplication([])
gui=PetManagementMainWindowEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()