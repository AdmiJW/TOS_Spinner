import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

import src.utils as utils

from src.Objects.RunestoneBoard import RunestoneBoard

import src.States.AbstractState as AbstractState
import src.States.Clearing as Clearing
import src.States.Quit as Quit

# Action state, where the player could be idling or dragging a runestone
class Action(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, board: RunestoneBoard = None):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self._next_state = self

        self.board = RunestoneBoard() if board is None else board


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()
            else:
                if self.board.handle_event(event):
                    self._next_state = Clearing.Clearing(self._clock, self.board)


    def update(self):
        dt = self._clock.tick( CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS
        self.board.update(dt)


    @utils.show_fps_if_set
    def render(self):
        self._screen.fill( C.BLACK )
        self.board.render( self._screen )


    def get_next_state(self):
        return self._next_state

