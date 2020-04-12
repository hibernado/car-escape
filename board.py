from constants import WHITE
from geom import Position
from vehicles import Colour


class Board:

    def __init__(self, size):
        self.size = size
        self.positions = []
        self._build_board()
        self.colour = Colour(WHITE)

    def _build_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.positions.append(Position(i, j))

