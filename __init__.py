from NEAT.Genome import Genome
from NEAT.Species import Species
from NEAT.Population import Population

from Network.Node import Node
from Network.Network import Network

from Simulations.XOR import XOR
from Simulations.SingleCartPole import CartPole

""" comment/uncomment these to choose which test to run """
# from Tests import XORTest
# from Tests import CartPoleTest

a = [1, 2, 3, 4]

a = a[:len(a) // 5]

print(a)
