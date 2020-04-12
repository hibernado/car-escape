WIDTH = 600
HEIGHT = 600
BOARD_SIZE = 6

RED = (255, 0, 0)
GREEN = (60, 179, 113)
DARKGREEN = (107, 142, 35)
MEDIUMGREEN = (32, 178, 170)
BLUE = (0, 0, 255)
DARKBLUE = (18, 104, 161)
BLACK = (0, 0, 0)
YELLOW = (255, 239, 0)
ORANGE = (255, 162, 0)
PURPLE = (75, 0, 130)
LIGHTPURPLE = (147, 112, 219)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
DARKGREY = (47, 79, 79)

VEHICLE_SETS = [
    [('car', 0, 0, 'vertical', ORANGE),
     ('lorry', 0, 2, 'vertical', PURPLE),
     ('car', 0, 5, 'horizontal', GREEN),
     ('car', 1, 3, 'horizontal', RED),
     ('lorry', 2, 0, 'horizontal', DARKGREEN),
     ('lorry', 3, 2, 'vertical', DARKBLUE),
     ('car', 4, 1, 'horizontal', BLUE),
     ('lorry', 5, 3, 'vertical', YELLOW)],

    [('car', 3, 3, 'vertical', ORANGE),
     ('lorry', 5, 2, 'vertical', LIGHTPURPLE),
     ('car', 4, 1, 'horizontal', PURPLE),
     ('car', 0, 4, 'vertical', GREEN),
     ('car', 0, 3, 'horizontal', RED),
     ('car', 0, 0, 'horizontal', DARKGREEN),
     ('lorry', 0, 2, 'horizontal', DARKBLUE),
     ('car', 4, 2, 'vertical', BLUE),
     ('car', 2, 0, 'vertical', PINK),
     ('lorry', 3, 5, 'horizontal', YELLOW),
     ('car', 3, 0, 'horizontal', DARKGREY)],

    [('car', 1, 3, 'horizontal', RED),
     ('lorry', 3, 1, 'vertical', YELLOW),
     ('car', 1, 0, 'vertical', ORANGE),
     ('car', 1, 2, 'horizontal', GREEN),
     ('lorry', 5, 0, 'vertical', LIGHTPURPLE),
     ('car', 2, 0, 'horizontal', BLUE)],

    [('car', 1, 3, 'horizontal', RED),
     ('lorry', 3, 3, 'vertical', LIGHTPURPLE),
     ('lorry', 0, 3, 'vertical', YELLOW),
     ('car', 2, 1, 'vertical', GREEN),
     ('lorry', 3, 2, 'horizontal', DARKBLUE),
     ('lorry', 2, 0, 'horizontal', DARKGREEN),
     ('car', 5, 0, 'vertical', ORANGE)],

    [('car', 1, 3, 'horizontal', RED),
     ('lorry', 0, 2, 'vertical', LIGHTPURPLE),
     ('car', 0, 5, 'horizontal', GREEN),
     ('lorry', 3, 3, 'vertical', YELLOW),
     ('car', 0, 0, 'vertical', PINK),
     ('lorry', 1, 2, 'horizontal', DARKGREEN),
     ('lorry', 4, 2, 'vertical', BLUE),
     ('car', 5, 2, 'vertical', DARKGREY),
     ('car', 5, 4, 'vertical', ORANGE),
     ('car', 4, 1, 'horizontal', PURPLE),
     ('car', 4, 0, 'horizontal', MEDIUMGREEN)]
]
