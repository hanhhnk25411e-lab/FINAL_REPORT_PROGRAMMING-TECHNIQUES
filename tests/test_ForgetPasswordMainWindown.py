from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.ForgetPassword.ForgertPassWordMainWindowEx import ForgertPassWordMainWindowEx

app=QApplication([])
gui=ForgertPassWordMainWindowEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()