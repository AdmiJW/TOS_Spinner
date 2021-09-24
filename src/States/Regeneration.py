import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

import src.utils as utils

from src.Objects.RunestoneBoard import RunestoneBoard
from src.Objects.ComboDisplayer import ComboDisplayer
from src.Objects.BackgroundManager import BackgroundManager
from src.Objects.ScoreTimeManager import ScoreTimeManager

import src.States.AbstractState as AbstractState
import src.States.Clearing as Clearing
import src.States.Quit as Quit

# Regeneration State - Runestones cleared should be regenerated. Runestones should fall like gravity affecting them
# - Build a grid off the board.
# - Check each runestone. If the bottom of runestone is unoccupied, make it fall down. (Swap places in grid)
# - Check each column. If the topmost grid is empty, generate a new stone and set location on it.
# - Once all is fallen, return to Clearing state to check if further clearing is required
class Regeneration(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, board: RunestoneBoard, combo_displyer: ComboDisplayer,
                 background: BackgroundManager, scoretime_manager: ScoreTimeManager, ongoing_combo:int,
                 cumulated_score:int, powered_queue:list):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self.board = board
        self.combo_displayer = combo_displyer
        self.background = background
        self._next_state = self
        self.scoretime_manager = scoretime_manager

        self.current_combo = ongoing_combo
        self.cumulated_score = cumulated_score
        self.powered_queue = powered_queue

        # Grid to check
        self.grid = self.board.get_grid_representation()


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()


    def update(self):
        dt = self._clock.tick( CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS
        self.update_gravity()
        self.create_new_runestones()
        self.board.update_linear(dt)
        self.combo_displayer.update(dt, self.current_combo)
        self.background.update()

        # Proceed back to clearing state only when all the stones are stable
        if all( [ stone and stone.is_stable() for row in self.grid for stone in row ] ):
            self._next_state = Clearing.Clearing( self._clock, self.board, self.combo_displayer, self.background,
                                                  self.scoretime_manager, self.current_combo, self.cumulated_score)



    @utils.show_fps_if_set
    @utils.draw_mouse
    def render(self):
        self._screen.fill( C.BLACK )
        self.background.render(self._screen)
        self.board.render( self._screen )
        self.combo_displayer.render( self._screen )
        self.scoretime_manager.render(self._screen)


    def get_next_state(self):
        return self._next_state


    ########################
    # State Specific Methods
    ########################
    # Make all runestone to fall to grid below it
    def update_gravity(self):
        for r in range( CF.BOARD_ROWS - 1 ):
            for c in range( CF.BOARD_COLS ):
                if self.grid[r][c] is None or self.grid[r+1][c] is not None:
                    continue
                self.grid[r][c].move_runestone_to(r+1, c)
                self.grid[r][c], self.grid[r+1][c] = None, self.grid[r][c]


    # Checks for column tops. If top is None, will generate a new runestone
    def create_new_runestones(self):
        for c in range(CF.BOARD_COLS):
            if self.grid[0][c] is None:
                if len(self.powered_queue):
                    stone = self.board.add_new_runestone(0, c, True, self.powered_queue.pop() )
                else:
                    stone = self.board.add_new_runestone(0, c)
                stone.render_rect.move_ip(0, -C.Sprite.TILE_SIZE[1])
                self.grid[0][c] = stone

