import os
import sys
from functools import partial

from PyQt6.QtWidgets import QPushButton, QMessageBox, QButtonGroup, QScrollArea
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QTimer, Qt

from Final_Report.models.employee import Employee
from Final_Report.models.employees import Employees
from Final_Report.ui.EmployeeManagement.EmployeeManagementMainWindow import Ui_MainWindow


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(sys.executable)
    return os.path.join(base_path, relative_path)


class EmployeeManagementMainWindowEx(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.current_employee = None
        self.last_added_employee = None
        self.last_updated_employee = None
        self.list_font = QFont("Lao MN", 11)

        self.genderGroup = QButtonGroup()
        self.genderGroup.addButton(self.radioButtonMale)
        self.genderGroup.addButton(self.radioButtonFemale)

        self.statusGroup = QButtonGroup()
        self.statusGroup.addButton(self.radioButtonActive)
        self.statusGroup.addButton(self.radioButtonOnleave)

        self.display_employees()
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
            color: black;
        }

        QDateEdit {
            background-color: white;
            color: black;
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
        return resource_path("Final_Report/datasets/employees.json")

    def get_image_dir(self):
        return resource_path("Final_Report/images")

    def setupSignalAndSlot(self):
        self.pushButtonUpdate.clicked.connect(self.process_update)
        self.pushButtonAdd.clicked.connect(self.process_add)
        self.lineEditSearch.returnPressed.connect(self.process_search)
        self.pushButtonBack.clicked.connect(self.go_back)

    def get_employee_icon(self, emp):
        img_dir = self.get_image_dir()
        gender = emp.gender.lower()
        role = emp.role.lower()

        if role == "doctor" and gender == "male":
            path = os.path.join(img_dir, "male_doctor.png")
        elif role == "doctor" and gender == "female":
            path = os.path.join(img_dir, "female_doctor.png")
        elif role == "caretaker" and gender == "male":
            path = os.path.join(img_dir, "male_caretaker.png")
        else:
            path = os.path.join(img_dir, "female_caretaker.png")

        return QIcon(path) if os.path.exists(path) else QIcon()

    def get_button_style(self, emp):
        if emp.status.lower() == "active":
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
            font-weight: normal;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
        """

    def display_employees(self):
        emps = Employees()
        emps.import_json(self.get_json_path())

        while self.verticalLayoutEmployees.count():
            child = self.verticalLayoutEmployees.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for emp in emps.list:
            btn = QPushButton(f"{emp.id} - {emp.full_name}")
            btn.setIcon(self.get_employee_icon(emp))
            btn.setStyleSheet(self.get_button_style(emp))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(40)
            btn.setFont(self.list_font)

            self.verticalLayoutEmployees.addWidget(btn)
            btn.clicked.connect(partial(self.view_detail, emp))

        target = self.last_added_employee
        if target:
            QTimer.singleShot(100, lambda: self.scroll_to_employee(target))
            self.last_added_employee = None

    def scroll_to_employee(self, emp_id):
        scroll_areas = self.MainWindow.findChildren(QScrollArea)
        if not scroll_areas:
            return

        scroll = scroll_areas[0]
        bar = scroll.verticalScrollBar()

        for i in range(self.verticalLayoutEmployees.count()):
            widget = self.verticalLayoutEmployees.itemAt(i).widget()
            if widget and emp_id in widget.text():
                bar.setValue(widget.y())
                break

    def view_detail(self, emp):
        self.current_employee = emp

        self.lineEditFullName.setText(emp.full_name)
        self.lineEditID.setText(emp.id)
        self.lineEditRole.setText(emp.role)
        self.lineEditPhoneNumber.setText(emp.phone)
        self.lineEditAssignedPet.setText(emp.assigned_pets)

        self.radioButtonMale.setChecked(emp.gender.lower() == "male")
        self.radioButtonFemale.setChecked(emp.gender.lower() != "male")

        self.radioButtonActive.setChecked(emp.status.lower() == "active")
        self.radioButtonOnleave.setChecked(emp.status.lower() != "active")

    def process_add(self):
        emps = Employees()
        emps.import_json(self.get_json_path())

        emp = Employee()

        ids = []
        for e in emps.list:
            try:
                ids.append(int(e.id.replace("E", "")))
            except:
                pass

        emp.id = f"E{max(ids)+1:03d}" if ids else "E001"

        emp.full_name = self.lineEditFullName.text()
        emp.role = self.lineEditRole.text()
        emp.phone = self.lineEditPhoneNumber.text()
        emp.assigned_pets = self.lineEditAssignedPet.text()

        emp.gender = "Male" if self.radioButtonMale.isChecked() else "Female"
        emp.status = "Active"

        emps.list.append(emp)
        emps.export_json(self.get_json_path())

        self.last_added_employee = emp.id

        QMessageBox.information(self.MainWindow, "Success", "Employee added")

        self.display_employees()
        self.clear_form()

    def process_update(self):
        if not self.current_employee:
            QMessageBox.warning(self.MainWindow, "Warning", "Please select an employee first!")
            return

        emps = Employees()
        emps.import_json(self.get_json_path())

        for emp in emps.list:
            if emp.id == self.current_employee.id:
                emp.full_name = self.lineEditFullName.text()
                emp.role = self.lineEditRole.text()
                emp.phone = self.lineEditPhoneNumber.text()
                emp.assigned_pets = self.lineEditAssignedPet.text()

                emp.gender = "Male" if self.radioButtonMale.isChecked() else "Female"
                emp.status = "Active" if self.radioButtonActive.isChecked() else "On leave"

                self.last_updated_employee = emp.id

        emps.export_json(self.get_json_path())
        QMessageBox.information(self.MainWindow, "Success", "Updated")

        self.display_employees()

    def clear_form(self):
        self.lineEditFullName.clear()
        self.lineEditID.clear()
        self.lineEditRole.clear()
        self.lineEditPhoneNumber.clear()
        self.lineEditAssignedPet.clear()

        self.radioButtonMale.setChecked(False)
        self.radioButtonFemale.setChecked(False)
        self.radioButtonActive.setChecked(True)

        self.current_employee = None

    def process_search(self):
        keyword = self.lineEditSearch.text().lower()

        emps = Employees()
        emps.import_json(self.get_json_path())

        while self.verticalLayoutEmployees.count():
            child = self.verticalLayoutEmployees.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for emp in emps.list:
            if keyword in emp.full_name.lower() or keyword in emp.id.lower():
                btn = QPushButton(f"{emp.id} - {emp.full_name}")
                btn.setIcon(self.get_employee_icon(emp))
                btn.setStyleSheet(self.get_button_style(emp))
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setMinimumHeight(40)
                btn.setFont(self.list_font)

                self.verticalLayoutEmployees.addWidget(btn)
                btn.clicked.connect(partial(self.view_detail, emp))

    def go_back(self):
        if hasattr(self, 'previous_window') and self.previous_window:
            self.previous_window.show()
        self.MainWindow.close()