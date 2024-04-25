import random

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

    def administer_medicine(self, rag, all_medicines, map_sp_sym):
        symptoms = []
        for p in self.patients:
            symptoms.append(p.get_symptoms())

        medications = rag.query_medications_for_patients(symptoms)

        for k, i in enumerate(self.patients):
            treatment = medications[k]
            prob = sum([map_sp_sym[self.specialty][sym] for sym in i.symptoms])
            if prob > 0.6:
                i.doctor_interaction(treatment, all_medicines)
            elif prob > 0.1:
                ran_med = random.choice(all_medicines)
                i.doctor_interaction([ran_med.name], all_medicines)
            else:
                i.die()


