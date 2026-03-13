import random

from models.pet import Pet
from models.pets import Pets

pet_names = [
    "Bella","Max","Charlie","Lucy","Milo","Luna","Rocky","Coco","Buddy","Daisy",
    "Bailey","Loki","Leo","Lily","Zoe","Ruby","Simba","Oscar","Toby","Nala"
]

species_list = ["Dog", "Cat"]
genders = ["Male", "Female"]
health_status = ["Healthy", "Injured", "Recovering"]
adoption_status = ["Adopted", "Not adopted"]

pets = Pets()
pet_list = []

for i in range(1,101):

    name = random.choice(pet_names)
    pet_id = f"P{i:03d}"
    species = random.choice(species_list)
    gender = random.choice(genders)

    year = random.randint(2024, 2026)

    if year == 2026:
        month = random.randint(1, 2)
    else:
        month = random.randint(1, 12)

    day = random.randint(1, 28)

    date = f"{year}-{month:02d}-{day:02d}"

    health = random.choice(health_status)
    adoption = random.choice(adoption_status)

    p = Pet(name, pet_id, species, gender, date, health, adoption)
    pet_list.append(p)

pets.add_items(pet_list)

print("List of Pets:")
pets.print_items()

print("Export Pets to JSON FILE:")
pets.export_json("../datasets/pets.json")