import os
import sys

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon

from Final_Report.ui.SignIn.SignInMainWindowEx import SignInMainWindowEx
from Final_Report.ui.WebPage.WebPageMainWindow import Ui_MainWindow


# ================= RESOURCE PATH =================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ================= CLASS =================
class WebPageMainWindowEx(QMainWindow):

    def __init__(self):
        super().__init__()

        # setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon(resource_path("Final_Report/images/icon_app.png")))

        self.setupUI()
        self.setupSignalAndSlot()

        self.login_window = None
        self.login_ui = None

    # ================= UI =================
    def setupUI(self):
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

        QPushButton#pushButtonSignIn {
            background-color: #2e7d32;
        }
        """)

        self.ui.pushButtonSignIn.setMinimumHeight(50)

    # ================= SIGNAL =================
    def setupSignalAndSlot(self):
        self.ui.pushButtonSignIn.clicked.connect(self.openSignInWindow)

    # ================= OPEN LOGIN =================
    def openSignInWindow(self):

        self.login_window = QMainWindow()

        self.login_ui = SignInMainWindowEx()
        self.login_ui.setupUi(self.login_window)

        self.login_ui.previous_window = self

        self.login_ui.showWindow()

        self.hide()