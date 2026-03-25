import os
import sys
from PyQt6.QtWidgets import QMessageBox, QButtonGroup

from Final_Report.models.Signup import Signup
from Final_Report.ui.Adopt.FileFactory import FileFactory
from Final_Report.ui.Adopt.AdoptMainWindow import Ui_MainWindow


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(sys.executable)

    return os.path.join(base_path, relative_path)


class AdoptMainWindowEx(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.fileFactory = FileFactory()
        self.arrData = []

        self.file_path = resource_path("Final_Report/datasets/signup.json")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        self.arrData = self.fileFactory.readData(
            path=self.file_path,
            ClassName=Signup
        )

        self.setupSignalAndSlot()

        self.MainWindow.setStyleSheet("""
        QPushButton {
            background-color: #2e7d32;
            color: white;
            padding: 6px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #43a047;
        }

        QLineEdit {
            border: 2px solid #2e7d32;
            border-radius: 6px;
            padding: 6px;
            background-color: white;
            color: black;
        }

        QDateEdit, QTimeEdit {
            background-color: white;
            color: black;
            border: 2px solid #2e7d32;
            border-radius: 6px;
            padding: 4px;
        }

        QDateEdit::drop-down {
            background-color: white;
        }

        QRadioButton {
            color: #1b5e20;
            font-size: 13px;
        }

        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid #2e7d32;
            background-color: white;
        }

        QRadioButton::indicator:checked {
            background-color: #2e7d32;
            border: 2px solid #2e7d32;
        }

        QRadioButton::indicator:hover {
            border: 2px solid #66bb6a;
        }
        """)

        self.dateEdit.setStyleSheet("background-color: white; color: black;")

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonSignUp.clicked.connect(self.processSignup)
        self.pushButtonBack.clicked.connect(self.go_back)

        self.groupLiving = QButtonGroup(self.MainWindow)
        self.groupLiving.addButton(self.radioButtonHouse)
        self.groupLiving.addButton(self.radioButtonApartment)

        self.groupOwned = QButtonGroup(self.MainWindow)
        self.groupOwned.addButton(self.radioButtonYes)
        self.groupOwned.addButton(self.radioButtonNo)

        self.groupPet = QButtonGroup(self.MainWindow)
        self.groupPet.addButton(self.radioButtonCat)
        self.groupPet.addButton(self.radioButtonDog)

    def showMessage(self, title, text, icon=QMessageBox.Icon.Information):
        msg = QMessageBox(self.MainWindow)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)

        msg.setStyleSheet("""
        QMessageBox {
            background-color: #e8f5e9;
        }

        QLabel {
            color: #1b5e20;
            font-size: 14px;
        }

        QPushButton {
            background-color: #2e7d32;
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: #66bb6a;
        }
        """)

        msg.exec()

    def validateForm(self):

        if self.lineEditFullName.text().strip() == "":
            self.showMessage("Error", "Full name required", QMessageBox.Icon.Warning)
            return False

        if self.groupLiving.checkedButton() is None:
            self.showMessage("Error", "Please choose where you live", QMessageBox.Icon.Warning)
            return False

        if self.groupOwned.checkedButton() is None:
            self.showMessage("Error", "Please choose owned pet before", QMessageBox.Icon.Warning)
            return False

        if self.groupPet.checkedButton() is None:
            self.showMessage("Error", "Please choose pet type", QMessageBox.Icon.Warning)
            return False

        if not self.radioButtonCommit.isChecked():
            self.showMessage("Error", "You must commit to continue", QMessageBox.Icon.Warning)
            return False

        return True

    def getFormData(self):
        return Signup(
            self.lineEditFullName.text(),
            self.lineEditPhoneNumber.text(),
            self.lineEditEmail.text(),
            self.groupLiving.checkedButton().text(),
            self.groupOwned.checkedButton().text(),
            self.groupPet.checkedButton().text(),
            self.lineEditReason.text(),
            self.dateEdit.date().toPyDate(),
            self.timeEdit.time().toString()
        )

    def processSignup(self):

        if not self.validateForm():
            return

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        newSignup = self.getFormData()

        self.arrData.append(newSignup)

        self.fileFactory.writeData(self.file_path, self.arrData)

        self.showMessage("Success", "Signed up successfully!")

        self.resetForm()

    def resetForm(self):

        self.lineEditFullName.clear()
        self.lineEditPhoneNumber.clear()
        self.lineEditEmail.clear()
        self.lineEditReason.clear()

        for group in [self.groupLiving, self.groupOwned, self.groupPet]:
            group.setExclusive(False)
            for btn in group.buttons():
                btn.setChecked(False)
            group.setExclusive(True)

        self.radioButtonCommit.setChecked(False)

    def go_back(self):

        if hasattr(self, 'previous_window') and self.previous_window:
            self.previous_window.show()

        self.MainWindow.close()