from PyQt6.QtWidgets import QMainWindow

from Final_Report.ui.Adopt.AdoptMainWindowEx import AdoptMainWindowEx
from ui.UserSystemMainWindow.UserSystemMainWindow import Ui_MainWindow


class UserSystemMainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.BtnSignUp.clicked.connect(self.open_signup)
    def showWindow(self):
        self.MainWindow.show()

    def open_signup(self):
        self.login_window = QMainWindow()
        self.login_ui = AdoptMainWindowEx()
        self.login_ui.setupUi(self.login_window)
        self.login_ui.showWindow()
        self.MainWindow.close()

