import pygame
import random

import src.CONFIG as CF
import src.CONSTANTS as C

import src.SpriteManager as SpriteManager

# A single instance of Runestone. Belongs to pygame.sprite.Sprite
#
# A Runestone will have two rects, one mainly used for rendering (Which has tweening effect on it), and another is the
# actual rect that resembles the actual location the runestone should be in. We call them render_rect and hitbox_rect
# During swapping, the hitbox_rect is swapped immediately with another, while the render_rect is not swapped, as it
# has tweening effect applied on it
#
# Since the runestone can be swapped, the runestone's rect position will have to be consistently
# updated for the swapping animation, To achieve this, we can extract out the runestone's position to be object's
# attribute
#
# When the player clicks on the Runestone, the Runestone will essentially be 'emptied' as if the Runestone is 'grabbed'
# by the player.
class Runestone(pygame.sprite.Sprite):
    def __init__(self, element: C.Element, row: int, col: int, is_powered: bool = False):
        super().__init__()
        self.row = row
        self.col = col
        self.element = element
        self.is_powered = is_powered


        self.ori_image = SpriteManager.get_regular_runestone(element) if not self.is_powered \
            else SpriteManager.get_powered_runestone(element)
        self.hover_image = SpriteManager.get_regular_runestone(element, True) if not self.is_powered \
            else SpriteManager.get_powered_runestone(element, True)
        self.image = self.ori_image

        self.top = CF.BOARD_OFFSET[1] + row * C.Sprite.TILE_SIZE_SCALED[1]
        self.left = CF.BOARD_OFFSET[0] + col * C.Sprite.TILE_SIZE_SCALED[0]
        self.render_rect = self.image.get_rect( top=self.top, left=self.left )
        self.hitbox_rect = self.render_rect.copy()



    # Moves the runestone's position to another runestone's position.
    # This is not 100% doing the swapping. The swapping also needs to be done in RunestoneBoard instance on 2D grid
    def swap_runestone_to(self, another_runestone):
        # PYTHON SWAPPING COOLZ
        self.row, self.col, another_runestone.row, another_runestone.col = \
            another_runestone.row, another_runestone.col, self.row, self.col
        self.top, self.left, another_runestone.top, another_runestone.left = \
            another_runestone.top, another_runestone.left, self.top, self.left
        # Also swaps the collision rects
        self.hitbox_rect, another_runestone.hitbox_rect = another_runestone.hitbox_rect, self.hitbox_rect


    # Makes the rendering to be done at the mouse's location. This method only changes the render_rect's position
    # and nothing else. This gives benefit of runestone moving back to its supposed place when released
    def follow_mouse(self, x, y):
        self.render_rect.center = (x,y)


    # Tests if a point is inside of the render rectangle
    def is_point_collide_render_rect(self, x, y):
        return self.render_rect.collidepoint(x, y)

    # Tests if a point is inside of the collide rectangle.
    # Some small optimization you can do is, collide rectangle is smaller, and is collide only IF is collide render rect
    def is_point_collide_hitbox_rect(self, x, y):
        return self.hitbox_rect.collidepoint(x, y)

    # Changes the image alpha value based on whether player is hovering over it
    def set_hovering(self, is_hover=False):
        self.image = self.ori_image if not is_hover else self.hover_image


    # Updates the position of render rect to move smoothly when swapped.
    def update(self, dt):
        top_increment = ( self.top - self.render_rect.top ) / CF.RUNESTONE_TWEEN_DIVISOR * dt
        left_increment = ( self.left - self.render_rect.left ) / CF.RUNESTONE_TWEEN_DIVISOR * dt
        self.render_rect.top += top_increment
        self.render_rect.left += left_increment


    # To overwrite the regular draw method
    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.render_rect)


    def __str__(self):
        return f"<Runestone Element {self.element} at ({self.row}, {self.col})>"

    # A static method. Returns a random Runestone value.
    @staticmethod
    def generate_random_element() -> C.Element:
        return random.choice( (*C.Element, ) )
