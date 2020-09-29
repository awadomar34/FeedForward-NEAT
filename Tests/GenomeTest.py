import random
import copy
from copy import deepcopy
from NEAT.Genome import Genome

a = 5

c1 = [1, 1, 4, 0, True]
c2 = [2, 2, 4, 0, False]
c3 = [3, 3, 4, 0, True]

c4 = [4, 2, 5, 0, True]
c5 = [5, 5, 4, 0, True]
c6 = [6, 1, 5, 0, True]

c7 = [7, 3, 5, 0, True]
c8 = [8, 3, 6, 0, True]
c9 = [9, 6, 4, 0, True]


n1 = [1, "input", 0]
n2 = [2, "input", 0]
n3 = [3, "input", 0]

n4 = [4, "output", 2]

n5 = [5, "hidden", 1]
n6 = [6, "hidden", 1]


g1 = Genome()
g2 = Genome()

# =================================================

g1.conn_genes.append(deepcopy(c1))
g1.conn_genes.append(deepcopy(c2))
g1.conn_genes.append(deepcopy(c3))
g1.conn_genes.append(deepcopy(c4))
g1.conn_genes.append(deepcopy(c5))
g1.conn_genes.append(deepcopy(c6))
g1.conn_genes.append(deepcopy(c7))

g1.node_genes.append(deepcopy(n1))
g1.node_genes.append(deepcopy(n2))
g1.node_genes.append(deepcopy(n3))
g1.node_genes.append(deepcopy(n4))
g1.node_genes.append(deepcopy(n5))



g2.conn_genes.append(deepcopy(c1))
g2.conn_genes.append(deepcopy(c2))
g2.conn_genes.append(deepcopy(c3))
g2.conn_genes.append(deepcopy(c4))
g2.conn_genes.append(deepcopy(c5))
g2.conn_genes.append(deepcopy(c6))
g2.conn_genes.append(deepcopy(c8))
g2.conn_genes.append(deepcopy(c9))
g2.conn_genes[2][4] = False

g2.node_genes.append(deepcopy(n1))
g2.node_genes.append(deepcopy(n2))
g2.node_genes.append(deepcopy(n3))
g2.node_genes.append(deepcopy(n4))
g2.node_genes.append(deepcopy(n5))
g2.node_genes.append(deepcopy(n6))

# =================================================

for c in g1.conn_genes:  # + g2.conn_genes:
    c[3] = 3.6879  # random.uniform(-a, a)

g1.print()
g2.print()

print(Genome.CompatibilityMetric(g1, g2))
