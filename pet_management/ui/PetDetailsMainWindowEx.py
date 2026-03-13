from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QColor

from models.rescue_cases import RescueCases
from models.rescue_case import RescueCase

from models.medical_records import MedicalRecords
from models.medical_record import MedicalRecord

from models.adopters import Adopters
from models.adopter import Adopter

from models.pets import Pets

from ui.PetDetailsMainWindow import Ui_MainWindow


class PetDetailsMainWindowEx(Ui_MainWindow):

    def __init__(self):

        self.lr = RescueCases()
        self.lm = MedicalRecords()
        self.la = Adopters()

        self.current_pet_id = None


    def setupUi(self, MainWindow):

        super().setupUi(MainWindow)

        self.MainWindow = MainWindow

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels([
            "Date", "Diagnosis", "P.I.C"
        ])

        self.lr.import_json("../datasets/rescue_cases.json")
        self.lm.import_json("../datasets/medical_records.json")
        self.la.import_json("../datasets/adopters.json")

        self.setupSignals()


    def showWindow(self):
        self.MainWindow.show()


# ---------------- SIGNALS ----------------

    def setupSignals(self):

        self.pushButtonBack.clicked.connect(self.go_back)

        self.pushButtonAdd.clicked.connect(self.add_new_information)
        self.pushButtonUpdate.clicked.connect(self.update_information)

        self.pushButtonAddRecord.clicked.connect(self.add_medical)

        self.tableWidget.cellClicked.connect(self.load_history_detail)


# ---------------- BACK ----------------

    def go_back(self):
        self.MainWindow.close()


# ---------------- LOAD PET ----------------

    def load_pet(self, pet_id, pet_name):

        self.current_pet_id = pet_id

        self.lineEditPetName.setText(pet_name)
        self.lineEditPetId.setText(pet_id)

        self.tabWidget.setCurrentIndex(0)

        self.load_rescue_case()
        self.load_medical_records()
        self.load_adopter()


# ---------------- RESCUE ----------------

    def load_rescue_case(self):

        for it in self.lr.list:

            if it.pet_id == self.current_pet_id:

                date = QDate.fromString(it.date, "yyyy-MM-dd")

                self.dateEditRescuDate.setDate(date)

                self.lineEditLocation.setText(it.location)
                self.lineEditStatus.setText(it.status)
                self.textEditDescription.setPlainText(it.description)

                return


    def add_rescue(self):

        date = self.dateEditRescuDate.date().toString("yyyy-MM-dd")

        location = self.lineEditLocation.text()
        status = self.lineEditStatus.text()
        description = self.textEditDescription.toPlainText()

        rc = RescueCase(
            self.current_pet_id,
            date,
            location,
            status,
            description
        )

        self.lr.add_item(rc)
        self.lr.export_json("../datasets/rescue_cases.json")

        QMessageBox.information(self.MainWindow, "Success", "Rescue case added")


    def update_rescue(self):

        date = self.dateEditRescuDate.date().toString("yyyy-MM-dd")

        location = self.lineEditLocation.text()
        status = self.lineEditStatus.text()
        description = self.textEditDescription.toPlainText()

        rc = RescueCase(
            self.current_pet_id,
            date,
            location,
            status,
            description
        )

        self.lr.update_rescue_case(rc)
        self.lr.export_json("../datasets/rescue_cases.json")

        QMessageBox.information(self.MainWindow, "Success", "Rescue case updated")


# ---------------- MEDICAL ----------------

    def load_medical_records(self):

        self.tableWidget.setRowCount(0)

        records = []

        for it in self.lm.list:
            if it.pet_id == self.current_pet_id:
                records.append(it)

        # sort ngày mới nhất
        records.sort(key=lambda x: x.date, reverse=True)

        for it in records:

            row = self.tableWidget.rowCount()

            self.tableWidget.insertRow(row)

            self.tableWidget.setItem(row, 0, QTableWidgetItem(it.date))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(it.diagnosis))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(it.person_in_charge))


# ---------------- CLICK HISTORY ----------------

    def load_history_detail(self, row, col):

        date = self.tableWidget.item(row, 0).text()

        for it in self.lm.list:

            if it.pet_id == self.current_pet_id and it.date == date:

                d = QDate.fromString(it.date, "yyyy-MM-dd")

                self.dateEditMedicalDate.setDate(d)

                self.lineEditPIC.setText(it.person_in_charge)
                self.lineEditDiagnosis.setText(it.diagnosis)
                self.lineEditTreatment.setText(it.treatment)

                if it.vaccination == "Yes":
                    self.radioButtonYes.setChecked(True)
                else:
                    self.radioButtonNo.setChecked(True)

                break


