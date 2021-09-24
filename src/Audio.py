# Singleton audio instance for sound effects and music
import pygame
import os.path as path

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(10)

BASE_PATH = path.join('assets', 'sound')

class SFX:
    COMBO_SOUNDS = [
        pygame.mixer.Sound( path.join(BASE_PATH, 'combo1.ogg') ),
        pygame.mixer.Sound( path.join(BASE_PATH, 'combo2.ogg') ),
        pygame.mixer.Sound( path.join(BASE_PATH, 'combo3.ogg') ),
        pygame.mixer.Sound( path.join(BASE_PATH, 'combo4.ogg') ),
        pygame.mixer.Sound( path.join(BASE_PATH, 'combo5.ogg') ),
        pygame.mixer.Sound( path.join(BASE_PATH, 'combo6.ogg') ),
        pygame.mixer.Sound( path.join(BASE_PATH, 'combo7.ogg') ),
        pygame.mixer.Sound( path.join(BASE_PATH, 'combo8.ogg') ),
        pygame.mixer.Sound( path.join(BASE_PATH, 'combo9.ogg') ),
        pygame.mixer.Sound( path.join(BASE_PATH, 'combo10.ogg') ),
    ]
    SPIN = pygame.mixer.Sound( path.join(BASE_PATH, 'spin.ogg') )
    FIVE_STONE = pygame.mixer.Sound(path.join(BASE_PATH, '5stones.ogg'))
    BUTTON_SELECT = pygame.mixer.Sound(path.join(BASE_PATH, 'button_select.ogg'))
    CHARGING = pygame.mixer.Sound(path.join(BASE_PATH, 'charging.ogg'))


class Music:
    CURR_PLAYING = None
    BATTLE_PATH = path.join(BASE_PATH, 'tos_battle.ogg')
    NIGHT_PATH = path.join(BASE_PATH, 'tos_night.ogg')


def play_combo(combo:int, runestone_count:int):
    if runestone_count < 5:
        SFX.COMBO_SOUNDS[ min(combo - 1, 9) ].play()
    else:
        SFX.FIVE_STONE.play()

def play_spin(): SFX.SPIN.play()
def play_button_select(): SFX.BUTTON_SELECT.play()
def play_charging(): SFX.CHARGING.play()

def play_battle_bgm():
    if Music.CURR_PLAYING == Music.BATTLE_PATH: return
    Music.CURR_PLAYING = Music.BATTLE_PATH
    pygame.mixer.music.stop()
    pygame.mixer.music.load( Music.BATTLE_PATH )
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def play_night_bgm():
    if Music.CURR_PLAYING == Music.NIGHT_PATH: return
    Music.CURR_PLAYING = Music.NIGHT_PATH
    pygame.mixer.music.stop()
    pygame.mixer.music.load( Music.NIGHT_PATH )
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.fadeout(500)
    Music.CURR_PLAYING = None
