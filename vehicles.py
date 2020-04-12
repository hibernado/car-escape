from colour import Colour
from geom import Position


class Vehicle:
    length = None

    def __init__(self, position, o, colour: Colour, is_escape_vehicle=False):
        self.selected = False
        self.colour = colour
        self.o = o
        self.position = position
        self.is_escape_vehicle = is_escape_vehicle

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


def get_vehicle_from_config(vehicle_type, x, y, orientation, rgb, escape_car_colour):
    if vehicle_type == 'car':
        vehicle = Car(Position(x, y), orientation, Colour(rgb))
    elif vehicle_type == 'lorry':
        vehicle =  Lorry(Position(x, y), orientation, Colour(rgb))
    else:
        raise Exception('Unknown vehicle_type! {}'.format(vehicle_type))

    if vehicle.colour == escape_car_colour:
        vehicle.is_escape_vehicle = True
    return vehicle
