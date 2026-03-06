from PyQt6.QtWidgets import QMainWindow
from ui.ForgetPassword.ForgertPassWordMainWindowEx import ForgertPassWordMainWindowEx
from ui.SignIn.SignInMainWindown import Ui_MainWindow

class SignInMainWindownEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButtonForgetPass.clicked.connect(self.openForgetPasswordWindow)

    def openForgetPasswordWindow(self):
        self.forget_window = QMainWindow()
        self.forget_ui = ForgertPassWordMainWindowEx()
        self.forget_ui.setupUi(self.forget_window)
        self.forget_ui.previous_window = self.MainWindow
        self.forget_ui.showWindow()
        self.MainWindow.hide()


