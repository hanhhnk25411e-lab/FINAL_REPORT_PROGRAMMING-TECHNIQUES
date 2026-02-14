import json

from employee_management.models.employee import Employee
from employee_management.models.my_collections import MyCollections


class Employees(MyCollections):
    def import_json(self,filename):
        with open(filename, encoding='utf8') as json_file:
            data = json.load(json_file)
            for p in data['employees']:
                it=Employee(p['full_name'],p['id'],p['gender'],p['role'],p['phone'],p['assigned_pets'],p['status'])
                self.add_item(it)


    def export_json(self,filename):
        data = {'employees': []}
        for it in self.list:
            data['employees'].append({
                'full_name': it.full_name,
                'id': it.id,
                'gender': it.gender,
                'role': it.role,
                'phone': it.phone,
                'assigned_pets': it.assigned_pets,
                'status': it.status,
            })
        with open(filename, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def update_employee(self, emp: Employee):
        for i, e in enumerate(self.list):
            if e.full_name == emp.full_name:
                self.list[i] = emp
                return True
        return False
