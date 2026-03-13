class Pet:
    def __init__(self, name=None, id=None, species=None, gender=None,
                 rescue_date=None, health_status=None, adoption_status=None):

        self.name = name
        self.id = id
        self.species = species
        self.gender = gender
        self.rescue_date = rescue_date
        self.health_status = health_status
        self.adoption_status = adoption_status

    def __str__(self):
        infor = f"{self.name}\t{self.id}\t{self.species}\t{self.gender}\t{self.rescue_date}\t{self.health_status}\t{self.adoption_status}"
        return infor