# *********************************************************************************************************
# ExplosionAnimation.py
# This file contains the class definition for handling explosion animations

# Author : This code was borrowed from https://www.pygame.org/wiki/Spritesheet, and optimized by Madusha Gamage
# Date : 11/25/2022
# *********************************************************************************************************

# Import dependencies
from classes import SpriteAnimationHelper
from helpers import Globals


class ExplosionAnimation(object):
    # Class constants
    IMAGE = 'sprites/explosion.png'

    def __init__(self, window, fps):
        """Constructor"""
        self.window = window

        # Load all sprites and initialize the animation iterator
        self.strips = (SpriteAnimationHelper.SpriteAnimationHelper(self.IMAGE, (0, 0, 64, 64), 4, Globals.BLACK, False, fps) +
                       SpriteAnimationHelper.SpriteAnimationHelper(self.IMAGE, (0, 64, 64, 64), 4, Globals.BLACK, False, fps) +
                       SpriteAnimationHelper.SpriteAnimationHelper(self.IMAGE, (0, 128, 64, 64), 4, Globals.BLACK, False, fps) +
                       SpriteAnimationHelper.SpriteAnimationHelper(self.IMAGE, (0, 192, 64, 64), 4, Globals.BLACK, False, fps))
        self.strips.iter()

    def show_at(self, x, y):
        """Show explosion at x,y coords"""
        image = self.strips.next()
        if image:
            self.window.blit(image, (x, y))
        else:
            self.strips.animation_complete = True

    def is_animation_complete(self):
        """Return True if animation is complete."""
        return self.strips.animation_complete

    def reset_animation(self):
        """Resets animation sequence"""
        self.strips.animation_complete = False
        self.strips.i = 0
