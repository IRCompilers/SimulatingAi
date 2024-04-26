from src.Entities.Doctor import Doctor
from src.Entities.Patient import Patient
import random


def assign_doc_patient(doctors: [Doctor], patients: [Patient], map_sp_sym: dict):
    """
    Doctor is a class. It has a property called specialty. (string)
                       It has a property called max_patients. (int)
    Patient is a class. It has a property called specialties_needed. (dictionary)
          Patient.specialties_needed[specialty] = score (int)
    map_sp_sym is a dictionary. It maps specialties to symptoms
           map_sp_sym[specialty] = {symp1: score, symp2: score, ...}
           this means: map_sp_sym[specialty][symp1] = score from 0-1

    """
    return find_best_assignment(doctors, patients, map_sp_sym, 10, 100, 100)


def fitness(solution: [int], doctors: [Doctor], patients: [Patient], map_sp_sym: dict):
    """
    Solution is a list of integers. Each integer represents the index of the doctor assigned to the patient
    """
    # Create a dictionary to store the patients assigned to each doctor
    doc_pat = {}
    for i in range(len(solution)):
        if solution[i] not in doc_pat:
            doc_pat[solution[i]] = []
        doc_pat[solution[i]].append(i)

        if len(doc_pat[solution[i]]) > doctors[solution[i]].max_patients:
            return 0

    # Calculate the fitness
    fitness = 0
    for doc in doc_pat:
        # Calculate the sum of the scores of the symptoms of the patients assigned to the doctor
        score = 0
        for pat in doc_pat[doc]:
            for sp in patients[pat].symptoms:
                score += map_sp_sym[doctors[doc].specialty][sp]

        # Add the score to the fitness
        fitness += score

    return fitness


def random_solution(doctors: [Doctor], patients: [Patient]):
    """
    Generate a random solution
    """
    return [random.randint(0, len(doctors) - 1) for _ in range(len(patients))]


def random_population(doctors: [Doctor], patients: [Patient], size: int):
    """
    Generate a population of random solutions
    """
    return [random_solution(doctors, patients) for _ in range(size)]


def select_best(population: [[int]], doctors: [Doctor], patients: [Patient], map_sp_sym: dict, n: int):
    """
    Select the best n solutions from a population
    """
    return sorted(population, key=lambda x: fitness(x, doctors, patients, map_sp_sym), reverse=True)[:n]


def mutate(solution: [int], doctors: [Doctor], patients: [Patient]):
    """
    Mutate a solution
    """
    i = random.randint(0, len(solution) - 1)
    solution[i] = random.randint(0, len(doctors) - 1)
    return solution


def crossover(solution1: [int], solution2: [int]):
    """
    Crossover two solutions
    """
    i = random.randint(0, len(solution1) - 1)
    return solution1[:i] + solution2[i:]


def new_population(best: [[int]], doctors: [Doctor], patients: [Patient], map_sp_sym: dict, size: int):
    """
    Generate a new population from the best solutions
    """
    new_population = []
    while len(new_population) < size:
        solution1 = random.choice(best)
        solution2 = random.choice(best)
        new_solution = crossover(solution1, solution2)
        if random.random() < 0.1:
            new_solution = mutate(new_solution, doctors, patients)
        new_population.append(new_solution)
    return new_population


def find_best_assignment(doctors: [Doctor], patients: [Patient], map_sp_sym: dict, n: int, size: int, generations: int):
    """
    Find the best assignment of doctors to patients
    """
    population = random_population(doctors, patients, size)
    for _ in range(generations):
        best = select_best(population, doctors, patients, map_sp_sym, n)
        population = new_population(best, doctors, patients, map_sp_sym, size)
    return select_best(population, doctors, patients, map_sp_sym, 1)[0]


"""

Esta es la implemetacion del un algoritmo genetico para la busqueda de la mejor forma de distribuir pacientes entre los doctores del hospital.

El algoritmo genetico fluye de la siguiente forma:
1. Empezamos con una poblacion de tamano 100 de soluciones al azar. Consideramos una solucion como una lista de enteros, donde cada entero representa el indice del doctor asignado al paciente
2. Utilizando una funcion de fitness (score) escogemos las 10 mejores soluciones entre esas
    1. Entrando un poco en como funciona la funcion de fitness. Esta lo que hace es simplemente dar la suma aditiva del valor que tiene para un doctor atender un sintoma, sumando ese valor de todos los doctores con todos los sintomas de todos sus pacientes. Dicho valor se extrae de un mapa ya predefinido en el conocimiento, q es un mapa de especialidad (la q tiene el doctor) x sintoma (el q tiene el paciente) -> valor de 0 a 1. Como caso extra si se da el caso de que en la solucion un doctor tiene asignado mas pacientes q su capacidad maxima entonces su valor de fitness es 0.
3. Luego realizamos un cruzamiento entre pares de esas 10 mejores poblaciones. Un cruzamiento es escoge un valor al azar y de ahi a la izquierda se coge la primera solucion y de ahi a la derecha se coge la segunda. Esto garantiza q la solucion nueva va a tener facciones de sus dos padres
4. (opcional) Existe la posibilidad de que esa nueva solucion hija mute, q es coge un valor al azar en su cadenas y cambiarlo por otro.
5. El objetivo es repetir desde el paso 2 hasta el paso 4 por 100 generaciones, y al final de esas 100 generaciones escoger la mejor solucion de todas las generaciones.

"""
