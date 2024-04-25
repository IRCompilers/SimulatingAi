import random

import numpy as np
from scipy.optimize import linear_sum_assignment
from abc import ABC, abstractmethod
from src.Entities.Medicine import Medicine
from src.Entities.Doctor import specialties


class Patient(ABC):
    def __init__(self, index, status, age_group, bed_assigned=None, allsymptoms = [], Symptom_Specialty = {}):
        self.index = index
        self.status = status
        self.bed_assigned = bed_assigned
        self.is_cured = False
        self.is_dead = False
        self.age_group = age_group
        self.symptoms: list = self.set_symptoms(allsymptoms)
        self.doc_assigned = None
        self.specialties_needed = {i : 0 for i in specialties}
        self.set_specialties_needed(Symptom_Specialty)

    def set_specialties_needed(self, Symptom_Specialty = {}):
        for i in self.symptoms:
            sp = Symptom_Specialty[i]
            self.specialties_needed[sp] += 1


    def get_symptoms(self):
        return ' and '.join(self.symptoms)

    def set_symptoms(self, AllSymptoms):
        amount = np.random.poisson(2) + 1
        return random.choices(population=AllSymptoms, k = amount)

    def doctor_interaction(self, treatment: list[str] = [], allmedicines : list[Medicine] = []):
        treatment = treatment if isinstance(treatment, list) else [treatment]

        for med in treatment:
            curr = [x for x in allmedicines if x.name == med]
            if len(curr) == 0:
                continue
            current = curr[0]

            if len(self.symptoms) == 0:
                break

            #cures the symptom with a 75% prob
            #gets a side_effect with a 10%

            for sym in self.symptoms:
                if current.treats(sym):
                    x = random.random()
                    if x > 0.25:
                        self.symptoms.remove(sym)
                    y = random.random()
                    if y < 0.1:
                        self.symptoms.append(random.choice(current.side_effects))



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
        return f'specialties needed: {self.specialties_needed}, symptoms: {self.get_symptoms()}'

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





