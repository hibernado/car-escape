import pyglet

from board import Board
from games import games
from geom import Position, DimensionMapping, Space

window = pyglet.window.Window(width=300, height=300)
space = Space(DimensionMapping(50, 25), DimensionMapping(50, 25))
vehicles = games[0]
board = Board(vehicles=vehicles, size=6, space=space)


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


if __name__ == "__main__":
    pyglet.app.run()
