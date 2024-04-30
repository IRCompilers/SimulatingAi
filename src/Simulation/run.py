import src.Simulation.Sim as sim
import random
import time

class SimStats:
    def __init__(self, icu, common, deaths, cured, discharged, doctors, initial_patients, lambda_, unused_icu, unused_c):
        self.icu = icu
        self.common = common
        self.deaths = deaths
        self.cured = cured
        self.discharged = discharged
        self.doctors = doctors
        self.unused_icu = unused_icu
        self.unused_common = unused_c

        self.cost = self.__cost_of_simulation()

        self.initial_patients = initial_patients
        self.lambda_ = lambda_

    def __cost_of_beds(self):
        return self.icu * 10000 + self.common * 3000

    def __cost_of_doctors(self):
        return self.doctors * 4000

    def __cost_of_deaths(self):
        return self.deaths * 7000

    def __cost_of_cured(self):
        return self.cured * 2000

    def __cost_of_discharged(self):
        return self.discharged * 3500

    def __cost_of_unused(self):
        return self.unused_icu * 10000 + self.unused_common * 5000

    def __cost_of_simulation(self):
        return (self.__cost_of_beds() + self.__cost_of_unused() + self.__cost_of_doctors() + self.__cost_of_deaths()
                - self.__cost_of_cured() - self.__cost_of_discharged())

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __str__(self):
        return f'ICU: {self.icu}, Common: {self.common}, Unused icu: {self.unused_icu}, Unused com: {self.unused_common}, Deaths: {self.deaths}, Cured: {self.cured}, Discharged: {self.discharged}, Doctors: {self.doctors}, Cost: {self.cost}'



def fitness(solution: SimStats):
    """
    Calculate the fitness of a simulation
    """
    return solution.cost


def random_solution(initial_patients, lambda_):
    """
    Generate a random solution
    """
    icu = random.randint(0, (initial_patients + lambda_) * 2)
    common = random.randint(0, (initial_patients + lambda_) * 2)
    d,c, a, doctors, unused_i, unused_c = sim.run(icu, common, initial_patients, lambda_, sim.calculate_cost_h)
    return SimStats(icu, common, d, c, a, doctors, initial_patients, lambda_, unused_i, unused_c)


def random_population(initial_patients, lambda_, size: int):
    """
    Generate a population of random solution
    """
    return [random_solution(initial_patients, lambda_) for _ in range(size)]


def select_best(population: [SimStats], initial_patients: int, lambda_:int, n: int):
    """
    Select the best n solutions from a population
    """
    return sorted(population, key=lambda x: fitness(x), reverse=False)[:n]


def mutate(solution: SimStats, initial_patients: int, lambda_:int):
    """
    Mutate a solution by changing the value of icu or common beds
    """
    x = random.randint(0, 3)
    if x == 0:
        solution.icu += 1
    elif x ==1:
        solution.common += 1
    elif x == 2 :
        solution.icu -= 1
    else:
        solution.common -= 1
    d,c,a,doc, unused_i, unused_c = sim.run(solution.icu, solution.common, initial_patients, lambda_, sim.calculate_cost_h)
    return SimStats(solution.icu, solution.common, d, c, a, doc, initial_patients, lambda_, unused_i, unused_c)


def crossover(solution1: SimStats, solution2: SimStats):
    """
    Crossover two solutions by swapping the values of icu and common beds
    """
    i = random.randint(0, 1)
    if i == 0:
        d,c,a,doc, unused_i, unused_c = sim.run(solution1.icu, solution2.common, solution1.initial_patients, solution1.lambda_, sim.calculate_cost_h)
        return SimStats(solution1.icu, solution2.common, d, c, a, doc, solution1.initial_patients, solution1.lambda_, unused_i, unused_c)
    else:
        d,c,a,doc, unused_i, unused_c = sim.run(solution2.icu, solution1.common, solution1.initial_patients, solution1.lambda_, sim.calculate_cost_h)
        return SimStats(solution2.icu, solution1.common, d, c, a, doc, solution1.initial_patients, solution1.lambda_, unused_i, unused_c)


def new_population(best: [SimStats], initial_patients: int, lambda_ :int, size: int):
    """
    Generate a new population from the best solutions
    """
    new_population = []
    while len(new_population) < size:
        solution1 = random.choice(best)
        solution2 = random.choice(best)
        new_solution = crossover(solution1, solution2)
        if random.random() < 0.1:
            new_solution = mutate(new_solution, initial_patients, lambda_)
        new_population.append(new_solution)
    return new_population


def find_best_assignment(initial_patients, lambda_):
    """
    Find the best parameters of icu and common beds for the simulation
    """
    population = random_population(initial_patients, lambda_, 50)
    for _ in range(20):
        start = time.time()
        print('Starting')
        best = select_best(population, initial_patients, lambda_,  5)
        population = new_population(best, initial_patients, lambda_, 50)
        end = time.time()
        print(f'Iteration finished : {(end-start)//60}')
    return select_best(population, initial_patients, lambda_, 1)[0]


best = find_best_assignment(30, 15)
print(best)

