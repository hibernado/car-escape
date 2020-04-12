import pyglet
from pyglet.gl import GL_QUADS

from colour import Colour
from euclid.dim2 import Vector


class Position(Vector):
    def __init__(self, x, y, board=None):
        super().__init__(x, y)
        self.board = board

    @property
    def location(self):
        return tuple((self.x, self.y))

    @property
    def vehicle(self):
        for vehicle in self.board.vehicles:
            if self.location in vehicle.coordinates:
                return vehicle
        return None

    def __repr__(self):
        return "Position {},{}".format(self.x, self.y)

class DimensionMapping:
    def __init__(self, unit_vector, const):
        self.uv = unit_vector
        self.const = const

    def map_to(self, val):
        return self.const + (self.uv * val)

    def map_from(self, dim_val):
        return (dim_val - self.const) / self.uv


class Space:
    def __init__(self, dim1, dim2):
        self._dim1 = dim1
        self._dim2 = dim2

    def map_space(self, value1, value2):
        x = round(self._dim1.map_from(value1))
        y = round(self._dim2.map_from(value2))
        # print("map_space {},{} --> {}:{}".format(value1, value2, x, y))
        return Position(x, y)

    def map_xy(self, position: Position):
        return self._dim1.map_to(position.x), self._dim2.map_to(position.y)


class Square:
    coordinate_count = 4  # Squares have 4 x,y coordinates

    def __init__(self, space, x, y, w, h, colour: Colour):
        self.space = space
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        # Todo: investigate glColor3f(1, 0, 0)
        self.colour = colour.rgb * self.coordinate_count

    @property
    def coordinates(self):

        p_a = Position(x=self._x - (self._w / 2), y=self._y - (self._h / 2))
        p_b = Position(x=self._x - (self._w / 2), y=self._y + (self._h / 2))
        p_c = Position(x=self._x + (self._w / 2), y=self._y + (self._h / 2))
        p_d = Position(x=self._x + (self._w / 2), y=self._y - (self._h / 2))

        r = []
        for p in [p_a, p_b, p_c, p_d]:
            r += self.space.map_xy(p)

        return [r]

    # color definition explained here:
    # https://stackoverflow.com/questions/55087102/pyglet-drawing-primitives-with-color
    def draw(self):
        for c in self.coordinates:
            a = pyglet.graphics.vertex_list(4, ('v2f', c), ('c3B', self.colour))
            a.draw(GL_QUADS)
