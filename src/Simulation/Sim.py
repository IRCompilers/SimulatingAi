from src.Simulation.AllStats import AllStats
from src.Simulation.DailyStats import DailyStats

class Simulation():
    def __init__(self, population, doctors, days):
        self.population = population
        self.doctors = doctors
        self.days = days
        self.stats = AllStats()

    def run(self):
        for day in range(self.days):
            daily_stats = DailyStats(day, self.population, self.doctors)
