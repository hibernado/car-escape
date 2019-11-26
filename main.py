import pyglet

from pyglet.gl import GL_QUADS

car_in_hand = None


class DimensionMapping:
    def __init__(self, unit_vector, const):
        self.uv = unit_vector
        self.const = const

    def get(self, val):
        return self.const + (self.uv * val)


class Space:
    def __init__(self, dim1, dim2):
        self._dim1 = dim1
        self._dim2 = dim2

    def space_to_xy(self, value1, value2):
        x = round( (value1-5) / 100)
        y = round( (value2-5) / 100)
        return x, y

    def map_xy(self, x, y):
        return self._dim1.get(x), self._dim2.get(y)

    # Todo: mapping board(1,1) -> space(dim1, dim2)
    # is not right. mixed logic between Space and DimensionMapping and Car (see .75*)
    # mapping is not working correctly !!!
    def map_x_vector(self, x):
        return self._dim1.get(x)

    def map_y_vector(self, y):
        return self._dim2.get(y)


class Square:
    coordinate_count = 4  # Squares have 4 x,y coordinates

    def __init__(self, space, x, y, w, h, color, border=None):
        self.space = space
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        # Todo: investigate glColor3f(1, 0, 0)
        self.color = color * self.coordinate_count

    def _coordinates(self, x, y, w, h):
        p_a = list(self.space.map_xy(x, y))
        p_b = list(self.space.map_xy(x, y + h))
        p_c = list(self.space.map_xy(x + w, y + h))
        p_d = list(self.space.map_xy(x + w, y))
        return p_a + p_b + p_c + p_d

    @property
    def coordinates(self):
        coords = [self._coordinates(self._x, self._y, self._w, self._h)]
        return coords

    # color definition explained here:
    # https://stackoverflow.com/questions/55087102/pyglet-drawing-primitives-with-color
    def draw(self):
        for c in self.coordinates:
            a = pyglet.graphics.vertex_list(4, ('v2f', c), ('c3B', self.color))
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
    coordinate_count = 4  # Squares have 4 x,y coordinates

    def __init__(self, space, x, y, o, color):
        # self.space = space
        # self.x = x
        # self.y = y
        # self.o = o
        # # Todo: investigate glColor3f(1, 0, 0)
        # self.color = color * self.coordinate_count
        if o == 'vertical':
            self.square = Square(space, x, y, 1, 2, color)
        else:
            self.square = Square(space, x, y, 2, 1, color)

    # def _coordinates(self, x, y):
    #     p_a = list(self.space.map_xy(x, y))
    #     p_b = list(self.space.map_xy(x, y))
    #     p_c = list(self.space.map_xy(x, y))
    #     p_d = list(self.space.map_xy(x, y))
    #     p_b[1] += .75 * self.space.map_y_vector(1)
    #     p_c[0] += .75 * self.space.map_x_vector(1)
    #     p_c[1] += .75 * self.space.map_y_vector(1)
    #     p_d[0] += .75 * self.space.map_x_vector(1)
    #     return p_a + p_b + p_c + p_d
    #
    # @property
    # def coordinates(self):
    #
    #     coords = [self._coordinates(self.x, self.y)]
    #     if self.o == 'vertical':
    #         coords.append(self._coordinates(self.x, self.y + 1))
    #     else:
    #         coords.append(self._coordinates(self.x + 1, self.y))
    #     return coords
    #
    # # color definition explained here:
    # # https://stackoverflow.com/questions/55087102/pyglet-drawing-primitives-with-color
    def draw(self):
        self.square.draw()
        # for c in self.coordinates:
        #     a = pyglet.graphics.vertex_list(4, ('v2f', c), ('c3B', self.color))
        #     a.draw(GL_QUADS)


window = pyglet.window.Window(width=600, height=600)
board = Board('images/grid.jpg')
dim1 = DimensionMapping(100, 5)
dim2 = DimensionMapping(100, 5)
space = Space(dim1, dim2)
cars = {  # (0, 0): Car(space, 0, 0, 'vertical', GREEN),
    # (1, 1): Car(space, 1, 1, 'horizontal', RED),
    # (3, 2): Car(space, 3, 2, 'horizontal', BLUE),
    (2, 1): Car(space, 2, 1, 'horizontal', BLACK)
}


@window.event
def on_draw():
    window.clear()
    # board.draw()
    for i in range(7):
        for j in range(7):
            Square(space, i, j, .9, .9, WHITE).draw()
    for loc, car in cars.items():
        car.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    global car_in_hand
    # button == mouse.LEFT
    loc = tuple(space.space_to_xy(x, y))
    print((x, y, loc))
    car = cars[loc]
    print(car.color)

    car_in_hand = car


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    print((x, y, dx, dy, buttons, modifiers))
    x_, y_ = space.space_to_xy(x, y)
    if car_in_hand:
        car_in_hand.x = x_
        car_in_hand.y = y_
        print('draw!')
        car_in_hand.draw()


@window.event
def on_mouse_release(x, y, button, modifiers):
    global car_in_hand
    if car_in_hand:
        car_in_hand = None


# @window.event
# def on_key_press(symbol, modifiers):
#     print('A key was pressed')


if __name__ == "__main__":
    pyglet.app.run()
