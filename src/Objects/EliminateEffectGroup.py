import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

from src.Objects.EliminateEffect import EliminateEffect

# Eliminate Effect Group. Pass in a group of Runestone to be eliminated, and this will generate respective group
# of eliminate effect to it.
class EliminateEffectGroup(pygame.sprite.Group):
    def __init__(self, group: list):
        super().__init__()

        # State = Current animation phase
        # Countdown = How many frames until next state?
        self.state = 0
        self.countdown = CF.ELIMINATE_ANIMATION_SPEED

        # Create EliminateEffect instances
        if len(group):
            element = group[0].element
            for runestone in group:
                self.add( EliminateEffect(element, runestone.row, runestone.col) )

    def update(self, dt):
        self.countdown -= round(dt)
        if self.countdown <= 0:
            self.countdown = CF.ELIMINATE_ANIMATION_SPEED
            self.state += 1

            if self.state < C.Sprite.ELIM_COUNT:
                super().update(self.state)

    def is_expired(self):
        return self.state >= C.Sprite.ELIM_COUNT