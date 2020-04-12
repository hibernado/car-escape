from euclid.dim2 import Path
from geom import Square, Position, Space
from vehicles import Vehicle
from constants import VEHICLE_SETS, BOARD_SIZE
from board import Board
from vehicles import get_vehicle_from_config


def vehicle_on_board(board: Board, vehicle: Vehicle, position):
    # if vehicle.colour == self.red and position.x > max(self.spaces)[0]:
    #     return True
    vob = vehicle.get_positions(position).intersection(board.positions) == vehicle.get_positions(position)
    if not vob:
        print('CANNOT MOVE VEHICLE OFF BOARD')
    return vob


def path_is_free(vehicle: Vehicle, vehicles: list, new_position: Position):
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
        return False
    return True


def valid_move(vehicle: Vehicle, new_position: Position):
    valid = vehicle.valid_move(new_position)
    if not valid:
        print('NOT A VALID VEHICLE MOVE !!!')
    return valid


def vehicle_moving(vehicle: Vehicle, new_position: Position):
    return vehicle.position != new_position


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
        if not vehicle_moving(vehicle, new_position):
            return None
        if not valid_move(vehicle, new_position):
            return None
        if not vehicle_on_board(self.board, vehicle, new_position):
            return None
        if not path_is_free(vehicle, self.vehicles, new_position):
            return None
        vehicle.move_to(new_position)
