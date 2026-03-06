from PyQt6.QtWidgets import QApplication, QMainWindow

from uiSignIn.SigninEx import SignInEx

app=QApplication([])
gui=SignInEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()