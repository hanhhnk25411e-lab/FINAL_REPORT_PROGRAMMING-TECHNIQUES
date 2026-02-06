import json
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Forget_Password.Pass import Ui_MainWindow



class PassEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.previous_window = None
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButtonContinueSignIn.clicked.connect(self.returnToSignIn)
        self.pushButtonTracePassword.clicked.connect(self.trace_password)
    def returnToSignIn(self):
        if self.previous_window is not None:
            self.previous_window.show()
        self.MainWindow.close()
    def trace_password(self):
        phone_input = self.lineEditPhone.text().strip()
        if not phone_input:
            QMessageBox.warning(self.MainWindow, "Warning", "Please enter your phone number!")
            return
        json_path = r"D:\LaNguyenMyDung_K254111447_K25411E\Python\FINAL_REPORT_PROGRAMMING-TECHNIQUES\Dung_BIAWEB\dataset\users.json"
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            found = False
            for user in users_data:
                if user.get('phone') == phone_input:
                    self.lineEditTracedPassword.setText(user.get('password'))
                    QMessageBox.information(self.MainWindow, "Success", "Password found successfully!")
                    found = True
                    break
            if not found:
                self.lineEditTracedPassword.clear()
                QMessageBox.warning(self.MainWindow, "Failed", "Phone number not found in database!")

        except FileNotFoundError:
            QMessageBox.critical(self.MainWindow, "File Error",
                                 "Could not find 'users.json' file!\nPlease check the path you pasted in the code.")
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "System Error", f"An error occurred: {e}")