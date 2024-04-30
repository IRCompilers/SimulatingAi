from src.Entities.Medicine import Medicine



class Treatment:
    def __init__(self, treatment: [Medicine], specialty: str, certainty: [int]):
        self.treatment = treatment
        self.specialty = specialty
        self.certainty = certainty


class AskSymptoms:
    def __init__(self, doctor):
        self.doctor = doctor

class AnswerSymptoms:
    def __init__(self, symptoms):
        self.symptoms = symptoms
