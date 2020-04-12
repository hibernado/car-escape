from board import Board
from config import Config
from euclid.dim2 import Path
from geom import Position
from vehicles import Vehicle, get_vehicle_from_config


def vehicle_off_board(board: Board, vehicle: Vehicle, position, side='both'):
    if side == 'left' and position.x >= vehicle.position.x:
        return None
    vehicle_on_board = vehicle.get_positions(position).intersection(board.positions) == vehicle.get_positions(position)
    if not vehicle_on_board:
        print('CANNOT MOVE VEHICLE OFF BOARD')
        return True


def path_contains_obstacle(vehicle: Vehicle, vehicles: list, new_position: Position):
    print("{}:{}".format(vehicle.position, new_position))
    positions_in_path = set()
    for p in Path(vehicle.position, new_position).get_vectors():
        positions_in_path = positions_in_path.union(vehicle.get_positions(p))

    positions_filled_by_other_cars = set()
    other_vehicles = [v for v in vehicles if v != vehicle]
    for other_vehicle in other_vehicles:
        positions_filled_by_other_cars = positions_filled_by_other_cars.union(other_vehicle.positions)

    if positions_filled_by_other_cars.intersection(positions_in_path):
        print('PATH IS NOT FREE')
        return True


def invalid_move(vehicle: Vehicle, new_position: Position):
    valid = vehicle.valid_move(new_position)
    if not valid:
        print('NOT A VALID VEHICLE MOVE !!!')
        return True


def vehicle_not_moving(vehicle: Vehicle, new_position: Position):
    if vehicle.position == new_position:
        return True


def is_escape_car(vehicle: Vehicle):
    return vehicle.is_escape_vehicle


class Game:

    def __init__(self, level: int, config: Config):
        self.level = level
        self.config = config
        self.board = Board(self.config.board_size, self.config.board_colour)
        self.vehicles = self._get_vehicles(self.level)

    def _get_vehicles(self, level):
        return [get_vehicle_from_config(*v, self.config.escape_car_colour) for v in self.config.vehicles[level - 1]]

    @property
    def selected_vehicle(self):
        for vehicle in self.vehicles:
            if vehicle.selected:
                return vehicle

    def select_vehicle(self, position: Position):
        for vehicle in self.vehicles:
            if position in vehicle.positions:
                vehicle.selected = True
                print("Vehicle selected @ {}".format(vehicle))

    def deselect_all_vehicles(self):
        for vehicle in self.vehicles:
            vehicle.selected = False

    def update(self, new_position: Position):
        if self.selected_vehicle:
            self.move_vehicle(self.selected_vehicle, new_position)
        if self.level_complete:
            self.level += 1
            self.vehicles = self._get_vehicles(self.level)

    @property
    def level_complete(self):
        for vehicle in self.vehicles:
            if vehicle.is_escape_vehicle:
                return vehicle_off_board(self.board, vehicle, vehicle.position, side='both') or False

    def move_vehicle(self, vehicle: Vehicle, new_position: Position):
        side = 'both'
        if is_escape_car(vehicle):
            side = 'left'
        if vehicle_not_moving(vehicle, new_position) or \
                invalid_move(vehicle, new_position) or \
                vehicle_off_board(self.board, vehicle, new_position, side) or \
                path_contains_obstacle(vehicle, self.vehicles, new_position):
            return None
        vehicle.move_to(new_position)
