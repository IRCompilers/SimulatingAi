import numpy as np
from scipy.optimize import linear_sum_assignment
import random
from abc import ABC, abstractmethod

class Patient(ABC):
    def __init__(self, index, status, age_group, bed_assigned=None, sickness = None, symptoms = []):
        self.index = index
        self.status = status
        self.bed_assigned = bed_assigned
        self.is_cured = False
        self.is_dead = False
        self.age_group = age_group
        self.symptoms = symptoms

    def get_symptoms(self):
        return ' and '.join(self.symptoms)

    def doctor_interaction(self, medicine: list[str] = []):
        #todo implement this

        # get medicines that work for my symptoms
        # check that the medicines given correspond
        # better or worse
        pass

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

    def interact(self):
        # todo add worsen and twice_worsen
        if self.is_dead or self.is_cured:
            return
        if self.bed_assigned is None:
            if self.status == 'critical':
                action = np.random.choice(["cure", "die", "better"], p=[0.05, 0.8, 0.15])
            elif self.status == 'grave':
                action = np.random.choice(["cure", "die", "better", "twice_better"], p=[0.1, 0.6, 0.1, 0.2])
            else:
                action = np.random.choice(["cure", "die", "better", "twice_better"], p=[0.3, 0.2, 0.3, 0.2])

        elif self.status == 'critical' and self.bed_assigned.typee == 'ICU':
            action = np.random.choice(["cure", "die", "better", "twice_better"], p=[0.3, 0.2, 0.3, 0.2])
        elif self.status == 'critical' and self.bed_assigned.typee == 'common':
            action = np.random.choice(["cure", "die", "better", "twice_better"], p=[0.1, 0.5, 0.3, 0.1])
        elif self.status == 'grave' and self.bed_assigned.typee == 'common':
            action = np.random.choice(["cure", "die", "better", "twice_better"], p=[0.2, 0.4, 0.3, 0.1])
        elif self.status == 'grave' and self.bed_assigned.typee == 'ICU':
            action = np.random.choice(["cure", "die", "better"], p=[0.2, 0.2, 0.6])
        elif self.status == 'regular' and self.bed_assigned.typee == 'ICU':
            action = np.random.choice(["cure", "die", "worsen", "twice_worsen"], p=[0.7, 0.1, 0.1,0.1])
        elif self.status == 'regular' and self.bed_assigned.typee == 'common':
            action = np.random.choice(["cure", "die", "worsen", "twice_worsen"], p=[0.4, 0.1, 0.3, 0.2])

        getattr(self, action)()

    def __str__(self):
        return f'{self.status} {self.age_group}'

    def __repr__(self):
        return self.__str__()

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





