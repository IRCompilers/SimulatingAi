class Day_Statistics:
    def __init__(self, day):
        self.day = day
        self.initial_critical_patients = 0
        self.initial_grave_patients = 0
        self.initial_regular_patients = 0

        self.new_critical_patients = 0
        self.new_grave_patients = 0
        self.new_regular_patients = 0

        self.final_critical_patients = 0
        self.final_grave_patients = 0
        self.final_regular_patients = 0

        self.critical_patients_cured = 0
        self.grave_patients_cured = 0
        self.regular_patients_cured = 0

        self.critical_patients_discharged = 0
        self.grave_patients_discharged = 0
        self.regular_patients_discharged = 0

        self.critical_patients_died = 0
        self.grave_patients_died = 0
        self.regular_patients_died = 0

        self.critical_to_grave = 0
        self.critical_to_regular = 0
        self.grave_to_critical = 0
        self.grave_to_regular = 0
        self.regular_to_critical = 0
        self.regular_to_grave = 0

        self.stay_critical = 0
        self.stay_grave = 0
        self.stay_regular = 0

        self.critical_ICU = 0
        self.critical_common = 0
        self.critical_none = 0
        self.grave_ICU = 0
        self.grave_common = 0
        self.grave_none = 0
        self.regular_ICU = 0
        self.regular_common = 0
        self.regular_none = 0

        self.unused_icu = 0
        self.unused_common = 0

        self.assignments = []

    def __str__(self):

        return (f"\n---------------------\nDay {self.day} \n"
                f"- Critical: {self.initial_critical_patients} -> {self.final_critical_patients} \n"
                f"- Grave: {self.initial_grave_patients} -> {self.final_grave_patients} \n"
                f"- Regular: {self.initial_regular_patients} -> {self.final_regular_patients} \n"
                f"- New Patients: \n"
                f"- Critical: {self.new_critical_patients} \n"
                f"- Grave: {self.new_grave_patients} \n"
                f"- Regular: {self.new_regular_patients} \n"
                f"- Critical Patients Cured: {self.critical_patients_cured} \n"
                f"- Grave Patients Cured: {self.grave_patients_cured} \n"
                f"- Regular Patients Cured: {self.regular_patients_cured} \n"
                f"- Critical Patients Died: {self.critical_patients_died} \n"
                f"- Grave Patients Died: {self.grave_patients_died} \n"
                f"- Regular Patients Died: {self.regular_patients_died} \n"
                f"- Evolutions:\n"
                f"- Critical to Grave: {self.critical_to_grave} \n"
                f"- Critical to Regular: {self.critical_to_regular} \n"
                f"- Grave to Critical: {self.grave_to_critical} \n"
                f"- Grave to Regular: {self.grave_to_regular} \n"
                f"- Regular to Critical: {self.regular_to_critical} \n"
                f"- Regular to Grave: {self.regular_to_grave} \n"
                f"- Assignments: \n"
                f"- Critical: ICU: {self.critical_ICU}, Common: {self.critical_common}, None: {self.critical_none} \n"
                f"- Grave: ICU: {self.grave_ICU}, Common: {self.grave_common}, None: {self.grave_none} \n"
                f"- Regular: ICU: {self.regular_ICU}, Common: {self.regular_common}, None: {self.regular_none} \n"
                f"- Assignments: \n"
                # f"{'\n'.join(self.assignments)} \n"
                f"---------------------\n")








