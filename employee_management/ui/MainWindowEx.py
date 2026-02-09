from functools import partial

from PyQt6.QtWidgets import QPushButton, QMessageBox

from employee_management.models.employee import Employee
from employee_management.models.employees import Employees
from employee_management.ui.MainWindow import Ui_MainWindow


class MainWindowEx(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
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

    def display_employees(self):
        #step 1: load dataset from assets.json
        emps = Employees()
        emps.import_json("../datasets/employees.json")

        #step 2: display data into GUI
        self.clearLayout(self.verticalLayoutEmployee)

        for emp in emps.list:
            btn = QPushButton(text=str(emp.full_name))

            # highlight theo role
            if emp.role.lower() == "doctor":
                btn.setStyleSheet("QPushButton { color: blue; font-weight: bold; }")

            elif emp.role.lower() == "caretaker":
                btn.setStyleSheet("QPushButton { color: green; }")

            # nếu đang nghỉ thì ưu tiên màu đỏ
            if emp.status.lower() == "on leave":
                btn.setStyleSheet("QPushButton { color: red; font-weight: bold; }")

            self.verticalLayoutEmployee.addWidget(btn)
            btn.clicked.connect(partial(self.view_detail, emp))
    def view_detail(self,emp):
        self.lineEditFullName.setText(str(emp.full_name))
        self.lineEditRole.setText(str(emp.role))
        self.lineEditPhone.setText(str(emp.phone))
        self.lineEditAssignedPets.setText(str(emp.assigned_pets))
        self.lineEditShift.setText(str(emp.shift))
        self.lineEditStatus.setText(str(emp.status))
    def setupSignalAndSlot(self):
        self.pushButtonAdd.clicked.connect(self.process_update)
    def process_update(self):
        emps = Employees()
        emps.import_json("../datasets/employees.json")
        emp=Employee()
        emp.full_name=self.lineEditFullName.text()
        emp.role=self.lineEditRole.text()
        emp.phone=self.lineEditPhone.text()
        emp.assigned_pets=self.lineEditAssignedPets.text()
        emp.shift=self.lineEditShift.text()
        emp.status=self.lineEditStatus.text()
        result=emps.update_employee(emp)
        if result==True:#update MEMORY successful
            #then we export data to HDD
            emps.export_json("../datasets/employees.json")
            self.msg=QMessageBox()
            self.msg.setText("Update data successful!")
            self.msg.show()
            #re-update UI:
            self.display_employees()
