"""
The world_environment module: contains static game objects that the player can interact with.
"""

import pygame
from constants import *


class Button:
    """
    A class used to represent buttons

    Attributes:
        x : float
            x coordinate
        y : float
            y coordinate
        image_name : str
            the name of the image that represents the button

    """

    def __init__(self, x, y, image_name):
        self.image = pygame.image.load(str(image_name))
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        """
        draws the button image to the screen and tracks the mouse click on each frame
        """
        
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and not self.clicked:
            self.clicked = True
            action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        # draw button
        screen.blit(self.image, self.rect)

        return action

class Platform(pygame.sprite.Sprite):
    """
    A class used to represent moving platforms
    the built-in update method is used

    Attributes:
        x : float
            x coordinate
        y : float
            y coordinate
        move_x : float
            speed on the x-axis
        move_y : float
            speed on the y-axis
    """

    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform.png').convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_x = move_x
        self.move_y = move_y
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Exit(pygame.sprite.Sprite):
    """
    A class used to represent exit doors
    the built-in update method is used

    Attributes:
        x : float
            x coordinate
        y : float
            y coordinate
    """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png').convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    """
    A class used to represent coins
    the built-in update method is used

    Attributes:
        x : float
            x coordinate
        y : float
            y coordinate
    """

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/coin.png').convert_alpha()
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Background():
    """
    A class used to represent the world

    Attributes:
        *args :  *(name strings of pictures(str), (xcoord(int), ycoord(int)))
            arguments are served in the order they are added to the background screen

    """

    def __init__(self, *args):
        self.background_pics = []
        try:
            for picture, coordinates in args:
                img = pygame.image.load(picture).convert_alpha()
                self.background_pics.append((img, coordinates))
        except pygame.error as err:
            raise SystemExit(err)

    def draw(self):
        """
        Draws background images
        """

        for picture, coordinates in self.background_pics:
            screen.blit(picture, coordinates)