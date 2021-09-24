import pygame

import src.utils as utils
import src.Audio as Audio

from src.Objects.RunestoneBoard import RunestoneBoard
from src.Objects.ComboDisplayer import ComboDisplayer
from src.Objects.BackgroundManager import BackgroundManager
from src.Objects.ScoreTimeManager import ScoreTimeManager


import src.States.AbstractState as AbstractState
import src.States.SplashScreen as SplashScreen
import src.States.Quit as Quit


# Initialization state. Only runs once, and immediately switches to the Action state.
class Initialization(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, level: int):
        self._screen = pygame.display.get_surface()
        self._clock = clock

        board = RunestoneBoard()
        combo_display = ComboDisplayer()
        background = BackgroundManager()
        scoretime_manager = ScoreTimeManager(level)

        self._next_state = SplashScreen.SplashScreen( self._clock, board, combo_display, background, scoretime_manager)

        Audio.play_battle_bgm()


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()


    def update(self):
        pass

    @utils.show_fps_if_set
    @utils.draw_mouse
    def render(self):
        pass

    def get_next_state(self):
        return self._next_state