# ---------------- ADD MEDICAL RECORD ----------------

    def add_medical(self):

        date = self.dateEditMedicalDate.date().toString("yyyy-MM-dd")

        person = self.lineEditPIC.text()
        diagnosis = self.lineEditDiagnosis.text()
        treatment = self.lineEditTreatment.text()

        vaccination = "Yes" if self.radioButtonYes.isChecked() else "No"

        mr = MedicalRecord(
            self.current_pet_id,
            date,
            person,
            diagnosis,
            treatment,
            vaccination
        )

        self.lm.add_item(mr)

        self.lm.export_json("../datasets/medical_records.json")

        # reload table
        self.load_medical_records()

        # tìm row vừa add
        for row in range(self.tableWidget.rowCount()):

            if self.tableWidget.item(row, 0).text() == date:

                highlight = QColor(255, 255, 150)

                for col in range(3):
                    self.tableWidget.item(row, col).setBackground(highlight)

                self.tableWidget.selectRow(row)

                # load dữ liệu lên form
                self.load_history_detail(row, 0)

                break

        QMessageBox.information(self.MainWindow, "Success", "Medical record added")


# ---------------- ADD / UPDATE BUTTON ----------------

    def add_new_information(self):

        index = self.tabWidget.currentIndex()

        if index == 0:
            self.add_rescue()

        elif index == 2:
            self.add_adopter()


    def update_information(self):

        index = self.tabWidget.currentIndex()

        if index == 0:
            self.update_rescue()

        elif index == 2:
            self.update_adopter()


# ---------------- ADOPTER ----------------

    def load_adopter(self):

        for it in self.la.list:

            if it.pet_id == self.current_pet_id:

                self.lineEditAdopterName.setText(it.full_name)
                self.lineEditAdopterId.setText(it.id)
                self.lineEditPhoneNumber.setText(it.phone)
                self.lineEditAddress.setText(it.address)

                date = QDate.fromString(it.adopted_date, "yyyy-MM-dd")
                self.dateEditAdoptDate.setDate(date)

                return

        self.lineEditAdopterName.clear()
        self.lineEditAdopterId.clear()
        self.lineEditPhoneNumber.clear()
        self.lineEditAddress.clear()


# ---------------- ADD ADOPTER ----------------

    def add_adopter(self):

        name = self.lineEditAdopterName.text()

        if name == "":
            QMessageBox.warning(self.MainWindow, "Warning", "Adopter name cannot be empty")
            return

        id_ = self.lineEditAdopterId.text()
        phone = self.lineEditPhoneNumber.text()
        address = self.lineEditAddress.text()
        date = self.dateEditAdoptDate.date().toString("yyyy-MM-dd")

        adopter = Adopter(
            self.current_pet_id,
            name,
            id_,
            phone,
            address,
            date
        )

        self.la.add_item(adopter)
        self.la.export_json("../datasets/adopters.json")

        self.update_pet_status("Adopted")

        QMessageBox.information(self.MainWindow, "Success", "Adopter added")


# ---------------- UPDATE ADOPTER ----------------

    def update_adopter(self):

        name = self.lineEditAdopterName.text()

        if name == "":

            self.la.list = [
                a for a in self.la.list
                if a.pet_id != self.current_pet_id
            ]

            self.la.export_json("../datasets/adopters.json")

            self.update_pet_status("Not adopted")

            QMessageBox.information(self.MainWindow, "Success", "Adopter removed")

            return


        id_ = self.lineEditAdopterId.text()
        phone = self.lineEditPhoneNumber.text()
        address = self.lineEditAddress.text()
        date = self.dateEditAdoptDate.date().toString("yyyy-MM-dd")

        adopter = Adopter(
            self.current_pet_id,
            name,
            id_,
            phone,
            address,
            date
        )

        self.la.update_adopter(adopter)
        self.la.export_json("../datasets/adopters.json")

        self.update_pet_status("Adopted")

        QMessageBox.information(self.MainWindow, "Success", "Adopter updated")


# ---------------- UPDATE PET STATUS ----------------

    def update_pet_status(self, status):

        pets = Pets()

        pets.import_json("../datasets/pets.json")

        for pet in pets.list:

            if pet.id == self.current_pet_id:

                pet.adoption_status = status
                break

        pets.export_json("../datasets/pets.json")