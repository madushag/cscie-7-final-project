# ************************************************************************************************
# Globals.py
# This file contains constants and other global values used elsewhere in the application

# Author : Madusha Gamage
# Date : 11/25/2022
# ************************************************************************************************

# Import dependencies
import pygame

pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (150, 0, 0)

##################################################################################################
# Initialize the screen and setup game globals
##################################################################################################
FPS = 60
IS_GAME_OVER = False
FONT_TINY = pygame.font.SysFont("Arial", 50)
FONT_SMALL = pygame.font.SysFont("System", 80)
FONT_LARGE = pygame.font.SysFont("System", 200)

GAME_OVER_TEXT = FONT_LARGE.render("GAME OVER", True, WHITE)
PRES_ESCAPE_TO_EXIT_TEXT = FONT_TINY.render("Press Escape to exit.", True, WHITE)

screensize = pygame.display.get_desktop_sizes()[0]
# Use the entire screen as much as possible, without going into full screen mode
SCREENSIZE_X = screensize[0] - 100
SCREENSIZE_Y = screensize[1] - 200
window = pygame.display.set_mode((SCREENSIZE_X, SCREENSIZE_Y), pygame.SCALED)
pygame.display.set_caption("SPACE INVADERS")


