import json
import os
from PyQt6.QtWidgets import QTableWidgetItem
from CustomerManagementMainWindow import Ui_MainWindow
from models.customer import Customer


class CustomerManagementMainWindowEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEditSearch.setText("")
        self.ui.lineEditSearch.setPlaceholderText("Find customer's name, phone number")
        self.file_path = "customers.json"
        self.customers = self.load_data()
        self.display_data(self.customers)
        self.ui.lineEditSearch.textChanged.connect(self.search_customer)
        self.ui.pushButtonAdd.clicked.connect(self.add_customer)

    def load_data(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Customer.from_dict(item) for item in data]
        except Exception as e:
            print(f"read file error: {e}")
            return []

    def display_data(self, data_list):
        self.ui.tableWidgetCustomer.setRowCount(len(data_list))
        for row, c in enumerate(data_list):
            self.ui.tableWidgetCustomer.setItem(row, 0, QTableWidgetItem(c.full_name))
            self.ui.tableWidgetCustomer.setItem(row, 1, QTableWidgetItem(c.pet))
            self.ui.tableWidgetCustomer.setItem(row, 2, QTableWidgetItem(c.phone))
            self.ui.tableWidgetCustomer.setItem(row, 3, QTableWidgetItem(c.service))
            self.ui.tableWidgetCustomer.setItem(row, 4, QTableWidgetItem(c.status))

    def search_customer(self):
        query = self.ui.lineEditSearch.text().lower()
        if not query:
            self.display_data(self.customers)
            return

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