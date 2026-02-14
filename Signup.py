class Signup:
    def __init__(self,
                 FullName,
                 PhoneNumber,
                 Email,
                 LivingType,
                 OwnedPetBefore,
                 PetType,
                 Reason,
                 AppointmentDate,
                 PreferredTime):

        self.FullName = FullName
        self.PhoneNumber = PhoneNumber
        self.Email = Email
        self.LivingType = LivingType
        self.OwnedPetBefore = OwnedPetBefore
        self.PetType = PetType
        self.Reason = Reason
        self.AppointmentDate = AppointmentDate
        self.PreferredTime = PreferredTime

    def __str__(self):
        return self.FullName + " - " + self.PetType
