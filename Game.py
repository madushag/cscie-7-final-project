# ***************************************************************************************
# Game.py
# This file contains the main logic that drives the game mechanics

# Usage :
#   python Game.py

# Author : Madusha Gamage
# Date : 11/25/2022

# 3rd PARTY CREDITS :
# Sound from Zapsplat.com
# ***************************************************************************************

# Import dependencies
import sys

from helpers import Utility, Globals
import pygame
import math
from classes import Bullet, Player, ExplosionAnimation
import helpers.Sounds as Sounds

# Load all graphic files
Utility.load_all_graphics()

# Play background theme music in a loop
Sounds.play_background_music(loop=True)

# Display startup splash logo
Utility.show_splash_logo()

# Setup sprite groups for enemies and bullets
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Initialize other game variables
clock = pygame.time.Clock()
run_game = True
player = Player.Player()
collisions = []
explosions = []
score = 0
game_over_explosions = []
has_enemy_breached_fort = False
is_game_over = False


# Main game loop
while run_game:
    clock.tick(Globals.FPS)

    # Continue to process game activities if game is not over
    if not is_game_over:
        # Based on difficulty level, show more or less enemies simultaneously
        Utility.spawn_enemies_based_on_difficulty(score, enemies)

        # Rotate the gun based on where the mouse cursor is on the screen
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if not player.is_looking_at_player:
            player.look_at((mouse_x, mouse_y))

        # Process any events
        for event in pygame.event.get():
            # If ESCAPE key is pressed, then exit game
            if Utility.is_escape_key_pressed(event):
                run_game = False

            # Shoot laser if a mouse button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Play sound effect
                Sounds.play_shooting_sound()

                # Determine if the mouse pointer is behind the gun barrell. We don't want to shoot if we are pointing
                # backwards!
                pivot_x, pivot_y = player.get_pivot()
                dist_to_pivot_x, dist_to_pivot_y = mouse_x - pivot_x, mouse_y - pivot_y
                distance_to_pivot = math.sqrt(dist_to_pivot_x ** 2 + dist_to_pivot_y ** 2)

                # Limit the number of bullets that can exit at a time on the screen to 100, and only shoot if we are
                # pointing forward
                if len(bullets) < 100 and distance_to_pivot > 100:
                    start_x, start_y = player.get_top()
                    mouse_x, mouse_y = event.pos
                    dir_x, dir_y = mouse_x - start_x, mouse_y - start_y
                    distance = math.sqrt(dir_x ** 2 + dir_y ** 2)
                    if distance > 0:
                        new_bullet = Bullet.Bullet(start_x, start_y, dir_x / distance, dir_y / distance, (0, 0, 0))
                        bullets.add(new_bullet)

    # Draw all bullets that we've shot
    for bullet in bullets:
        bullet.move()

        # If a bullet leaves the screen dimensions, then destroy it
        if bullet.x < 0 or bullet.x > Globals.SCREENSIZE_X or bullet.y < 0 or bullet.y > Globals.SCREENSIZE_Y:
            bullets.remove(bullet)

        # Check if any of the bullets hit an enemy. If it did, then kill the enemy, and show explosion
        collided_enemy = pygame.sprite.spritecollide(bullet, enemies, True)
        if collided_enemy:
            # Play sound effect and destroy the bullet
            Sounds.play_explosion_sound()
            bullets.remove(bullet)

            # Initialize an explosion and track the collision location
            explosion_animation = ExplosionAnimation.ExplosionAnimation(Globals.window, Globals.FPS / 10)
            collisions.append((collided_enemy[0], explosion_animation))

            # We scored!
            score += 1

    # Refresh screen with new positions for animated sprites
    Utility.redraw_screen(bullets, player, score, has_enemy_breached_fort)

    # If a bullet hit an enemy, then show an explosion
    if len(collisions) > 0:

        # Each collision should have a corresponding explosion. Process each individually so the explosion
        # animation completes independently of each other
        for collision in collisions:
            explosion = collision[1]
            explosion.show_at(collision[0].rect.x, collision[0].rect.y)
            if explosion.is_animation_complete():
                collisions.remove(collision)

    # If game isn't continue to process enemy activities
    if not is_game_over:
        # Animate enemies by moving them
        for enemy in enemies:
            enemy.move()
            Globals.window.blit(enemy.image, enemy.rect)

            # If any enemy has breached our fort, then its GAME OVER!
            if enemy.has_breached_fort():
                has_enemy_breached_fort = True

    # If an enemy has breached the fort, then setup final explosion animation sequence
    if has_enemy_breached_fort and len(game_over_explosions) == 0:
        # Play sound effect
        Sounds.play_game_over_sound()

        # Setup explosions throughout the fort walls, with varying explosion speeds
        for i in range(0, Utility.SCREENSIZE_X, 60):
            if i % 40:
                explosion_animation = ExplosionAnimation.ExplosionAnimation(Globals.window, Globals.FPS / 10)
                game_over_explosions.append(((i, Utility.SCREENSIZE_Y - 100), explosion_animation))
            else:
                explosion_animation = ExplosionAnimation.ExplosionAnimation(Globals.window, Globals.FPS / 6)
                game_over_explosions.append(((i, Utility.SCREENSIZE_Y - 50), explosion_animation))
        # Explode fort
        game_over_explosions.append(
            ((player.get_rect()), ExplosionAnimation.ExplosionAnimation(Globals.window, Globals.FPS / 4)))
        game_over_explosions.append(
            ((player.get_pivot()), ExplosionAnimation.ExplosionAnimation(Globals.window, Globals.FPS / 4)))

    # Animate all explosions to completion before finishing up gaming mode
    if not is_game_over and len(game_over_explosions) > 0:
        for explosion in game_over_explosions:
            explosion[1].show_at(explosion[0][0], explosion[0][1])
            if explosion[1].is_animation_complete():
                game_over_explosions.remove(explosion)
        if len(game_over_explosions) == 0:
            is_game_over = True

    # If we've finished all explosion animations (then game is over), display game over banner
    elif is_game_over:
        Globals.window.fill(Globals.RED)
        Globals.window.blit(Globals.GAME_OVER_TEXT,
                            ((Utility.SCREENSIZE_X / 2) - (Globals.GAME_OVER_TEXT.get_width() / 2),
                             ((Utility.SCREENSIZE_Y / 2) - (Globals.GAME_OVER_TEXT.get_height() / 2))))
        Globals.window.blit(Globals.PRES_ESCAPE_TO_EXIT_TEXT,
                            ((Utility.SCREENSIZE_X / 2) - (Globals.PRES_ESCAPE_TO_EXIT_TEXT.get_width() / 2),
                             ((Utility.SCREENSIZE_Y / 2) - (Globals.PRES_ESCAPE_TO_EXIT_TEXT.get_height() / 2)) + 100))
        # Process any events
        for event in pygame.event.get():
            # If ESCAPE key is pressed, then exit game
            if Utility.is_escape_key_pressed(event):
                run_game = False

    # Update the screen graphics
    pygame.display.update()

# quiting the game
pygame.quit()
sys.exit()
