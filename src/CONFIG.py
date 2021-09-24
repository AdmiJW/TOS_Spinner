import src.CONSTANTS as C

SHOW_FPS = True
USE_CUSTOM_CURSOR = True
DESIRED_FPS = 60

# Runestone related configuration
RUNESTONE_TWEEN_DIVISOR = 2   # If set to 1, there will be no tweening (animation). Higher value = slower movement
RUNESTONE_LINEAR_FALL_SPEED = 15     # Falling runestone speed
RUNESTONE_STABILITY_TOLERANCE = 3

# Elimination Effect related configuration
ELIMINATE_ANIMATION_SPEED = 2           # Unit in frames

# Board Related Configurations
BOARD_ROWS = 5
BOARD_COLS = 6
BOARD_OFFSET = ((C.SCREEN_WIDTH - C.Sprite.TILE_SIZE_SCALED[0] * BOARD_COLS) // 2,
                C.SCREEN_HEIGHT - C.Sprite.TILE_SIZE_SCALED[1] * BOARD_ROWS - 10)

# Text Related
COMBO_FADEOUT_SPEED = 2

# Time allowed for spinning
TIME_LIMIT_IN_SECONDS = 6
TIME_LIMIT_IN_FRAMES = TIME_LIMIT_IN_SECONDS * DESIRED_FPS

# Scoring Related Configuration
BASE_LEVEL_REQ = 4000
LEVEL_INCREMENT = 1000
LEVEL_TIME_LIMIT_IN_SECONDS = 60         # In Seconds
LEVEL_TIME_LIMIT_IN_FRAMES = (LEVEL_TIME_LIMIT_IN_SECONDS + 1) * DESIRED_FPS
SCORE_PER_TILE_ELIM = 25
SCORE_PER_POWERED_ELIM = 75
