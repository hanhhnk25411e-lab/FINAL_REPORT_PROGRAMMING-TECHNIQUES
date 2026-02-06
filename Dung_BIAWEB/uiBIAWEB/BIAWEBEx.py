from PyQt6.QtWidgets import QMainWindow

from uiBIAWEB.BIAWEB import Ui_MainWindow
from uiSignIn.SigninEx import SignInEx


class BIAWEBEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonSignIn.clicked.connect(self.openSignInWindow)

    def openSignInWindow(self):
        self.login_window = QMainWindow()
        self.login_ui = SignInEx()
        self.login_ui.setupUi(self.login_window)
        self.login_ui.showWindow()
        self.MainWindow.close()

