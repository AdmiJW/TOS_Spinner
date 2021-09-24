import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

from src.FontFactory import FontFactory

# An object to simply display the current ongoing combo.
class ComboDisplayer:
    BOTTOM = C.SCREEN_HEIGHT - 20
    RIGHT = C.SCREEN_WIDTH - 20
    INIT_OFFSET = 20

    def __init__(self):
        self.combo = -1

        self.combo_t = FontFactory.generate_l_text(' Combo!!', C.BROWN_TEXT_1, C.BROWN_TEXT_2,
                                                   ((C.WHITE, 1), (C.BLACK, 5)))
        self.combo_t_rect = self.combo_t.get_rect(bottom=C.SCREEN_HEIGHT-20, right=C.SCREEN_WIDTH-20)
        # To initialize in change_text()
        self.combo_n = self.combo_n_rect = self.percent = self.percent_rect = None
        self.change_text(0)
        self.combo_t.set_alpha(0)
        self.combo_n.set_alpha(0)
        self.percent.set_alpha(0)


    # If combo is not passed in, it means we should start fading out the text
    def update(self, dt:float, combo:int = None):
        if combo is not None and 0 < combo != self.combo:
            self.combo = combo
            self.change_text(combo)
        # Fading out
        elif combo is None:
            self.combo = -1
            self.combo_t.set_alpha(max(0, self.combo_t.get_alpha() - CF.COMBO_FADEOUT_SPEED * dt))
            self.combo_n.set_alpha(max(0, self.combo_n.get_alpha() - CF.COMBO_FADEOUT_SPEED * dt))
            self.percent.set_alpha(max(0, self.percent.get_alpha() - CF.COMBO_FADEOUT_SPEED * dt))

        # Adjust the offset while the combo text is not done animating
        if self.combo_n_rect.bottom != ComboDisplayer.BOTTOM:
            self.combo_n_rect.move_ip( -2, 2 )



    def render(self, surface: pygame.Surface):
        surface.blit( self.combo_t, self.combo_t_rect )
        surface.blit( self.combo_n, self.combo_n_rect )
        surface.blit( self.percent, self.percent_rect )


    # Changes the text of combo_n and percentage to match with the provided combo
    def change_text(self, combo:int):
        self.combo_n = FontFactory.generate_l_text(f'{combo}', C.BROWN_TEXT_1, C.BROWN_TEXT_2,
                                                   ((C.WHITE, 1), (C.BLACK, 5)))
        self.combo_n_rect = self.combo_n.get_rect(bottom=ComboDisplayer.BOTTOM - ComboDisplayer.INIT_OFFSET,
                                                  right=self.combo_t_rect.left + ComboDisplayer.INIT_OFFSET)
        self.percent = FontFactory.generate_m_text(f'+ {50 *combo}%', C.BROWN_TEXT_1, C.BROWN_TEXT_2,
                                                   ((C.WHITE, 1), (C.BLACK, 5)))
        self.percent_rect = self.percent.get_rect(bottom=self.combo_t_rect.top + 35, right=ComboDisplayer.RIGHT)

        self.combo_t.set_alpha(255)
        self.combo_n.set_alpha(255)
        self.percent.set_alpha(255)
