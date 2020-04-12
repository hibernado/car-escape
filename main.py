import argparse
import sys

import pyglet

from game import Game
from geom import Space, DimensionMapping
from config import Config

window = pyglet.window.Window(width=Config.width,
                              height=Config.height)

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

    game = Game(level, Config)
    space = Space(DimensionMapping(Config.width / game.board.size, Config.width / game.board.size / 2),
                  DimensionMapping(Config.width / game.board.size, Config.width / game.board.size / 2))

    pyglet.app.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', required=True)
    args = parser.parse_args(sys.argv[1:])
    handler(level=int(args.level))


if __name__ == "__main__":
    main()
