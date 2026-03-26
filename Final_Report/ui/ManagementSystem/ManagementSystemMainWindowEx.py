from PyQt6.QtWidgets import QMainWindow

from Final_Report.ui.Appointment.AppointmentMainWindowEx import AppointmentMainWindowEx
from Final_Report.ui.CustomerManagement.CustomerManagementMainWindowEx import CustomerManagementMainWindowEx
from Final_Report.ui.EmployeeManagement.EmployeeManagementMainWindowEx import EmployeeManagementMainWindowEx
from Final_Report.ui.ManagementSystem.ManagementSystemMainWindow import Ui_MainWindow
from Final_Report.ui.PetManagement.PetManagementMainWindowEx import PetManagementMainWindowEx
from Final_Report.ui.Statistics.StatisticsMainWindowEx import StatisticsMainWindowEx


class ManagementSystemMainWindowEx(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        self.pushButtonEmployees.clicked.connect(self.openEmployeeManagement)
        self.pushButton_2.clicked.connect(self.openCustomerManagement)
        self.pushButton_3.clicked.connect(self.openPetManagement)
        self.pushButtonAppointment.clicked.connect(self.openAppointment)
        self.pushButtonStats.clicked.connect(self.openStatistics)
        self.pushButtonBack.clicked.connect(self.go_back)

        self.MainWindow.setStyleSheet("""
        QPushButton {
            background-color: #2e7d32;
            color: white;
            padding: 10px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #43a047;
        }
        QPushButton#pushButtonBack {
            background-color: #c62828;
        }
        QPushButton#pushButtonStats {
            background-color: #1565c0;
        }
        """)

    def showWindow(self):
        self.MainWindow.show()

    def openEmployeeManagement(self):
        self.employee_window = QMainWindow()
        self.employee_ui = EmployeeManagementMainWindowEx()
        self.employee_ui.setupUi(self.employee_window)
        self.employee_ui.previous_window = self.MainWindow
        self.employee_window.show()
        self.MainWindow.hide()

    def openCustomerManagement(self):
        self.customer_window = CustomerManagementMainWindowEx()
        self.customer_window.previous_window = self.MainWindow
        self.customer_window.show()
        self.MainWindow.hide()

    def openPetManagement(self):
        self.pet_window = QMainWindow()
        self.pet_ui = PetManagementMainWindowEx()
        self.pet_ui.setupUi(self.pet_window)
        self.pet_ui.previous_window = self.MainWindow
        self.pet_window.show()
        self.MainWindow.hide()

    def openAppointment(self):
        self.app_window = QMainWindow()
        self.app_ui = AppointmentMainWindowEx()
        self.app_ui.setupUi(self.app_window)
        self.app_ui.previous_window = self.MainWindow
        self.app_ui.showWindow()
        self.MainWindow.hide()

    def openStatistics(self):
        self.stat_window = QMainWindow()
        self.stat_ui = StatisticsMainWindowEx()
        self.stat_ui.setupUi(self.stat_window)
        self.stat_ui.previous_window = self.MainWindow
        self.stat_window.show()
        self.MainWindow.hide()

    def go_back(self):
        if hasattr(self, 'previous_window') and self.previous_window:
            self.previous_window.show()
        self.MainWindow.close()