import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

import src.utils as utils
import src.Audio as Audio

from src.Objects.RunestoneBoard import RunestoneBoard
from src.Objects.EliminateEffectGroup import EliminateEffectGroup
from src.Objects.ComboDisplayer import ComboDisplayer
from src.Objects.BackgroundManager import BackgroundManager
from src.Objects.ScoreTimeManager import ScoreTimeManager

import src.States.AbstractState as AbstractState
import src.States.Action as Action
import src.States.Regeneration as Regeneration
import src.States.Quit as Quit

# Clearing state, where the board is checked for matches, and clears it.
# ====================================
# 1. Init
# - A 2D matrix board is constructed.
# - Every runestone in the board is evaluated - Whether it should be eliminated or not
# - Perform DFS on the tokens to find a potential area of runestone to remove. Filter those who does not need to be
#   eliminated as in above step.
# - If in this DFS group there is runestones to be eliminated, add to be animated later
# ====================================
# 2. Loop
# - While we still have eliminations to animate, continue.
class Clearing(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, board: RunestoneBoard, combo_displayer: ComboDisplayer,
                 background: BackgroundManager, scoretime_manager: ScoreTimeManager, ongoing_combo:int = 0,
                 cumulated_score:int = 0):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self.board = board
        self.combo_displayer = combo_displayer
        self.background = background
        self.scoretime_manager = scoretime_manager
        self._next_state = self

        self.current_combo = ongoing_combo
        self.cumulated_score = cumulated_score
        self.powered_queue = []             # A list of powered runestones we should generate in Regeneration state

        self.eliminate_grps = self._get_matches()
        self.eliminate_index = 0
        if not len(self.eliminate_grps):
            self.effect_group = EliminateEffectGroup( [] )    # Use empty list as placeholder, kinda like Null pattern
        else:
            # Update first combo
            to_elim = self.eliminate_grps[self.eliminate_index]
            score = sum(CF.SCORE_PER_POWERED_ELIM if stone.is_powered else CF.SCORE_PER_TILE_ELIM for stone in to_elim)

            if len(to_elim) >= 5:
                self.powered_queue.append( to_elim[0].element )
            self.current_combo += 1
            self.scoretime_manager.update_score( score )
            self.cumulated_score += score
            self.board.remove( *to_elim )
            self.effect_group = EliminateEffectGroup( to_elim )
            Audio.play_combo(self.current_combo, len(to_elim) )



    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()


    def update(self):
        dt = self._clock.tick( CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS
        self.board.update(dt)
        self.effect_group.update(dt)
        self.background.update()

        if self.effect_group.is_expired():
            self.eliminate_index += 1
            if self.eliminate_index >= len( self.eliminate_grps ):
                # We've eliminated some stones, and we should regenerate with new stones.
                if len(self.eliminate_grps):
                    self._next_state = Regeneration.Regeneration(self._clock, self.board, self.combo_displayer,
                                                                 self.background, self.scoretime_manager,
                                                                 self.current_combo, self.cumulated_score,
                                                                 self.powered_queue)
                # If it initially has no stones to eliminate to begin with, go back Action.
                # Don't forget to take combo bonus into account
                else:
                    self.scoretime_manager.update_score( int(self.cumulated_score * self.current_combo * 0.5) )
                    self._next_state = Action.Action(self._clock, self.board, self.combo_displayer, self.background,
                                                     self.scoretime_manager)
                    # Sound
                    Audio.play_charging()
            else:
                # Another combo.
                to_elim = self.eliminate_grps[self.eliminate_index]
                score = sum(CF.SCORE_PER_POWERED_ELIM if stone.is_powered else CF.SCORE_PER_TILE_ELIM
                            for stone in to_elim)

                if len(to_elim) >= 5:
                    self.powered_queue.append(to_elim[0].element)
                self.current_combo += 1
                self.scoretime_manager.update_score( score )
                self.cumulated_score += score
                self.board.remove( *to_elim )
                self.effect_group = EliminateEffectGroup( to_elim )
                Audio.play_combo(self.current_combo, len(to_elim) )

        self.combo_displayer.update(dt, self.current_combo)


    @utils.show_fps_if_set
    @utils.draw_mouse
    def render(self):
        self._screen.fill( C.BLACK )
        self.background.render(self._screen)
        self.board.render( self._screen )
        self.effect_group.draw(self._screen)
        self.combo_displayer.render( self._screen )
        self.scoretime_manager.render(self._screen)


    def get_next_state(self):
        return self._next_state


    ##########################
    # State Specific methods
    ##########################
    # get_matches will return a list of groups that are supposed to be eliminated.
    def _get_matches(self):
        should_eliminate = [ [False] * CF.BOARD_COLS for _ in range(CF.BOARD_ROWS) ]
        visited = [ [False] * CF.BOARD_COLS for _ in range(CF.BOARD_ROWS) ]
        matches = []

        # Step 1: Gridify the board for easier checking.
        grid = self.board.get_grid_representation()

        # Step 2: Row Check. Size 3+ only
        for r in range( CF.BOARD_ROWS ):
            for c in range( CF.BOARD_COLS - 2 ):
                if grid[r][c].element == grid[r][c+1].element == grid[r][c+2].element:
                    should_eliminate[r][c] = should_eliminate[r][c+1] = should_eliminate[r][c+2] = True

        # Step 3: Column check. Size 3+ only.
        for c in range( CF.BOARD_COLS ):
            for r in range( CF.BOARD_ROWS - 2 ):
                if grid[r][c].element == grid[r+1][c].element == grid[r+2][c].element:
                    should_eliminate[r][c] = should_eliminate[r+1][c] = should_eliminate[r+2][c] = True

        # Step 4: DFS on each of those runestones (Only if never visited)
        for r in range(CF.BOARD_ROWS):
            for c in range(CF.BOARD_COLS):
                if visited[r][c]: continue
                group_elems = []
                Clearing._dfs(r,c,grid,grid[r][c].element,visited,group_elems)

                # Step 4.1: Filter group_elems according to should_eliminate
                group_elems = list(filter( lambda e: should_eliminate[e.row][e.col], group_elems ))

                # Step 4.2: If not empty, append to the list of groups to eliminate
                if len( group_elems ):
                    matches.append( group_elems )

        return matches



    # Perform dfs to obtain a group of touching runestones
    @staticmethod
    def _dfs(row, col, grid, element, visited, result):
        # Base cases - Do not search this grid
        if row < 0 or row >= CF.BOARD_ROWS or col < 0 or col >= CF.BOARD_COLS or visited[row][col] \
                or grid[row][col].element != element:
            return

        visited[row][col] = True
        result.append(grid[row][col])
        # Recursion
        Clearing._dfs(row + 1, col, grid, element, visited, result)
        Clearing._dfs(row - 1, col, grid, element, visited, result)
        Clearing._dfs(row, col + 1, grid, element, visited, result)
        Clearing._dfs(row, col - 1, grid, element, visited, result)










