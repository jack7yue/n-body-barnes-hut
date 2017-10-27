from barnes_hut import Body
import numpy as np

STRUCTURAL_LENGTH = 1.0


def plummer(a):
    """
    Generates a point using CDF for Plummer model
    :param a: structural length
    :return: new Body object with position and velocity based on distribution
    """
    phi = np.random.uniform(0, 2 * np.pi)
    theta = np.arccos(np.random.uniform(-1, 1))
    r = a / np.sqrt(np.random.uniform(0, 1) ** (-2 / 3) - 1)
    v = np.random.uniform(0, 1) * np.sqrt(2.0) * (1.0 + r * r) ** (-0.25)

    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    vx = v * np.sin(theta) * np.cos(phi)
    vy = v * np.sin(theta) * np.sin(phi)
    return Body(x, y, vx, vy)


def n_bodies(n):
    bodies = [plummer(STRUCTURAL_LENGTH) for _ in range(n)]
    return bodies
