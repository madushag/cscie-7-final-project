# *********************************************************************************************************
# Enemy.py
# This file contains the class definition for the Enemy object that represents the invading space aliens

# Author : Madusha Gamage
# Date : 11/25/2022
# *********************************************************************************************************

# Import dependencies
import pygame
from helpers import Utility
import random


class Enemy(pygame.sprite.Sprite):

    # Class constants
    SPEED = 1

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.image = pygame.image.load("sprites/alien_ship.png")
        self.image = pygame.transform.scale(self.image, (70, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, Utility.SCREENSIZE_X - 40), 0)
        self.breached_fort = False

    def move(self):
        """Move alien object at the predetermined speed"""
        self.rect.move_ip(0, self.SPEED)

        # If enemy object has moved beyond the bottom of the screen
        if self.rect.bottom > Utility.SCREENSIZE_Y:
            self.breached_fort = True

    def has_breached_fort(self):
        """Check if an enemy has breached the fort"""
        return self.breached_fort
