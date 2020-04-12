from colour import Colour
from geom import Position


class Board:

    def __init__(self, size: int, colour: Colour):
        self.size = size
        self.positions = []
        self.colour = colour
        self._build_board()

    def _build_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.positions.append(Position(i, j))
