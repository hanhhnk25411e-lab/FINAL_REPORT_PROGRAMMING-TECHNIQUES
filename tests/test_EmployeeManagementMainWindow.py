from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.EmployeeManagement.EmployeeManagementMainWindowEx import EmployeeManagementMainWindowEx

app=QApplication([])
gui=EmployeeManagementMainWindowEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()