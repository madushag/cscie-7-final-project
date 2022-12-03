# *********************************************************************************************************
# Enemy.py
# This file contains the class definition for displaying an animation based on sprite images

# Author : This code was borrowed from https://www.pygame.org/wiki/Spritesheet, and optimized by Madusha Gamage
# Date : 11/25/2022
# *********************************************************************************************************

# Import dependencies
import pygame


class SpriteHelper(object):
    def __init__(self, filename):
        """Constructor"""
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, color_key=None):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, color_key=None):
        """Loads multiple images, supply a list of coordinates"""
        return [self.image_at(rect, color_key) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, color_key=None):
        """Loads a strip of images and returns them as a list"""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, color_key)
