from PyQt6.QtWidgets import QApplication, QMainWindow

from uiBIAWEB.BIAWEBEx import BIAWEBEx

app=QApplication([])
gui=BIAWEBEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()