from models.pets import Pets

ps = Pets()

ps.import_json("../datasets/pets.json")

print("List of Pets:")
ps.print_items()