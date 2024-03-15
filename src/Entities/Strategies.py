from abc import ABC, abstractmethod
import random

AllSicknesses = []
AllSymptoms = []

class Strategy(ABC):
    @abstractmethod
    def diagnose(self, patient):
        pass

    @abstractmethod
    def treat(self, patient):
        pass

class RandomStrategy(Strategy):
    def diagnose(self, patient):
        symptoms = patient.get_symptoms()
        possible_sicknesses = [sickness for sickness in AllSicknesses if all(symptom in symptoms for symptom in sickness.get_symptoms())]
        return random.choice(possible_sicknesses) if possible_sicknesses else None

    def treat(self, patient):
        if patient.get_diagnosis():
            return random.choice(patient.get_diagnosis().get_treatments())
        else:
            symp = patient.get_symptoms()
            return random.choice([symptom for symptom in symp if symptom.get_treatments()]) if symp else None

class MaxStrategy(Strategy):
    def diagnose(self, patient):
        symptoms = patient.get_symptoms()
        possible_sicknesses = [sickness for sickness in AllSicknesses if any(symptom in symptoms for symptom in sickness.get_symptoms())]
        scores = {sickness: sum(symptom in sickness.get_symptoms() for symptom in symptoms) for sickness in possible_sicknesses}
        return max(scores, key=scores.get) if scores else None

    def treat(self, patient):
        if patient.get_diagnosis():
            return max(patient.get_diagnosis().get_treatments(), key=lambda x: x.get_treatments())
        else:
            symp = patient.get_symptoms()
            return max([symptom for symptom in symp if symptom.get_treatments()], key=lambda x: x.get_treatments()) if symp else None

class MinStrategy(Strategy):
    def diagnose(self, patient):
        symptoms = patient.get_symptoms()
        possible_sicknesses = [sickness for sickness in AllSicknesses if any(symptom in symptoms for symptom in sickness.get_symptoms())]
        scores = {sickness: sum(symptom in sickness.get_symptoms() for symptom in symptoms) for sickness in possible_sicknesses}
        return min(scores, key=scores.get) if scores else None

    def treat(self, patient):
        if patient.get_diagnosis():
            return min(patient.get_diagnosis().get_treatments(), key=lambda x: x.get_treatments())
        else:
            symp = patient.get_symptoms()
            return min([symptom for symptom in symp if symptom.get_treatments()], key=lambda x: x.get_treatments()) if symp else None


