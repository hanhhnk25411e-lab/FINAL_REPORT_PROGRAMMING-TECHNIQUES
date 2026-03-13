import json

from models.medical_record import MedicalRecord
from models.my_collections import MyCollections


class MedicalRecords(MyCollections):

    # -------- IMPORT JSON --------
    def import_json(self, filename):

        with open(filename, encoding='utf8') as json_file:

            data = json.load(json_file)

            for m in data['medical_records']:

                it = MedicalRecord(
                    m['pet_id'],
                    m['date'],
                    m['person_in_charge'],
                    m['diagnosis'],
                    m['treatment'],
                    m['vaccination']
                )

                self.add_item(it)

    # -------- EXPORT JSON --------
    def export_json(self, filename):

        data = {'medical_records': []}

        for it in self.list:

            data['medical_records'].append({

                'pet_id': it.pet_id,
                'date': it.date,
                'person_in_charge': it.person_in_charge,
                'diagnosis': it.diagnosis,
                'treatment': it.treatment,
                'vaccination': it.vaccination

            })

        with open(filename, 'w', encoding='utf8') as outfile:

            json.dump(data, outfile, ensure_ascii=False, indent=4)

    # -------- UPDATE RECORD --------
    def update_medical_record(self, mr: MedicalRecord):

        for i, m in enumerate(self.list):

            if m.pet_id == mr.pet_id and m.date == mr.date:

                self.list[i] = mr

                return True

        return False