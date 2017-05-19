from BarnesHut import *
import Initialization


timestep = 0.1
gravitational_constant = 0.000005


particles = Initialization.n_bodies(1000)

tree = QuadTree(particles, timestep, 10, gravitational_constant, 0.5)

while True:
    tree.step()
