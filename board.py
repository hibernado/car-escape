from constants import WHITE
from euclid.dim2 import Path
from geom import Square, Position
from vehicles import Vehicle, Colour
from constants import RED


class Board:

    def __init__(self, size, space):
        self.vehicles = []
        self.size = size
        self.space = space
        self.spaces = []
        self.background_squares = []
        self._build_board()
        self.red = Colour(RED)

    def _build_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.spaces.append(Position(i, j))

        for p in self.spaces:
            square = Square(self.space, p.x, p.y, .95, .95, Colour(WHITE))
            self.background_squares.append(square)

    def draw(self):
        for square in self.background_squares:
            square.draw()
        for car in self.vehicles:
            squares = []
            for p in car.positions:
                squares.append(Square(self.space, p.x, p.y, .85, .85, car.colour))
            for square in squares:
                square.draw()

    def add_car(self, car):
        self.vehicles.append(car)

    def vehicle_on_board(self, vehicle: Vehicle, position):
        # if vehicle.colour == self.red and position.x > max(self.spaces)[0]:
        #     return True
        vob = vehicle.get_positions(position).intersection(self.spaces) == vehicle.get_positions(position)
        return vob

    def move_vehicle(self, vehicle: Vehicle, new_position):
        if vehicle.position == new_position:
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

    def path_is_free(self, vehicle, new_position: Position):
        current_position = vehicle.position
        print("{}:{}".format(current_position, new_position))

        p = Path(current_position, new_position)
        positions = []
        for p in p.get_vectors():
            positions += vehicle.get_positions(p)

        for p in positions:
            p.board = self

        if any([p.vehicle for p in positions if p.vehicle and p.vehicle != vehicle]):
            return False
        return True
