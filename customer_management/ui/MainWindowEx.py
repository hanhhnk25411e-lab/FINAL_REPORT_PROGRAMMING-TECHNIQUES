import json
import os
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from MainWindow import Ui_MainWindow
from Customer import Customer


class MainWindowEx(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.file_path = "customers.json"
        self.customers = self.load_data()
        self.display_data(self.customers)
        self.ui.input_search.textChanged.connect(self.search_customer)
        self.ui.btn_add.clicked.connect(self.add_customer)

    def load_data(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Customer.from_dict(item) for item in data]

    def display_data(self, data_list):
        self.ui.table_customers.setRowCount(len(data_list))
        for row, c in enumerate(data_list):
            self.ui.table_customers.setItem(row, 0, QTableWidgetItem(c.full_name))
            self.ui.table_customers.setItem(row, 1, QTableWidgetItem(c.pet))
            self.ui.table_customers.setItem(row, 2, QTableWidgetItem(c.phone))
            self.ui.table_customers.setItem(row, 3, QTableWidgetItem(c.service))
            self.ui.table_customers.setItem(row, 4, QTableWidgetItem(c.status))

    def search_customer(self):
        query = self.ui.input_search.text().lower()
        results = [c for c in self.customers if query in c.full_name.lower() or query in c.phone]
        self.display_data(results)

    def add_customer(self):
        new_c = Customer("New Client", "Cat", "000", "Bath", "Pending")
        self.customers.append(new_c)
        self.save_data()
        self.display_data(self.customers)

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.customers], f, indent=4, ensure_ascii=False)