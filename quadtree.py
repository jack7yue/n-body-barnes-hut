import math


class QuadNode:
    def __init__(self, x1, y1, x2, y2, parent=None):
        self.parent = parent
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x_center = (self.x2 + self.x1) / 2
        self.y_center = (self.y2 + self.y1) / 2
        self.x_com, self.y_com = self.x_center, self.y_center  # centre of mass
        self.particle = None
        self.num_particles = 0
        self.children = []
        self.centre_mass = 0

    def subdivide(self):
        self.children = [QuadNode(self.x1, self.y1, self.x_center, self.y_center),
                         QuadNode(self.x_center, self.y1, self.x2, self.y_center),
                         QuadNode(self.x_center, self.y_center, self.x2, self.y2),
                         QuadNode(self.x1, self.y_center, self.x_center, self.y2)]

    def insert(self, particle):
        if self.out_of_bound(particle.x, particle.y):
            return

        index = self.get_quadrant(particle)

        if self.children:
            self.children[index].insert(particle)

        elif self.particle:  # if this node already has a particle, create children and move this particle
            self.subdivide()
            this_particle_index = self.get_quadrant(self.particle)
            self.children[this_particle_index].insert(self.particle)
            self.children[index].insert(particle)
            self.particle = None  # remove particle from this node

        else:
            self.particle = particle

        self.num_particles += 1

    def compute_centre_mass(self):
        total_mass = 0
        x_com = 0
        y_com = 0

        if self.num_particles == 1:
            x_com = self.particle.x
            y_com = self.particle.y
            total_mass = 1  # particle.mass for single particle

        elif self.num_particles > 1:
            for child in self.children:
                child.compute_centre_mass()
                total_mass += child.num_particles  # all masses are currently 1.0
                node_mass = child.num_particles
                x_com += node_mass * child.x_com
                y_com += node_mass * child.y_com
            self.x_com = x_com / total_mass
            self.y_com = y_com / total_mass

    def out_of_bound(self, x, y):
        return not (self.x1 < x <= self.x2 and self.y1 > y >= self.y2)

    def get_quadrant(self, particle):
        """
            Quadrants are as such:
            0 | 1
            3 | 2
        """
        if particle.x < self.x_center and particle.y >= self.y_center:
            return 0

        elif particle.x >= self.x_center and particle.y >= self.y_center:
            return 1

        elif particle.x >= self.x_center and particle.y < self.y_center:
            return 2

        else:
            return 3

    def should_approximate(self, particle, threshold):
        if particle == self.particle:
            return False

        radius = self.x2 - self.x1
        dx = particle.x - self.x_com
        dy = particle.y - self.y_com
        d = math.sqrt(dx*dx + dy*dy)
        ratio = d / radius
        return ratio < threshold


class QuadTree:
    root = None

    def __init__(self, particles, timestep, size, g_const, threshold):
        self.particles = particles
        self.g_const = g_const
        self.timestep = timestep
        self.threshold = threshold
        self.size = size

    def build_tree(self):
        self.root = QuadNode(-self.size, self.size, self.size, -self.size)
        for particle in self.particles:
            self.root.insert(particle)
        self.root.compute_centre_mass()

    def step(self):
        self.build_tree()
        for particle in self.particles:
            queue = [self.root]  # start with root node

            while queue:
                node = queue.pop()

                if node.should_approximate(particle, self.threshold) and node.num_particles:  # ignore empty nodes
                    particle.kick(node, self.g_const, self.threshold)

                else:
                    queue.extend(node.children)  # recurse iteratively over children of node

            particle.drift(self.timestep)

