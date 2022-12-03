# ************************************************************************************************
# Utility.py
# This file contains utility methods used by the application

# Author : Madusha Gamage
# Date : 11/25/2022
# ************************************************************************************************

# Import dependencies
import math
from classes import Enemy
from .Globals import *


def load_all_graphics():
    """Load all graphics"""
    global background_image, walltile_image, fort_image, castle_image, laser_image, splash_logo

    background_image = pygame.image.load("sprites/background.jpg").convert_alpha()
    background_image = pygame.transform.scale(background_image, (SCREENSIZE_X, SCREENSIZE_Y))

    walltile_image = pygame.image.load("sprites/wall_resized.png").convert_alpha()
    walltile_image = pygame.transform.scale(walltile_image, (walltile_image.get_width(), 80))

    fort_image = pygame.image.load("sprites/fort.png").convert_alpha()
    fort_image = pygame.transform.scale(fort_image, (80, 150))

    castle_image = pygame.image.load("sprites/castle.png").convert_alpha()
    castle_image = pygame.transform.scale(castle_image, (80, 120))

    laser_image = pygame.image.load("sprites/laser.png")
    laser_image = pygame.transform.scale(laser_image, (10, 40))

    splash_logo = pygame.image.load("sprites/splash_logo.png")


def show_splash_logo():
    """Shows the startup splash logo for the game"""
    window.blit(splash_logo, (
    (SCREENSIZE_X / 2) - (splash_logo.get_width() / 2), (SCREENSIZE_Y / 2) - (splash_logo.get_height() / 2)))
    pygame.display.update()
    pygame.time.wait(3000)


def redraw_background(is_game_over):
    """ Draw all background graphics """
    # Draw background
    window.blit(background_image, (0, 0))

    if not is_game_over:
        # Draw fort wall
        wall_y_coord = SCREENSIZE_Y - 50
        brick_width, brick_height = walltile_image.get_width(), walltile_image.get_height()
        for x in range(0, int(SCREENSIZE_X / 2) - brick_width, brick_width):
            window.blit(walltile_image, (x, wall_y_coord))
        for x in range(int(SCREENSIZE_X / 2) + 40, SCREENSIZE_X, brick_width):
            window.blit(walltile_image, (x, wall_y_coord))

        # Draw fort
        window.blit(fort_image, ((SCREENSIZE_X / 2) - (fort_image.get_width() / 2), SCREENSIZE_Y - 120))
        # Draw two corner castles
        window.blit(castle_image, (0, SCREENSIZE_Y - 120))
        window.blit(castle_image, (SCREENSIZE_X - castle_image.get_width(), SCREENSIZE_Y - 120))


def blit_rotate(surface, image, pos, origin_pos, angle):
    """Rotate an image based on an angle"""

    # calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    sin_a, cos_a = math.sin(math.radians(angle)), math.cos(math.radians(angle))
    min_x, min_y = min([0, sin_a * h, cos_a * w, sin_a * h + cos_a * w]), max(
        [0, sin_a * w, -cos_a * h, sin_a * w - cos_a * h])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(origin_pos[0], -origin_pos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - origin_pos[0] + min_x - pivot_move[0], pos[1] - origin_pos[1] - min_y + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surface.blit(rotated_image, origin)


def redraw_screen(bullets_list, player, score, is_game_over):
    """Redraw all graphical elements on the screen"""
    redraw_background(is_game_over)

    # Show scores
    scores_text = FONT_SMALL.render(f"SCORE : {str(score)}", False, RED, WHITE)
    window.blit(scores_text, (10, 10))

    # Show any visible bullets
    for bullet in bullets_list:
        bullet.draw()

    # If game is not over, then show player cannon
    if not is_game_over:
        player.draw()


def spawn_enemies_based_on_difficulty(score, enemies):
    """Controls the number of enemies that appear on the screen, based on the score"""
    if 0 <= score <= 10:
        if len(enemies) <= 0:
            enemies.add(Enemy.Enemy())
    elif 10 < score <= 20:
        if len(enemies) < 2:
            enemies.add(Enemy.Enemy())
    elif 20 < score <= 30:
        if len(enemies) < 4:
            enemies.add(Enemy.Enemy())
    elif 30 < score:
        if len(enemies) < 6:
            enemies.add(Enemy.Enemy())


def is_escape_key_pressed(event):
    """Returns true if the ESCAPE key is pressed"""
    # If ESCAPE key is pressed, then exit game
    if event.type == pygame.KEYDOWN:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return True
    return False
