import pyglet

from board import Board
from constants import WIDTH, HEIGHT, BOARD_SIZE
from data import games
from geom import Position, DimensionMapping, Space

window = pyglet.window.Window(width=WIDTH, height=HEIGHT)


@window.event
def on_draw():
    window.clear()
    board.draw()


@window.event
def on_mouse_press(dim1, dim2, button, modifiers):
    x, y = space.map_space(dim1, dim2)
    position = Position(x, y, board)
    if position.vehicle:
        position.vehicle.selected = True
        print("Vehicle selected @{}".format(position.vehicle.coordinates))


@window.event
def on_mouse_drag(dim1, dim2, dx, dy, buttons, modifiers):
    x, y = space.map_space(dim1, dim2)
    position = Position(x, y, board)
    for vehicle in vehicles:
        if vehicle.selected:
            board.move_vehicle(vehicle, new_position=position)


@window.event
def on_mouse_release(dim1, dim2, button, modifiers):
    for vehicle in vehicles:
        if vehicle.selected:
            vehicle.selected = False


def main():
    global vehicles
    global board
    global space

    space = Space(DimensionMapping(WIDTH / BOARD_SIZE, WIDTH / BOARD_SIZE / 2),
                  DimensionMapping(WIDTH / BOARD_SIZE, WIDTH / BOARD_SIZE / 2))
    board = Board(size=BOARD_SIZE, space=space)
    vehicles = games[0]
    board.vehicles = vehicles
    pyglet.app.run()


if __name__ == "__main__":
    main()
