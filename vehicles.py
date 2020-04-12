from colour import Colour
from geom import Position


class Vehicle:
    length = None

    def __init__(self, x, y, o, colour: Colour):
        self.selected = False
        self.colour = colour
        self.o = o
        self.position = Position(x, y)

    @property
    def positions(self):
        return self.get_positions(self.position)

    def get_positions(self, position):
        if self.o == 'vertical':
            return set(Position(position.x, position.y + i) for i in range(self.length))
        else:
            return set(Position(position.x + i, position.y) for i in range(self.length))

    def valid_move(self, new_position):
        if self.o == 'vertical':
            return self.position.x == new_position.x
        return self.position.y == new_position.y

    def move_to(self, position):
        self.position = position


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
