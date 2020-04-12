import argparse
import sys

import pyglet

from game import Game
from geom import Space, DimensionMapping
from constants import WIDTH, HEIGHT, BOARD_SIZE

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)


@window.event
def on_draw():
    window.clear()
    space.draw(game.board, game.vehicles)


@window.event
def on_mouse_press(dim1, dim2, button, modifiers):
    position = space.map_space(dim1, dim2)
    game.select_vehicle(position)


@window.event
def on_mouse_drag(dim1, dim2, dx, dy, buttons, modifiers):
    position = space.map_space(dim1, dim2)
    game.update(new_position=position)


@window.event
def on_mouse_release(dim1, dim2, button, modifiers):
    game.deselect_all_vehicles()


def handler(level: int):
    global game
    global space

    game = Game(level)
    space = Space(DimensionMapping(WIDTH / game.board.size, WIDTH / game.board.size / 2),
                  DimensionMapping(WIDTH / game.board.size, WIDTH / game.board.size / 2))

    pyglet.app.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', required=True)
    args = parser.parse_args(sys.argv[1:])
    handler(level=int(args.level))


if __name__ == "__main__":
    main()
