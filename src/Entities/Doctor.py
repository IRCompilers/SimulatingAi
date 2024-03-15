from abc import ABC

class Doctor(ABC):
    def __init__(self, name, strategy, years_of_experience):
        self.name = name
        self.strategy = strategy
        self.years_of_experience = years_of_experience

    def __repr__(self):
        return f"Doctor {self.name}"

    def diagnose(self, patient):
        return self.strategy.diagnose(patient)

    def treat(self, patient):
        return self.strategy.treat(patient)



