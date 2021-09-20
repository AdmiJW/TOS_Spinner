import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

import src.utils as utils

from src.Objects.RunestoneBoard import RunestoneBoard

import src.States.AbstractState as AbstractState
import src.States.Action as Action
import src.States.Quit as Quit

# Clearing state, where the board is checked for matches, and clears it.
# ====================================
# 1. Init
# - A 2D matrix board is constructed.
# - Using Disjoint Set, rows and columns are checked (Size 3+)
# - At the end, find disjoint sets that have at least size 3. These are the runestones we need to eliminate.
# - Our state will have a 'eliminating' attribute, which represents the group currently being 'eliminated' with
#   animation
# ====================================
# 2. Loop
# - While we still have eliminations to animate, continue.
class Clearing(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock, board: RunestoneBoard):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self.board = board
        self._next_state = Action.Action(self._clock, self.board)

        for r in self._get_matches():
            for e in r: print(f"({e.row}, {e.col})", end="\t")
            print("")



    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()


    def update(self):
        dt = self._clock.tick( CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS
        self.board.update(dt)


    @utils.show_fps_if_set
    def render(self):
        self._screen.fill( C.BLACK )
        self.board.render( self._screen )


    def get_next_state(self):
        return self._next_state


    ##########################
    # State Specific methods
    ##########################
    # get_matches will return a list of groups that are supposed to be eliminated.
    def _get_matches(self):
        # Step 1: Gridify the board for easier checking. Also initilaize the disjoint set
        grid = [ [None] * CF.BOARD_COLS for i in range(CF.BOARD_ROWS) ]
        ds = utils.DisjointSet( self.board )
        for runestone in self.board:
            grid[runestone.row][runestone.col] = runestone

        # Step 2: Row Check. Size 3+ only
        for r in range( CF.BOARD_ROWS ):
            i, size = 1, 1
            while i < CF.BOARD_COLS:
                if grid[r][i].element is grid[r][i-1].element:
                    size += 1
                else:
                    if size >= 3:
                        for j in range(i-size, i-1):
                            ds.union( grid[r][j], grid[r][i-1] )
                    size = 1
                i += 1
            # Also check at the end of each row.
            if size >= 3:
                for j in range(CF.BOARD_COLS - size, CF.BOARD_COLS - 1):
                    ds.union(grid[r][j], grid[r][CF.BOARD_COLS - 1])

        # Step 3: Column check. Size 3+ only.
        for c in range( CF.BOARD_COLS ):
            i, size = 1, 1
            while i < CF.BOARD_ROWS:
                if grid[i][c].element == grid[i-1][c].element:
                    size += 1
                else:
                    if size >= 3:
                        for j in range(i-size, i-1):
                            ds.union( grid[j][c], grid[i-1][c] )
                    size = 1
                i += 1
            # Also check at the end of each row.
            if size >= 3:
                for j in range(CF.BOARD_ROWS - size, CF.BOARD_ROWS - 1):
                    ds.union(grid[j][c], grid[CF.BOARD_ROWS - 1][c])

        # Step 4: Iterate the board once more and group those who belong to the same disjoint set
        mapper = dict()
        for runestone in self.board:
            parent = ds.get_parent_node(runestone)
            if parent.size >= 3:
                mapper.setdefault(parent, []).append(runestone)

        # Step 5: Return the groups of elements to eliminate
        return mapper.values()








