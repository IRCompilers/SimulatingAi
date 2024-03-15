class DailyStats:
    def __init__(self, day, patients, doctors):
        self.day = day
        self.patients = patients
        self.doctors = doctors
        self.stats = {}
        self.doctors_diagnosis = {}
        self.stats['correctly_diagnosed'] = 0
        self.stats['incorrectly_diagnosed'] = 0
        self.stats['not_diagnosed'] = 0
        self.stats['cured'] = 0
        self.stats['not_cured'] = 0

    def __repr__(self):
        return f"Day {self.day} stats"

    def calculate_stats(self):
        for doctor in self.doctors:
            self.doctors_diagnosis[doctor] = {}
            self.doctors_diagnosis[doctor]['correctly_diagnosed'] = 0
            self.doctors_diagnosis[doctor]['incorrectly_diagnosed'] = 0
            self.doctors_diagnosis[doctor]['not_diagnosed'] = 0
            self.doctors_diagnosis[doctor]['cured'] = 0
            self.doctors_diagnosis[doctor]['not_cured'] = 0

        for patient in self.patients:
            if patient.correctly_diagnosed():
                self.stats['correctly_diagnosed'] += 1
                self.doctors_diagnosis[patient.get_doctor()]['correctly_diagnosed'] += 1
            elif patient.get_diagnosis():
                self.stats['incorrectly_diagnosed'] += 1
                self.doctors_diagnosis[patient.get_doctor()]['incorrectly_diagnosed'] += 1
            else:
                self.stats['not_diagnosed'] += 1
                self.doctors_diagnosis[patient.get_doctor()]['not_diagnosed'] += 1
            if patient.is_cured:
                self.stats['cured'] += 1
                self.doctors_diagnosis[patient.get_doctor()]['cured'] += 1
            else:
                self.stats['not_cured'] += 1
                self.doctors_diagnosis[patient.get_doctor()]['not_cured'] += 1
        self.stats['doctors_diagnosis'] = self.doctors_diagnosis

    def get_stats(self):
        if not self.stats:
            self.calculate_stats()
        return self.stats







