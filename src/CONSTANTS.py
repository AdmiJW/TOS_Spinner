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
BROWN_TEXT_1 = (209, 177, 123)
BROWN_TEXT_2 = (130, 84, 8)
YELLOW_1 = (241, 196, 15)
YELLOW_2 = (243, 156, 18)


# Simply an enum for name of elements
class Element(Enum):
    DARK = 0
    FIRE = 1
    HEART = 2
    LIGHT = 3
    WOOD = 4
    WATER = 5


# Font Paths
FONT_BOLD_PATH = path.join('assets', 'font', 'Teko-Bold.ttf')
FONT_LIGHT_PATH = path.join('assets', 'font', 'Teko-Light.ttf')
FONT_MEDIUM_PATH = path.join('assets', 'font', 'Teko-Medium.ttf')
FONT_REGULAR_PATH = path.join('assets', 'font', 'Teko-Regular.ttf')
FONT_SEMIBOLD_PATH = path.join('assets', 'font', 'Teko-SemiBold.ttf')


class Sprite:
    BASE_PATH = path.join('assets', 'img')

    MOUSE_PATH = path.join(BASE_PATH, 'cursor_moveItem.png')

    BACKGROUND_PATH = path.join(BASE_PATH, 'Card_background.png')

    TIME_ICON_PATH = path.join(BASE_PATH, 'clock.png')
    TIME_ICON_SCALED = (32, 32)

    TIME_BAR_PATH = path.join(BASE_PATH, 'timeclip.png')
    TIME_BAR_SCALED = (SCREEN_WIDTH - 30, 16)

    TILE_PATH = path.join(BASE_PATH, 'runestones.png')
    TILE_SIZE = (128, 128)
    TILE_OFFSET = (0, 0)
    TILE_MARGIN = (0, 0)
    TILE_ROWS = 2
    TILE_COLS = 6
    TILE_COUNT = 12
    TILE_SCALE = 0.6
    TILE_SIZE_SCALED = (TILE_SIZE[0] * TILE_SCALE, TILE_SIZE[1] * TILE_SCALE)

    ELIM_PATHS = {
        Element.FIRE: path.join(BASE_PATH, 'fire_elim.png'),
        Element.HEART: path.join(BASE_PATH, 'heart_elim.png'),
        Element.LIGHT: path.join(BASE_PATH, 'light_elim.png'),
        Element.DARK: path.join(BASE_PATH, 'shadow_elim.png'),
        Element.WATER: path.join(BASE_PATH, 'water_elim.png'),
        Element.WOOD: path.join(BASE_PATH, 'wood_elim.png')
    }
    ELIM_SIZE = (64, 64)
    ELIM_OFFSET = (0, 0)
    ELIM_MARGIN = (0, 0)
    ELIM_ROWS = 2
    ELIM_COLS = 5
    ELIM_COUNT = 10
    ELIM_SCALE = TILE_SIZE_SCALED[0] / ELIM_SIZE[0]        # I want it scaled to same size as tiles
    ELIM_SIZE_SCALED = (ELIM_SIZE[0] * ELIM_SCALE, ELIM_SIZE[1] * ELIM_SCALE)
