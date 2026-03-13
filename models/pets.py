import json

from models.pet import Pet
from models.my_collections import MyCollections


class Pets(MyCollections):

    def import_json(self, filename):
        with open(filename, encoding='utf8') as json_file:
            data = json.load(json_file)
            for p in data['pets']:
                it = Pet(
                    p['name'],
                    p['id'],
                    p['species'],
                    p['gender'],
                    p['rescue_date'],
                    p['health_status'],
                    p['adoption_status']
                )
                self.add_item(it)

    def export_json(self, filename):
        data = {'pets': []}

        for it in self.list:
            data['pets'].append({
                'name': it.name,
                'id': it.id,
                'species': it.species,
                'gender': it.gender,
                'rescue_date': it.rescue_date,
                'health_status': it.health_status,
                'adoption_status': it.adoption_status
            })

        with open(filename, 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def update_pet(self, pet: Pet):
        for i, p in enumerate(self.list):
            if p.id == pet.id:
                self.list[i] = pet
                return True
        return False