from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.SignIn.SigninMainWindownEx import SignInMainWindownEx

app=QApplication([])
gui=SignInMainWindownEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()