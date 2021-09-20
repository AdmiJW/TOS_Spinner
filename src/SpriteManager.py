import pygame

import src.CONSTANTS as C

# Load in the spritesheets
_RUNESTONE_SPRITESHEET = pygame.image.load(C.Sprite.TILE_PATH).convert_alpha()
_RUNESTONE_SPRITESHEET_BRIGHTER = _RUNESTONE_SPRITESHEET.copy()
_RUNESTONE_SPRITESHEET_BRIGHTER.fill( (100,100,100), special_flags=pygame.BLEND_RGB_ADD )


def _retrieve_sprite(sheet: pygame.Surface, sprite_id: int, offset: tuple, size: tuple, margin: tuple, n_rows: int,
                     n_cols: int, is_row_direction=True):
    row = (sprite_id // n_cols) if is_row_direction else (sprite_id % n_rows)
    col = (sprite_id % n_cols) if is_row_direction else (sprite_id // n_rows)
    top_position = offset[1] + row * (margin[1] + size[1])
    left_position = offset[0] + col * (margin[0] + size[0])
    return sheet.subsurface((left_position, top_position, *size))



def get_regular_runestone(element: C.Element, is_highlighted:bool = False):
    target_size = tuple(map(int, (size * C.Sprite.TILE_SCALE for size in C.Sprite.TILE_SIZE)))
    original = _retrieve_sprite(_RUNESTONE_SPRITESHEET_BRIGHTER if is_highlighted else _RUNESTONE_SPRITESHEET,
                                element.value, C.Sprite.TILE_OFFSET, C.Sprite.TILE_SIZE,
                                C.Sprite.TILE_MARGIN, C.Sprite.TILE_ROWS, C.Sprite.TILE_COLS, True)
    return pygame.transform.smoothscale(original, target_size)


def get_powered_runestone(element: C.Element, is_highlighted:bool = False):
    target_size = tuple(map(int, (size * C.Sprite.TILE_SCALE for size in C.Sprite.TILE_SIZE)))
    original = _retrieve_sprite(_RUNESTONE_SPRITESHEET_BRIGHTER if is_highlighted else _RUNESTONE_SPRITESHEET,
                                element.value + C.Sprite.TILE_COUNT // 2,
                                C.Sprite.TILE_OFFSET, C.Sprite.TILE_SIZE, C.Sprite.TILE_MARGIN, C.Sprite.TILE_ROWS,
                                C.Sprite.TILE_COLS, True)
    return pygame.transform.smoothscale(original, target_size)