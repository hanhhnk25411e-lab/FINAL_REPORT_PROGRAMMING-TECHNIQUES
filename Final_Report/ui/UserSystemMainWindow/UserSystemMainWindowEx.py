from PyQt6.QtWidgets import QMainWindow

from Final_Report.ui.Adopt.AdoptMainWindowEx import AdoptMainWindowEx
from Final_Report.ui.UserSystemMainWindow.UserSystemMainWindow import Ui_MainWindow


class UserSystemMainWindowEx(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.BtnSignUp.clicked.connect(self.open_signup)
        self.BtnSignUpBack.clicked.connect(self.go_back)

        self.setStyleSheet("""
        QPushButton {
            background-color: #2e7d32;
            color: white;
            padding: 10px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #43a047;
        }
        QPushButton#BtnSignUpBack {
            background-color: #c62828;
        }
        """)

    def open_signup(self):

        self.signup_window = QMainWindow()

        self.signup_ui = AdoptMainWindowEx()
        self.signup_ui.setupUi(self.signup_window)

        self.signup_ui.previous_window = self

        self.signup_ui.showWindow()

        self.hide()


    def go_back(self):

        if hasattr(self, 'previous_window') and self.previous_window:
            self.previous_window.show()

        self.close()