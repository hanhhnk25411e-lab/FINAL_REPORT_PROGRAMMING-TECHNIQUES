class Adopter:

    def __init__(self, pet_id=None, full_name=None, id=None,
                 phone=None, address=None, adopted_date=None):

        self.pet_id = pet_id
        self.full_name = full_name
        self.id = id
        self.phone = phone
        self.address = address
        self.adopted_date = adopted_date


    def __str__(self):

        infor = f"{self.pet_id}\t{self.full_name}\t{self.id}\t{self.phone}\t{self.address}\t{self.adopted_date}"

        return infor