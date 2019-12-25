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
        # print("map_space {},{} --> {}:{}".format(value1, value2, x, y))
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


class Car:
    length = 2

    def __init__(self, x, y, o, colour):
        self.selected = False
        self.colour = colour
        self.o = o
        self.colour = colour
        self.location = BaseLocation(x, y)

    @property
    def coordinates(self):
        return self.get_coordinates(self.location)

    def valid_move(self, new_position):
        if self.o == 'vertical':
            return self.location.x == new_position.x
        return self.location.y == new_position.y

    def get_coordinates(self, position):
        if self.o == 'vertical':
            return [(position.x, position.y + i) for i in range(self.length)]
        else:
            return [(position.x + i, position.y) for i in range(self.length)]

    def move_to(self, position):
        self.location = position


class Lorry(Car):
    length = 3


class BaseLocation:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def location(self):
        return tuple((self.x, self.y))

    def __repr__(self):
        return "Location {},{}".format(self.x, self.y)


class Position(BaseLocation):
    def __init__(self, x, y, board):
        super().__init__(x, y)
        self.board = board

    @property
    def vehicle(self):
        for vehicle in self.board.vehicles:
            if self.location in vehicle.coordinates:
                return vehicle
        return None


RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (18, 161, 123)
BLUE = (0, 0, 255)
DARKBLUE = (18, 104, 161)
BLACK = (0, 0, 0)
YELLOW = (255, 239, 0)
ORANGE = (255, 162, 0)
PURPLE = (94, 0, 255)
WHITE = (255, 255, 255)

SETS = [[Car(0, 0, 'vertical', ORANGE),
         Lorry(0, 2, 'vertical', PURPLE),
         Car(0, 5, 'horizontal', GREEN),
         Car(1, 3, 'horizontal', RED),
         Lorry(2, 0, 'horizontal', DARKGREEN),
         Lorry(3, 2, 'vertical', DARKBLUE),
         Car(4, 1, 'horizontal', BLUE),
         Lorry(5, 3, 'vertical', YELLOW)]
        ]


class Board:

    def __init__(self, vehicles, size, space):
        self.vehicles = vehicles
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
            for coord in car.coordinates:
                x, y = coord
                squares.append(Square(self.space, x, y, .85, .85, car.colour))
            for square in squares:
                square.draw()

    def add_car(self, car):
        self.vehicles.append(car)

    def vehicle_on_board(self, vehicle, position):
        vob = len(set(vehicle.get_coordinates(position)).intersection(set(self.spaces))) == vehicle.length
        return vob

    #Todo : sometimes the car collide. Please investigate this!
    def vehicles_collide(self, vehicle_a, vehicle_b):
        return set(vehicle_a.coordinates).intersection(set(vehicle_b.coordinates))

    def move_vehicle(self, vehicle, new_position):
        if not vehicle.valid_move(new_position):
            print('NOT A VALID VEHICLE MOVE !!!')
            return None
        if not self.vehicle_on_board(vehicle, new_position):
            print('CANNOT MOVE VEHICLE OFF BOARD')
            return None
        if not self.path_is_free(vehicle, new_position):
            print('PATH IS NOT FREE')
            return None
        vehicle.move_to(new_position)

    def path_is_free(self, vehicle, new_position):
        # todo: refactor this it is ugly!
        x1, y1 = vehicle.coordinates[0]
        x2, y2 = vehicle.get_coordinates(new_position)[0]
        # print("ALT x1 {}, y1 {}, x2 {}, y2 {}".format(x1, y1, x2, y2))
        if x2 >= x1:
            range_func = range(x1, x2 + 1, 1)
        else:
            range_func = range(x1, x2 - 1, -1)

        for x in range_func:
            for car_ in self.vehicles:
                if car_ is not vehicle and self.vehicles_collide(Car(x, y1, vehicle.o, vehicle.colour), car_):
                    return False
        if y2 >= y1:
            range_func = range(y1, y2 + 1, 1)
        else:
            range_func = range(y1, y2 - 1, -1)

        for y in range_func:
            for car_ in self.vehicles:
                if car_ is not vehicle and self.vehicles_collide(Car(x1, y, vehicle.o, vehicle.colour), car_):
                    return False

        return True

    def get_position(self, x, y):
        return Position(x, y, self)


window = pyglet.window.Window(width=300, height=300)
dim1 = DimensionMapping(50, 25)
dim2 = DimensionMapping(50, 25)
space = Space(dim1, dim2)
vehicles = SETS[0]
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
