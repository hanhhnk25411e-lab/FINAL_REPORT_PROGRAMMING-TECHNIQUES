from employee_management.models.employee import Employee
from employee_management.models.employees import Employees

le=Employees()
e1=Employee("Nguyễn Văn A","Doctor","0486394866","3 pets","Morning","Active")
e2=Employee("Lê Thị B","Caretaker","0694769442","2 pets","Afternoon","Active")
e3=Employee("Nguyễn Thị C","Caretaker","0385743957","4 pets","Evening","On leave")
e4=Employee("Phạm Văn D","Doctor","0396749657","3 pets","Night","Active")
e5=Employee("Trương Văn E","Doctor","0937539672","3 pets","Evening","Active")
e6=Employee("Võ Thị F","Caretaker","0485837592","4 pets","Morning","Acitve")
e7=Employee("Phạm Văn G","Doctor","0320574482","2 pets","Afternoon","Active")
e8=Employee("Dương Văn H","Doctor","0938672573","3 pets","Morning","On leave")
e9=Employee("Trần Thị I","Caretaker","0395673957","4 pets","Night","Active")
e10=Employee("Hồ Văn J","Caretaker","0395836502","2 pets","Evening","Active")
le.add_items([e1,e2,e3,e4,e5,e6,e7,e8,e9,e10])
print("List of Employee:")
le.print_items()
print("Export Employees to JSON FILE:")
le.export_json("../datasets/employees.json")