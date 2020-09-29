from Network.Network import Network

from math import cos, pi, sin
import random


class CartPole(object):
    gravity = 9.8  # acceleration due to gravity, positive is downward, m/sec^2
    mcart = 1.0  # cart mass in kg
    mpole = 0.1  # pole mass in kg
    lpole = 0.5  # half the pole length in meters
    time_step = 0.01  # time step in seconds

    def __init__(self, x=None, theta=None, dx=None, dtheta=None, position_limit=2.4, angle_limit_radians=36*pi/180):
        self.position_limit = position_limit
        self.angle_limit_radians = angle_limit_radians

        if x is None:
            x = random.uniform(-0.5 * self.position_limit, 0.5 * self.position_limit)

        if theta is None:
            theta = random.uniform(-0.5 * self.angle_limit_radians, 0.5 * self.angle_limit_radians)

        if dx is None:
            dx = random.uniform(-1.0, 1.0)

        if dtheta is None:
            dtheta = random.uniform(-1.0, 1.0)

        self.t = 0.0
        self.x = x
        self.theta = theta

        self.dx = dx
        self.dtheta = dtheta

        self.xacc = 0.0
        self.tacc = 0.0

    def step(self, force):
        # Locals for readability.
        g = self.gravity
        mp = self.mpole
        mc = self.mcart
        mt = mp + mc
        L = self.lpole
        dt = self.time_step

        # see; http://coneural.org/florian/papers/05_cart_pole.pdf
        st = sin(self.theta)
        ct = cos(self.theta)

        tacc1 = (g * st + ct * (-force - mp * L * self.dtheta ** 2 * st) / mt) / (L * (4.0 / 3 - mp * ct ** 2 / mt))
        xacc1 = (force + mp * L * (self.dtheta ** 2 * st - tacc1 * ct)) / mt

        # Update position/angle.
        self.x += dt * self.dx
        self.theta += dt * self.dtheta

        # Update velocities.
        self.dx += xacc1 * dt
        self.dtheta += tacc1 * dt

        # Remember current acceleration for next step.
        self.tacc = tacc1
        self.xacc = xacc1
        self.t += dt

    def getScaledState(self):
        """Get full state, scaled into (approximately) [0, 1]."""
        return [0.5 * (self.x + self.position_limit) / self.position_limit,
                (self.dx + 0.75) / 1.5,
                0.5 * (self.theta + self.angle_limit_radians) / self.angle_limit_radians,
                (self.dtheta + 1.0) / 2.0]

    @staticmethod
    def TrainPopulation(population, cart_parameters=None):
        # GENERATION_LIMIT = 1000
        # for i in range(GENERATION_LIMIT):
        i = 0
        while True:
            # print("Gen: %s" % i)
            population.print()
            if i % 50 == 0:
                population.champion.print()

            CartPole.RunGame(population.genomes, cart_parameters)
            population.champion = max(population.genomes, key=lambda genome: genome.fitness)

            if population.champion.fitness > 60:
                population.champion.print()
                break
            else:
                population.speciation()
            i += 1

        return population.champion

    @staticmethod
    def RunGame(genomes, cart_parameters=None):
        runs_per_network = 5
        for genome in genomes:

            network = Network.InitialiseNetwork(genome)
            fitnesses = []
            for run in range(runs_per_network):
                if cart_parameters is None:
                    cart = CartPole()
                else:
                    cart = CartPole(cart_parameters[0], cart_parameters[1],
                                    cart_parameters[2], cart_parameters[3])

                while cart.t < 60:
                    inputs = cart.getScaledState()
                    action = network.evaluateLayers(inputs)

                    # apply the force to the cart
                    force = DiscreteForce(action)
                    # force = ContinuousForce(action)
                    cart.step(force)

                    # stop if the network fails to keep the cart or pole exceed the limits
                    if abs(cart.x) > cart.position_limit or abs(cart.theta) > cart.angle_limit_radians:
                        break

                fitness = cart.t
                fitnesses.append(fitness)

            genome.fitness = min(fitnesses)


def DiscreteForce(action):
    return 10.0 if action[0] > 0.5 else -10.0


def ContinuousForce(action):
    return 20*(action[0] - 0.5)
