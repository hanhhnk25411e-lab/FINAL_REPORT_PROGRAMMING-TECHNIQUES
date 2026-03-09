class Customer:
    def __init__(self, full_name, pet, phone, service, status):
        self.full_name = full_name
        self.pet = pet
        self.phone = phone
        self.service = service
        self.status = status

    def to_dict(self):
        """Chuyển đổi đối tượng sang dictionary để lưu JSON"""
        return {
            "full_name": self.full_name,
            "pet": self.pet,
            "phone": self.phone,
            "service": self.service,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        """Tạo lại đối tượng từ dữ liệu JSON"""
        return Customer(
            data.get('full_name', ''),
            data.get('pet', ''),
            data.get('phone', ''),
            data.get('service', ''),
            data.get('status', 'Pending')
        )