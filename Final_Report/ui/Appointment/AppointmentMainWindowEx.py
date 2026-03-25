import os
import sys
import json
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

from Final_Report.ui.Appointment.AppointmentMainWindow import Ui_MainWindow


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(sys.executable)
    return os.path.join(base_path, relative_path)


class AppointmentMainWindowEx(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.arrData = []
        self.file_path = resource_path("Final_Report/datasets/signup.json")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.previous_window = None
        self.setupSignalAndSlot()

        self.MainWindow.setStyleSheet("""
        QPushButton {
            background-color: #2e7d32;
            color: white;
            padding: 8px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #43a047;
        }

        QPushButton#pushButtonBack {
            background-color: #c62828;
        }

        QLineEdit {
            border: 2px solid #2e7d32;
            border-radius: 6px;
            padding: 6px;
            background-color: white;
            color: black;
        }

        QListWidget {
            border: 2px solid #2e7d32;
            border-radius: 8px;
            padding: 6px;
            background-color: white;
        }

        QListWidget::item {
            padding: 10px;
            border-radius: 6px;
            margin: 4px;
            color: rgb(17, 46, 13);
        }

        QListWidget::item:selected {
            background-color: #1b5e20;
            color: white;
        }
        """)

    def setupSignalAndSlot(self):
        self.pushButtonBack.clicked.connect(self.go_back)
        self.listWidgetAppointment.itemClicked.connect(self.display_customer_details)
        self.pushButtonToggleStatus.clicked.connect(self.toggle_status)

    def showWindow(self):
        self.MainWindow.show()
        self.load_json()
        self.load_data_to_list()

    def load_json(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                self.arrData = json.load(f)
            except:
                self.arrData = []

    def save_json(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.arrData, f, indent=4, ensure_ascii=False)

    def go_back(self):
        if hasattr(self, 'previous_window') and self.previous_window:
            self.previous_window.show()
        self.MainWindow.close()

    def load_data_to_list(self):
        self.listWidgetAppointment.clear()

        for customer in self.arrData:
            status = customer.get("Status", "Not Yet")
            name = customer.get("FullName", "")
            phone = customer.get("PhoneNumber", "")

            item = QListWidgetItem(f"{name} - {phone}")
            item.setData(Qt.ItemDataRole.UserRole, customer)

            if status == "Done":
                item.setBackground(QColor("#2e7d32"))
            else:
                item.setBackground(QColor("#c62828"))

            item.setForeground(QColor("white"))

            self.listWidgetAppointment.addItem(item)

    def display_customer_details(self, item):
        customer = item.data(Qt.ItemDataRole.UserRole)

        self.lineEditFullName.setText(customer.get("FullName", ""))
        self.lineEditPhone.setText(customer.get("PhoneNumber", ""))
        self.lineEditEmail.setText(customer.get("Email", ""))
        self.lineEditLiving.setText(customer.get("LivingType", ""))
        self.lineEditAdopt.setText(customer.get("PetType", ""))
        self.lineEditAppointment.setText(customer.get("AppointmentDate", ""))

        self.pushButtonToggleStatus.setText(customer.get("Status", "Not Yet"))

    def toggle_status(self):
        item = self.listWidgetAppointment.currentItem()
        if not item:
            return

        customer = item.data(Qt.ItemDataRole.UserRole)

        current = customer.get("Status", "Not Yet")
        new_status = "Done" if current == "Not Yet" else "Not Yet"

        customer["Status"] = new_status

        if new_status == "Done":
            item.setBackground(QColor("#2e7d32"))
        else:
            item.setBackground(QColor("#c62828"))

        item.setForeground(QColor("white"))

        self.pushButtonToggleStatus.setText(new_status)

        self.save_json()