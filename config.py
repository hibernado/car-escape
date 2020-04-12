from colour import Colour
from constants import BOARD_SIZE, WHITE, VEHICLE_SETS, RED
from constants import WIDTH, HEIGHT


class Config:
    board_size = BOARD_SIZE
    board_colour = Colour(WHITE)
    vehicles = VEHICLE_SETS
    width = WIDTH
    height = HEIGHT
    escape_car_colour = Colour(RED)