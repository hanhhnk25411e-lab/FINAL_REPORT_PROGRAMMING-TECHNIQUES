class MedicalRecord:

    def __init__(self, pet_id=None, date=None, person_in_charge=None,
                 diagnosis=None, treatment=None, vaccination=None):

        self.pet_id = pet_id
        self.date = date
        self.person_in_charge = person_in_charge
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.vaccination = vaccination


    def __str__(self):

        infor = f"{self.pet_id}\t{self.date}\t{self.person_in_charge}\t{self.diagnosis}\t{self.treatment}\t{self.vaccination}"

        return infor