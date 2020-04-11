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
     Car(3, 0, 'horizontal', DARKGREY)
     ]
]
