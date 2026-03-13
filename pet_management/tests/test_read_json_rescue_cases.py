from models.rescue_cases import RescueCases

rc = RescueCases()

rc.import_json("../datasets/rescue_cases.json")

print("List of Rescue Cases:")
rc.print_items()