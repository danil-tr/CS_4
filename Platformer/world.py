"""
The world module: contains World class, which is responsible for displaying game objects on the screen.
"""

import pygame
from pygame.locals import *
from constants import *
from world_environment import Platform, Coin, Exit
from enemies import Enemy, Lava

class World():
    """
    A class used to represent the world

    Attributes:
        data : two-dimensional array
            represent the world
        world : class World
            the world in which you want to draw the player
        blob_group : pygame.sprite.Group()

        lava_group : pygame.sprite.Group()

        exit_group : pygame.sprite.Group()

        coin_group : pygame.sprite.Group()

        platform_group : pygame.sprite.Group()

    """

    def __init__(self, data, blob_group, lava_group, exit_group, coin_group, platform_group):
        self.tile_list = []
        self.data = data
        self.platform_group = platform_group
        self.blob_group = blob_group
        self.lava_group = lava_group
        self.exit_group = exit_group
        self.coin_group = coin_group
        self.platform_group = platform_group
        self.make_world()
        self.level_completed = False

    def draw(self):
        """
        Fill the world with elementary blocks
        """

        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

    def make_world(self):
        """
        Parsing a two-dimensional array and filling in sprite groups
        """

        try:
            dirt_img = pygame.image.load('img/dirt.png').convert_alpha()
            grass_img = pygame.image.load('img/grass.png').convert_alpha()
        except pygame.error as err:
            raise SystemExit(err)

        # fill background with data
        for row_count, row in enumerate(self.data):
            for tile_count, tile in enumerate(row):
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = tile_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = tile_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                elif tile == 3:
                    blob = Enemy(tile_count * tile_size, row_count * tile_size + 15)
                    self.blob_group.add(blob)
                elif tile == 4:
                    platform = Platform(tile_count * tile_size, row_count * tile_size, 1, 0)
                    self.platform_group.add(platform)
                elif tile == 5:
                    platform = Platform(tile_count * tile_size, row_count * tile_size, 0, 1)
                    self.platform_group.add(platform)
                elif tile == 6:
                    lava = Lava(tile_count * tile_size, row_count * tile_size + (tile_size // 2))
                    self.lava_group.add(lava)
                elif tile == 7:
                    coin = Coin(tile_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    self.coin_group.add(coin)
                elif tile == 8:
                    level_exit = Exit(tile_count * tile_size, row_count * tile_size - (tile_size // 2))
                    self.exit_group.add(level_exit)


