import pygame

import src.CONFIG as CF
import src.CONSTANTS as C

import src.utils as utils
import src.Audio as Audio

from src.FontFactory import FontFactory

import src.States.AbstractState as AbstractState
import src.States.Quit as Quit
import src.States.Initialization as Initialization

from src.Objects.BackgroundManager import BackgroundManager

# Main Menu state. Nothing to elaborate
class MainMenu(AbstractState.AbstractState):
    def __init__(self, clock: pygame.time.Clock):
        self._screen = pygame.display.get_surface()
        self._clock = clock
        self._next_state = self

        self.background = BackgroundManager()
        self.current_selection = -1             # Used to indicate whether the sound should play
        self.white_blindfold = None

        centerx, centery = self._screen.get_rect().center

        # Title
        self.title = FontFactory.generate_xl_text('TOS', C.BROWN_TEXT_1, C.BROWN_TEXT_2,
                                                  ((C.BLACK, 10), (C.WHITE,5)))
        self.title2 = FontFactory.generate_xl_text('Spinner', C.BROWN_TEXT_1, C.BROWN_TEXT_2,
                                                   ((C.BLACK, 10), (C.WHITE,5)))
        self.title_rect = self.title.get_rect(centerx=centerx, centery=centery-200)
        self.title_rect2 = self.title2.get_rect(centerx=centerx, centery=centery-100)

        # Buttons
        NORMAL_CLR1, NORMAL_CLR2 = C.BROWN_TEXT_1, C.BROWN_TEXT_2
        HIGHLIGHT_CLR1, HIGHLIGHT_CLR2 = C.YELLOW_1, C.YELLOW_2
        OUTLINE = ( (C.BLACK, 4), )

        self.buttons = [
            (
                FontFactory.generate_m2_text('Start Game', NORMAL_CLR1, NORMAL_CLR2, OUTLINE),
                FontFactory.generate_m2_text('Start Game', HIGHLIGHT_CLR1, HIGHLIGHT_CLR2, OUTLINE),
            ),
            (
                FontFactory.generate_m2_text('Toggle FPS', NORMAL_CLR1, NORMAL_CLR2, OUTLINE),
                FontFactory.generate_m2_text('Toggle FPS', HIGHLIGHT_CLR1, HIGHLIGHT_CLR2, OUTLINE)
            ),
            (
                FontFactory.generate_m2_text('Toggle Fullscreen', NORMAL_CLR1, NORMAL_CLR2, OUTLINE),
                FontFactory.generate_m2_text('Toggle Fullscreen', HIGHLIGHT_CLR1, HIGHLIGHT_CLR2, OUTLINE)
            ),
            (
                FontFactory.generate_m2_text('Custom Cursor', NORMAL_CLR1, NORMAL_CLR2, OUTLINE),
                FontFactory.generate_m2_text('Custom Cursor', HIGHLIGHT_CLR1, HIGHLIGHT_CLR2, OUTLINE)
            ),
            (
                FontFactory.generate_m2_text('Quit', NORMAL_CLR1, NORMAL_CLR2, OUTLINE),
                FontFactory.generate_m2_text('Quit', HIGHLIGHT_CLR1, HIGHLIGHT_CLR2, OUTLINE)
            )
        ]
        self.button_rects = [
            self.buttons[0][0].get_rect(centerx=centerx, centery=centery + 60),
            self.buttons[1][0].get_rect(centerx=centerx, centery=centery + 120),
            self.buttons[2][0].get_rect(centerx=centerx, centery=centery + 180),
            self.buttons[3][0].get_rect(centerx=centerx, centery=centery + 240),
            self.buttons[4][0].get_rect(centerx=centerx, centery=centery + 300)
        ]

        Audio.play_night_bgm()


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._next_state = Quit.Quit()
            # Check for any hovering.
            elif event.type == pygame.MOUSEMOTION:
                x,y = event.pos
                is_hovering_any_button = False
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(x,y):
                        if self.current_selection != i:
                            Audio.play_spin()
                        self.current_selection = i
                        is_hovering_any_button = True
                        break
                if not is_hovering_any_button: self.current_selection = -1
            # Button clicked while on any of button. Check
            elif event.type == pygame.MOUSEBUTTONDOWN and self.current_selection != -1:
                if self.current_selection == 0:
                    self.white_blindfold = pygame.Surface( (C.SCREEN_WIDTH, C.SCREEN_HEIGHT) )
                    self.white_blindfold.fill( C.WHITE )
                    self.white_blindfold.set_alpha( 0 )
                    Audio.stop_music()
                elif self.current_selection == 1:
                    CF.SHOW_FPS = not CF.SHOW_FPS
                elif self.current_selection == 2:
                    pygame.display.toggle_fullscreen()
                elif self.current_selection == 3:
                    pygame.mouse.set_visible(CF.USE_CUSTOM_CURSOR)
                    CF.USE_CUSTOM_CURSOR = not CF.USE_CUSTOM_CURSOR
                else:
                    self._next_state = Quit.Quit()
                # Sound
                Audio.play_button_select()


    def update(self):
        dt = self._clock.tick( CF.DESIRED_FPS ) * 0.001 * CF.DESIRED_FPS
        self.background.update()

        if self.white_blindfold is not None:
            self.white_blindfold.set_alpha( min(255, self.white_blindfold.get_alpha() + 5 * dt) )

            if self.white_blindfold.get_alpha() == 255:
                self._next_state = Initialization.Initialization(self._clock, 1)


    @utils.show_fps_if_set
    @utils.draw_mouse
    def render(self):
        self._screen.fill( C.BLACK )
        self.background.render(self._screen)
        self._screen.blit( self.title, self.title_rect )
        self._screen.blit( self.title2, self.title_rect2 )

        for i, ( (btn, btn_h), rect) in enumerate( zip(self.buttons, self.button_rects )):
            self._screen.blit(btn if self.current_selection != i else btn_h, rect)

        if self.white_blindfold is not None:
            self._screen.blit( self.white_blindfold, (0,0) )


    def get_next_state(self):
        return self._next_state
