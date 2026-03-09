from models.employees import Employees

le=Employees()
le.import_json("../datasets/employees.json")
print("List of Employees:")
le.print_items()
