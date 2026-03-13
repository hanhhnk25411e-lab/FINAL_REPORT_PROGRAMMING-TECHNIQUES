import os
from functools import partial

from PyQt6.QtWidgets import QPushButton, QMessageBox, QButtonGroup, QMainWindow, QScrollArea
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QDate, QSize, QTimer

from models.pet import Pet
from models.pets import Pets

from ui.PetManagementMainWindow import Ui_MainWindow
from ui.PetDetailsMainWindowEx import PetDetailsMainWindowEx


class PetManagementMainWindowEx(Ui_MainWindow):

    def setupUi(self, MainWindow):

        super().setupUi(MainWindow)

        self.MainWindow = MainWindow
        self.current_pet = None

        self.last_added_pet = None
        self.last_updated_pet = None

        font = QFont("Segoe UI Black", 12)

        self.lineEditName.setFont(font)
        self.lineEditID.setFont(font)
        self.lineEditSpecies.setFont(font)
        self.lineEditHealthStatus.setFont(font)

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


    def showWindow(self):
        self.MainWindow.show()


# ---------------- PATH ----------------

    def get_base_dir(self):
        return os.path.dirname(os.path.dirname(__file__))


    def get_json_path(self):
        return os.path.join(self.get_base_dir(), "datasets", "pets.json")


    def get_image_dir(self):
        return os.path.join(self.get_base_dir(), "images")


# ---------------- SIGNALS ----------------

    def setupSignalAndSlot(self):

        self.pushButtonUpdate.clicked.connect(self.process_update)
        self.pushButtonAdd.clicked.connect(self.process_add)

        self.lineEditEnterInfor.returnPressed.connect(self.process_search)

        self.pushButtonMoreDetails.clicked.connect(self.show_details)


# ---------------- ICON ----------------

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

        if os.path.exists(path):
            return QIcon(path)

        return QIcon()


# ---------------- STYLE ----------------

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
            font-family: "Segoe UI Black";
            font-weight: bold;
            padding: 6px;
            border-radius: 6px;
            text-align: left;
        }}

        QPushButton:hover {{
            background-color: {hover};
        }}
        """


# ---------------- DISPLAY PETS ----------------

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

            self.verticalLayoutPets.addWidget(btn)

            btn.clicked.connect(partial(self.view_detail, pet))

        target = self.last_added_pet if self.last_added_pet else self.last_updated_pet

        if target:
            for pet in pets.list:
                if pet.id == target:
                    self.view_detail(pet)
                    break


# ---------------- VIEW PET ----------------

    def view_detail(self, pet):

        self.current_pet = pet

        self.lineEditName.setText(pet.name)
        self.lineEditID.setText(pet.id)
        self.lineEditSpecies.setText(pet.species)
        self.lineEditHealthStatus.setText(pet.health_status)

        date = QDate.fromString(pet.rescue_date, "yyyy-MM-dd")
        self.dateEdit.setDate(date)

        if pet.gender.lower() == "male":
            self.radioButtonMale.setChecked(True)
        else:
            self.radioButtonFemale.setChecked(True)

        if pet.adoption_status.lower() == "adopted":
            self.radioButtonAdopted.setChecked(True)
        else:
            self.radioButtonNotAdopted.setChecked(True)


# ---------------- SHOW DETAILS ----------------

    def show_details(self):

        if self.current_pet is None:

            QMessageBox.warning(
                self.MainWindow,
                "Warning",
                "Please select a pet first!"
            )
            return

        self.details_window = QMainWindow()

        self.details_ui = PetDetailsMainWindowEx()

        self.details_ui.setupUi(self.details_window)

        self.details_ui.load_pet(
            self.current_pet.id,
            self.current_pet.name
        )

        self.details_ui.showWindow()

        # refresh ngay khi đóng cửa sổ details
        self.details_window.closeEvent = self.details_closed


# ---------------- DETAILS CLOSED ----------------

    def details_closed(self, event):

        pets = Pets()
        pets.import_json(self.get_json_path())

        if self.current_pet:
            for p in pets.list:
                if p.id == self.current_pet.id:
                    self.current_pet = p
                    break

        self.display_pets()

        event.accept()


# ---------------- UPDATE ----------------

    def process_update(self):

        if self.current_pet is None:
            QMessageBox.warning(self.MainWindow,"Warning","Please select a pet first!")
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

        QMessageBox.information(self.MainWindow,"Success","Update successful")

        self.display_pets()


# ---------------- ADD PET ----------------

    def process_add(self):

        pets = Pets()
        pets.import_json(self.get_json_path())

        pet = Pet()

        pet.name = self.lineEditName.text()

        ids = []

        for p in pets.list:
            try:
                ids.append(int(p.id.replace("P","")))
            except:
                pass

        new_id = max(ids) + 1 if ids else 1

        pet.id = f"P{new_id:03d}"

        pet.species = self.lineEditSpecies.text()
        pet.health_status = self.lineEditHealthStatus.text()

        pet.rescue_date = self.dateEdit.date().toString("yyyy-MM-dd")

        pet.gender = "Male" if self.radioButtonMale.isChecked() else "Female"

        pet.adoption_status = "Not adopted"

        pets.list.append(pet)

        pets.export_json(self.get_json_path())

        self.last_added_pet = pet.id

        QMessageBox.information(self.MainWindow,"Success","Pet added")

        self.display_pets()

        self.clear_form()

        QTimer.singleShot(200,self.scroll_to_bottom)


# ---------------- SCROLL ----------------

    def scroll_to_bottom(self):

        scroll_areas = self.MainWindow.findChildren(QScrollArea)

        if scroll_areas:

            scroll = scroll_areas[0].verticalScrollBar()

            scroll.setValue(scroll.maximum())


# ---------------- CLEAR FORM ----------------

    def clear_form(self):

        self.lineEditName.clear()
        self.lineEditID.clear()
        self.lineEditSpecies.clear()
        self.lineEditHealthStatus.clear()

        self.radioButtonMale.setChecked(False)
        self.radioButtonFemale.setChecked(False)

        self.radioButtonNotAdopted.setChecked(True)

        self.current_pet = None


# ---------------- SEARCH ----------------

    def process_search(self):

        keyword = self.lineEditEnterInfor.text().lower()

        pets = Pets()
        pets.import_json(self.get_json_path())

        while self.verticalLayoutPets.count():
            child = self.verticalLayoutPets.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for pet in pets.list:

            if keyword in pet.name.lower() or keyword in pet.id.lower():

                btn = QPushButton(f"{pet.id} - {pet.name}")

                btn.setIcon(self.get_pet_icon(pet))
                btn.setIconSize(QSize(24, 24))

                btn.setStyleSheet(self.get_button_style(pet))

                self.verticalLayoutPets.addWidget(btn)

                btn.clicked.connect(partial(self.view_detail, pet))