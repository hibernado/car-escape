import math
from itertools import accumulate

import numpy as np


def get_unit_vector(v):
    return Vector(v.x / v.norm, v.y / v.norm)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def angle(self):
        return np.arctan2(self.y, self.x)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return "({},{})".format(self.x, self.y)


class Path:

    def __init__(self, start, end):
        self.v = end - start
        self.u = get_unit_vector(self.v)
        self.o = start

    def get_vectors(self):
        assert self.v.norm.is_integer()
        displacements = list(accumulate([Vector(0, 0)] + [self.u] * int(self.v.norm)))
        vectors = [d + self.o for d in displacements]
        return vectors
