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
        x = round(self._dim1.map_from(value1))
        y = round(self._dim2.map_from(value2))
        print("map_space {},{} --> {}:{}".format(value1, value2, x, y))
        return tuple((x, y))

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


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Car:
    length = 2

    def __init__(self, x, y, o, colour):
        self.selected = False
        self.colour = colour
        self.x = x
        self.y = y
        self.o = o
        self.colour = colour
        self.xy_coords = []
        self.squares = []
        self.move_to(BaseLocation(x, y))

    def valid_move(self, new_position):
        if self.o == 'vertical':
            return self.x == new_position.x
        return self.y == new_position.y

    # todo: merge with get_coords
    def get_new_position(self, x, y):
        print("Current position: {}".format(self.xy_coords))
        xy_coords = [(x, y)]
        if self.o == 'vertical':
            xy_coords.append((x, y + 1))
        else:
            xy_coords.append((x + 1, y))
        print("New position: {}".format(xy_coords))
        return xy_coords

    def get_coords(self, position):
        return self.get_new_position(position.x, position.y)

    def move_to(self, position):
        self.xy_coords = self.get_coords(position)
        self.x, self.y = self.xy_coords[0]


class Board:

    def __init__(self, cars, size, space):
        self.vehicles = cars
        self.size = size
        self.space = space

        self.spaces = []
        for i in range(size):
            for j in range(size):
                self.spaces.append((i, j))

        self.background_squares = []

        for loc in self.spaces:
            x, y = loc
            square = Square(space, x, y, .95, .95, WHITE)
            self.background_squares.append(square)

        self.draw()

    def draw(self):
        for square in self.background_squares:
            square.draw()
        for car in self.vehicles:
            squares = []
            for coord in car.xy_coords:
                x, y = coord
                squares.append(Square(self.space, x, y, .85, .85, car.colour))
            for square in squares:
                square.draw()


    def add_car(self, car):
        self.vehicles.append(car)

    def vehicle_on_board(self, vehicle, position):
        vob = len(set(vehicle.get_coords(position)).intersection(set(self.spaces))) == vehicle.length
        print('VOB: {}'.format(vehicle.get_coords(position)))
        return vob

    def move_vehicle(self, vehicle, new_position):
        if not vehicle.valid_move(new_position):
            print('NOT VALID VEHICLE MOVE !!!')
            return None
        if not self.vehicle_on_board(vehicle, new_position):
            print('CANNOT MOVE VEHICLE OFF BOARD')
            return None
        if not self.path_is_free(vehicle, vehicle.x, vehicle.y, new_position.x, new_position.y):
            print('PATH IS NOT FREE')
            return None
        vehicle.move_to(new_position)

    def path_is_free(self, car, x1, y1, x2, y2):
        print("x1 {}, y1 {}, x2 {}, y2 {}".format(x1, y1, x2, y2))
        # Todo: Needs refactoring!!! Ugly
        if x2 >= x1:
            range_func = range(x1, x2 + 1, 1)
        else:
            range_func = range(x1, x2 - 1, -1)

        for x in range_func:
            for car_ in self.vehicles:
                if car_ is not car and set(car.get_new_position(x, y1)).intersection(set(car_.xy_coords)):
                    return False
        if y2 >= y1:
            range_func = range(y1, y2 + 1, 1)
        else:
            range_func = range(y1, y2 - 1, -1)

        for y in range_func:
            for car_ in self.vehicles:
                if car_ is not car and set(car.get_new_position(x1, y)).intersection(set(car_.xy_coords)):
                    return False

        return True

    def get_position(self, x, y):
        return Position(x, y, self)


class BaseLocation:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def location(self):
        return tuple((self.x, self.y))


class Position(BaseLocation):
    def __init__(self, x, y, board):
        super().__init__(x, y)
        self.board = board

    @property
    def vehicle(self):
        for vehicle in self.board.vehicles:
            if self.location in vehicle.xy_coords:
                return vehicle
        return None


window = pyglet.window.Window(width=600, height=600)
dim1 = DimensionMapping(100, 50)
dim2 = DimensionMapping(100, 50)
space = Space(dim1, dim2)
cars = [Car(space, 1, 1, 'horizontal', BLACK),
        Car(space, 3, 1, 'vertical', BLUE),
        Car(space, 1, 3, 'vertical', GREEN),
        Car(space, 3, 3, 'horizontal', RED)]
board = Board(cars=cars, size=6, space=space)


@window.event
def on_draw():
    window.clear()
    board.draw()


@window.event
def on_mouse_press(dim1, dim2, button, modifiers):
    x, y = space.map_space(dim1, dim2)
    position = board.get_position(x, y)
    if position.vehicle:
        position.vehicle.selected = True
        print("Vehicle selected @{}".format(position.vehicle.xy_coords))


@window.event
def on_mouse_drag(dim1, dim2, dx, dy, buttons, modifiers):
    x, y = space.map_space(dim1, dim2)
    position = board.get_position(x, y)
    for car in cars:
        if car.selected:
            board.move_vehicle(car, new_position=position)


@window.event
def on_mouse_release(dim1, dim2, button, modifiers):
    for car in cars:
        if car.selected:
            car.selected = False


# @window.event
# def on_key_press(symbol, modifiers):
#     print('A key was pressed')


if __name__ == "__main__":
    pyglet.app.run()
