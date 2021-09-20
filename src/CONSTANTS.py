import os.path as path
from enum import Enum

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720

# Colors in RGB
BLACK = (1,1,1)
WHITE = (255,255,255)
RED = (255,0,0)
BROWN_1 = (35,19,10)
BROWN_2 = (55,33,16)


# Simply an enum for name of elements
class Element(Enum):
    DARK = 0
    FIRE = 1
    HEART = 2
    LIGHT = 3
    WOOD = 4
    WATER = 5


class Sprite:
    BASE_PATH = path.join('assets', 'img')

    TILE_PATH = path.join(BASE_PATH, 'runestones.png')
    TILE_SIZE = (128, 128)
    TILE_OFFSET = (0, 0)
    TILE_MARGIN = (0, 0)
    TILE_ROWS = 2
    TILE_COLS = 6
    TILE_COUNT = 12
    TILE_SCALE = 0.6
    TILE_SIZE_SCALED = (TILE_SIZE[0] * TILE_SCALE, TILE_SIZE[1] * TILE_SCALE)
