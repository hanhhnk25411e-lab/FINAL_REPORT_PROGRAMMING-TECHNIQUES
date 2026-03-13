import random

from models.medical_record import MedicalRecord
from models.medical_records import MedicalRecords


doctors = [
    "Dr. Smith","Dr. Brown","Dr. Taylor","Dr. Wilson",
    "Dr. Thomas","Dr. White","Dr. Lee","Dr. Clark"
]

diagnosis_list = [
    "Injury",
    "Fever",
    "Skin disease",
    "Broken leg",
    "Vaccination",
    "Dental issue"
]

treatments = [
    "Medicine",
    "Surgery",
    "Bandage",
    "Observation",
    "Injection"
]

vaccination = ["Yes","No"]


records = MedicalRecords()
record_list = []

# 100 pets
pet_ids = [f"P{i:03d}" for i in range(1,101)]

for pet_id in pet_ids:

    for i in range(5):   # 5 history mỗi pet

        year = random.randint(2024,2026)

        if year == 2026:
            month = random.randint(1,2)
        else:
            month = random.randint(1,12)

        day = random.randint(1,28)

        date = f"{year}-{month:02d}-{day:02d}"

        doctor = random.choice(doctors)

        diagnosis = random.choice(diagnosis_list)

        treatment = random.choice(treatments)

        vac = random.choice(vaccination)

        mr = MedicalRecord(
            pet_id,
            date,
            doctor,
            diagnosis,
            treatment,
            vac
        )

        record_list.append(mr)


records.add_items(record_list)

print("List of Medical Records:")
records.print_items()

print("Export Medical Records to JSON FILE:")
records.export_json("../datasets/medical_records.json")