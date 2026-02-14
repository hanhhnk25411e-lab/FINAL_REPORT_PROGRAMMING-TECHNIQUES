class Employee:
    def __init__(self, full_name=None, role=None, phone=None, assigned_pets=None, shift=None, status=None):
        self.full_name = full_name
        self.role = role
        self.phone = phone
        self.assigned_pets = assigned_pets
        self.shift= shift
        self.status = status
    def __str__(self):
        infor=f"{self.full_name}\t{self.role}\t{self.phone}\t{self.assigned_pets}\t{self.shift}"
        return infor
