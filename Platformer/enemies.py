"""
The enemies module: contains objects that the game reloads when interacting with.
"""

import pygame
from constants import *


class Enemy(pygame.sprite.Sprite):
    """
    A class used to represent the blob

    Attributes:
        x : float
            x coordinate
        y : float
            y coordinate
    """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        """
        Allows the enemy to move left and right
        """

        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
    """
    A class used to represent the lava
    the built-in update method is used

    Attributes:
        x : float
            x coordinate
        y : float
            y coordinate
    """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png').convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

