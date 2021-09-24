import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

import src.utils as utils

from src.FontFactory import FontFactory

import src.States.AbstractState as AbstractState
import src.States.Action as Action
import src.States.Quit as Quit

from src.Objects.RunestoneBoard import RunestoneBoard
from src.Objects.ComboDisplayer import ComboDisplayer
from src.Objects.BackgroundManager import BackgroundManager
from src.Objects.ScoreTimeManager import ScoreTimeManager

# SplashScreen state, Showing the level with animation
class SplashScreen(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, board: RunestoneBoard, combo_displayer: ComboDisplayer,
                 background: BackgroundManager, scoretime_manager: ScoreTimeManager):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self._next_state = self

        self.board = board
        self.combo_displayer = combo_displayer
        self.background = background
        self.scoretime_manager = scoretime_manager

        # 3 states:
        # 1 - Blindfold fades to invisible
        # 2 - Title fades down
        # 3 - Prompt text becomes visible
        # 4 - Waiting user input
        self.state_n = 1

        centerx, centery = self._screen.get_rect().center
        self.centery = centery

        self._white_blindfold = pygame.Surface((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        self._white_blindfold.fill(C.WHITE)
        self._white_blindfold.set_alpha(255)

        self._title = FontFactory.generate_xl_text(f'Level {self.scoretime_manager.level}', C.YELLOW_1, C.YELLOW_2,
                                                   ((C.BLACK, 10), (C.WHITE, 5)))
        self._title_rect = self._title.get_rect(bottom=0, centerx=centerx)

        self._title_bg = pygame.Surface((C.SCREEN_WIDTH, self._title.get_height() - 20))
        self._title_bg.fill(C.BLACK)
        self._title_bg.set_alpha(210)
        self._title_bg_rect = self._title_bg.get_rect(centery=self._title_rect.centery)

        self._prompt = FontFactory.generate_m_text('Click to continue', C.YELLOW_1, C.YELLOW_2,
                                                   ((C.BLACK, 4), (C.WHITE, 2)))
        self._prompt.set_alpha(0)
        self._prompt_rect = self._prompt.get_rect(top=self.centery + 100, centerx=centerx)


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.state_n == 4:
                self._next_state = Action.Action(self._clock, self.board, self.combo_displayer, self.background,
                                                 self.scoretime_manager)


    def update(self):
        dt = self._clock.tick( CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS
        self.background.update()

        # State 1: Blindfold alpha decreases
        if self.state_n == 1:
            self._white_blindfold.set_alpha(max(0, self._white_blindfold.get_alpha() - 6))
            if self._white_blindfold.get_alpha() == 0:
                self.state_n = 2
        # State 2: Lower the text
        elif self.state_n == 2:
            difference = self.centery - self._title_rect.centery
            self._title_rect.centery += max(2, difference * dt / 15)
            self._title_bg_rect.centery = self._title_rect.centery
            if self.centery - 5 <= self._title_rect.centery <= self.centery + 5:
                self.state_n = 3
        # State 3: Set text visible.
        else:
            self._prompt.set_alpha(255)
            self.state_n = 4


    @utils.show_fps_if_set
    @utils.draw_mouse
    def render(self):
        self._screen.fill( C.BLACK )
        self.background.render(self._screen)
        self.board.render( self._screen )
        self.combo_displayer.render( self._screen )
        self.scoretime_manager.render( self._screen )

        self._screen.blit(self._white_blindfold, (0, 0))
        self._screen.blit(self._title_bg, self._title_bg_rect)
        self._screen.blit(self._title, self._title_rect)
        self._screen.blit(self._prompt, self._prompt_rect)


    def get_next_state(self):
        return self._next_state
