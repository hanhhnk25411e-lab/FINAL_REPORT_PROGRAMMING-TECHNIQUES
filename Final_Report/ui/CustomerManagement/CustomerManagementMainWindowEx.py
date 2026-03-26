import json
import os
import sys

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QTableWidgetItem, QMainWindow, QPushButton, QDateEdit
from PyQt6.QtGui import QColor

from Final_Report.models.customer import Customer
from Final_Report.ui.CustomerManagement.CustomerManagementMainWindow import Ui_MainWindow


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


class CustomerManagementMainWindowEx(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.lineEditSearch.setText("")

        self.file_path = ensure_file("customers.json")

        self.customers = self.load_data()
        self.display_data(self.customers)

        self.ui.lineEditSearch.returnPressed.connect(self.search_customer)

        self.ui.tableWidgetCustomer.cellChanged.connect(self.update_data_from_table)
        self.ui.pushButtonAdd.clicked.connect(self.add_customer)
        self.ui.pushButtonBack.clicked.connect(self.go_back)

        self.setStyleSheet("""
        QPushButton {
            background-color: #2e7d32;
            color: white;
            padding: 6px;
            border-radius: 8px;
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
        }
        QTableWidget {
            border: 2px solid #2e7d32;
            border-radius: 8px;
        }

        QHeaderView::section {
            background-color: #2e7d32;
            color: white;
            border: 1px solid #1b5e20;
        }

        QTableWidget::item:selected {
            background-color: #1b5e20;
            color: white;
        }
        """)

        self.ui.pushButtonAdd.setMinimumHeight(40)
        self.ui.pushButtonBack.setMinimumHeight(35)

    def load_data(self):
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Customer.from_dict(item) for item in data]
        except:
            return []

    def display_data(self, data_list):

        self.ui.tableWidgetCustomer.blockSignals(True)
        self.ui.tableWidgetCustomer.setRowCount(len(data_list))

        for row, c in enumerate(data_list):
            def set_item(col, text):
                item = QTableWidgetItem(text)
                item.setForeground(QColor(17, 46, 13))
                self.ui.tableWidgetCustomer.setItem(row, col, item)

            set_item(0, c.full_name)
            set_item(1, c.pet)
            set_item(2, c.phone)
            set_item(3, c.service)

            progress_btn = QPushButton(c.status)
            progress_btn.setMinimumWidth(120)

            if c.status == "Done":
                progress_btn.setStyleSheet("background-color:#2e7d32;color:white;border-radius:12px;")
            else:
                progress_btn.setStyleSheet("background-color:#fb8c00;color:white;border-radius:12px;")

            progress_btn.clicked.connect(lambda _, r=row: self.toggle_progress(r))
            self.ui.tableWidgetCustomer.setCellWidget(row, 4, progress_btn)

            date_edit = QDateEdit()
            date_edit.setCalendarPopup(True)
            date_edit.setDate(QDate.currentDate())
            self.ui.tableWidgetCustomer.setCellWidget(row, 5, date_edit)

            schedule_btn = QPushButton("Not Scheduled")
            schedule_btn.setMinimumWidth(140)
            schedule_btn.setStyleSheet("background-color:#c62828;color:white;border-radius:12px;")

            schedule_btn.clicked.connect(lambda _, r=row: self.toggle_schedule(r))
            self.ui.tableWidgetCustomer.setCellWidget(row, 6, schedule_btn)

        self.ui.tableWidgetCustomer.blockSignals(False)

    def toggle_progress(self, row):
        btn = self.ui.tableWidgetCustomer.cellWidget(row, 4)

        if btn.text() == "Processing":
            btn.setText("Done")
            btn.setStyleSheet("background-color:#2e7d32;color:white;border-radius:12px;")
        else:
            btn.setText("Processing")
            btn.setStyleSheet("background-color:#fb8c00;color:white;border-radius:12px;")

        self.save_data()

    def toggle_schedule(self, row):
        btn = self.ui.tableWidgetCustomer.cellWidget(row, 6)

        if btn.text() == "Not Scheduled":
            btn.setText("Scheduled")
            btn.setStyleSheet("background-color:#2e7d32;color:white;border-radius:12px;")
        else:
            btn.setText("Not Scheduled")
            btn.setStyleSheet("background-color:#c62828;color:white;border-radius:12px;")

    def search_customer(self):
        query = self.ui.lineEditSearch.text().lower().strip()

        if not query:
            self.display_data(self.customers)
            return

        results = []

        for c in self.customers:
            searchable_text = " ".join([
                str(c.full_name),
                str(c.pet),
                str(c.phone),
                str(c.service),
                str(c.status)
            ]).lower()

            if query in searchable_text:
                results.append(c)

        self.display_data(results)

    def add_customer(self):
        new_c = Customer("New Client", "Cat", "000", "Bath", "Processing")
        self.customers.append(new_c)
        self.save_data()
        self.display_data(self.customers)

    def save_data(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.customers], f, indent=4, ensure_ascii=False)

    def update_data_from_table(self, row, col):
        item = self.ui.tableWidgetCustomer.item(row, col)
        if not item:
            return

        text = item.text()

        if col == 0:
            self.customers[row].full_name = text
        elif col == 1:
            self.customers[row].pet = text
        elif col == 2:
            self.customers[row].phone = text
        elif col == 3:
            self.customers[row].service = text

        self.save_data()

    def go_back(self):
        if hasattr(self, 'previous_window') and self.previous_window:
            self.previous_window.show()

        self.close()