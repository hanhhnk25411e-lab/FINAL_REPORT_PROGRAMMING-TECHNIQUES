from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.PetDetailsMainWindowEx import PetDetailsMainWindowEx

app=QApplication([])
gui=PetDetailsMainWindowEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()