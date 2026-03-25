import json

from Final_Report.models.adopter import Adopter
from Final_Report.models.my_collections import MyCollections


class Adopters(MyCollections):

    # -------- IMPORT JSON --------
    def import_json(self, filename):

        with open(filename, encoding='utf8') as json_file:

            data = json.load(json_file)

            for a in data['adopters']:

                it = Adopter(
                    a['pet_id'],
                    a['full_name'],
                    a['id'],
                    a['phone'],
                    a['address'],
                    a['adopted_date']
                )

                self.add_item(it)


    # -------- EXPORT JSON --------
    def export_json(self, filename):

        data = {'adopters': []}

        for it in self.list:

            data['adopters'].append({

                'pet_id': it.pet_id,
                'full_name': it.full_name,
                'id': it.id,
                'phone': it.phone,
                'address': it.address,
                'adopted_date': it.adopted_date

            })

        with open(filename, 'w', encoding='utf8') as outfile:

            json.dump(data, outfile, ensure_ascii=False, indent=4)


    # -------- UPDATE ADOPTER --------
    def update_adopter(self, adopter: Adopter):

        for i, a in enumerate(self.list):

            if a.pet_id == adopter.pet_id:

                self.list[i] = adopter

                return True

        return False