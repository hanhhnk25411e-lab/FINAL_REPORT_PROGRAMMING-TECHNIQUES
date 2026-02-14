from employee_management.models.employee import Employee
from employee_management.models.employees import Employees

le=Employees()
e1=Employee("Nguyễn Văn A","NV001","Male","Doctor","0486394866","3 pets","Active")
e2=Employee("Lê Thị B","NV002","Female","Caretaker","0694769442","2 pets","Active")
e3=Employee("Nguyễn Thị C","NV003","Female","Caretaker","0385743957","4 pets","On leave")
e4=Employee("Phạm Văn D","NV004","Male","Doctor","0396749657","3 pets","Active")
e5=Employee("Trương Thị E","NV005","Female","Doctor","0937539672","3 pets","Active")
e6=Employee("Võ Văn F","NV006","Male","Caretaker","0485837592","4 pets","Acitve")
e7=Employee("Phạm Thị G","NV007","Female","Doctor","0320574482","2 pets","Active")
e8=Employee("Dương Văn H","NV008","Male","Doctor","0938672573","3 pets","On leave")
e9=Employee("Trần Thị I","NV009","Female","Caretaker","0395673957","4 pets","Active")
e10=Employee("Hồ Văn J","NV010","Male","Caretaker","0395836502","2 pets","Active")
le.add_items([e1,e2,e3,e4,e5,e6,e7,e8,e9,e10])
print("List of Employee:")
le.print_items()
print("Export Employees to JSON FILE:")
le.export_json("../datasets/employees.json")