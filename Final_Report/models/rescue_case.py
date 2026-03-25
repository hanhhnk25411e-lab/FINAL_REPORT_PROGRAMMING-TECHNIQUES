class RescueCase:
    def __init__(self, pet_id=None, date=None, location=None, status=None, description=None):
        self.pet_id = pet_id
        self.date = date
        self.location = location
        self.status = status
        self.description = description

    def __str__(self):
        infor = f"{self.pet_id}\t{self.date}\t{self.location}\t{self.status}\t{self.description}"
        return infor