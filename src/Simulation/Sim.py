from src.Entities.Patient import Patient, ICU_Bed, Common_Bed
from src.Simulation.DailyStats import Day_Statistics
import numpy as np
import numpy
from scipy.optimize import linear_sum_assignment
# from src.Rag.rag import RAG
import json
import os, pathlib

simulat = []
AllSymptoms = []


class Simulation:
    def __init__(self, n_icu_beds, n_common_beds, n_patients=40, lambda_=20):
        self.n_icu_beds = n_icu_beds
        self.n_common_beds = n_common_beds
        self.n_patients = n_patients
        self.lambda_ = lambda_
        self.patients = []
        self.beds = []
        self.daily_stats = []
        self.costs = np.zeros((n_patients, n_icu_beds + n_common_beds))
        # initialization of the RAG
        # self.rag = RAG()
        self.simulate()

    def generate_patient(self, index):
        age = np.random.choice(["young_adult", "adult", "senior"], p=[0.3, 0.4, 0.3])
        status = np.random.choice(["grave", "critical", "regular"], p=[0.3, 0.2, 0.5])
        return Patient(index, status, age, allsymptoms= AllSymptoms)

    def initialize(self):
        pat = [self.generate_patient(i) for i in range(self.n_patients)]
        self.patients = pat

        for i in range(self.n_icu_beds):
            self.beds.append(ICU_Bed(i))
        for i in range(self.n_icu_beds, self.n_icu_beds + self.n_common_beds):
            self.beds.append(Common_Bed(i))

    def set_costs_matrix(self):
        self.costs = np.zeros((len(self.patients), self.n_icu_beds + self.n_common_beds))
        for i, p in enumerate(self.patients):
            for j, n in enumerate(self.beds):
                self.costs[i, j] = self.calculate_cost(p, n)

    def calculate_cost(self, patient, bed):

        if patient.age_group == 'senior' and patient.status == "critical" and bed.typee == "ICU":
            return 1
        elif patient.age_group == 'senior' and patient.status == "critical" and bed.typee == "common":
            return 4
        elif patient.age_group == 'senior' and patient.status == "grave" and bed.typee == "ICU":
            return 7
        elif patient.age_group == 'senior' and patient.status == "grave" and bed.typee == "common":
            return 10
        elif patient.age_group == 'senior' and patient.status == "regular" and bed.typee == "ICU":
            return 16
        elif patient.age_group == 'senior' and patient.status == "regular" and bed.typee == "common":
            return 13

        elif patient.age_group == 'adult' and patient.status == "critical" and bed.typee == "ICU":
            return 2
        elif patient.age_group == 'adult' and patient.status == "critical" and bed.typee == "common":
            return 5
        elif patient.age_group == 'adult' and patient.status == "grave" and bed.typee == "ICU":
            return 8
        elif patient.age_group == 'adult' and patient.status == "grave" and bed.typee == "common":
            return 11
        elif patient.age_group == 'adult' and patient.status == "regular" and bed.typee == "ICU":
            return 17
        elif patient.age_group == 'adult' and patient.status == "regular" and bed.typee == "common":
            return 14

        elif patient.age_group == 'young_adult' and patient.status == "critical" and bed.typee == "ICU":
            return 3
        elif patient.age_group == 'young_adult' and patient.status == "critical" and bed.typee == "common":
            return 6
        elif patient.age_group == 'young_adult' and patient.status == "grave" and bed.typee == "ICU":
            return 9
        elif patient.age_group == 'young_adult' and patient.status == "grave" and bed.typee == "common":
            return 12
        elif patient.age_group == 'young_adult' and patient.status == "regular" and bed.typee == "ICU":
            return 18
        elif patient.age_group == 'young_adult' and patient.status == "regular" and bed.typee == "common":
            return 15

    def assign_beds(self):
        assignments = []
        # row_ind, col_ind = hg.assign_beds(self.costs)
        row_ind, col_ind = linear_sum_assignment(self.costs)
        for i in range(len(row_ind)):
            self.patients[row_ind[i]].bed_assigned = self.beds[col_ind[i]]
            assignments.append(f'{str(self.patients[row_ind[i]])} -> {str(self.beds[col_ind[i]])}')

        # set to None the ones not assigned
        for i in range(len(self.patients)):
            if i not in row_ind:
                self.patients[i].bed_assigned = None

        return assignments

    def add_new_patients(self):
        # poisson distribution
        new_p = numpy.random.poisson(self.lambda_)
        new_critical_patients = 0
        new_grave_patients = 0
        new_regular_patients = 0

        for i in range(new_p):
            np = self.generate_patient(self.n_patients)
            self.patients.append(np)
            self.n_patients += 1
            if np.status == "critical":
                new_critical_patients += 1
            elif np.status == "grave":
                new_grave_patients += 1
            else:
                new_regular_patients += 1

        return new_critical_patients, new_grave_patients, new_regular_patients

    def simulate(self):
        self.initialize()
        for k in range(30):
            stats = Day_Statistics(k)
            stats.initial_critical_patients = sum([1 for i in self.patients if i.status == "critical"])
            stats.initial_grave_patients = sum([1 for i in self.patients if i.status == "grave"])
            stats.initial_regular_patients = sum([1 for i in self.patients if i.status == "regular"])

            self.set_costs_matrix()
            assignm = self.assign_beds()
            stats.assignments = assignm

            for i in self.patients:
                stat = i.status
                bed = 'none' if i.bed_assigned is None else i.bed_assigned.typee
                var = f'{stat}_{bed}'
                stats.__dict__[var] += 1

            new_p = []
            symptoms = []
            for p in self.patients:
                symptoms.append(p.get_symptoms())

            # medications = self.rag.query_medications_for_patients(symptoms)

            for ind, i in enumerate(self.patients):
                old_status = i.status

                # if i.bed_assigned is not None:
                #     i.doctor_interaction(medications[ind])

                i.interact()
                if i.is_cured:
                    self.n_patients -= 1
                    status = f'{i.status}_patients_cured'
                    stats.__dict__[status] += 1
                elif i.is_dead:
                    self.n_patients -= 1
                    status = f'{i.status}_patients_died'
                    stats.__dict__[status] += 1
                else:
                    new_p.append(i)
                    new_status = i.status
                    if old_status != new_status:
                        stats.__dict__[f'{old_status}_to_{new_status}'] += 1

            self.patients = new_p

            new_critical, new_grave, new_regular = self.add_new_patients()
            stats.new_critical_patients = new_critical
            stats.new_grave_patients = new_grave
            stats.new_regular_patients = new_regular

            stats.final_critical_patients = sum([1 for i in self.patients if i.status == "critical"])
            stats.final_grave_patients = sum([1 for i in self.patients if i.status == "grave"])
            stats.final_regular_patients = sum([1 for i in self.patients if i.status == "regular"])

            self.daily_stats.append(stats)


def start_simulation(icu_beds, common_beds, initial_p, lambda_):
    global simulat, AllSymptoms

    poss = []
    # load all possible symptoms
    with open('..\..\data\Drugs.json') as f:
        doc = json.load(f)

    for i in doc:
        for j in i['side_effects']:
            poss.append(j)

    AllSymptoms = list(set(poss))


    try:
        sim = Simulation(icu_beds, common_beds, initial_p, lambda_)
        simulat = sim.daily_stats
        return True
    except Exception as e:
        print(e)
        return False


def get_day_statistics(day):
    return [i.__dict__ for i in simulat if i.day == day][0]


def get_deaths():
    return [x.grave_patients_died + x.critical_patients_died + x.regular_patients_died for x in simulat]


def get_cured():
    return [x.grave_patients_cured + x.critical_patients_cured + x.regular_patients_cured for x in simulat]


def get_patients_better():
    return [x.critical_to_grave + x.critical_to_regular + x.grave_to_regular for x in simulat]


def get_patients_worse():
    return [x.grave_to_critical + x.regular_to_critical + x.regular_to_grave for x in simulat]


start_simulation(1, 25, 93, 50)
