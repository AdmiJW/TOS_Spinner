import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

from src.FontFactory import FontFactory

# ScoreTimeManager - Responsible for keeping time and score of one single level.
# Handles countdown for time limit, and scoring for level passing
class ScoreTimeManager:
    LEFT_MARGIN = 20
    TOP_MARGIN = 40
    Y_GAP = 0
    X_GAP = 5
    OUTLINE = ( (C.BLACK, 4), (C.WHITE,2) )

    def __init__(self, level: int):
        self.level = level
        self.score = 0
        self.target = CF.BASE_LEVEL_REQ + (level - 1) * CF.LEVEL_INCREMENT
        self.timeleft = CF.LEVEL_TIME_LIMIT_IN_FRAMES
        self.current_shown_time = CF.LEVEL_TIME_LIMIT_IN_SECONDS

        # Labels
        self.level_l = FontFactory.generate_m2_text('Level: ', C.BROWN_TEXT_1, C.BROWN_TEXT_2, ScoreTimeManager.OUTLINE)
        self.score_l = FontFactory.generate_m2_text('Score: ', C.BROWN_TEXT_1, C.BROWN_TEXT_2, ScoreTimeManager.OUTLINE)
        self.timeleft_l = FontFactory.generate_m2_text('Time Left: ', C.BROWN_TEXT_1, C.BROWN_TEXT_2,
                                                       ScoreTimeManager.OUTLINE)
        # Values
        self.level_t = FontFactory.generate_m2_text(f'{level}', C.BROWN_TEXT_1, C.BROWN_TEXT_2, ScoreTimeManager.OUTLINE)
        self.score_t = FontFactory.generate_m2_text('0', C.BROWN_TEXT_1, C.BROWN_TEXT_2, ScoreTimeManager.OUTLINE)
        self.target_t = FontFactory.generate_m2_text(f' / {self.target}', C.BROWN_TEXT_1, C.BROWN_TEXT_2,
                                                     ScoreTimeManager.OUTLINE)
        self.timeleft_t = FontFactory.generate_m2_text(f'{self.current_shown_time}', C.BROWN_TEXT_1, C.BROWN_TEXT_2,
                                                       ScoreTimeManager.OUTLINE)

        # Rectangles
        self.level_l_rect = self.level_l.get_rect(top=ScoreTimeManager.TOP_MARGIN, left=ScoreTimeManager.LEFT_MARGIN)
        self.score_l_rect = self.score_l.get_rect(top=self.level_l_rect.bottom + ScoreTimeManager.Y_GAP,
                                                  left=ScoreTimeManager.LEFT_MARGIN)
        self.timeleft_l_rect = self.timeleft_l.get_rect(top=self.score_l_rect.bottom + ScoreTimeManager.Y_GAP,
                                                        left=ScoreTimeManager.LEFT_MARGIN)
        self.level_t_rect = self.level_t.get_rect(top=ScoreTimeManager.TOP_MARGIN,
                                                  left=self.level_l_rect.right + ScoreTimeManager.X_GAP)
        self.score_t_rect = self.score_t.get_rect(top=self.score_l_rect.top,
                                                  left=self.score_l_rect.right + ScoreTimeManager.X_GAP)
        self.target_t_rect = self.target_t.get_rect(top=self.score_l_rect.top,
                                                    left=self.score_t_rect.right + ScoreTimeManager.X_GAP)
        self.timeleft_t_rect = self.timeleft_t.get_rect(top=self.timeleft_l_rect.top,
                                                        left=self.timeleft_l_rect.right + ScoreTimeManager.X_GAP)

    # Updates the position of render rect to move smoothly when swapped.
    def update_time(self, dt: float):
        self.timeleft -= dt

        # The time left in seconds changed. Update the text (No need for rect update, since rect only uses top left)
        if self.timeleft // CF.DESIRED_FPS != self.current_shown_time:
            self.current_shown_time = self.timeleft // CF.DESIRED_FPS
            self.timeleft_t = FontFactory.generate_m2_text(f'{self.current_shown_time:.0f}', C.BROWN_TEXT_1,
                                                           C.BROWN_TEXT_2, ScoreTimeManager.OUTLINE)


    def update_score(self, score_delta: int):
        self.score += score_delta
        self.score_t = FontFactory.generate_m2_text(f'{self.score}', C.BROWN_TEXT_1, C.BROWN_TEXT_2,
                                                    ScoreTimeManager.OUTLINE)
        self.score_t_rect = self.score_t.get_rect(top=self.score_l_rect.top,
                                                  left=self.score_l_rect.right + ScoreTimeManager.X_GAP)
        self.target_t_rect = self.target_t.get_rect(top=self.score_l_rect.top,
                                                    left=self.score_t_rect.right + ScoreTimeManager.X_GAP)


    # To overwrite the regular draw method
    def render(self, surface: pygame.Surface):
        # Labels
        surface.blit( self.level_l, self.level_l_rect )
        surface.blit( self.score_l, self.score_l_rect )
        surface.blit( self.timeleft_l, self.timeleft_l_rect )
        # Values
        surface.blit( self.level_t, self.level_t_rect)
        surface.blit( self.score_t, self.score_t_rect)
        surface.blit( self.target_t, self.target_t_rect)
        surface.blit( self.timeleft_t, self.timeleft_t_rect)

    # Determines whether the level is passed
    def is_passed(self):
        return self.score >= self.target

    # Determines whether the level failed
    def is_failed(self):
        return self.timeleft <= 0