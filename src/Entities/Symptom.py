from abc import ABC

class Symptom(ABC):
    def __init__(self, name, treatments):
        self.name = name
        self.treatments = treatments

    def __repr__(self):
        return f"{self.name}"

    def get_treatments(self):
        return self.treatments



# treatments = [Symptoms]