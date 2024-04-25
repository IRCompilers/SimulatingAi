specialties = ['cardiology',
               'dermatology',
               'endocrinology',
               'gastroenterology',
               'hematology',
               'infectious disease',
               'nephrology',
               'neurology',
               'oncology',
               'ophthalmology',
               'orthopedics',
               'otolaryngology',
               'pediatrics',
               'pulmonology',
               'rheumatology',
               'urology',
               'psychiatry',
               'surgery',
               'anesthesiology',
               'radiology',
               'emergency medicine',
               'family medicine']

class Doctor():
    def __init__(self, specialty, max_patients):
        self.specialty = specialty
        self.max_patients = max_patients
        self.patients = []

    def __str__(self):
        return f'{self.specialty} doctor'

    def __repr__(self):
        return self.__str__()

    def assign_patient(self, patient):
        self.patients.append(patient)

    def reset(self):
        self.patients = []