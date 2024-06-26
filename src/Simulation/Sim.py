import random

from dotenv import load_dotenv

from src.Entities.Patient import Patient, ICU_Bed, Common_Bed
from src.Entities.Medicine import Medicine
from src.Simulation.DailyStats import Day_Statistics
import numpy as np
import numpy
from scipy.optimize import linear_sum_assignment
from src.Rag.rag import RAG
from src.Rag.rag_config import RagConfig
import json
import os, pathlib
import pandas as pd
import time
import matplotlib.pyplot as plt
from src.helpers.a_star import get_assignment, tabulate_values

import google.generativeai as genai

from src.Entities.Doctor import Doctor, specialties
from src.helpers.doc_assign import assign_doc_patient

names = ['John', 'Mary', 'Alice', 'Bob', 'Eve', 'Charlie', 'David', 'Elena', 'Fiona', 'George', 'Helen', 'Ivan', 'Julia',
         'Kevin', 'Linda', 'Michael', 'Nancy', 'Oscar', 'Paul', 'Quinn', 'Rachel', 'Steve', 'Tina', 'Ursula', 'Victor',
         'Wendy', 'Xavier', 'Yvonne', 'Zack', 'Abigail', 'Benjamin', 'Catherine', 'Daniel', 'Emily', 'Frank', 'Grace',
         'Henry', 'Isabel', 'Jack', 'Katherine', 'Liam', 'Megan', 'Nathan', 'Olivia', 'Peter', 'Quincy', 'Rebecca',
         'Samuel', 'Tiffany', 'Ulysses', 'Violet', 'William', 'Xander', 'Yasmine', 'Zoe', 'Adam', 'Bella', 'Charles',
         'Diana', 'Ethan', 'Fiona', 'Gerald', 'Hannah', 'Ian', 'Jasmine', 'Kyle', 'Laura', 'Mason', 'Nina', 'Owen',
         'Patricia', 'Quentin', 'Rose', 'Stephen', 'Tara', 'Usher', 'Victoria', 'Walter', 'Xena', 'Yara', 'Zara', 'Ava',
         'Bart', 'Cara', 'Dylan', 'Ella', 'Felix', 'Gina', 'Harry', 'Iris', 'Jake', 'Kara', 'Liam', 'Mia', 'Nathanial',
         'Olivia', 'Peter', 'Quinn', 'Ryan', 'Sophia', 'Tom', 'Ursula', 'Victor', 'Wendy', 'Xander', 'Yvonne', 'Zack']

surnames = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson',
            'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark',
            'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'Hernandez', 'King', 'Wright', 'Lopez',
            'Hill', 'Scott', 'Green', 'Adams', 'Baker', 'Gonzalez', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts',
            'Turner', 'Phillips', 'Campbell', 'Parker', 'Evans', 'Edwards', 'Collins', 'Stewart', 'Sanchez', 'Morris',
            'Rogers', 'Reed', 'Cook', 'Morgan', 'Bell', 'Murphy', 'Bailey', 'Rivera', 'Cooper', 'Richardson', 'Cox',
            'Howard', 'Ward', 'Torres', 'Peterson', 'Gray', 'Ramirez', 'James', 'Watson', 'Brooks', 'Kelly', 'Sanders',
            'Price', 'Bennett', 'Wood', 'Barnes', 'Ross', 'Henderson', 'Coleman', 'Jenkins', 'Perry', 'Powell', 'Long',
            'Patterson', 'Hughes', 'Flores', 'Washington', 'Butler', 'Simmons', 'Foster', 'Gonzales', 'Bryant', 'Alexander',
            'Russell', 'Griffin', 'Diaz', 'Hayes']

simulat = []
AllSymptoms = []
AllMedicines = []

# engine = AssignmentCost()
def calculate_cost_h(patient):
    return len(patient.symptoms)


def calculate_cost_g(patient, bed):
    # engine.reset()
    # engine.declare(Fact(bed = bed, state = patient.status, age = patient.age_group))
    # return engine.run()

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


def create_rag():
    # load_dotenv()
    # os.environ["TOKENIZERS_PARALLELISM"] = "true"
    # api_key = os.getenv('GOOGLE_API_KEY')

    api_key = 'jajajajajaja'

    data = pd.read_csv('..\..\data\Drugs.csv')
    rag_config = RagConfig(use_persistence=False, use_llm=False, gemini_api_key=api_key)
    return RAG(data=data, config=rag_config)


