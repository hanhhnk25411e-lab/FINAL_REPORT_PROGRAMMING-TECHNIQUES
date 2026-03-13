from models.medical_records import MedicalRecords

mr = MedicalRecords()

mr.import_json("../datasets/medical_records.json")

print("List of Medical Records:")
mr.print_items()