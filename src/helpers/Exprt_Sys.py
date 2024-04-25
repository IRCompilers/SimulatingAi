from experta import *

class Assignment(Fact):
    pass


class AssignmentCost(KnowledgeEngine):
    @Rule(Fact(bed = 'ICU', state = 'critical', age = 'senior'))
    def ICU_critical_senior(self):
        return 1

    @Rule(Fact(bed = 'ICU', state = 'critical', age = 'adult'))
    def ICU_critical_adult(self):
        return 2

    @Rule(Fact(bed = 'ICU', state = 'critical', age = 'young_adult'))
    def ICU_critical_young_adult(self):
        return 3

    @Rule(Fact(bed = 'common', state = 'critical', age = 'senior'))
    def common_critical_senior(self):
        return 4

    @Rule(Fact(bed = 'common', state = 'critical', age = 'adult'))
    def common_critical_adult(self):
        return 5

    @Rule(Fact(bed = 'common', state = 'critical', age = 'young_adult'))
    def common_critical_young_adult(self):
        return 6

    @Rule(Fact(bed = 'ICU', state = 'grave', age = 'senior'))
    def ICU_grave_senior(self):
        return 7

    @Rule(Fact(bed = 'ICU', state = 'grave', age = 'adult'))
    def ICU_grave_adult(self):
        return 8

    @Rule(Fact(bed = 'ICU', state = 'grave', age = 'young_adult'))
    def ICU_grave_young_adult(self):
        return 9

    @Rule(Fact(bed = 'common', state = 'grave', age = 'senior'))
    def common_grave_senior(self):
        return 10

    @Rule(Fact(bed = 'common', state = 'grave', age = 'adult'))
    def common_grave_adult(self):
        return 11

    @Rule(Fact(bed = 'common', state = 'grave', age = 'young_adult'))
    def common_grave_young_adult(self):
        return 12

    @Rule(Fact(bed = 'common', state = 'regular', age = 'senior'))
    def common_regular_senior(self):
        return 13

    @Rule(Fact(bed = 'common', state = 'regular', age = 'adult'))
    def common_regular_adult(self):
        return 14

    @Rule(Fact(bed = 'common', state = 'regular', age = 'young_adult'))
    def common_regular_young_adult(self):
        return 15

    @Rule(Fact(bed = 'ICU', state = 'regular', age = 'senior'))
    def ICU_regular_senior(self):
        return 16

    @Rule(Fact(bed = 'ICU', state = 'regular', age = 'adult'))
    def ICU_regular_adult(self):
        return 17

    @Rule(Fact(bed = 'ICU', state = 'regular', age = 'young_adult'))
    def ICU_regular_young_adult(self):
        return 18

    @Rule(Assignment())
    def assignment_cost(self):
        return 0






    