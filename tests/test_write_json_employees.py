import random

from models.employee import Employee
from models.employees import Employees

first_names = [
    "James","John","Robert","Michael","William","David","Richard","Joseph","Thomas","Charles",
    "Mary","Patricia","Jennifer","Linda","Elizabeth","Barbara","Susan","Jessica","Sarah","Karen"
]

last_names = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
    "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin"
]

roles = ["Doctor", "Caretaker"]
genders = ["Male", "Female"]
statuses = ["Active", "On leave"]

employees = Employees()
employee_list = []

for i in range(1, 101):

    name = random.choice(first_names) + " " + random.choice(last_names)
    emp_id = f"E{i:03d}"
    gender = random.choice(genders)
    role = random.choice(roles)

    phone = "0" + "".join([str(random.randint(0,9)) for _ in range(9)])

    pets = f"{random.randint(1,5)} pets"

    status = random.choice(statuses)

    emp = Employee(name, emp_id, gender, role, phone, pets, status)
    employee_list.append(emp)

employees.add_items(employee_list)

print("List of Employees:")
employees.print_items()

print("Export Employees to JSON FILE:")
employees.export_json("../datasets/employees.json")