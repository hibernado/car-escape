from colour import Colour
from geom import Position


class Vehicle:
    length = None

    def __init__(self, x, y, o, colour: Colour):
        self.selected = False
        self.colour = colour
        self.o = o
        self.location = Position(x, y)

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


class Car(Vehicle):
    length = 2


class Lorry(Vehicle):
    length = 3


def get_vehicle_from_config(vehicle_type, x, y, orientation, rgb):
    if vehicle_type == 'car':
        return Car(x, y, orientation, Colour(rgb))
    elif vehicle_type == 'lorry':
        return Lorry(x, y, orientation, Colour(rgb))
    else:
        raise Exception('Unknown vehicle_type! {}'.format(vehicle_type))
