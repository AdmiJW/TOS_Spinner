import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

import src.Audio as Audio

from src.Objects.Runestone import Runestone

# Runestone Board
class RunestoneBoard(pygame.sprite.Group):
    WIDTH = C.Sprite.TILE_SIZE_SCALED[0] * CF.BOARD_COLS
    HEIGHT = C.Sprite.TILE_SIZE_SCALED[1] * CF.BOARD_ROWS

    TIME_ICON = pygame.transform.smoothscale(
        pygame.image.load(C.Sprite.TIME_ICON_PATH).convert_alpha(),
        C.Sprite.TIME_ICON_SCALED
    )
    TIME_BAR = pygame.transform.smoothscale(
        pygame.image.load(C.Sprite.TIME_BAR_PATH).convert_alpha(),
        C.Sprite.TIME_BAR_SCALED
    )
    TIME_ICON_RECT = TIME_ICON.get_rect(bottom=CF.BOARD_OFFSET[1], left=0)
    TIME_BAR_RECT = TIME_BAR.get_rect(centery=TIME_ICON_RECT.centery, left=TIME_ICON_RECT.centerx)

    def __init__(self, board=None):
        super().__init__()
        self.background = RunestoneBoard.get_checkerboard_background()

        # self.dragged - Runestone instance currently being dragged
        # self.is_swapped - Boolean flag, If the player is dragging AND Swapped at least 1 runestone. Used to check
        #                   if the timer should decrement (If we are implementing based on timer, not on turns)
        # self.is_released - Boolean flag, If previously got dragged stone & already released. Used to indicate that
        #                    we should proceed to the Clearing state
        self.dragged = None
        self.is_swapped = False
        self.is_released = False

        # Rectangle for drawing timebar
        self.timebar_area = RunestoneBoard.TIME_BAR.get_rect()

        # Convert board of C.Element enums into actual Runestone instances
        board = RunestoneBoard.generate_board() if board is None else board
        for i,row in enumerate(board):
            for j,element in enumerate(row):
                self.add( Runestone(element, i, j) )



    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Currently dragging a runestone
            if self.dragged is not None:
                # Mouse moves out of boundary! Release the token!
                if not self.background.get_rect(top=CF.BOARD_OFFSET[1], left=CF.BOARD_OFFSET[0]).collidepoint(x, y):
                    self.dragged.image.set_alpha(255)
                    self.dragged = None
                    self.is_released = True
                    return
                self.dragged.follow_mouse(x,y)

            for runestone in self:
                is_render_collide = runestone.is_point_collide_render_rect(x,y)
                is_hitbox_collide = runestone.is_point_collide_hitbox_rect(x,y)
                runestone.set_hovering(is_render_collide)

                # Clicked on a runestone - Start dragging
                if event.type == pygame.MOUSEBUTTONDOWN and self.dragged is None and is_render_collide:
                    self.dragged = runestone
                    self.dragged.image.set_alpha(128)
                    self.is_released = False            # To handle case: Drag but no swapping occur.

                # Currently dragging && hit another runestone - Swap time
                if is_hitbox_collide and self.dragged is not None and self.dragged != runestone:
                    Audio.play_spin()
                    self.dragged.swap_runestone_to(runestone)
                    self.is_swapped = True

        # Mouse released while dragging a runestone - Release
        elif event.type == pygame.MOUSEBUTTONUP and self.dragged is not None:
            self.release_dragged_runestone()


    def update(self, dt):
        for runestone in self:
            runestone.update(dt) if self.dragged != runestone else None

    # Update the runestone movement but in linear fashion, used when falling stones in Regeneration State
    def update_linear(self, dt):
        for runestone in self:
            runestone.update_linear(dt) if self.dragged != runestone else None


    def render(self, surface: pygame.Surface):
        surface.blit( self.background, CF.BOARD_OFFSET )
        for runestone in self:
            runestone.render(surface)
        surface.blit( RunestoneBoard.TIME_BAR, RunestoneBoard.TIME_BAR_RECT, area=self.timebar_area)
        surface.blit( RunestoneBoard.TIME_ICON, RunestoneBoard.TIME_ICON_RECT )


    # Release currently dragged runestone.
    def release_dragged_runestone(self):
        if self.dragged is None: return
        self.dragged.image.set_alpha(255)
        self.dragged = None
        self.is_released = True


    def update_timebar(self, framesleft: int):
        width = framesleft * RunestoneBoard.TIME_BAR_RECT.width / CF.TIME_LIMIT_IN_FRAMES
        self.timebar_area.width = width


    # Reset self.is_swapped and self.is_released all to False. Used when transitioning to Clearing state
    def reset_internal_state(self):
        self.is_swapped = self.is_released = False
        self.timebar_area = RunestoneBoard.TIME_BAR.get_rect()


    # Obtains a grid-like representation of current state of board. It should be matrix of size ROWxCOLUMN,
    # and those grid who are occupied, should be filled with Runestone instance, otherwise None
    def get_grid_representation(self):
        grid = [[None] * CF.BOARD_COLS for _ in range(CF.BOARD_ROWS)]
        for runestone in self:
            grid[runestone.row][runestone.col] = runestone
        return grid


    # Adds a runestone with selected element (or random by default) into the board
    def add_new_runestone(self, row: int, col: int, is_powered:bool = False, element: C.Element = None):
        if element is None:
            element = Runestone.generate_random_element()
        new_stone = Runestone(element, row, col, is_powered)
        self.add( new_stone )
        return new_stone


    # Returns a pygame.Surface which resembles the background of the checkerboard
    @staticmethod
    def get_checkerboard_background():
        surface = pygame.Surface( (RunestoneBoard.WIDTH, RunestoneBoard.HEIGHT) )
        surface.fill( C.BROWN_1 )

        for r in range(CF.BOARD_ROWS):
            for c in range(CF.BOARD_COLS):
                if r % 2 == c % 2: continue
                pygame.draw.rect(surface, C.BROWN_2, (r * C.Sprite.TILE_SIZE_SCALED[0],
                                                      c * C.Sprite.TILE_SIZE_SCALED[1],
                                                      *C.Sprite.TILE_SIZE_SCALED) )
        return surface


    # Generates a board according to size in CONFIG, a list of C.Element Enums
    @staticmethod
    def generate_board():
        return [ [ Runestone.generate_random_element() for _ in range(CF.BOARD_COLS)] for _ in range(CF.BOARD_ROWS)]
