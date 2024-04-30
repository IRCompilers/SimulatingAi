import random
from src.Entities.Message import Treatment, AskSymptoms, AnswerSymptoms

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
    def __init__(self, specialty, max_patients, name):
        self.specialty = specialty
        self.max_patients = max_patients
        self.patients = []
        self.name = name

    def __str__(self):
        return f'{self.name}: {", ".join([p.name for p in self.patients]) if len(self.patients) > 0 else "No patients"}'

    def __repr__(self):
        return self.__str__()

    def assign_patient(self, patient):
        self.patients.append(patient)

    def reset(self):
        self.patients = []

    def administer_medicine(self, rag, all_medicines, map_sp_sym):
        symptoms = []

        for p in self.patients:
            answer = self.send_message(p, AskSymptoms(doctor=self))
            symps = answer.symptoms

            symptoms.append(symps)

        print(symptoms)
        medications = rag.query_medications_for_patients(symptoms)

        for k, i in enumerate(self.patients):
            treatment = medications[k]
            prob = [map_sp_sym[self.specialty][sym] for sym in i.symptoms]

            treatment = treatment if isinstance(treatment, list) else [treatment]
            treatment = [random.choice(all_medicines)] if sum(prob) < 0.5 else \
                [x for x in all_medicines if x.name in treatment]

            msg = Treatment(treatment, self.specialty, prob)
            self.send_message(i, msg)

    def send_message(self, patient, message):
        return patient.receive_message(message)