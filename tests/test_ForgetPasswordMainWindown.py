from PyQt6.QtWidgets import QApplication, QMainWindow

from Forget_Password.PassEx import PassEx

app=QApplication([])
gui=PassEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()