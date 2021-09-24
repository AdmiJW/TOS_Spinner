import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

# Background manager. Responsible for the background when in game especially the parallax functionality
class BackgroundManager:
    BACKGROUND_IMG = pygame.image.load( C.Sprite.BACKGROUND_PATH ).convert()
    WIDTH = C.SCREEN_WIDTH
    HEIGHT = CF.BOARD_OFFSET[1]
    LEFTOVER_WIDTH = WIDTH - BACKGROUND_IMG.get_width()
    LEFTOVER_HEIGHT = HEIGHT - BACKGROUND_IMG.get_height()

    def __init__(self):
        super().__init__()
        self.area = BackgroundManager.BACKGROUND_IMG.get_rect(width=BackgroundManager.WIDTH,
                                                              height=BackgroundManager.HEIGHT)

    # Updates the position of render rect to move smoothly when swapped.
    def update(self):
        x, y = pygame.mouse.get_pos()
        target_left = -(x * BackgroundManager.LEFTOVER_WIDTH / C.SCREEN_WIDTH)
        target_top = -(y * BackgroundManager.LEFTOVER_HEIGHT / C.SCREEN_HEIGHT)
        self.area.left += (target_left - self.area.left) / 5
        self.area.top += (target_top - self.area.top) / 5

    # To overwrite the regular draw method
    def render(self, surface: pygame.Surface):
        surface.blit(BackgroundManager.BACKGROUND_IMG, (0,0), self.area)
