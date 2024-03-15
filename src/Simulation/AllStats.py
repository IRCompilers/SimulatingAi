from src.Simulation import DailyStats

class AllStats:
    def __init__(self):
        self.stats = []
        self.total_stats = None

    def add_stats(self, daily_stats):
        self.stats.append(daily_stats)

    def __calculate_stats(self):
        #sum all the stats

        total_stats = {}
        total_stats['correctly_diagnosed'] = 0
        total_stats['incorrectly_diagnosed'] = 0
        total_stats['not_diagnosed'] = 0
        total_stats['cured'] = 0
        total_stats['not_cured'] = 0
        total_stats['doctors_diagnosis'] = {}

        for daily_stats  in self.stats:
            stats = daily_stats.get_stats()
            total_stats['correctly_diagnosed'] += stats['correctly_diagnosed']
            total_stats['incorrectly_diagnosed'] += stats['incorrectly_diagnosed']
            total_stats['not_diagnosed'] += stats['not_diagnosed']
            total_stats['cured'] += stats['cured']
            total_stats['not_cured'] += stats['not_cured']
            for doctor in stats['doctors_diagnosis']:
                if doctor not in total_stats['doctors_diagnosis']:
                    total_stats['doctors_diagnosis'][doctor] = {}
                    total_stats['doctors_diagnosis'][doctor]['correctly_diagnosed'] = 0
                    total_stats['doctors_diagnosis'][doctor]['incorrectly_diagnosed'] = 0
                    total_stats['doctors_diagnosis'][doctor]['not_diagnosed'] = 0
                    total_stats['doctors_diagnosis'][doctor]['cured'] = 0
                    total_stats['doctors_diagnosis'][doctor]['not_cured'] = 0
                total_stats['doctors_diagnosis'][doctor]['correctly_diagnosed'] += stats['doctors_diagnosis'][doctor]['correctly_diagnosed']
                total_stats['doctors_diagnosis'][doctor]['incorrectly_diagnosed'] += stats['doctors_diagnosis'][doctor]['incorrectly_diagnosed']
                total_stats['doctors_diagnosis'][doctor]['not_diagnosed'] += stats['doctors_diagnosis'][doctor]['not_diagnosed']
                total_stats['doctors_diagnosis'][doctor]['cured'] += stats['doctors_diagnosis'][doctor]['cured']
                total_stats['doctors_diagnosis'][doctor]['not_cured'] += stats['doctors_diagnosis'][doctor]['not_cured']

        self.total_stats = total_stats

    def get_stats(self):
        if not self.total_stats:
            self.__calculate_stats()
        return self.total_stats


