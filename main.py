import pyglet

from pyglet.gl import GL_QUADS


class DimensionMapping:
    def __init__(self, unit_vector, const):
        self.uv = unit_vector
        self.const = const

    def map_to(self, val):
        return self.const + (self.uv * val)

    def map_from(self, dim_val):
        return (dim_val - self.const) / self.uv


class Space:
    def __init__(self, dim1, dim2):
        self._dim1 = dim1
        self._dim2 = dim2

    def map_space(self, value1, value2):
        x = self._dim1.map_from(value1)
        y = self._dim2.map_from(value2)
        return x, y

    def map_xy(self, x, y):
        return self._dim1.map_to(x), self._dim2.map_to(y)


class Square:
    coordinate_count = 4  # Squares have 4 x,y coordinates

    def __init__(self, space, x, y, w, h, colour):
        self.space = space
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        # Todo: investigate glColor3f(1, 0, 0)
        self.colour = colour * self.coordinate_count

    def _coordinates(self, x, y, w, h):
        p_a = list(self.space.map_xy(x - (w / 2), y - (h / 2)))
        p_b = list(self.space.map_xy(x - (w / 2), y + (h / 2)))
        p_c = list(self.space.map_xy(x + (w / 2), y + (h / 2)))
        p_d = list(self.space.map_xy(x + (w / 2), y - (h / 2)))
        return p_a + p_b + p_c + p_d

    @property
    def coordinates(self):
        coords = [self._coordinates(self._x, self._y, self._w, self._h)]
        return coords

    # color definition explained here:
    # https://stackoverflow.com/questions/55087102/pyglet-drawing-primitives-with-color
    def draw(self):
        for c in self.coordinates:
            a = pyglet.graphics.vertex_list(4, ('v2f', c), ('c3B', self.colour))
            a.draw(GL_QUADS)


class Board:
    def __init__(self, image_path):
        self.image = pyglet.sprite.Sprite(pyglet.image.load(image_path))

    def draw(self):
        self.image.draw()


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Car:
    def __init__(self, space, x, y, o, colour):
        # remove selected from Car class
        self.selected = False
        self.colour = colour
        self.space = space
        self.x = x
        self.y = y
        self.o = o
        self.colour = colour
        self.xy_coords = []
        self.squares = []
        self.move_to(self.x, self.y)

    def valid_move(self, x, y):
        if self.o == 'vertical':
            return x == self.x
        return y == self.y

    def move_to(self, x, y):
        if not self.valid_move(x, y):
            print('{}.{} -> {}.{} Not Allowed!!!'.format(self.x, self.y, x, y))
            return None
        self.xy_coords = [(x, y)]
        if self.o == 'vertical':
            self.xy_coords.append((x, y + 1))
        else:
            self.xy_coords.append((x + 1, y))

        self.squares = []
        for coord in self.xy_coords:
            x, y = coord
            self.squares.append(Square(self.space, x, y, .85, .85, self.colour))

    def draw(self):
        for square in self.squares:
            square.draw()


window = pyglet.window.Window(width=600, height=600)
board = Board('images/grid.jpg')
dim1 = DimensionMapping(100, 50)
dim2 = DimensionMapping(100, 50)
space = Space(dim1, dim2)
cars = [Car(space, 1, 1, 'horizontal', BLACK),
        Car(space, 3, 1, 'vertical', BLUE),
        Car(space, 1, 3, 'vertical', GREEN),
        Car(space, 3, 3, 'horizontal', RED)]


@window.event
def on_draw():
    window.clear()
    # board.draw()
    for i in range(7):
        for j in range(7):
            Square(space, i, j, .95, .95, WHITE).draw()
    for car in cars:
        car.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    loc = tuple(round(val) for val in space.map_space(x, y))
    for car in cars:
        if loc in car.xy_coords:
            car.selected = True


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    x_, y_ = tuple(round(val) for val in space.map_space(x, y))
    for car in cars:
        if car.selected:
            car.move_to(x_, y_)


@window.event
def on_mouse_release(x, y, button, modifiers):
    for car in cars:
        if car.selected:
            car.selected = False


# @window.event
# def on_key_press(symbol, modifiers):
#     print('A key was pressed')


if __name__ == "__main__":
    pyglet.app.run()
