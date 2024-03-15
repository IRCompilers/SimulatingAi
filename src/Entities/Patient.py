from abc import ABC
import random

class Patient(ABC):
    def __init__(self, symptoms, actual_diagnosis):
        self.symptoms = symptoms
        self.actual_diagnosis = actual_diagnosis
        self.doctor_diagnosis = None
        self.doctor_treatment = []
        self.doctor_assigned = None
        self.is_cured = False

    def __repr__(self):
        return f"Patient with {self.actual_diagnosis}"

    def assign_doctor(self, doctor):
        self.doctor_assigned = doctor

    def get_diagnosis(self):
        return self.doctor_diagnosis

    def correctly_diagnosed(self):
        return self.actual_diagnosis == self.doctor_diagnosis

    def __treat(self, medicine):
        x = f'{self.actual_diagnosis} treated with {medicine}'
        x += f' thought to be {self.doctor_diagnosis}' if not self.correctly_diagnosed() else ''
        self.doctor_treatment.append(x)

    def __evolve(self, medicine):
        if medicine in self.actual_diagnosis.treatments:
            self.is_cured = True if random.random() < 0.5 else False
        else:
            #get a random symptom from the actual diagnosis that i dont already have and add it to my symptoms
            new_symptoms = [symptom for symptom in self.actual_diagnosis.symptoms if symptom not in self.symptoms]
            (self.symptoms.append(random.choice(new_symptoms)) if new_symptoms else None) if random.random() < 0.5 else None

    def take_medicine(self, medicine):
        self.__treat(medicine)
        self.__evolve(medicine)

    def get_treatment(self):
        return self.doctor_treatment

    def is_cured(self):
        return self.is_cured

    def get_doctor(self):
        return self.doctor_assigned

    def get_symptoms(self):
        return self.symptoms





