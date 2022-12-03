from helpers import Utility
import pygame
import math


class Player:
    def __init__(self):
        self.width = 50
        self.height = 100
        self.cannon = pygame.image.load("sprites/cannon2.png").convert_alpha()
        self.cannon = pygame.transform.scale(self.cannon, (self.width, self.height))
        self.image = self.cannon
        self.x = (Utility.SCREENSIZE_X/2) - (self.cannon.get_width()/2)
        self.y = Utility.SCREENSIZE_Y - 200
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.look_at_pos = (self.x, self.y)
        self.is_looking_at_player = False
        self.angle = 0

    def get_rect(self):
        self.rect.topleft = (self.x, self.y)
        return self.rect

    def get_pivot(self):
        player_rect = self.cannon.get_rect(center=self.get_rect().center)
        return player_rect.centerx, player_rect.top + 103

    def get_angle(self):
        pivot_abs = self.get_pivot()
        dx = self.look_at_pos[0] - pivot_abs[0]
        dy = self.look_at_pos[1] - pivot_abs[1]
        return math.degrees(math.atan2(-dy, dx))

    def get_top(self):
        pivot_x, pivot_y = self.get_pivot()
        angle = self.get_angle()
        length = 100
        top_x = pivot_x + length * math.cos(math.radians(angle))
        top_y = pivot_y - length * math.sin(math.radians(angle))
        return top_x, top_y

    def draw(self):
        gun_size = self.image.get_size()
        pivot_abs = self.get_pivot()
        pivot_rel = (gun_size[0] // 2, 105)
        angle = self.get_angle() - 90
        Utility.blit_rotate(Utility.window, self.image, pivot_abs, pivot_rel, angle)

    def look_at(self, coordinate):
        self.look_at_pos = coordinate

