import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

from src.Objects.Runestone import Runestone

# Runestone Board
class RunestoneBoard(pygame.sprite.Group):
    WIDTH = C.Sprite.TILE_SIZE_SCALED[0] * CF.BOARD_COLS
    HEIGHT = C.Sprite.TILE_SIZE_SCALED[1] * CF.BOARD_ROWS

    def __init__(self, board=None):
        super().__init__()
        self.background = RunestoneBoard.get_checkerboard_background()

        self.dragged = None                         # Dragged Runestone tile

        # Convert board of C.Element enums into actual Runestone instances
        board = RunestoneBoard.generate_board() if board is None else board
        for i,row in enumerate(board):
            for j,element in enumerate(row):
                self.add( Runestone(element, i, j) )

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if self.dragged is not None:
                self.dragged.follow_mouse(x,y)

            for runestone in self:
                is_render_collide = runestone.is_point_collide_render_rect(x,y)
                is_hitbox_collide = runestone.is_point_collide_hitbox_rect(x,y)
                runestone.set_hovering(is_render_collide)

                if event.type == pygame.MOUSEBUTTONDOWN and self.dragged is None and is_render_collide:
                    self.dragged = runestone
                    self.dragged.image.set_alpha(128)

                if is_hitbox_collide and self.dragged is not None and self.dragged != runestone:
                    self.dragged.swap_runestone_to(runestone)

        elif event.type == pygame.MOUSEBUTTONUP and self.dragged is not None:
            self.dragged.image.set_alpha(255)
            self.dragged = None
            return True





    def update(self, dt):
        for runestone in self:
            runestone.update(dt) if self.dragged != runestone else None


    def render(self, surface: pygame.Surface):
        surface.blit( self.background, CF.BOARD_OFFSET )
        for runestone in self:
            runestone.render(surface)


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
