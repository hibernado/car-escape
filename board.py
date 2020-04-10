from constants import WHITE
from euclid.dim2 import Path
from geom import Square, Position


class Board:

    def __init__(self, vehicles, size, space):
        self.vehicles = vehicles
        self.size = size
        self.space = space

        self.spaces = []
        for i in range(size):
            for j in range(size):
                self.spaces.append((i, j))

        self.background_squares = []

        for loc in self.spaces:
            x, y = loc
            square = Square(space, x, y, .95, .95, WHITE)
            self.background_squares.append(square)

        self.draw()

    def draw(self):
        for square in self.background_squares:
            square.draw()
        for car in self.vehicles:
            squares = []
            for coord in car.coordinates:
                x, y = coord
                squares.append(Square(self.space, x, y, .85, .85, car.colour))
            for square in squares:
                square.draw()

    def add_car(self, car):
        self.vehicles.append(car)

    def vehicle_on_board(self, vehicle, position):
        vob = len(set(vehicle.get_coordinates(position)).intersection(set(self.spaces))) == vehicle.length
        return vob

    def move_vehicle(self, vehicle, new_position):
        if vehicle.location == new_position:
            # vehicle is not moving
            return None
        if not vehicle.valid_move(new_position):
            print('NOT A VALID VEHICLE MOVE !!!')
            return None
        if not self.vehicle_on_board(vehicle, new_position):
            print('CANNOT MOVE VEHICLE OFF BOARD')
            return None
        if not self.path_is_free(vehicle, new_position):
            print('PATH IS NOT FREE')
            return None
        vehicle.move_to(new_position)

    def path_is_free(self, vehicle, new_position):
        current_position = vehicle.location
        print("{}:{}".format(current_position, new_position))

        p = Path(current_position, new_position)
        coords = []
        for p in p.get_vectors():
            coords += vehicle.get_coordinates(p)

        positions = [Position(l[0], l[1], self) for l in coords]
        if any([p.vehicle for p in positions if p.vehicle and p.vehicle != vehicle]):
            return False
        return True

    def get_position(self, x, y):
        return Position(x, y, self)
