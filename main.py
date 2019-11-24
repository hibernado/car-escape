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


class Car:

    def __init__(self, space, x, y, o):
        self.space = space
        self.x = x
        self.y = y
        self.o = o

    @property
    def coordinates(self):
        p_a = list(self.space.map_xy(self.x, self.y))
        p_b = list(self.space.map_xy(self.x, self.y))
        p_c = list(self.space.map_xy(self.x, self.y))
        p_d = list(self.space.map_xy(self.x, self.y))
        p_b[1] += .75 * self.space.map_y_vector(1)
        p_c[0] += .75 * self.space.map_x_vector(1)
        p_c[1] += .75 * self.space.map_y_vector(1)
        p_d[0] += .75 * self.space.map_x_vector(1)
        print(p_a + p_b + p_c + p_d)
        return p_a + p_b + p_c + p_d

    @property
    def color(self):
        #     glColor3f(1, 0, 0)
        coordinate_count = 4  # Square
        return (255, 0, 0) * coordinate_count

    # color definition explained here:
    # https://stackoverflow.com/questions/55087102/pyglet-drawing-primitives-with-color
    def draw(self):
        a = pyglet.graphics.vertex_list(4, ('v2f', self.coordinates), ('c3B', self.color))
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
    car = Car(space, 0, 0, 'vertical')
    car.draw()

# @window.event
# def on_key_press(symbol, modifiers):
#     print('A key was pressed')


if __name__ == "__main__":
    pyglet.app.run()
