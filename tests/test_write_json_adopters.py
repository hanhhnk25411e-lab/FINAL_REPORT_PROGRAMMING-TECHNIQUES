import random
import json

from models.adopter import Adopter
from models.adopters import Adopters


first_names = [
    "James","John","Robert","Michael","William","David","Richard","Joseph",
    "Thomas","Charles","Daniel","Matthew","Anthony","Mark","Paul"
]

last_names = [
    "Smith","Johnson","Brown","Taylor","Wilson","Moore",
    "Jackson","Martin","Lee","Perez","Thompson"
]

cities = [
    "New York","London","Paris","Tokyo","Sydney",
    "Berlin","Toronto","Singapore","Seoul","Madrid"
]


# ---------------- READ PETS ----------------

with open("../datasets/pets.json", encoding="utf8") as f:

    data = json.load(f)

pets = data["pets"]


# ---------------- FIND ADOPTED PETS ----------------

adopted_pets = []

for p in pets:

    if p["adoption_status"] == "Adopted":

        adopted_pets.append(p)


# chỉ lấy tối đa 50
adopted_pets = adopted_pets[:50]


# ---------------- CREATE ADOPTERS ----------------

adopters = Adopters()
adopter_list = []

count = 1

for pet in adopted_pets:

    name = random.choice(first_names) + " " + random.choice(last_names)

    adopter_id = f"A{count:03d}"

    phone = "0" + "".join(str(random.randint(0,9)) for _ in range(9))

    address = random.choice(cities)

    rescue_date = pet["rescue_date"]

    year,month,day = map(int,rescue_date.split("-"))

    adopted_year = year
    adopted_month = random.randint(month,12)
    adopted_day = random.randint(1,28)

    adopted_date = f"{adopted_year}-{adopted_month:02d}-{adopted_day:02d}"

    ad = Adopter(
        pet["id"],
        name,
        adopter_id,
        phone,
        address,
        adopted_date
    )

    adopter_list.append(ad)

    count += 1


adopters.add_items(adopter_list)

print("List of Adopters:")
adopters.print_items()

print("Export Adopters to JSON FILE:")
adopters.export_json("../datasets/adopters.json")