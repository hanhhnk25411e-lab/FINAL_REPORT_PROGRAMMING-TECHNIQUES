import os
import sys
from functools import partial

from PyQt6.QtWidgets import QPushButton, QMessageBox, QButtonGroup, QMainWindow, QScrollArea
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QDate, QSize, QTimer, Qt

from Final_Report.models.pet import Pet
from Final_Report.models.pets import Pets
from Final_Report.ui.PetManagement.PetDetailsMainWindowEx import PetDetailsMainWindowEx
from Final_Report.ui.PetManagement.PetManagementMainWindow import Ui_MainWindow


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../.."))

    return os.path.join(project_root, relative_path)

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


class PetManagementMainWindowEx(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.current_pet = None
        self.last_added_pet = None
        self.last_updated_pet = None

        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit.setMaximumDate(QDate.currentDate())

        self.genderGroup = QButtonGroup()
        self.genderGroup.addButton(self.radioButtonMale)
        self.genderGroup.addButton(self.radioButtonFemale)

        self.adoptionGroup = QButtonGroup()
        self.adoptionGroup.addButton(self.radioButtonAdopted)
        self.adoptionGroup.addButton(self.radioButtonNotAdopted)

        self.display_pets()
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
            padding: 2px;
            border-radius: 6px;
            background-color: white;
            color: rgb(17, 46, 13);
        }

        QDateEdit {
            background-color: white;
            color: rgb(17, 46, 13);
            border-radius: 6px;
            padding: 2px;
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

        QScrollArea {
            border: none;
        }
        """)

    def showWindow(self):
        self.MainWindow.show()

    def get_json_path(self):
        return ensure_file("pets.json")

    def get_image_dir(self):
        return resource_path("Final_Report/images")

    def setupSignalAndSlot(self):
        self.pushButtonUpdate.clicked.connect(self.process_update)
        self.pushButtonAdd.clicked.connect(self.process_add)
        self.lineEditEnterInfor.returnPressed.connect(self.process_search)
        self.pushButtonMoreDetails.clicked.connect(self.show_details)
        self.pushButtonBack.clicked.connect(self.go_back)

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
        }
        QPushButton {
            background-color: #2e7d32;
            color: white;
            border-radius: 6px;
            padding: 6px 12px;
        }
        """)

        msg.exec()

    def get_pet_icon(self, pet):
        img_dir = self.get_image_dir()
        species = pet.species.lower()
        gender = pet.gender.lower()

        if species == "dog" and gender == "male":
            path = os.path.join(img_dir, "ic.male_dog")
        elif species == "dog" and gender == "female":
            path = os.path.join(img_dir, "ic.female_dog")
        elif species == "cat" and gender == "male":
            path = os.path.join(img_dir, "ic.male_cat")
        else:
            path = os.path.join(img_dir, "ic.female_cat")

        return QIcon(path) if os.path.exists(path) else QIcon()

    def get_button_style(self, pet):
        if pet.adoption_status.lower() == "adopted":
            bg = "#2e7d32"
            hover = "#43a047"
        else:
            bg = "#c62828"
            hover = "#e53935"

        return f"""
        QPushButton {{
            background-color: {bg};
            color: white;
            padding: 6px;
            border-radius: 6px;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
        """

    def display_pets(self):
        pets = Pets()
        pets.import_json(self.get_json_path())

        while self.verticalLayoutPets.count():
            child = self.verticalLayoutPets.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for pet in pets.list:
            btn = QPushButton(f"{pet.id} - {pet.name}")
            btn.setIcon(self.get_pet_icon(pet))
            btn.setIconSize(QSize(24, 24))
            btn.setStyleSheet(self.get_button_style(pet))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(40)

            self.verticalLayoutPets.addWidget(btn)
            btn.clicked.connect(partial(self.view_detail, pet))

        target = self.last_added_pet
        if target:
            QTimer.singleShot(100, lambda: self.scroll_to_pet(target))
            self.last_added_pet = None

    def scroll_to_pet(self, pet_id):
        scroll = self.MainWindow.findChildren(QScrollArea)[0]
        bar = scroll.verticalScrollBar()

        for i in range(self.verticalLayoutPets.count()):
            widget = self.verticalLayoutPets.itemAt(i).widget()
            if widget and pet_id in widget.text():
                bar.setValue(widget.y())
                break

    def view_detail(self, pet):
        self.current_pet = pet

        self.lineEditName.setText(pet.name)
        self.lineEditID.setText(pet.id)
        self.lineEditSpecies.setText(pet.species)
        self.lineEditHealthStatus.setText(pet.health_status)

        self.dateEdit.setDate(QDate.fromString(pet.rescue_date, "yyyy-MM-dd"))

        self.radioButtonMale.setChecked(pet.gender.lower() == "male")
        self.radioButtonFemale.setChecked(pet.gender.lower() != "male")

        self.radioButtonAdopted.setChecked(pet.adoption_status.lower() == "adopted")
        self.radioButtonNotAdopted.setChecked(pet.adoption_status.lower() != "adopted")

    def show_details(self):
        if self.current_pet is None:
            self.showMessage("Warning", "Please select a pet first!", QMessageBox.Icon.Warning)
            return

        self.details_window = QMainWindow()
        self.details_ui = PetDetailsMainWindowEx()
        self.details_ui.setupUi(self.details_window)

        self.details_ui.load_pet(self.current_pet.id, self.current_pet.name)
        self.details_window.show()

        self.details_window.closeEvent = self.details_closed

    def details_closed(self, event):
        self.display_pets()
        if self.current_pet:
            pets = Pets()
            pets.import_json(self.get_json_path())

            for p in pets.list:
                if p.id == self.current_pet.id:
                    self.view_detail(p)
                    break

        event.accept()
    def process_update(self):
        if self.current_pet is None:
            self.showMessage("Warning", "Please select a pet first!", QMessageBox.Icon.Warning)
            return

        pets = Pets()
        pets.import_json(self.get_json_path())

        for pet in pets.list:
            if pet.id == self.current_pet.id:
                pet.name = self.lineEditName.text()
                pet.species = self.lineEditSpecies.text()
                pet.health_status = self.lineEditHealthStatus.text()
                pet.rescue_date = self.dateEdit.date().toString("yyyy-MM-dd")
                pet.gender = "Male" if self.radioButtonMale.isChecked() else "Female"
                pet.adoption_status = "Adopted" if self.radioButtonAdopted.isChecked() else "Not adopted"
                self.last_updated_pet = pet.id

        pets.export_json(self.get_json_path())
        self.showMessage("Success", "Update successful")

        self.display_pets()

    def process_add(self):
        pets = Pets()
        pets.import_json(self.get_json_path())

        pet = Pet()
        pet.name = self.lineEditName.text()

        ids = [int(p.id.replace("P", "")) for p in pets.list if p.id.startswith("P")]
        pet.id = f"P{max(ids)+1:03d}" if ids else "P001"

        pet.species = self.lineEditSpecies.text()
        pet.health_status = self.lineEditHealthStatus.text()
        pet.rescue_date = self.dateEdit.date().toString("yyyy-MM-dd")
        pet.gender = "Male" if self.radioButtonMale.isChecked() else "Female"
        pet.adoption_status = "Not adopted"

        pets.list.append(pet)
        pets.export_json(self.get_json_path())

        self.last_added_pet = pet.id

        self.showMessage("Success", "Pet added")

        self.display_pets()
        self.clear_form()

    def clear_form(self):
        self.lineEditName.clear()
        self.lineEditID.clear()
        self.lineEditSpecies.clear()
        self.lineEditHealthStatus.clear()

        self.radioButtonMale.setChecked(False)
        self.radioButtonFemale.setChecked(False)
        self.radioButtonNotAdopted.setChecked(True)

        self.current_pet = None

    def process_search(self):
        keyword = self.lineEditEnterInfor.text().lower()

        pets = Pets()
        pets.import_json(self.get_json_path())

        while self.verticalLayoutPets.count():
            child = self.verticalLayoutPets.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for pet in pets.list:
            searchable_text = " ".join([
                str(pet.id),
                str(pet.name),
                str(pet.species),
                str(pet.health_status),
                str(pet.gender),
                str(pet.adoption_status),
                str(pet.rescue_date)
            ]).lower()

            if keyword in searchable_text:
                btn = QPushButton(f"{pet.id} - {pet.name}")
                btn.setIcon(self.get_pet_icon(pet))
                btn.setIconSize(QSize(24, 24))
                btn.setStyleSheet(self.get_button_style(pet))
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setMinimumHeight(40)

                self.verticalLayoutPets.addWidget(btn)
                btn.clicked.connect(partial(self.view_detail, pet))

    def go_back(self):
        if hasattr(self, 'previous_window') and self.previous_window:
            self.previous_window.show()
        self.MainWindow.close()