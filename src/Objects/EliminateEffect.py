import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

import src.SpriteManager as SpriteManager

# A Elimination Effect Sprite. When runestone are matched 3 or more times, the runestone will be eliminated,
# playing this animation.
class EliminateEffect(pygame.sprite.Sprite):
    def __init__(self, element: C.Element, row: int, col: int):
        super().__init__()
        self.element = element

        self.image = SpriteManager.get_elimination_animation(element, 0)
        self.rect = self.image.get_rect( top=CF.BOARD_OFFSET[1] + row * C.Sprite.ELIM_SIZE_SCALED[1],
                                         left=CF.BOARD_OFFSET[0] + col * C.Sprite.ELIM_SIZE_SCALED[0] )

    # Proceeds a state ahead. State is provided by the EliminateEffectGroup object
    def update(self, state: int):
        self.image = SpriteManager.get_elimination_animation(self.element, state)
