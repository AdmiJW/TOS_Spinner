import pygame

import src.CONSTANTS as C
import src.utils as utils


# Class Specified to generate game-themed texts
class FontFactory:
    M_FONT = pygame.font.Font(C.FONT_REGULAR_PATH, 35)
    M2_FONT = pygame.font.Font(C.FONT_REGULAR_PATH, 45)
    L_FONT = pygame.font.Font(C.FONT_SEMIBOLD_PATH, 75)
    XL_FONT = pygame.font.Font(C.FONT_BOLD_PATH, 95)


    @staticmethod
    def generate_m_text(text: str, color1: tuple, color2: tuple, outline=((C.BLACK, 6),)):
        return utils.compile_outlines(utils.get_shaded_text(FontFactory.M_FONT, text, color1, color2), outline)


    @staticmethod
    def generate_m2_text(text: str, color1: tuple, color2: tuple, outline=((C.BLACK, 6),)):
        return utils.compile_outlines(utils.get_shaded_text(FontFactory.M2_FONT, text, color1, color2), outline)


    @staticmethod
    def generate_l_text(text: str, color1: tuple, color2: tuple, outline=((C.BLACK, 8), (C.WHITE, 4))):
        return utils.compile_outlines(utils.get_shaded_text(FontFactory.L_FONT, text, color1, color2), outline)

    @staticmethod
    def generate_xl_text(text: str, color1: tuple, color2: tuple, outline=((C.BLACK, 8), (C.WHITE, 6))):
        return utils.compile_outlines(utils.get_shaded_text(FontFactory.XL_FONT, text, color1, color2), outline)
