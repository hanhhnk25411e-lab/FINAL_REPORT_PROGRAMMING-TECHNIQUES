import random

from models.rescue_case import RescueCase
from models.rescue_cases import RescueCases


locations = [
    "District 1","District 2","District 3","District 4",
    "Park","Market","Street","Highway","Bridge","School"
]

statuses = ["Rescued","Under treatment","Recovered"]

cases = RescueCases()
case_list = []

# ===== 100 PET IDs =====
pet_ids = [f"P{i:03d}" for i in range(1,101)]


for pet_id in pet_ids:

    year = random.randint(2024, 2026)

    if year == 2026:
        month = random.randint(1, 2)
    else:
        month = random.randint(1, 12)

    day = random.randint(1, 28)

    date = f"{year}-{month:02d}-{day:02d}"

    location = random.choice(locations)
    status = random.choice(statuses)
    description = "Rescue operation"

    rc = RescueCase(
        pet_id,
        date,
        location,
        status,
        description
    )

    case_list.append(rc)


cases.add_items(case_list)


print("List of Rescue Cases:")
cases.print_items()


print("Export Rescue Cases to JSON FILE:")
cases.export_json("../datasets/rescue_cases.json")