class Simulation:
    def __init__(self, n_icu_beds, n_common_beds, n_patients=40, lambda_=20, h=calculate_cost_h, rag = None):
        self.n_icu_beds = n_icu_beds
        self.n_common_beds = n_common_beds
        self.n_patients = n_patients
        self.lambda_ = lambda_
        self.patients = []
        self.beds = []
        self.daily_stats = []
        self.costs = np.zeros((n_patients, n_icu_beds + n_common_beds))
        self.costs = [[0 for i in range(self.n_patients)] for j in range(self.n_icu_beds + self.n_common_beds)]
        self.costs2 = [[0 for i in range(self.n_patients)] for j in range(self.n_icu_beds + self.n_common_beds)]

        self.h = h

        self.rag = rag

        self.doctors = self.generate_docs()

        self.map_symp_specialty = self.map_symp_specialty()

        self.simulate()

    def generate_docs(self):
        doctors = []

        beds = self.n_icu_beds + self.n_common_beds
        amount = 0

        while True:
            if amount >= beds:
                break
            val = random.randint(1, 4)
            amount += val

            doc = Doctor(specialty=np.random.choice(specialties),
                         max_patients=val,
                         name=np.random.choice(names) + " " + np.random.choice(surnames))
            doctors.append(doc)

        return doctors

    def generate_patient(self, index):
        age = np.random.choice(["young_adult", "adult", "senior"], p=[0.3, 0.4, 0.3])
        status = np.random.choice(["grave", "critical", "regular"], p=[0.3, 0.2, 0.5])
        name = np.random.choice(names) + " " + np.random.choice(surnames)
        return Patient(index, status, age, allsymptoms=AllSymptoms, Symptom_Specialty=Symptom_Specialty, name=name)

    def map_symp_specialty(self):
        map = {}
        for i in specialties:
            perc = {}
            for j in AllSymptoms:
                sp = Symptom_Specialty[j]
                perc[j] = np.random.uniform(0, 0.8) if sp != i else np.random.uniform(0.8, 1)
            map[i] = perc

        json.dump(map, open('..\..\data\Symptom_Specialty.json', 'w'))
        return map

    def initialize(self):
        pat = [self.generate_patient(i) for i in range(self.n_patients)]
        self.patients = pat

        for i in range(self.n_icu_beds):
            self.beds.append(ICU_Bed(i))
        for i in range(self.n_icu_beds, self.n_icu_beds + self.n_common_beds):
            self.beds.append(Common_Bed(i))

    def set_costs_matrix(self):
        self.costs = [[0 for i in range(len(self.patients))] for j in range(self.n_icu_beds + self.n_common_beds)]

        for i, p in enumerate(self.patients):
            for j, n in enumerate(self.beds):
                self.costs[j][i] = calculate_cost_g(p, n)


    def assign_beds(self):
        assignments = []
        unused_icu = 0
        unused_common = 0
        col_ind, row_ind = linear_sum_assignment(self.costs)
        for i in range(len(row_ind)):
            self.patients[row_ind[i]].bed_assigned = self.beds[col_ind[i]]
            assignments.append(f'{str(self.patients[row_ind[i]])} -> {str(self.beds[col_ind[i]])}')

        # set to None the ones not assigned
        for i in range(len(self.patients)):
            if i not in row_ind:
                self.patients[i].bed_assigned = None

        used = []
        for x in col_ind:
            used.append(x)
        unused = [x for x in range(len(self.beds)) if x not in used]

        unused_icu = len([x for x in unused if x < self.n_icu_beds])
        unused_common = len(unused) - unused_icu


        return assignments, unused_icu, unused_common

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

    def assign_doctors(self):

        for i in self.doctors:
            i.reset()

        pat = [i for i in self.patients if i.bed_assigned is not None]

        permutation = assign_doc_patient(self.doctors, pat , self.map_symp_specialty)
        for i, doc in enumerate(permutation):
            doctor = self.doctors[doc]
            patient = pat[i]
            doctor.assign_patient(patient)
            patient.doc_assigned = doctor


    def simulate(self):
        self.initialize()

        for k in range(10):
            stats = Day_Statistics(k)

            stats.initial_critical_patients = sum([1 for i in self.patients if i.status == "critical"])
            stats.initial_grave_patients = sum([1 for i in self.patients if i.status == "grave"])
            stats.initial_regular_patients = sum([1 for i in self.patients if i.status == "regular"])

            self.set_costs_matrix()
            assignm, unused_icu, unused_common = self.assign_beds()
            stats.assignments = assignm
            stats.unused_icu = unused_icu
            stats.unused_common = unused_common

            for i in self.patients:
                stat = i.status
                bed = 'none' if i.bed_assigned is None else i.bed_assigned.typee
                var = f'{stat}_{bed}'
                stats.__dict__[var] += 1

            self.assign_doctors()

            for i in self.doctors:
                i.administer_medicine(self.rag, AllMedicines, self.map_symp_specialty)

            new_p = []

            for ind, i in enumerate(self.patients):
                old_status = i.status

                i.interact()
                if i.is_cured:
                    self.n_patients -= 1
                    status = f'{i.status}_patients_discharged'
                    stats.__dict__[status] += 1
                    if len(i.symptoms) == 0:
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
                    else:
                        stats.__dict__[f'stay_{new_status}'] += 1

            self.patients = new_p

            new_critical, new_grave, new_regular = self.add_new_patients()
            stats.new_critical_patients = new_critical
            stats.new_grave_patients = new_grave
            stats.new_regular_patients = new_regular

            stats.final_critical_patients = sum([1 for i in self.patients if i.status == "critical"])
            stats.final_grave_patients = sum([1 for i in self.patients if i.status == "grave"])
            stats.final_regular_patients = sum([1 for i in self.patients if i.status == "regular"])

            self.daily_stats.append(stats)




