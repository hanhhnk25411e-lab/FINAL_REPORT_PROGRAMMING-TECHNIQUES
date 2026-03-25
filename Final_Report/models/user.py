class User:
    def __init__(self, email=None, password=None, phone=None, role=None):
        self.email = email
        self.password=password
        self.phone = phone
        self.role = role
    def __str__(self):
        infor=f"{self.email}\t{self.password}\t{self.phone}\t{self.role}"
        return infor
