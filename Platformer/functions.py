"""
The function module: contains the necessary functions for working with 
the World class and displaying text on the screen
"""

import json
from os import path
from world import World
from constants import *


def draw_text(text, font, text_col, x, y):
    """
    Draws text to the screen when the function is called

    Args:
        text (str):  Output text

        font (pygame.font): Font for text

        text_col (tuple[Literal[255], Literal[255], Literal[255]]): RGB color

        x (float): x coordinate

        y (float): y coordinate

    Returns:
        None
    """

    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def load_world(level, stage):
    """
    Pulls data from a json file and returns it as a two-dimensional array

    Args:
        level(int): level of stage to be load
        stage(int): game's stage number
    Returns:
        two-dimensional array with representation of the world
    """
    if (stage == 1):
        stage_path = path.join('levels', 'green_hills_stage.json')

    level_index = f'level{level}'

    with open(stage_path, 'rb') as stage_file:
        world_data = json.load(stage_file)

    return world_data[level_index]


# function to reset level
def reset_level(level, player, blob_group, lava_group, exit_group, coin_group, score_coin, platform_group):
    """
    Reloads the level when the player is defeated

    Input: accepts a group of sprites associated with the world

    Args:
        level(int):

        player(pygame.sprite.Group()): 

        blob_group(pygame.sprite.Group()):

        lava_group(pygame.sprite.Group()):

        exit_group(pygame.sprite.Group()):

        coin_group(pygame.sprite.Group():

        score_coin(pygame.sprite.Group()):

        platform_group(pygame.sprite.Group()):

    Returns:
        world (World): instance of the class World with reseted level
    """
    player.reset(2*tile_size, screen_height - 2.6*tile_size)

    platform_group.empty()
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()
    coin_group.add(score_coin)

    world_data = load_world(level,stage)
    world = World(world_data, blob_group, lava_group, exit_group, coin_group, platform_group)

    return world
