from constants import *
from vehicles import Car, Lorry

vehicle_sets = [
    [Car(0, 0, 'vertical', ORANGE),
     Lorry(0, 2, 'vertical', PURPLE),
     Car(0, 5, 'horizontal', GREEN),
     Car(1, 3, 'horizontal', RED),
     Lorry(2, 0, 'horizontal', DARKGREEN),
     Lorry(3, 2, 'vertical', DARKBLUE),
     Car(4, 1, 'horizontal', BLUE),
     Lorry(5, 3, 'vertical', YELLOW)],

    [Car(3, 3, 'vertical', ORANGE),
     Lorry(5, 2, 'vertical', LIGHTPURPLE),
     Car(4, 1, 'horizontal', PURPLE),
     Car(0, 4, 'vertical', GREEN),
     Car(0, 3, 'horizontal', RED),
     Car(0, 0, 'horizontal', DARKGREEN),
     Lorry(0, 2, 'horizontal', DARKBLUE),
     Car(4, 2, 'vertical', BLUE),
     Car(2, 0, 'vertical', PINK),
     Lorry(3, 5, 'horizontal', YELLOW),
     Car(3, 0, 'horizontal', DARKGREY)],

    [Car(1, 3, 'horizontal', RED),
     Lorry(3, 1, 'vertical', YELLOW),
     Car(1, 0, 'vertical', ORANGE),
     Car(1, 2, 'horizontal', GREEN),
     Lorry(5, 0, 'vertical', LIGHTPURPLE),
     Car(2, 0, 'horizontal', BLUE)],

    [Car(1, 3, 'horizontal', RED),
     Lorry(3, 3, 'vertical', LIGHTPURPLE),
     Lorry(0, 3, 'vertical', YELLOW),
     Car(2, 1, 'vertical', GREEN),
     Lorry(3, 2, 'horizontal', DARKBLUE),
     Lorry(2, 0, 'horizontal', DARKGREEN),
     Car(5, 0, 'vertical', ORANGE)],

    [Car(1, 3, 'horizontal', RED),
     Lorry(0, 2, 'vertical', LIGHTPURPLE),
     Car(0, 5, 'horizontal', GREEN),
     Lorry(3, 3, 'vertical', YELLOW),
     Car(0, 0, 'vertical', PINK),
     Lorry(1, 2, 'horizontal', DARKGREEN),
     Lorry(4, 2, 'vertical', BLUE),
     Car(5, 2, 'vertical', DARKGREY),
     Car(5, 4, 'vertical', ORANGE),
     Car(4, 1, 'horizontal', PURPLE),
     Car(4, 0, 'horizontal', MEDIUMGREEN)]
]
