

def compute_acceleration(x1, y1, x2, y2, mass, g_const):
    rx = x2 - x1
    ry = y2 - y1
    r2 = rx ** 2 + ry ** 2
    a_x = (g_const * mass) / r2
    a_y = (g_const * mass) / r2
    return a_x, a_y


class Body:
    def __init__(self, x, y, v_x, v_y):
        self.mass = 1

        # Position
        self.x = x
        self.y = y
        self.z = 0

        # Velocity
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = 0

    # Leapfrog Integration (Drift-Kick-Drift)
    def drift(self, timestep):  # drift
        self.x += self.v_x * timestep
        self.y += self.v_y * timestep

    def kick(self, node, g_const, timestep):  # drift-kick
        x = self.x * self.v_x * timestep / 2
        y = self.y * self.v_y * timestep / 2
        y = self.z * self.v_z * timestep / 2

        a = compute_acceleration(x, y, node.x_com, node.y_com, node.centre_mass, g_const)
        self.v_x += a[0] * timestep
        self.v_y += a[1] * timestep
