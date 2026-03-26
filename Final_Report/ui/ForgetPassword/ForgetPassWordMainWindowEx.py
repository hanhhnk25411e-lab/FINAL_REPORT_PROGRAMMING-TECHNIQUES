import json
import os
import sys
from PyQt6.QtWidgets import QMessageBox

from Final_Report.ui.ForgetPassword.ForgetPassWordMainWindow import Ui_MainWindow


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


class ForgetPassWordMainWindowEx(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.previous_window = None
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
        QPushButton#pushButtonContinueSignIn {
            background-color: #1565c0;
        }
        QPushButton#pushButtonTracePassword {
            background-color: #2e7d32;
        }
        QLineEdit {
            border: 2px solid #2e7d32;
            border-radius: 6px;
            padding: 6px;
        }
        """)

        self.pushButtonTracePassword.setMinimumHeight(40)
        self.pushButtonContinueSignIn.setMinimumHeight(35)
        self.lineEditPhone.setFocus()

    def setupSignalAndSlot(self):
        self.pushButtonContinueSignIn.clicked.connect(self.returnToSignIn)
        self.pushButtonTracePassword.clicked.connect(self.trace_password)

    def showWindow(self):
        self.MainWindow.show()

    def returnToSignIn(self):
        if self.previous_window is not None:
            self.previous_window.show()
        self.MainWindow.close()

    def trace_password(self):

        phone_input = self.lineEditPhone.text().strip()

        if not phone_input:
            QMessageBox.warning(self.MainWindow, "Warning", "Please enter your phone number!")
            return

        json_path = ensure_file("users.json")

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                users_data = json.load(f)

            found = False

            for user in users_data.get('users', []):
                if user.get('phone') == phone_input:
                    self.lineEditTracedPassword.setText(user.get('password'))
                    QMessageBox.information(self.MainWindow, "Success", "Password found successfully!")
                    found = True
                    break

            if not found:
                self.lineEditTracedPassword.clear()
                QMessageBox.warning(self.MainWindow, "Failed", "Phone number not found in database!")

        except FileNotFoundError:
            QMessageBox.critical(
                self.MainWindow,
                "File Error",
                f"Cannot find users.json!\nPath:\n{json_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self.MainWindow,
                "System Error",
                f"An error occurred:\n{e}"
            )