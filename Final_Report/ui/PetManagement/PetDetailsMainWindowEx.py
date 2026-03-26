import os
import sys
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6.QtCore import QDate

from Final_Report.models.rescue_cases import RescueCases
from Final_Report.models.rescue_case import RescueCase
from Final_Report.models.medical_records import MedicalRecords
from Final_Report.models.medical_record import MedicalRecord
from Final_Report.models.adopters import Adopters
from Final_Report.models.adopter import Adopter
from Final_Report.models.pets import Pets
from Final_Report.ui.PetManagement.PetDetailsMainWindow import Ui_MainWindow


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
            import json
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    return data_path


class PetDetailsMainWindowEx(Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.lr = RescueCases()
        self.lm = MedicalRecords()
        self.la = Adopters()

        self.current_pet_id = None

        self.path_rescue = ensure_file("rescue_cases.json")
        self.path_medical = ensure_file("medical_records.json")
        self.path_adopter = ensure_file("adopters.json")
        self.path_pet = ensure_file("pets.json")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow


        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels([
            "Date", "Diagnosis", "P.I.C"
        ])

        self.lr.import_json(self.path_rescue)
        self.lm.import_json(self.path_medical)
        self.la.import_json(self.path_adopter)

        self.setupSignals()

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
            padding: 2px;
            border-radius: 6px;
            background-color: white;
            color: rgb(17, 46, 13);
            border: 0.5px solid #2e7d32;
        }
        QTextEdit {
            padding: 2px;
            border-radius: 6px;
            background-color: white;
            color: rgb(17, 46, 13);
            border: 0.5px solid #2e7d32;
        }
        QDateEdit {
            background-color: white;
            color: rgb(17, 46, 13);
            border-radius: 6px;
            padding: 2px;
            border: 0.5px solid #2e7d32;
        }

        QRadioButton {
            color: #1b5e20;
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
        }

        QTableWidget {
            background-color: white;
            border: 2px solid #2e7d32;
        }

        QHeaderView::section {
            background-color: #2e7d32;
            color: white;
        }
        """)

        self.dateEditRescuDate.setStyleSheet("background:white;color:black;")
        self.dateEditMedicalDate.setStyleSheet("background:white;color:black;")
        self.dateEditAdoptDate.setStyleSheet("background:white;color:black;")
        self.tabWidget.currentChanged.connect(self.set_focus_by_tab)

    def showWindow(self):
        self.MainWindow.show()

    def setupSignals(self):
        self.pushButtonBack.clicked.connect(self.go_back)
        self.pushButtonAdd.clicked.connect(self.add_new_information)
        self.pushButtonUpdate.clicked.connect(self.update_information)
        self.pushButtonAddRecord.clicked.connect(self.add_medical)
        self.tableWidget.cellClicked.connect(self.load_history_detail)

    def go_back(self):
        self.MainWindow.close()

    def load_pet(self, pet_id, pet_name):
        self.current_pet_id = pet_id

        self.lineEditPetName.setText(pet_name)
        self.lineEditPetId.setText(pet_id)

        self.tabWidget.setCurrentIndex(0)

        self.load_rescue_case()
        self.load_medical_records()
        self.load_adopter()

    def load_rescue_case(self):
        for it in self.lr.list:
            if it.pet_id == self.current_pet_id:
                self.dateEditRescuDate.setDate(QDate.fromString(it.date, "yyyy-MM-dd"))
                self.lineEditLocation.setText(it.location)
                self.lineEditStatus.setText(it.status)
                self.textEditDescription.setPlainText(it.description)
                return

    def add_rescue(self):
        rc = RescueCase(
            self.current_pet_id,
            self.dateEditRescuDate.date().toString("yyyy-MM-dd"),
            self.lineEditLocation.text(),
            self.lineEditStatus.text(),
            self.textEditDescription.toPlainText()
        )
        self.lr.add_item(rc)
        self.lr.export_json(self.path_rescue)
        QMessageBox.information(self.MainWindow, "Success", "Rescue case added")

    def update_rescue(self):
        rc = RescueCase(
            self.current_pet_id,
            self.dateEditRescuDate.date().toString("yyyy-MM-dd"),
            self.lineEditLocation.text(),
            self.lineEditStatus.text(),
            self.textEditDescription.toPlainText()
        )
        self.lr.update_rescue_case(rc)
        self.lr.export_json(self.path_rescue)
        QMessageBox.information(self.MainWindow, "Success", "Rescue case updated")

    def load_medical_records(self):
        self.tableWidget.setRowCount(0)

        records = [it for it in self.lm.list if it.pet_id == self.current_pet_id]
        records.sort(key=lambda x: x.date, reverse=True)

        for it in records:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)

            self.tableWidget.setItem(row, 0, QTableWidgetItem(it.date))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(it.diagnosis))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(it.person_in_charge))

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

    def add_medical(self):
        mr = MedicalRecord(
            self.current_pet_id,
            self.dateEditMedicalDate.date().toString("yyyy-MM-dd"),
            self.lineEditPIC.text(),
            self.lineEditDiagnosis.text(),
            self.lineEditTreatment.text(),
            "Yes" if self.radioButtonYes.isChecked() else "No"
        )

        self.lm.add_item(mr)
        self.lm.export_json(self.path_medical)

        self.load_medical_records()

        QMessageBox.information(self.MainWindow, "Success", "Medical record added")

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

    def load_adopter(self):
        pets = Pets()
        pets.import_json(self.path_pet)

        pet_status = "Not adopted"
        for p in pets.list:
            if p.id == self.current_pet_id:
                pet_status = p.adoption_status
                break

        if pet_status.lower() != "adopted":
            self.lineEditAdopterName.clear()
            self.lineEditAdopterId.clear()
            self.lineEditPhoneNumber.clear()
            self.lineEditAddress.clear()
            return

        # nếu adopted thì mới load
        for it in self.la.list:
            if it.pet_id == self.current_pet_id:
                self.lineEditAdopterName.setText(it.full_name)
                self.lineEditAdopterId.setText(it.id)
                self.lineEditPhoneNumber.setText(it.phone)
                self.lineEditAddress.setText(it.address)

                date = QDate.fromString(it.adopted_date, "yyyy-MM-dd")
                self.dateEditAdoptDate.setDate(date)
                return

    def add_adopter(self):
        name = self.lineEditAdopterName.text()

        if name == "":
            QMessageBox.warning(self.MainWindow, "Warning", "Adopter name cannot be empty")
            return

        adopter = Adopter(
            self.current_pet_id,
            name,
            self.lineEditAdopterId.text(),
            self.lineEditPhoneNumber.text(),
            self.lineEditAddress.text(),
            self.dateEditAdoptDate.date().toString("yyyy-MM-dd")
        )

        self.la.add_item(adopter)
        self.la.export_json(self.path_adopter)

        self.update_pet_status("Adopted")

        QMessageBox.information(self.MainWindow, "Success", "Adopter added")

    def update_adopter(self):
        name = self.lineEditAdopterName.text()

        if name == "":
            self.la.list = [a for a in self.la.list if a.pet_id != self.current_pet_id]
            self.la.export_json(self.path_adopter)

            self.update_pet_status("Not adopted")

            QMessageBox.information(self.MainWindow, "Success", "Adopter removed")
            return

        adopter = Adopter(
            self.current_pet_id,
            name,
            self.lineEditAdopterId.text(),
            self.lineEditPhoneNumber.text(),
            self.lineEditAddress.text(),
            self.dateEditAdoptDate.date().toString("yyyy-MM-dd")
        )

        self.la.update_adopter(adopter)
        self.la.export_json(self.path_adopter)

        self.update_pet_status("Adopted")

        QMessageBox.information(self.MainWindow, "Success", "Adopter updated")


    def update_pet_status(self, status):
        pets = Pets()
        pets.import_json(self.path_pet)

        for pet in pets.list:
            if pet.id == self.current_pet_id:
                pet.adoption_status = status
                break

        pets.export_json(self.path_pet)

    def set_focus_by_tab(self, index):
        if index == 0:
            self.lineEditPetName.setFocus()
        elif index == 1:
            self.lineEditPIC.setFocus()