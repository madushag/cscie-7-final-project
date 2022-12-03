# ************************************************************************************************
# Bullet.py
# This file contains the class definition for the Bullet object that represents the lasers
# that we shoot at the invading aliens

# Author : Madusha Gamage
# Date : 11/25/2022
# ************************************************************************************************

# Import dependencies
import pygame
from helpers import Utility, Globals
import math


class Bullet(pygame.sprite.Sprite):

    # Class constants
    BULLET_SPEED = 10

    def __init__(self, x, y, dir_x, dir_y, color):
        """ Constructor """
        super().__init__()
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.image = Utility.laser_image
        self.rect = self.image.get_rect()
        self.center = (self.x, self.y)
        self.speed = self.BULLET_SPEED
        self.color = color

    def move(self):
        """Move bullet in the specified direction at the defined speed"""
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

    def draw(self):
        """Draw bullet rotated at the correct angle that corresponds to the direction that the gun is pointed at"""
        self.rect.center = (round(self.x), round(self.y))

        # Calculate the angle of rotation and draw a new instance of the image at that angle
        angle = math.degrees(math.atan2(-self.dir_y, self.dir_x)) - 90
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)

        pygame.draw.rect(Globals.window, self.color, rotated_rect)
        Globals.window.blit(rotated_image, rotated_rect)
