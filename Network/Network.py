from Network.Node import Node


class Network(object):
    def __init__(self):
        self.node_dict = {}  # a map of nodes; {ID: node}
        self.layers = []

        self.num_of_layers = 0
        self.input_indices = []

    def print(self):
        print("========================================\n")
        for node in self.node_dict.values():
            node.print()

    def printLayers(self):
        for i in range(len(self.layers)):
            print("Layer %s" % i)
            for node in self.layers[i]:
                node.print()

    def resetNodes(self):
        for node in self.node_dict.values():
            node.value = 0
            node.activated = False

    def evaluateLayers(self, input_values):
        self.resetNodes()

        if len(self.layers[0]) != len(input_values):
            self.print()
            for node in self.layers[0]:
                node.print()
            print("Input vals {}".format(input_values))
            raise Exception("Number of inputs do not match number of input nodes.\n Num of input nodes %s"
                            % len(self.layers[0]))

        for node, val in zip(self.layers[0], input_values):
            node.value = val

        for layer in self.layers:
            for node in layer:
                # activate connections
                for conn in node.output_connections:
                    to_node = self.node_dict[conn[2]]
                    to_node.value += conn[3]*node.output()

        # get outputs
        outputs = []
        for node in self.layers[-1]:
            # outputs.append(node.value)
            outputs.append(node.output())

        return outputs

    @staticmethod
    def InitialiseNetwork(genome):
        network = Network()  # empty network

        genome.calcMaxDepth()

        network.layers = [[] for _ in range(genome.max_depth)]

        # get all the nodes and make a dictionary
        node_index = 0
        for node_gene in genome.node_genes:
            # create new node
            new_node = Node(node_gene)

            # add new node to dictionary
            network.node_dict[new_node.number] = new_node
            
            try:
                network.layers[new_node.layer].append(new_node)
            except:
                genome.print()
                print(network.layers)

            node_index += 1

        # go through connections and add them to nodes
        for conn_gene in genome.conn_genes:
            if conn_gene[4]:
                node = network.node_dict[conn_gene[1]]
                node.output_connections.append(conn_gene)

        return network




























# 08 April 2020, 3:49 AM
# my brain has been fried, pls kill me to make he pain stop. im either dying on the inside
# or my brain doesn't have the energy to have a will to live, i think its the latter but still
# just put me down
