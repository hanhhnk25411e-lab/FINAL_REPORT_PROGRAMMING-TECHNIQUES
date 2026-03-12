from models.adopters import Adopters

ad = Adopters()

ad.import_json("../datasets/adopters.json")

print("List of Adopters:")
ad.print_items()