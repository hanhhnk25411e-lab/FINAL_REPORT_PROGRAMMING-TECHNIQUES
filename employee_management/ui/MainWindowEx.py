import os
from functools import partial

from PyQt6.QtWidgets import QPushButton, QMessageBox
from PyQt6.QtGui import QFont

from employee_management.models.employee import Employee
from employee_management.models.employees import Employees
from employee_management.ui.MainWindow import Ui_MainWindow


class MainWindowEx(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        font = QFont("Segoe UI Black", 12)

        self.lineEditFullName.setFont(font)
        self.lineEditRole.setFont(font)
        self.lineEditPhone.setFont(font)
        self.lineEditAssignedPets.setFont(font)
        self.lineEditShift.setFont(font)
        self.lineEditStatus.setFont(font)

        self.display_employees()
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def get_button_style(self, emp):
        # Role decides text color
        if emp.role.lower() == "doctor":
            text_color = "rgb(235, 225, 41)"  # yellow
        else:
            text_color = "white"  # caretaker

        # Status decides background (priority)
        if emp.status.lower() == "on leave":
            bg_color = "#c62828"
            hover_color = "#e53935"
        else:
            bg_color = "rgb(123, 177, 95)"
            hover_color = "rgb(150, 205, 120)"

        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                font-family: "Segoe UI Black";
                font-weight: bold;
                padding: 6px;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    def display_employees(self):
        self.current_index = None

        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, "datasets", "employees.json")

        emps = Employees()
        emps.import_json(json_path)

        self.clearLayout(self.verticalLayoutEmployee)

        for idx, emp in enumerate(emps.list):
            btn = QPushButton(str(emp.full_name))
            btn.setStyleSheet(self.get_button_style(emp))

            self.verticalLayoutEmployee.addWidget(btn)
            btn.clicked.connect(partial(self.view_detail, emp, idx))

    def view_detail(self, emp, idx):
        self.current_index = idx

        self.lineEditFullName.setText(str(emp.full_name))
        self.lineEditRole.setText(str(emp.role))
        self.lineEditPhone.setText(str(emp.phone))
        self.lineEditAssignedPets.setText(str(emp.assigned_pets))
        self.lineEditShift.setText(str(emp.shift))
        self.lineEditStatus.setText(str(emp.status))

    def setupSignalAndSlot(self):
        self.pushButtonUpdate.clicked.connect(self.process_update)
        self.pushButtonAdd.clicked.connect(self.process_add)
        self.lineEditEnter.returnPressed.connect(self.process_search)

    def process_update(self):
        if self.current_index is None:
            QMessageBox.warning(self.MainWindow, "Warning", "Please select an employee first!")
            return

        emps = Employees()
        emps.import_json("../datasets/employees.json")

        emp = emps.list[self.current_index]

        emp.full_name = self.lineEditFullName.text()
        emp.role = self.lineEditRole.text()
        emp.phone = self.lineEditPhone.text()
        emp.assigned_pets = self.lineEditAssignedPets.text()
        emp.shift = self.lineEditShift.text()
        emp.status = self.lineEditStatus.text()

        emps.export_json("../datasets/employees.json")

        QMessageBox.information(self.MainWindow, "Success", "Update data successful!")
        self.display_employees()

    def process_add(self):
        emps = Employees()
        emps.import_json("../datasets/employees.json")

        emp = Employee()
        emp.full_name = self.lineEditFullName.text().strip()
        emp.role = self.lineEditRole.text().strip()
        emp.phone = self.lineEditPhone.text().strip()
        emp.assigned_pets = self.lineEditAssignedPets.text().strip()
        emp.shift = self.lineEditShift.text().strip()
        emp.status = self.lineEditStatus.text().strip()

        if emp.full_name == "":
            QMessageBox.warning(self.MainWindow, "Warning", "Full name is required!")
            return

        emps.list.append(emp)
        emps.export_json("../datasets/employees.json")

        QMessageBox.information(self.MainWindow, "Success", "Add new employee successful!")

        self.display_employees()

        self.lineEditFullName.clear()
        self.lineEditRole.clear()
        self.lineEditPhone.clear()
        self.lineEditAssignedPets.clear()
        self.lineEditShift.clear()
        self.lineEditStatus.clear()

    def process_search(self):
        self.current_index = None

        base_dir = os.path.dirname(os.path.dirname(__file__))
        json_path = os.path.join(base_dir, "datasets", "employees.json")

        emps = Employees()
        emps.import_json(json_path)

        keyword = self.lineEditEnter.text().strip().lower()

        self.clearLayout(self.verticalLayoutEmployee)

        if keyword == "":
            self.display_employees()
            return

        results = [
            emp for emp in emps.list
            if keyword in emp.full_name.lower()
            or keyword in emp.role.lower()
            or keyword in emp.phone.lower()
            or keyword in emp.assigned_pets.lower()
            or keyword in emp.shift.lower()
            or keyword in emp.status.lower()
        ]

        for idx, emp in enumerate(results):
            btn = QPushButton(str(emp.full_name))
            btn.setStyleSheet(self.get_button_style(emp))

            self.verticalLayoutEmployee.addWidget(btn)
            btn.clicked.connect(partial(self.view_detail, emp, idx))
