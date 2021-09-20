import src.CONSTANTS as C

SHOW_FPS = True
DESIRED_FPS = 60

# Runestone related configuration
RUNESTONE_TWEEN_DIVISOR = 2   # If set to 1, there will be no tweening (animation). Higher value = slower anim

# Board Related Configurations
BOARD_ROWS = 5
BOARD_COLS = 6
BOARD_OFFSET = ((C.SCREEN_WIDTH - C.Sprite.TILE_SIZE_SCALED[0] * BOARD_COLS) // 2,
                C.SCREEN_HEIGHT - C.Sprite.TILE_SIZE_SCALED[1] * BOARD_ROWS - 10)
