import pygame
pygame.init()       # Initialize the pygame before import any other module

import src.CONSTANTS as C

# Sets the screen mode here.
pygame.display.set_mode( (C.SCREEN_WIDTH, C.SCREEN_HEIGHT), pygame.SCALED )
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# Importing Game related stuff
import src.States.MainMenu as MainMenu

# Singleton Game instance. The game loop resides here.
# A Game instance is a state machine. In each game loop, the state's
# - handle_input()
# - update()
# - render()
# - get_next_state()
# will be called.
class Game:
    def __init__(self):
        self._state = MainMenu.MainMenu(clock)

    def run(self):
        while self._state is not None:
            self._state.handle_input()
            self._state.update()
            self._state.render()
            pygame.display.flip()
            self._state = self._state.get_next_state()
