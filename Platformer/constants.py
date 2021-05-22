"""
The constants module: contains global variables and game settings:

Options:
    fps(int) - fps option

    screen_width(int) - width of the screen

    screen_height(int) - height of the screen

    screen(pygame.display) - game screen from the pygame module

    tile_size(int) - size of the elementary screen block for filling the world with objects

    level(int) - current level of game

    max_levels(int) - number of levels to complete the game

    sound_volume(float) - soun volume from 0 to 1

"""

import pygame


# fps option
clock = pygame.time.Clock()
fps = 60

# set size of window
screen_width = 1000
screen_height = 1000

# make window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# define sound settings
sound_volume = 0.5

# define colours
white = (255, 255, 255)
blue = (0, 0, 255)

# define game variables
tile_size = 50
level = 1
max_levels = 7
game_over = False
game_completed = False
main_menu = True
score = 0
