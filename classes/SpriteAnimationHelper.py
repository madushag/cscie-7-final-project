# *********************************************************************************************************
# SpriteAnimationHelper.py
# This file contains the class definition for the Enemy object that represents the invading space aliens
#
# Author : This code was borrowed from https://www.pygame.org/wiki/Spritesheet
# Date : 11/25/2022
# *********************************************************************************************************

# Import dependencies
import classes.SpriteHelper as SpriteHelper


class SpriteAnimationHelper(object):
    """sprite strip animator

    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """

    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim

        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.

        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.

        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        ss = SpriteHelper.SpriteHelper(filename)
        self.images = ss.load_strip(rect, count, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames
        self.animation_complete = False

    def iter(self):
        """Initialize the animation iterator"""
        self.i = 0
        self.f = self.frames
        return self

    def next(self):
        """Get next image in the animation sequence"""
        if self.i >= len(self.images):
            if not self.loop:
                self.animation_complete = True
                return None
            else:
                self.i = 0
                self.animation_complete = True
                return None

        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image

    def __add__(self, ss):
        """Overloaded add operator to combine sprite images"""
        self.images.extend(ss.images)
        return self
