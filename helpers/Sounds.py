# ************************************************************************************************
# Sounds.py
# This file contains helper methods for playing game sounds

# Author : Madusha Gamage
# Date : 12/3/2022
# ************************************************************************************************

import pygame


def play_background_music(loop):
    """Play background music"""
    if loop:
        pygame.mixer.Sound('sounds/background_music.wav').play(-1)
    else:
        pygame.mixer.Sound('sounds/background_music.wav').play()


def play_shooting_sound():
    """Play shooting sound"""
    pygame.mixer.Sound('sounds/laser_2.wav').play()


def play_explosion_sound():
    """Play explosion sound"""
    pygame.mixer.Sound('sounds/explosion.wav').play()


def play_game_over_sound():
    """Play game over sound"""
    pygame.mixer.Sound('sounds/bigboom.wav').play()
