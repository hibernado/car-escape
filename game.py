from board import Board
from constants import VEHICLE_SETS, BOARD_SIZE
from euclid.dim2 import Path
from geom import Position
from vehicles import Vehicle
from vehicles import get_vehicle_from_config


def vehicle_off_board(board: Board, vehicle: Vehicle, position):
    # if vehicle.colour == self.red and position.x > max(self.spaces)[0]:
    #     return True
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


class Game:

    def __init__(self, level: int):
        self.board = Board(size=BOARD_SIZE)
        self.vehicles = [get_vehicle_from_config(*v) for v in VEHICLE_SETS[level - 1]]

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
        self.move_vehicle(self.selected_vehicle, new_position)

    def move_vehicle(self, vehicle: Vehicle, new_position: Position):
        if vehicle_not_moving(vehicle, new_position) or \
                invalid_move(vehicle, new_position) or \
                vehicle_off_board(self.board, vehicle, new_position) or \
                path_contains_obstacle(vehicle, self.vehicles, new_position):
            return None
        vehicle.move_to(new_position)
