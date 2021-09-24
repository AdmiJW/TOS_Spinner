import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

import src.utils as utils
import src.Audio as Audio

from src.FontFactory import FontFactory

import src.States.AbstractState as AbstractState
import src.States.MainMenu as MainMenu
import src.States.Initialization as Initialization
import src.States.Quit as Quit

from src.Objects.RunestoneBoard import RunestoneBoard
from src.Objects.ComboDisplayer import ComboDisplayer
from src.Objects.BackgroundManager import BackgroundManager
from src.Objects.ScoreTimeManager import ScoreTimeManager

# Victory/Gameover state, Both actually follows similar pattern.
class Victory_GameOver(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, board: RunestoneBoard, combo_displayer: ComboDisplayer,
                 background: BackgroundManager, scoretime_manager: ScoreTimeManager, is_victory:bool):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self._next_state = self

        self.board = board
        self.combo_displayer = combo_displayer
        self.background = background
        self.scoretime_manager = scoretime_manager

        self.is_victory = is_victory

        # 3 states:
        # 1 - Move the title text down
        # 2 - Show text (score, level, prompt). Note if game over, then on click, next state is main menu immediately
        # 3 - Waiting for input
        # 4 - (Only when Victory) If is victory, fade the white blindfold
        self.state_n = 1

        centerx, centery = self._screen.get_rect().center
        self.centery = centery

        self.white_blindfold = pygame.Surface( (C.SCREEN_WIDTH, C.SCREEN_HEIGHT) )
        self.white_blindfold.fill( C.WHITE )
        self.white_blindfold.set_alpha(0)
        self.black_blindfold = pygame.Surface( (C.SCREEN_WIDTH, C.SCREEN_HEIGHT) )
        self.black_blindfold.fill( C.BLACK )
        self.black_blindfold.set_alpha(0)

        self.title = FontFactory.generate_xl_text('Victory' if self.is_victory else 'Game Over',
                                                  C.YELLOW_1, C.YELLOW_2, ((C.BLACK, 10), (C.WHITE, 5)))
        self.title_rect = self.title.get_rect(bottom=0, centerx=centerx)

        self.title_bg = pygame.Surface( (C.SCREEN_WIDTH, self.title.get_height() - 20))
        self.title_bg.fill( C.BLACK )
        self.title_bg.set_alpha(210)
        self.title_bg_rect = self.title_bg.get_rect(centery=self.title_rect.centery)

        self.level = FontFactory.generate_m_text(f'Level: {self.scoretime_manager.level}',
                                                 C.YELLOW_1, C.YELLOW_2, ((C.BLACK, 4), (C.WHITE, 2)))
        self.level.set_alpha(0)
        self.level_rect = self.level.get_rect(centery=self.centery+120, centerx=centerx)
        self.score = FontFactory.generate_m_text(f'Final Score: {self.scoretime_manager.score}',
                                                 C.YELLOW_1, C.YELLOW_2, ((C.BLACK, 4), (C.WHITE, 2)))
        self.score.set_alpha(0)
        self.score_rect = self.score.get_rect(centery=self.centery+160, centerx=centerx)

        self.prompt = FontFactory.generate_m_text('Click to continue', C.YELLOW_1, C.YELLOW_2,
                                                  ((C.BLACK, 4), (C.WHITE, 2)))
        self.prompt.set_alpha(0)
        self.prompt_rect = self.prompt.get_rect(top=self.centery + 220, centerx=centerx)


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.state_n == 3:
                if self.is_victory:
                    self.state_n = 4
                else:
                    Audio.stop_music()
                    self._next_state = MainMenu.MainMenu(self._clock)


    def update(self):
        dt = self._clock.tick( CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS
        self.background.update()

        # State 1: Lower text
        if self.state_n == 1:
            difference = self.centery - self.title_rect.centery
            self.title_rect.centery += max(2, difference * dt / 15)
            self.title_bg_rect.centery = self.title_rect.centery
            if self.centery - 5 <= self.title_rect.centery <= self.centery + 5:
                self.state_n = 2
        # State 2: Show text
        elif self.state_n == 2:
            self.black_blindfold.set_alpha(160)
            self.level.set_alpha(255)
            self.score.set_alpha(255)
            self.prompt.set_alpha(255)
            self.state_n = 3
        # State 4: Fade to white
        elif self.state_n == 4:
            self.white_blindfold.set_alpha( min(255, self.white_blindfold.get_alpha() + 5) )
            if self.white_blindfold.get_alpha() == 255:
                self._next_state = Initialization.Initialization(self._clock, self.scoretime_manager.level + 1)


    @utils.show_fps_if_set
    @utils.draw_mouse
    def render(self):
        self._screen.fill( C.BLACK )
        self.background.render(self._screen)
        self.board.render( self._screen )
        self.combo_displayer.render( self._screen )
        self.scoretime_manager.render( self._screen )

        self._screen.blit( self.black_blindfold, (0,0) )
        self._screen.blit( self.title_bg, self.title_bg_rect )
        self._screen.blit( self.title, self.title_rect )
        self._screen.blit( self.level, self.level_rect )
        self._screen.blit( self.score, self.score_rect )
        self._screen.blit( self.prompt, self.prompt_rect )
        self._screen.blit( self.white_blindfold, (0,0) )

    def get_next_state(self):
        return self._next_state
