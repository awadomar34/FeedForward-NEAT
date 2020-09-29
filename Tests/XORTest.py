from NEAT.Population import Population
from Simulations.XOR import XOR


n = 2  # number of test


gen_avg = 0
successful_runs = 0
for i in range(0, n):
    population = Population.InitialisePopulation(3, 1)

    print("Run number %s:\n" % (i+1))
    solution_genome = XOR.TrainPopulation(population)

    if population.champion.fitness >= 3.9:  # % accuracy is fine
        gen_avg += population.curr_gen_num
        successful_runs += 1
        print("MAX FITNESS REACHED.\n")

        genome_stats = population.champion.genomeStats()
        print("Champion structure: %s hidden nodes, %s enabled connections" % (genome_stats[0], genome_stats[1]))

        # uncomment this to write to results to a file
        # with open('XORResults.csv', 'a') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(result)

gen_avg /= successful_runs
print("successful_runs: %s, gen avg: %s" % (successful_runs, gen_avg))
