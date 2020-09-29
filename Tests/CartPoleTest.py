from NEAT.Population import Population
from Simulations.SingleCartPole import CartPole


n = 1  # number of tests

results = []
for i in range(0, n):
    pop = Population.InitialisePopulation(4, 1)

    CartPole.TrainPopulation(pop)
    pop.print()
    pop.champion.print()

    print("MAX FITNESS REACHED.\n")

    genome_stats = pop.champion.genomeStats()
    print("Champion structure: %s hidden nodes, %s enabled connections" % (genome_stats[0], genome_stats[1]))

    # uncomment this to write to results to a file
    # with open('XORResults_1.csv', 'a') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(result)
