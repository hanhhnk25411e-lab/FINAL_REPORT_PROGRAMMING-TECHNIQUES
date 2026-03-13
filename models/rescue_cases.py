import json

from models.rescue_case import RescueCase
from models.my_collections import MyCollections


class RescueCases(MyCollections):

    def import_json(self, filename):
        with open(filename, encoding='utf8') as json_file:
            data = json.load(json_file)

            for r in data['rescue_cases']:

                it = RescueCase(
                    r['pet_id'],
                    r['date'],
                    r['location'],
                    r['status'],
                    r['description']
                )

                self.add_item(it)

    def export_json(self, filename):

        data = {'rescue_cases': []}

        for it in self.list:

            data['rescue_cases'].append({
                'pet_id': it.pet_id,
                'date': it.date,
                'location': it.location,
                'status': it.status,
                'description': it.description
            })

        with open(filename, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def update_rescue_case(self, rc: RescueCase):

        for i, r in enumerate(self.list):

            if r.pet_id == rc.pet_id and r.date == rc.date:
                self.list[i] = rc
                return True

        return False