def start_simulation(icu_beds, common_beds, initial_p, lambda_, h):
    global simulat, AllSymptoms
    try:
        sim = Simulation(icu_beds, common_beds, initial_p, lambda_, h, rag)
        simulat = sim.daily_stats
        return sim
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


def get_patients_discharged():
    return [x.grave_patients_discharged + x.critical_patients_discharged + x.regular_patients_discharged for x in
            simulat]


def get_critical_same():
    return [x.stay_critical for x in simulat]


def get_grave_same():
    return [x.stay_grave for x in simulat]


def get_regular_same():
    return [x.stay_regular for x in simulat]

def get_unused_icu():
    return [x.unused_icu for x in simulat]

def get_unused_common():
    return [x.unused_common for x in simulat]



def run(icu, common, init, lambda_, h):
    deaths = []
    cured = []
    better = []
    worse = []
    discharged = []
    critical_same = []
    grave_same = []
    regular_same = []
    unused_icu = []
    unused_common = []

    for i in range(4):
        sim = start_simulation(icu, common, init, lambda_, h)
        deaths.append(get_deaths())
        cured.append(get_cured())
        better.append(get_patients_better())
        worse.append(get_patients_worse())
        discharged.append(get_patients_discharged())
        critical_same.append(get_critical_same())
        grave_same.append(get_grave_same())
        regular_same.append(get_regular_same())
        unused_icu.append(get_unused_icu())
        unused_common.append(get_unused_common())

    def stats(title, arr):
        mean_arr = [np.mean([x[day] for x in arr]) for day in range(10)]
        return sum(mean_arr)

    d = stats('Deaths', deaths)
    c = stats('Cured', cured)
    stats('Better', better)
    stats('Worse', worse)
    a = stats('Discharged', discharged)
    stats('Critical_Same', critical_same)
    stats('Grave_Same', grave_same)
    stats('Regular_Same', regular_same)
    u_icu = stats('Unused beds', unused_icu)
    u_c = stats('Unused common', unused_common)

    context = (f'I am doing a simulation of a hospital with {icu} ICU beds and {common} Common beds. The initial number '
               f'of patients is {init} and the patients are generated following a poisson distribution with lambda {lambda_}.'
               f'I will give you the amount of daily deaths and daily discharged patients.'
               f'Also the amount of patients that got better and the amount of patients that got worse.'
               f'Create a story narrating what happened in the hospital during these 10 days '
               f'based on the statistics I will provide you. These numbers are the average of 5 simulations, so remember that '
               f'the numbers are not exact but an average of 5 simulations. '
               f'Daily deaths: {[np.mean([x[day] for x in deaths]) for day in range(10)]}'
               f'Daily discharged: {[np.mean([x[day] for x in discharged]) for day in range(10)]}'
               f'Daily better: {[np.mean([x[day] for x in better]) for day in range(10)]}'
               f'Daily worse: {[np.mean([x[day] for x in worse]) for day in range(10)]}'
               f'\n Also give your opinion on the hospital management.')

    # print(context)

    # print(genai.GenerativeModel('gemini-pro').generate_content(context).text)

    return d, c, a, len(sim.doctors), u_icu, u_c


# __________INITIALIZATION___________
rag = create_rag()

poss = []
# load all possible symptoms
with open('..\..\data\Drugs.json') as f:
    doc = json.load(f)

for i in doc:
    for j in i['side_effects']:
        poss.append(j)
    med = Medicine(i['name'], i['prescribed_for'], i['side_effects'])
    AllMedicines.append(med)

AllSymptoms = list(set(poss))

Symptom_Specialty = {}

for i in AllSymptoms:
    Symptom_Specialty[i] = np.random.choice(specialties)





















