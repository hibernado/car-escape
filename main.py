import pyglet

from pyglet.gl import GL_QUADS


class DimensionMapping:
    def __init__(self, vector_array, const):
        self.pa = vector_array
        self.const = const

    def __getitem__(self, index):
        return sum(self.pa[0:index]) + self.const


class Space:
    def __init__(self, dim1, dim2):
        self._dim1 = dim1
        self._dim2 = dim2

    def map_xy(self, x, y):
        return self._dim1[x], self._dim2[y]

    # Todo: mapping board(1,1) -> space(dim1, dim2)
    # is not right. mixed logic between Space and DimensionMapping and Car (see .75*)
    def map_x_vector(self, x):
        if x > 0:
            r = self._dim1[x] - self._dim1[x - 1]
        else:
            r = self._dim1[x]
        return r

    def map_y_vector(self, y):
        if y > 0:
            r = self._dim2[y] - self._dim2[y - 1]
        else:
            r = self._dim2[y]
        return r


class Board:
    def __init__(self, image_path):
        self.image = pyglet.sprite.Sprite(pyglet.image.load(image_path))

    def draw(self):
        self.image.draw()


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


class Car:
    coordinate_count = 4  # Squares have 4 x,y coordinates

    def __init__(self, space, x, y, o, color):
        self.space = space
        self.x = x
        self.y = y
        self.o = o
        # Todo: investigate glColor3f(1, 0, 0)
        self.color = color * self.coordinate_count

    def _coordinates(self, x, y):
        p_a = list(self.space.map_xy(x, y))
        p_b = list(self.space.map_xy(x, y))
        p_c = list(self.space.map_xy(x, y))
        p_d = list(self.space.map_xy(x, y))
        p_b[1] += .75 * self.space.map_y_vector(1)
        p_c[0] += .75 * self.space.map_x_vector(1)
        p_c[1] += .75 * self.space.map_y_vector(1)
        p_d[0] += .75 * self.space.map_x_vector(1)
        return p_a + p_b + p_c + p_d

    @property
    def coordinates(self):

        coords = [self._coordinates(self.x, self.y)]
        if self.o == 'vertical':
            coords.append(self._coordinates(self.x, self.y + 1))
        else:
            coords.append(self._coordinates(self.x + 1, self.y))
        return coords

    # color definition explained here:
    # https://stackoverflow.com/questions/55087102/pyglet-drawing-primitives-with-color
    def draw(self):
        for c in self.coordinates:
            a = pyglet.graphics.vertex_list(4, ('v2f', c), ('c3B', self.color))
            a.draw(GL_QUADS)


window = pyglet.window.Window(width=600, height=600)
board = Board('images/grid.jpg')
dim1 = DimensionMapping([85, 85, 84, 83, 84, 84], 58)
dim2 = DimensionMapping([85, 84, 84, 84, 84, 84], 58)


@window.event
def on_draw():
    window.clear()
    board.draw()
    space = Space(dim1, dim2)
    cars = [
        Car(space, 0, 0, 'vertical', GREEN),
        Car(space, 1, 1, 'horizontal', RED),
        Car(space, 3, 2, 'horizontal', BLUE),
        Car(space, 4, 4, 'vertical', BLACK)
    ]
    for car in cars:
        car.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    print((x, y, button, modifiers))


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    print((x, y, dx, dy, buttons, modifiers))


# @window.event
# def on_key_press(symbol, modifiers):
#     print('A key was pressed')


if __name__ == "__main__":
    pyglet.app.run()
