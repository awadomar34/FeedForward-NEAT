import copy
import random

perturbation_range = 0.5  # weight mutation range
weight_range = 2.5  # weight initialisation range

weight_max = 30  # weight range, ie all w exist in [-weight_max, weight_max]


class Genome(object):
    def __init__(self):
        self.node_genes = []
        self.conn_genes = []
        self.fitness = 0
        self.max_depth = 0

    def print(self):
        """
        prints the genome's attributes and all its genes

        :return: no return
        """
        print("Num. of nodes: %s, Num. of conns: %s, Fitness: %s"
              % (len(self.node_genes), len(self.conn_genes), self.fitness))
        for node in self.node_genes:
            print("Node: (ID=%s, %s, depth=%s)" % (node[0], node[1], node[2]))
        for conn in self.conn_genes:
            print("\t(ID=%s, %s->%s, W=%s, on=%s)" % (conn[0], conn[1], conn[2], round(conn[3], 2), conn[4]))
        print()

    def printString(self):
        """
        creates and returns a string with all the genome's attributes and genes. however this is not used anymore

        return: string
        """
        string = "Num. of nodes: %s, Num. of conns: %s, Fitness: %s\n" \
                 % (len(self.node_genes), len(self.conn_genes), self.fitness)
        for node in self.node_genes:
            string += "Node: (ID=%s, %s, depth=%s\n" % (node[0], node[1], node[2])
        for conn in self.conn_genes:
            string += "\t(ID=%s, %s->%s, W=%s, on=%s\n" % (conn[0], conn[1], conn[2], conn[3], conn[4])

        return string

    def genomeString(self):
        """
        creates and returns a string which makes it easy to rebuild the genome

        :return: the genome string
        """
        # string = "\n%s,%s,%s," % (len(self.node_genes), len(self.conn_genes), self.fitness)
        string = 'g,%s,%s,%s,%s,\n' % (self.fitness, self.max_depth, len(self.node_genes), len(self.conn_genes))
        for node in self.node_genes:
            string += "n,%s,%s,%s,\n" % (node[0], node[1], node[2])
        for conn in self.conn_genes:
            string += "c,%s,%s,%s,%s,%s,\n" % (conn[0], conn[1], conn[2], conn[3], conn[4])

        return string

    @staticmethod
    def stringToGenome(genotype):
        """
        creates and returns a genome from the genome string. using the format of the method directly above
        'genomeString()'

        :param genotype: a string which has been made by 'genomeString()' containing the genetic make up of the genome
                                to be created
        :return: a genome
        """
        lines = genotype.split("\n")

        genome = Genome()
        for line in lines:
            genome_details = line.split(",")

            if genome_details[0] == 'f':
                genome.fitness = float(genome_details[1])
                genome.max_depth = int(genome_details[2])
                # num_of_nodes = int(genome_details[3])
                # num_of_conns = int(genome_details[4])

            elif genome_details[0] == 'n':
                new_node = [int(genome_details[1]), genome_details[2], int(genome_details[3])]  # [number, type, depth]
                genome.node_genes.append(new_node)

            elif genome_details[0] == 'c':
                new_conn = [int(genome_details[1]), int(genome_details[2]), int(genome_details[3]),
                            float(genome_details[4]), bool(genome_details[5])]  # [innov, from, to, weight, enabled]
                genome.conn_genes.append(new_conn)

        return genome

    def genomeStats(self):
        """
        counts the number of hidden nodes and enabled connections of the genome
        used to collect results

        :return: number of hidden nodes and enabled connections as a list
        """
        hidden_nodes = 0
        enabled_conns = 0
        for node in self.node_genes:
            if node[1] == 'hidden':
                hidden_nodes += 1

        for conn in self.conn_genes:
            if conn[4]:
                enabled_conns += 1


        return [hidden_nodes, enabled_conns]

    def clone(self):
        """
        creates and returns an exact clone of the genome

        :return: a genome exactly the same as this one
        """
        clone = Genome()
        clone.node_genes = copy.deepcopy(self.node_genes)
        clone.conn_genes = copy.deepcopy(self.conn_genes)
        clone.fitness = self.fitness

        return clone

    def randomWeightsClone(self):
        """
        creates and returns an clone of this genome with same stucture but randomised weights

        :return: a genome with the same topology as this one
        """
        clone = Genome()
        clone.node_genes = copy.deepcopy(self.node_genes)
        clone.conn_genes = copy.deepcopy(self.conn_genes)
        for conn in clone.conn_genes:
            conn[3] = random.uniform(-weight_range, weight_range)
        clone.fitness = self.fitness

        return clone

    # ====== MUTATION METHODS ======
    def mutateWeights(self):
        """
        iterates through the connections genes. Each connection gene has a 90% chance of being perturbed by a small
        floating point number chosen from a uniform distribution. The variable that decides the range of the uniform
        distribution is  'perturbation_range', declared at the top of the file

        :return: no return
        """
        for conn in self.conn_genes:
            r = random.random()  # 0 <= r < 1
            if r < 0.9:
                # uniform perturbation; the paper simply states uniform perturbation, im interpreting that as add
                # a small random value to the weight
                conn[3] += random.uniform(-perturbation_range, perturbation_range)

                # if conn[3] > weight_max:
                #     conn[3] = weight_max
                #
                # elif conn[3] < -weight_max:
                #     conn[3] = -weight_max
            else:
                conn[3] = random.uniform(-weight_range, weight_range)

    def addNode(self):
        """
        turns connection (a,b) into connections (a,c) & (c,b), where a, b & c are nodes, and c is the new node gene

        :return: no return
        """

        # randomly select a connection and disable it
        old_conn = random.choice(self.conn_genes)
        while not old_conn[4]:
            # if the connection is already disabled, choose a new one
            old_conn = random.choice(self.conn_genes)
        old_conn[4] = False

        # create the new node c
        new_node = self.NewNodeGene('hidden', old_conn)

        # create the connection (a,c)
        new_conn_1 = self.NewConnectionGene(old_conn[1], new_node[0], 1)

        # create the connection (c,b)
        new_conn_2 = self.NewConnectionGene(new_node[0], old_conn[2], old_conn[3])

        self.node_genes.append(new_node)
        # self.conn_genes.extend([new_conn_1, new_conn_2])
        self.conn_genes.append(new_conn_1)
        self.conn_genes.append(new_conn_2)


        self.calcMaxDepth()

    def connectionExists(self, node_1, node_2):
        """
        used in addConnection().
        returns true if there is a connection between node_1 and node_2

        :param node_1: node gene
        :param node_2: node gene
        :return: boolean value
        """

        for conn in self.conn_genes:
            # if conn.enabled:
            if node_1[0] == conn[1] and node_2[0] == conn[2]:
                # print("connection exists")
                return True

        return False

    def addConnection(self):
        """
        adds a connection between 2 previously unconnected nodes. The connection needs to be feed-forward.
        this method should really use a swap function if the depth of node_1 is higher than the depth of node_2
        but instead it moves the index which chooses node_1 down by 1, and move the index which choose node_2 up
        "don't fix it if it ain't broke", im taking this advice to heart

        :return: no return
        """

        # roll for m and n
        m = random.randint(0, len(self.node_genes)-1)
        n = random.randint(0, len(self.node_genes)-1)

        counter = 0
        counter_limit = len(self.node_genes)**2
        connection_valid = False
        while not connection_valid and counter < counter_limit:
            node_1 = self.node_genes[m]
            node_2 = self.node_genes[n]
            connection_valid = True

            # if the connection isn't valid, then randomly move one of the indices along in their respective directions
            if node_1[2] >= node_2[2] or self.connectionExists(node_1, node_2):
                connection_valid = False

                # check if m can be iterated.
                if m == 0:
                    # since m cannot be iterated, check if n can be
                    if n == len(self.node_genes)-1:
                        # re-roll m
                        m = random.randint(0, len(self.node_genes)-1)
                    else:
                        n += 1

                # check if n can be iterated
                elif n == len(self.node_genes)-1:
                    if m == 0:
                        # re-roll n
                        n = random.randint(0, len(self.node_genes)-1)
                    else:
                        m -= 1

                # if they can both be iterated, then randomly choose one and iterate it in its direction
                else:
                    if random.random() < 0.5:
                        m -= 1
                    else:
                        n += 1

            counter += 1

        if counter < counter_limit and connection_valid:
            new_conn = self.NewConnectionGene(node_1[0], node_2[0], random.uniform(-weight_range, weight_range))
            self.conn_genes.append(new_conn)

        # make sure that the node's depths are consistent
        self.calcMaxDepth()

    # ====== MISC METHODS ======
    def matchingGene(self, connection_to_find):
        """
        finds a similar connection gene to connection_to_find

        :param connection_to_find: connection gene
        :return: a connection gene which is similar to connection_to_find (has the same innovation number)
             or: None
        """
        # returns
        # this is used in Crossover() but it doesn't need to be static

        for conn in self.conn_genes:
            if conn[0] == connection_to_find[0]:
                return conn

        return None

    def calcMaxDepth(self):
        """
        calculates the depth of every node and the max depth of the genome using a breadth first search.

        :return: no return
        """
        checked = [False]*len(self.node_genes)
        node_dict = {}
        node_index = 0
        curr_depth = []
        for node in self.node_genes:
            node_dict[node[0]] = node_index
            node_index += 1

            if node[1] == 'input':
                node[2] = 0
                curr_depth.append(node)


        next_depth = []
        d = 1
        # while curr_depth isn't empty
        while curr_depth:
            # for every node in the current depth
            for node in curr_depth:

                for conn in self.conn_genes:
                    if node[0] == conn[1]:
                        to_index = node_dict[conn[2]]
                        if not checked[to_index]:
                            self.node_genes[to_index][2] = d
                            next_depth.append(self.node_genes[to_index])

                if node[1] != 'output':
                    index = node_dict[node[0]]
                    checked[index] = True

            curr_depth = next_depth
            next_depth = []
            d += 1
            # print("curr_depth = %s, next_depth = %s" % (len(curr_depth), len(next_depth)))

        self.max_depth = d - 1
        self.node_genes.sort(key=lambda n: n[2])

    # ====== NODE & CONNECTION METHODS ======
    @staticmethod
    def NewConnectionGene(from_node, to_node, weight, enabled=True):
        """
        searches through the connection history file to see if a connection with the same details as the input
        parameters. If none exist, a new record is made in the file with the correct innovation number.
        A connection gene is made and returned with the correct innovation number

        :param from_node: an integer, the number of the node the connections connects from
        :param to_node: an integer, the number of the node the connections connects to
        :param weight: a float, the desired weight of the new connection
        :param enabled: a boolean, whether or not the desired connection is enabled or not
        :return: a connection gene with the correct innovation number
        """
        #

        conn_file = open("conn_history.txt", 'r')
        lines = conn_file.readlines()

        for line in lines:
            words = line.split(',')
            innov = int(words[0])
            frm = int(words[1])
            to = int(words[2])

            if frm == from_node and to == to_node:
                # close the file, its not needed anymore
                conn_file.close()

                new_conn = [innov, from_node, to_node, weight, enabled]
                return new_conn

        # if the conn doesnt already exist
        conn_file.close()

        conn_file = open('conn_history.txt', 'a')

        innov = len(lines)+1
        conn_file.write("%s,%s,%s,\n" % (innov, from_node, to_node))

        conn_file.close()

        new_conn = [innov, from_node, to_node, weight, enabled]
        return new_conn

    @staticmethod
    def NewNodeGene(typ, conn):
        """
        searches through the node history file to see if there is a node which has been created through disabling a
        connection with the same innovation number as conn, the input parameter.

        :param typ: string, the type of the desired node. The options are 'input', 'hidden' or 'output'
        :param conn: a connection gene which has been disabled to create a new node
        :return: a node gene with the correct number
        """
        if typ not in ['input', 'hidden', 'output']:
            raise Exception("Invalid node type. Valid node types are 'input', 'hidden' or 'output'.")

        # returns a node with the correct number. this should be used whenever a new node is made

        if typ == 'hidden':
            node_file = open("node_history.txt", 'r')
            lines = node_file.readlines()

            for line in lines:
                words = line.split(',')
                number = int(words[0])
                conn_num = int(words[1])

                if conn_num == conn[0]:
                    new_node = [number, typ, -1]  # (node num, type, depth)

                    # close the file and return the conn
                    node_file.close()
                    return new_node

            # if the conn doesnt already exist
            node_file.close()

            node_file = open('node_history.txt', 'a')
            new_number = len(lines) + 1
            node_file.write("%s,%s,\n" % (new_number, conn[0]))
            node_file.close()

            new_node = [new_number, typ, -1]

            return new_node
        else:
            node_file = open('node_history.txt', 'r')
            new_number = len(node_file.readlines()) + 1
            node_file.close()

            node_file = open('node_history.txt', 'a')
            node_file.write("%s,0,\n" % new_number)
            node_file.close()

            new_node = [new_number, typ, -1]  # (node num, type, depth)

            return new_node

    # ====== STATIC GENOME METHODS ======
    @staticmethod
    def InitialiseGenome(num_inputs=1, num_outputs=1):
        """
        creates and returns a fully connected genome, with no nodes in the hidden layer

        :param num_inputs: integer, the number of input nodes in the desired genome. Bias nodes are considered input
                                    nodes
        :param num_outputs: integer, the number of output nodes in the desired genome.
        :return: a genome, representing a fully connected network with no hidden nodes, only inout and output nodes
        """

        genome = Genome()

        # make the input nodes
        for i in range(num_inputs):
            new_node = Genome.NewNodeGene('input', None)
            genome.node_genes.append(new_node)

        # make the output nodes
        for i in range(num_outputs):
            new_node = Genome.NewNodeGene('output', None)
            genome.node_genes.append(new_node)

        # connect all the input & bias nodes to the output nodes
        for node in genome.node_genes:
            if node[1] == 'input' or node[1] == 'bias':
                # make a connection to every output node
                # for i in range(num_inputs+num_bias, num_inputs+num_bias+num_outputs):
                for i in range(num_inputs, num_inputs + num_outputs):
                    new_conn = Genome.NewConnectionGene(node[0], genome.node_genes[i][0],
                                                        random.uniform(-weight_range, weight_range))
                    genome.conn_genes.append(new_conn)

        genome.calcMaxDepth()

        return genome

    @staticmethod
    def Crossover(genome_1, genome_2):
        if genome_1.fitness > genome_2.fitness:
            parent_1 = genome_1
            parent_2 = genome_2
        elif genome_1.fitness < genome_2.fitness:
            parent_1 = genome_2
            parent_2 = genome_1
        else:  # genome_1.fitness == genome_2.fitness:
            if random.random() < 0.5:
                parent_1 = genome_2
                parent_2 = genome_1
            else:
                parent_1 = genome_1
                parent_2 = genome_2

        parent_1.conn_genes.sort(key=lambda c: c[0])
        parent_2.conn_genes.sort(key=lambda c: c[0])
        # now assume parent_1 is the fitter parent

        # make an empty child genome
        child = Genome()

        m = 0
        n = 0
        while m < len(parent_1.conn_genes) and n < len(parent_2.conn_genes):
            if parent_1.conn_genes[m][0] == parent_2.conn_genes[n][0]:
                # matching gene
                if random.random() < 0.4:
                    # 40% chance of average
                    conn_to_add = parent_1.conn_genes[m].copy()
                    conn_to_add[3] = (parent_1.conn_genes[m][3] + parent_2.conn_genes[n][3])/2
                else:
                    # 60% chance randomly choosing
                    if random.random() < 0.5:
                        conn_to_add = parent_1.conn_genes[m].copy()
                    else:
                        conn_to_add = parent_2.conn_genes[n].copy()

                # 25% chance the conn gets re-enabled
                if not parent_1.conn_genes[m][4] or not parent_2.conn_genes[n][4]:
                    if random.random() < 0.25:
                        conn_to_add[4] = True

                child.conn_genes.append(conn_to_add)

                m += 1
                n += 1
            elif parent_1.conn_genes[m][0] > parent_2.conn_genes[n][0]:
                # do nothing, we don't want the parent_2 disjoint conn
                n += 1
            else:  # parent_1.conn_genes[m][0] < parent_2.conn_genes[n][0]
                child.conn_genes.append(parent_1.conn_genes[m].copy())
                m += 1

        while m < len(parent_1.conn_genes):
            child.conn_genes.append(parent_1.conn_genes[m].copy())
            m += 1

        # give the child all of the fitter parent's nodes to ensure consistency of the topology
        child.node_genes = parent_1.node_genes.copy()

        return child

    @staticmethod
    def CompatibilityMetric(genome_1, genome_2):
        # returns the distance between 2 genomes

        genes_1 = copy.deepcopy(genome_1.conn_genes)
        genes_2 = copy.deepcopy(genome_2.conn_genes)

        genes_1.sort(key=lambda conn: conn[0])
        genes_2.sort(key=lambda conn: conn[0])

        # the number of genes of the larger genome
        N = max(len(genes_1), len(genes_2))

        W = 0  # sum of weights differences of matching genes
        count_W = 0  # number of matching genes
        D = 0  # number of disjoint genes
        # E = 0  # number of excess genes

        # do a loop for the NON-EXCESS connections
        m = 0
        n = 0
        while m < len(genes_1) and n < len(genes_2):
            if genes_1[m][0] == genes_2[n][0]:
                W += abs(genes_1[m][3] - genes_2[n][3])  # fuck. this was a + for so long. FUCK. FUCK. FUCK.
                count_W += 1

                m += 1
                n += 1
            else:
                D += 1
                if genes_1[m][0] < genes_2[n][0]:
                    m += 1
                else:
                    n += 1

        # then add the rest as excess connections
        E = (len(genes_1) - m) + (len(genes_2) - n)  # number of excess genes


        # set constants of the distance equation
        C1 = 1
        C2 = 1
        C3 = 0.4
        if count_W == 0:
            count_W = 1  # n=0 => W=0 so 0/1=0.

        if N < 20:
            distance = C1*E + C2*D + C3*(W/count_W)
        else:
            distance = (C1*E + C2*D)/N + C3*(W/count_W)

        # return [E, D, W, n]
        return distance
