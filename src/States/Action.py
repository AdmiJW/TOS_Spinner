import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

import src.utils as utils

import src.States.AbstractState as AbstractState
import src.States.Clearing as Clearing
import src.States.Quit as Quit
import src.States.Victory_GameOver as Victory_GameOver

from src.Objects.RunestoneBoard import RunestoneBoard
from src.Objects.ComboDisplayer import ComboDisplayer
from src.Objects.BackgroundManager import BackgroundManager
from src.Objects.ScoreTimeManager import ScoreTimeManager

# Action state, where the player could be idling or dragging a runestone
class Action(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, board: RunestoneBoard, combo_displayer: ComboDisplayer,
                 background: BackgroundManager, scoretime_manager: ScoreTimeManager):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self._next_state = self

        self.board = board
        self.combo_displayer = combo_displayer
        self.background = background
        self.scoretime_manager = scoretime_manager

        # Time limit for dragging runestones
        self.timer = CF.TIME_LIMIT_IN_FRAMES

        # Check for the score. If passing, then initiate process to go to next level
        if self.scoretime_manager.is_passed():
            self._next_state = Victory_GameOver.Victory_GameOver( self._clock, self.board, self.combo_displayer,
                                                                  self.background, self.scoretime_manager, True )


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()
            else:
                self.board.handle_event(event)


    def update(self):
        dt = self._clock.tick( CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS
        self.board.update(dt)
        self.combo_displayer.update(dt)
        self.background.update()
        self.scoretime_manager.update_time(dt)

        # Level time decremented. Check if time limit is up?
        if self.scoretime_manager.is_failed():
            self._next_state = Victory_GameOver.Victory_GameOver(self._clock, self.board, self.combo_displayer,
                                                                 self.background, self.scoretime_manager, False)

        # Timer decrement
        if self.board.is_swapped:
            self.timer -= dt
            self.board.update_timebar(self.timer)

            if self.timer <= 0: self.board.release_dragged_runestone()


        # Transition to clearing state.
        if self.board.is_swapped and self.board.is_released:
            self.board.reset_internal_state()
            self._next_state = Clearing.Clearing(self._clock, self.board, self.combo_displayer, self.background,
                                                 self.scoretime_manager)


    @utils.show_fps_if_set
    @utils.draw_mouse
    def render(self):
        self._screen.fill( C.BLACK )
        self.background.render(self._screen)
        self.board.render( self._screen )
        self.combo_displayer.render( self._screen )
        self.scoretime_manager.render( self._screen )


    def get_next_state(self):
        return self._next_state
