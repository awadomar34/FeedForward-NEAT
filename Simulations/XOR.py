from Network.Network import Network
import random


class XOR(object):
    input_vals = [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    expected_vals = [0, 1, 1, 0]

    def __init__(self):
        pass

    @staticmethod
    def TrainPopulation(population):
        for i in range(500):
            population.print()
            if population.curr_gen_num % 100 == 0:
                population.champion.print()
            XOR.RunGame(population.genomes)

            if population.champion.fitness >= 3.9:  # % accuracy is fine
                print("\nMAX FITNESS REACHED.")
                population.champion.print()
                population.print()
                break

            population.speciation()

        return population.champion

    @staticmethod
    def RunGame(genomes):
        indices = [0, 1, 2, 3]
        random.shuffle(indices)
        for genome in genomes:
            network = Network.InitialiseNetwork(genome)
            genome.fitness = 4
            for i in indices:
                output = network.evaluateLayers(XOR.input_vals[i])
                genome.fitness -= (output[0] - XOR.expected_vals[i])**2
                # f_delta = (output[0] - XOR.expected_vals[i])**2
                # print(f_delta)
