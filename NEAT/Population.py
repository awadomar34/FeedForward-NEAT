from NEAT.Genome import Genome
from NEAT.Species import Species
import random

# mutation parameters
mutate_weights_prob = 0.8
add_node_prob = 0.03
add_conn_prob = 0.05


# reproduction parameters
interspecies_mating_prob = 0.001
single_parent_prob = 0.25
mating_only_prob = 0.2  # no mutation after crossover

# elimination parameters
elitism = 2  # number of champions from each species
survival_threshold = 0.2  # amount of species we want to keep

# species parameters
max_stagnation = 15  # one of the parameters

# distance threshold
compatibilty_threshold = 3
# C1 = 1
# C2 = 1
# C3 = 1
# N = 20  # 'large' genome size

# fitness criterion; how a species's fitness should be calculated
fitness_criterion = 'mean'  # 'max'


class Population(object):
    population_size = 150

    def __init__(self):
        self.genomes = []
        self.curr_gen_num = 0
        self.species_list = []
        self.champion = Genome()  # empty genome

    def print(self):
        print("Gen.: %s, Num. of species: %s, Champion fitness: %.2f, Population size: %s\n" %
              (self.curr_gen_num, len(self.species_list), self.champion.fitness, len(self.genomes)))

    def printString(self):
        string = "Gen.: %s, Num. of species: %s, Champion fitness: %.2f, Population size: %s\n" \
               % (self.curr_gen_num, len(self.species_list), self.champion.fitness, len(self.genomes))
        # string += self.champion.printString()

        return string

    def populationString(self):
        string = "p,%s,%s,%s,%s,\n" % (self.curr_gen_num, len(self.species_list), round(self.champion.fitness, 2),
                                       len(self.genomes))

        return string

    def fullPrint(self):
        self.print()
        for g in self.genomes:
            g.print()

    def speciesPrint(self):
        self.print()
        i = 1
        for s in self.species_list:
            print("Species no. %s\n==============\n" % i)
            i += 1
            s.print()

    # ====== SELECTION METHODS ======
    def speciation(self):
        # reset all the species and clear next_gen
        for species in self.species_list:
            species.reset()
        next_gen_genomes = []

        # speciation loop; split population into species. place each genome into a species
        for genome in self.genomes:
            species_found = False
            for species in self.species_list:
                if Genome.CompatibilityMetric(genome, species.mascot) < compatibilty_threshold:
                    species.members.append(genome)
                    species_found = True
                    break

            if not species_found:
                new_species = Species(genome)
                self.species_list.append(new_species)

        # elimination loop
        total_adjusted_fitness = 0
        ratio_to_keep = int(1/survival_threshold)
        for species in self.species_list:
            # find species average fitness
            # if species.unchanged_fitness < max_stagnation:
            # only species which are allowed to reproduce should be considered when
            # calculating total_adjusted_fitness
            if fitness_criterion == 'max':
                species.fitness = max(member.fitness for member in species.members)
            else:
                for genome in species.members:
                    species.fitness += genome.fitness
                species.fitness = species.fitness/len(species.members)


            total_adjusted_fitness += species.fitness

            # SORT THE MEMBERS
            species.members.sort(key=lambda g: g.fitness, reverse=True)
            species.mascot = species.members[0]  # species champion
            next_gen_genomes.extend(species.members[0:elitism])  # add champ to next gen

            # check for new champion
            if species.members[0].fitness > self.champion.fitness:
                self.champion = species.members[0]

            # make sure list slicing doesn't kill the elites
            if len(species.members) < ratio_to_keep*elitism:
                # if the list slicing mechanic is gonna get rid of the elite, only keep the elite
                species.members = species.members[0:elitism]
            else:
                species.members = species.members[:len(species.members) // ratio_to_keep]


        # reproduction loop
        for species in self.species_list:
            if species.unchanged_fitness < max_stagnation:
                num_of_offspring = self.population_size*(species.fitness/total_adjusted_fitness)

                i = 0
                while i < num_of_offspring and len(next_gen_genomes) < self.population_size:
                    # print(i)
                    child = self.getOffspring(species)

                    next_gen_genomes.append(child)
                    i += 1

                    if len(next_gen_genomes) > self.population_size:
                        break
            else:
                # species stagnated
                self.species_list.remove(species)
                # for member in species.members:
                #     try:
                #         self.genomes.remove(member)
                #     except:
                #         print("member not found")


        self.genomes = next_gen_genomes
        self.curr_gen_num += 1

    def getOffspring(self, species):
        mutate = True

        r = random.random()
        # chance of inter-species crossover
        if r < interspecies_mating_prob:
            parent_1 = random.choice(species.members)
            parent_2 = random.choice(random.choice(self.species_list).members)

            child = Genome.Crossover(parent_1, parent_2)

            # 20% chance no mutation after crossover
            if random.random() < mating_only_prob:
                mutate = False

        # chance of a single parent
        elif r < single_parent_prob:
            # select a random member of the species, its off spring is a clone of it
            child = random.choice(species.members).clone()

        # chance the new genome is a result of normal crossover
        else:
            # pick 2 random member of the species to be parents
            # parent_1 = random.choice(species.members)
            # parent_2 = random.choice(species.members)

            parent_1, parent_2 = random.choices(species.members, k=2)

            child = Genome.Crossover(parent_1, parent_2)

            # 20% chance no mutation after crossover
            if random.random() < mating_only_prob:
                mutate = False

        # mutate the child
        if mutate:
            # 80% chance weights are mutated
            if random.random() < mutate_weights_prob:
                child.mutateWeights()

            # chance a new node is added
            if random.random() < add_node_prob:
                child.addNode()

            # chance a new connection is added
            if random.random() < add_conn_prob:
                child.addConnection()

        return child

    # ====== STATIC METHODS ======
    @staticmethod
    def InitialisePopulation(num_inputs=1, num_outputs=1):
        # returns a population filled with the same genome

        # clear the files used for innov history
        conn_file = open('conn_history.txt', 'w')
        conn_file.close()
        node_file = open('node_history.txt', 'w')
        node_file.close()

        # make the initial genome to fill the population with
        genome = Genome.InitialiseGenome(num_inputs, num_outputs)

        # create the population
        population = Population()
        # set the population champion
        population.champion = genome.clone()

        # fill population
        while len(population.genomes) < Population.population_size:
            population.genomes.append(genome.randomWeightsClone())

        return population
