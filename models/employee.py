class Employee:
    def __init__(self, full_name=None, id=None, gender=None, role=None, phone=None, assigned_pets=None, status=None):
        self.full_name = full_name
        self.id=id
        self.gender=gender
        self.role = role
        self.phone = phone
        self.assigned_pets = assigned_pets
        self.status = status
    def __str__(self):
        infor=f"{self.full_name}\t{self.id}\t{self.gender}\t{self.role}\t{self.phone}\t{self.assigned_pets}\t{self.status}"
        return infor
