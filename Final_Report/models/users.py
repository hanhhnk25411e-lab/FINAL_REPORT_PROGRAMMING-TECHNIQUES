import json
from Final_Report.models.my_collections import MyCollections
from Final_Report.models.user import User


class Users(MyCollections):
    def import_json(self, filename):
        with open(filename, encoding='utf8') as json_file:
            data = json.load(json_file)
            for p in data['users']:
                it = User(p['email'], p['password'], p['phone'], p['role'])
                self.add_item(it)

    def export_json(self, filename):
        data = {'users': []}
        for it in self.list:
            data['users'].append({
                'email': it.email,
                'password': it.password,
                'phone': it.phone,
                'role': it.role
            })
        with open(filename, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
