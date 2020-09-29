import random


class Species(object):
    def __init__(self, mascot):
        self.mascot = mascot
        self.members = []
        self.members.append(self.mascot)

        self.fitness = 0  # determines the number of offspring for this species
        self.previous_fitness = 0  # to keep track of stagnant species
        self.unchanged_fitness = 0  # number of generations the avg fitness hasn't increased

    def print(self):
        print("Num. of members: %s, avg. fitness: %s\n"
              % (len(self.members), self.fitness))
        self.mascot.print()

    def reset(self):
        # used at the beginning of speciation
        if len(self.members) > 0:
            self.mascot = random.choice(self.members)

        self.members = [self.mascot]

        # check if species average has increased
        if self.fitness <= self.previous_fitness:
            self.unchanged_fitness += 1
        else:
            self.unchanged_fitness = 0

        self.previous_fitness = self.fitness
        self.fitness = 0
