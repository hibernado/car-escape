from geom import BaseLocation


class Car:
    length = 2

    def __init__(self, x, y, o, colour):
        self.selected = False
        self.colour = colour
        self.o = o
        self.colour = colour
        self.location = BaseLocation(x, y)

    @property
    def coordinates(self):
        return self.get_coordinates(self.location)

    def valid_move(self, new_position):
        if self.o == 'vertical':
            return self.location.x == new_position.x
        return self.location.y == new_position.y

    def get_coordinates(self, position):
        if self.o == 'vertical':
            return [(position.x, position.y + i) for i in range(self.length)]
        else:
            return [(position.x + i, position.y) for i in range(self.length)]

    def move_to(self, position):
        self.location = position


class Lorry(Car):
    length = 3
