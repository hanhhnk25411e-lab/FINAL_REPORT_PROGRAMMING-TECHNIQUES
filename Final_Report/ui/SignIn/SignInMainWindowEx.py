import json
import os
import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Final_Report.ui.ForgetPassword.ForgetPassWordMainWindowEx import ForgetPassWordMainWindowEx
from Final_Report.ui.ManagementSystem.ManagementSystemMainWindowEx import ManagementSystemMainWindowEx
from Final_Report.ui.SignIn.SignInMainWindown import Ui_MainWindow
from Final_Report.ui.UserSystemMainWindow.UserSystemMainWindowEx import UserSystemMainWindowEx


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

    return os.path.join(project_root, relative_path.replace("Final_Report/", ""))

def get_data_path(filename):
    base = resource_path("Final_Report/PawsResQ")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, filename)


def ensure_file(filename):
    data_path = get_data_path(filename)

    if not os.path.exists(data_path):
        source = resource_path(f"Final_Report/datasets/{filename}")

        if os.path.exists(source):
            import shutil
            shutil.copy(source, data_path)
        else:
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump({"users": []}, f)

    return data_path


class SignInMainWindowEx(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.MainWindow = MainWindow

        self.setupSignalAndSlot()

        self.MainWindow.setStyleSheet("""
        QPushButton {
            background-color: #2e7d32;
            color: white;
            padding: 10px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #43a047;
        }
        QPushButton#pushButtonForgetPass {
            background-color: #1565c0;
        }
        QLineEdit {
            border: 2px solid #2e7d32;
            border-radius: 6px;
            padding: 6px;
        }
        """)

        self.pushButtonSignIn.setMinimumHeight(40)
        self.pushButtonForgetPass.setMinimumHeight(35)

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonForgetPass.clicked.connect(self.openForgetPasswordWindow)
        self.pushButtonSignIn.clicked.connect(self.checkLogin)

    def get_json_path(self):
        return ensure_file("users.json")

    def checkLogin(self):

        account_input = self.lineEditEmail.text().strip()
        password_input = self.lineEditPassword.text().strip()

        if not account_input or not password_input:
            QMessageBox.warning(
                self.MainWindow,
                "Warning",
                "Please enter your email/phone and password!"
            )
            return

        try:
            with open(self.get_json_path(), 'r', encoding='utf-8') as f:
                users_data = json.load(f)

            user_found = None

            for user in users_data.get('users', []):
                if (
                    (user.get('email') == account_input or user.get('phone') == account_input)
                    and user.get('password') == password_input
                ):
                    user_found = user
                    break

            if user_found:

                role = user_found.get('role')

                if role == 'customer':
                    QMessageBox.information(self.MainWindow, "Success", "Login successful! Welcome Customer.")
                    self.openCustomerInterface()

                elif role == 'manager':
                    QMessageBox.information(self.MainWindow, "Success", "Login successful! Welcome Manager.")
                    self.openManagerInterface()

            else:
                QMessageBox.critical(self.MainWindow, "Error", "Invalid email/phone or password!")

        except FileNotFoundError:
            QMessageBox.critical(self.MainWindow, "File Error", "Cannot find users.json!")

        except Exception as e:
            QMessageBox.critical(self.MainWindow, "System Error", f"An error occurred:\n{e}")

    def openForgetPasswordWindow(self):

        self.forget_window = QMainWindow()

        self.forget_ui = ForgetPassWordMainWindowEx()
        self.forget_ui.setupUi(self.forget_window)

        self.forget_ui.previous_window = self.MainWindow

        self.forget_window.show()
        self.MainWindow.hide()

    def openCustomerInterface(self):

        self.customer_ui = UserSystemMainWindowEx()
        self.customer_ui.previous_window = self.MainWindow

        self.customer_ui.show()

        self.MainWindow.hide()

    def openManagerInterface(self):

        self.manager_window = QMainWindow()

        self.manager_ui = ManagementSystemMainWindowEx()
        self.manager_ui.setupUi(self.manager_window)

        self.manager_ui.previous_window = self.MainWindow

        self.manager_window.show()
        self.MainWindow.hide()