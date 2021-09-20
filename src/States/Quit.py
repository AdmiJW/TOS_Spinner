import sys
import pygame
import src.States.AbstractState as AbstractState

# A Pseudo State that is ran when player quits the game by pressing X or sorts.
class Quit(AbstractState.AbstractState):
    def __init__(self):
        pygame.quit()
        sys.exit()
