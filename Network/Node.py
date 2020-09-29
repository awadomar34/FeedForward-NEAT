import math
import numpy as np


class Node(object):
    def __init__(self, node_gene=None):
        self.number = node_gene[0]
        self.type = node_gene[1]
        self.layer = node_gene[2]

        self.value = 0
        self.output_connections = []

        self.error = 0
        self.input_connections = []

    def print(self):
        print("Node num.: %s, node typ: %s, layer: %s, Num. of conns: %s"
              % (self.number, self.type, self.layer, len(self.output_connections)))

    def output(self):
        return self.Sigmoid(self.value)

    def transferDerivative(self):
        return self.output() * (1 - self.output())

    @staticmethod
    def Sigmoid(x):
        return 1/(1+np.exp(-4.9*x))
