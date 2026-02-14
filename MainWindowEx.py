import datetime
from PyQt6.QtWidgets import QMessageBox, QButtonGroup
from FileFactory import FileFactory
from MainWindow import Ui_MainWindow
from Signup import Signup


class MainWindowEx(Ui_MainWindow):

    def __init__(self):
        self.fileFactory = FileFactory()
        self.arrData = []

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # đọc dữ liệu nếu có
        self.arrData = self.fileFactory.readData("signup.json", Signup)

        # =========================
        # TẠO BUTTON GROUP RIÊNG
        # =========================

        # House / Apartment
        self.groupLiving = QButtonGroup(self.MainWindow)
        self.groupLiving.addButton(self.radioButton)
        self.groupLiving.addButton(self.radioButton_2)

        # Yes / No
        self.groupOwned = QButtonGroup(self.MainWindow)
        self.groupOwned.addButton(self.radioButton_3)
        self.groupOwned.addButton(self.radioButton_4)

        # Cat / Dog
        self.groupPet = QButtonGroup(self.MainWindow)
        self.groupPet.addButton(self.radioButton_5)
        self.groupPet.addButton(self.radioButton_6)

        # nút sign up
        self.pushButton.clicked.connect(self.processSignup)

    # =========================
    # VALIDATE
    # =========================

    def validateForm(self):

        if self.lineEdit.text().strip() == "":
            QMessageBox.warning(self.MainWindow, "Error", "Full name required")
            return False

        if self.groupLiving.checkedButton() is None:
            QMessageBox.warning(self.MainWindow, "Error", "Please choose where you live")
            return False

        if self.groupOwned.checkedButton() is None:
            QMessageBox.warning(self.MainWindow, "Error", "Please choose owned pet before")
            return False

        if self.groupPet.checkedButton() is None:
            QMessageBox.warning(self.MainWindow, "Error", "Please choose pet type")
            return False

        if not self.radioButton_7.isChecked():
            QMessageBox.warning(self.MainWindow, "Error", "You must commit to continue")
            return False

        return True

    # =========================
    # LẤY DATA
    # =========================

    def getFormData(self):

        fullName = self.lineEdit.text()
        phone = self.lineEdit_2.text()
        email = self.lineEdit_3.text()
        reason = self.lineEdit_4.text()

        living = self.groupLiving.checkedButton().text()
        owned = self.groupOwned.checkedButton().text()
        pet = self.groupPet.checkedButton().text()

        date = self.dateEdit.date().toPyDate()
        time = self.timeEdit.time().toString()

        return Signup(fullName, phone, email,
                      living, owned, pet,
                      reason, date, time)

    # =========================
    # SIGN UP
    # =========================

    def processSignup(self):

        if not self.validateForm():
            return

        newSignup = self.getFormData()

        self.arrData.append(newSignup)

        self.fileFactory.writeData("signup.json", self.arrData)

        QMessageBox.information(self.MainWindow, "Success", "Signed up successfully!")

        self.resetForm()

    # =========================
    # RESET FORM
    # =========================

    def resetForm(self):

        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()

        self.groupLiving.setExclusive(False)
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.groupLiving.setExclusive(True)

        self.groupOwned.setExclusive(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.groupOwned.setExclusive(True)

        self.groupPet.setExclusive(False)
        self.radioButton_5.setChecked(False)
        self.radioButton_6.setChecked(False)
        self.groupPet.setExclusive(True)

        self.radioButton_7.setChecked(False)
