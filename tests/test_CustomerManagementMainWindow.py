import sys
from PyQt6.QtWidgets import QApplication
from ui.CustomerManagement.CustomerManagementMainWindowEx import CustomerManagementMainWindowEx

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomerManagementMainWindowEx()
    window.show()
    sys.exit(app.exec())