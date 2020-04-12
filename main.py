import argparse
import sys

import pyglet

from board import Board
from constants import WIDTH, HEIGHT, BOARD_SIZE, VEHICLE_SETS
from geom import DimensionMapping, Space
from vehicles import get_vehicle_from_config

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)


@window.event
def on_draw():
    window.clear()
    board.draw()


@window.event
def on_mouse_press(dim1, dim2, button, modifiers):
    position = space.map_space(dim1, dim2)
    position.board = board
    if position.vehicle:
        position.vehicle.selected = True
        print("Vehicle selected @{}".format(position.vehicle))


@window.event
def on_mouse_drag(dim1, dim2, dx, dy, buttons, modifiers):
    position = space.map_space(dim1, dim2)
    position.board = board
    for vehicle in vehicles:
        if vehicle.selected:
            board.move_vehicle(vehicle, new_position=position)


@window.event
def on_mouse_release(dim1, dim2, button, modifiers):
    for vehicle in vehicles:
        if vehicle.selected:
            vehicle.selected = False


def handler(level: int):
    global vehicles
    global board
    global space

    space = Space(DimensionMapping(WIDTH / BOARD_SIZE, WIDTH / BOARD_SIZE / 2),
                  DimensionMapping(WIDTH / BOARD_SIZE, WIDTH / BOARD_SIZE / 2))
    board = Board(size=BOARD_SIZE, space=space)
    vehicles = [get_vehicle_from_config(*v) for v in VEHICLE_SETS[level - 1]]
    board.vehicles = vehicles
    pyglet.app.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', required=True)
    args = parser.parse_args(sys.argv[1:])
    handler(level=int(args.level))


if __name__ == "__main__":
    main()
