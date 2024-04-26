import random

import numpy as np
from scipy.optimize import linear_sum_assignment
from abc import ABC, abstractmethod
from src.Entities.Medicine import Medicine
from src.Entities.Doctor import specialties


class Patient(ABC):
    def __init__(self, index, status, age_group, bed_assigned=None, allsymptoms = [], Symptom_Specialty = {}, name = ""):
        self.index = index
        self.status = status
        self.bed_assigned = bed_assigned
        self.is_cured = False
        self.is_dead = False
        self.age_group = age_group
        self.symptoms: list = self.set_symptoms(allsymptoms)
        self.doc_assigned = None
        self.specialties_needed = {i : 0 for i in specialties}
        self.Symptom_Specialty = Symptom_Specialty
        self.set_specialties_needed()
        self.name = name

    def set_specialties_needed(self):
        dic = {i : 0 for i in specialties}
        for i in self.symptoms:
            sp = self.Symptom_Specialty[i]
            dic[sp] += 1
        self.specialties_needed = dic


    def get_symptoms(self):
        return ' and '.join(self.symptoms)

    def set_symptoms(self, AllSymptoms):
        amount = np.random.poisson(2) + 1
        return random.choices(population=AllSymptoms, k = amount)

    def doctor_interaction(self, treatment: list[str] = [], allmedicines : list[Medicine] = [], is_specialist = False):
        treatment = treatment if isinstance(treatment, list) else [treatment]

        for med in treatment:
            curr = [x for x in allmedicines if x.name == med]
            if len(curr) == 0:
                continue
            current = curr[0]

            if len(self.symptoms) == 0:
                break

            for sym in self.symptoms:
                factor_cure = 0.9 if is_specialist else 0.6 if self.doc_assigned.specialty == self.Symptom_Specialty[
                    sym] else 0.3
                factor_side_effect = 0.1 if is_specialist else 0.3 if self.doc_assigned.specialty == self.Symptom_Specialty[
                    sym] else 0.6
                if current.treats(sym):
                    x = random.random()
                    if x < factor_cure:
                        self.symptoms.remove(sym)
                y = random.random()
                if y < factor_side_effect:
                    self.symptoms.append(random.choice(current.side_effects))

        self.set_specialties_needed()


    def cure(self):
        self.is_cured = True

    def die(self):
        self.is_dead = True

    def better(self):
        if self.status == 'critical':
            self.status = 'grave'
            return
        elif self.status == 'grave':
            self.status = 'regular'
            return
        else:
            self.is_cured = True

    def twice_better(self):
        if self.status == 'critical':
            self.status = 'regular'
            return
        else:
            self.is_cured = True

    def worsen(self):
        if self.status == 'grave':
            self.status = 'critical'
            return
        elif self.status == 'regular':
            self.status = 'grave'
            return
        else:
            self.is_dead = True

    def twice_worsen(self):
        if self.status == 'regular':
            self.status = 'critical'
        else:
            self.is_dead = True

    def do_nothing(self):
        pass

    def interact(self):
        if len(self.symptoms) == 0:
            self.cure()

        if self.is_dead or self.is_cured:
            return

        if self.bed_assigned is None and self.status == 'critical':
            action = np.random.choice(["cure", "die", "better", "do_nothing"], p=[0.05, 0.8, 0.05, 0.1])
        elif self.bed_assigned is None and self.status == 'grave':
            action = np.random.choice(["cure", "die", "better", "worsen", "do_nothing"], p=[0.05, 0.4, 0.1, 0.15, 0.3])
        elif self.bed_assigned is None and self.status == 'regular':
            action = np.random.choice(["cure", "die", "worsen", "twice_worsen", "do_nothing"], p=[0.3, 0.1, 0.3, 0.1, 0.2])

        elif self.status == 'critical' and self.bed_assigned.typee == 'ICU':
            action = np.random.choice(["cure", "die", "better", "twice_better", "do_nothing"], p=[0.1, 0.2, 0.4, 0.15, 0.15])
        elif self.status == 'critical' and self.bed_assigned.typee == 'common':
            action = np.random.choice(["cure", "die", "better", "twice_better", "do_nothing"], p=[0.05, 0.5, 0.2, 0.1, 0.15])

        elif self.status == 'grave' and self.bed_assigned.typee == 'common':
            action = np.random.choice(["cure", "die", "better", "worsen", "do_nothing"], p=[0.1, 0.2, 0.3, 0.2, 0.2])
        elif self.status == 'grave' and self.bed_assigned.typee == 'ICU':
            action = np.random.choice(["cure", "die", "better", "worsen", "do_nothing"], p=[0.2, 0.1, 0.4, 0.1, 0.2])

        elif self.status == 'regular' and self.bed_assigned.typee == 'ICU':
            action = np.random.choice(["cure", "die", "worsen", "twice_worsen", "do_nothing"], p=[0.7, 0.05, 0.1, 0.05, 0.1])
        elif self.status == 'regular' and self.bed_assigned.typee == 'common':
            action = np.random.choice(["cure", "die", "worsen", "twice_worsen", "do_nothing"], p=[0.4, 0.1, 0.2, 0.1, 0.2])

        getattr(self, action)()

    def __str__(self):
        return f'{self.name} with status {self.status} and age group {self.age_group}'

    def __repr__(self):
        return self.__str__()

# _________________________________________________________________
class Beds:
    def __init__(self, index, typee):
        self.index = index
        self.typee = typee

    def __str__(self):
        return f"Bed type {self.typee}"

class ICU_Bed(Beds):
    def __init__(self, index):
        super().__init__(index, "ICU")

class Common_Bed(Beds):
    def __init__(self, index):
        super().__init__(index, "common")





