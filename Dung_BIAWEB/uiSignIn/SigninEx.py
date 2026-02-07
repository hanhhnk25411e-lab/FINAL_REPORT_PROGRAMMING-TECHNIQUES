from PyQt6.QtWidgets import QMainWindow

from Forget_Password.PassEx import PassEx
from uiSignIn.Signin import Ui_MainWindow


class SignInEx(Ui_MainWindow):
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
        self.forget_ui = PassEx()
        self.forget_ui.setupUi(self.forget_window)
        self.forget_ui.previous_window = self.MainWindow
        self.forget_ui.showWindow()
        self.MainWindow.hide()


