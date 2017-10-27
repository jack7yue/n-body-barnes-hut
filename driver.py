from quadtree import QuadTree
import models


timestep = 0.1
gravitational_constant = 0.000005


particles = models.n_bodies(1000)

tree = QuadTree(particles, timestep, 10, gravitational_constant, 0.5)

while True:
    tree.step()
