import os
import sys
from functools import partial

from PyQt6.QtWidgets import QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from Final_Report.ui.Adopt.FileFactory import FileFactory
from Final_Report.models.Signup import Signup
from Final_Report.ui.Appointment.AppointmentMainWindow import Ui_MainWindow


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


class AppointmentMainWindowEx(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.fileFactory = FileFactory()
        self.arrData = []
        self.file_path = ensure_file("signup.json")
        self.list_font = QFont("Lao MN", 11)
        self.current_customer = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.previous_window = None
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

        QPushButton#pushButtonBack {
            background-color: #c62828;
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
        """)

    def setupSignalAndSlot(self):
        self.pushButtonBack.clicked.connect(self.go_back)
        self.pushButtonToggleStatus.clicked.connect(self.toggle_status)
        self.lineEditSearch.returnPressed.connect(self.process_search)

    def showWindow(self):
        self.MainWindow.show()

        self.arrData = self.fileFactory.readData(self.file_path, Signup)

        self.display_list()

    def get_button_style(self, customer):
        status = getattr(customer, "Status", "Not Yet")

        if status == "Done":
            bg = "#2e7d32"
            hover = "#43a047"
        else:
            bg = "#c62828"
            hover = "#e53935"

        return f"""
        QPushButton {{
            background-color: {bg};
            color: white;
            padding: 8px;
            border-radius: 8px;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
        """

    def display_list(self, data=None):
        if data is None:
            data = self.arrData

        while self.verticalLayoutAppointment.count():
            child = self.verticalLayoutAppointment.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for customer in data:
            name = getattr(customer, "FullName", "")
            phone = getattr(customer, "PhoneNumber", "")

            btn = QPushButton(f"{name} - {phone}")
            btn.setFont(self.list_font)
            btn.setStyleSheet(self.get_button_style(customer))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(40)

            self.verticalLayoutAppointment.addWidget(btn)
            btn.clicked.connect(partial(self.view_detail, customer))

    def view_detail(self, customer):
        self.current_customer = customer

        self.lineEditFullName.setText(getattr(customer, "FullName", ""))
        self.lineEditPhone.setText(getattr(customer, "PhoneNumber", ""))
        self.lineEditEmail.setText(getattr(customer, "Email", ""))
        self.lineEditLiving.setText(getattr(customer, "LivingType", ""))
        self.lineEditAdopt.setText(getattr(customer, "PetType", ""))
        self.lineEditAppointment.setText(getattr(customer, "AppointmentDate", ""))

        status = getattr(customer, "Status", "Not Yet")
        self.pushButtonToggleStatus.setText(status)

        if status == "Done":
            self.pushButtonToggleStatus.setStyleSheet("background-color:#2e7d32;color:white;")
        else:
            self.pushButtonToggleStatus.setStyleSheet("background-color:#c62828;color:white;")

    def toggle_status(self):
        if not self.current_customer:
            return

        current = getattr(self.current_customer, "Status", "Not Yet")

        if current == "Not Yet":
            new_status = "Done"
        else:
            new_status = "Not Yet"

        setattr(self.current_customer, "Status", new_status)

        self.fileFactory.writeData(self.file_path, self.arrData)

        self.display_list()

        self.pushButtonToggleStatus.setText(new_status)

        if new_status == "Done":
            self.pushButtonToggleStatus.setStyleSheet("background-color:#2e7d32;color:white;")
        else:
            self.pushButtonToggleStatus.setStyleSheet("background-color:#c62828;color:white;")

    def process_search(self):
        keyword = self.lineEditSearch.text().lower()

        filtered = []
        for c in self.arrData:
            name = getattr(c, "FullName", "").lower()
            phone = getattr(c, "PhoneNumber", "").lower()

            if keyword in name or keyword in phone:
                filtered.append(c)

        self.display_list(filtered)

    def go_back(self):
        if hasattr(self, 'previous_window') and self.previous_window:
            self.previous_window.show()
        self.MainWindow.close()