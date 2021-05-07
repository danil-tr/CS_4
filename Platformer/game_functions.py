import pygame
import pickle
from os import path
from game_objects import *
from game_constants import *

#display score
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#load world data
def load_world(level):
    data_path = path.join('levels', f'level{level}_data')

    if path.exists(data_path):
        with open(data_path, 'rb') as pickle_in:
            world_data = pickle.load(pickle_in)
    else:
        print("Oops")
    return world_data

#function to reset level
def reset_level(level, player, blob_group, lava_group, exit_group, coin_group, score_coin, platform_group):
    player.reset(100, screen_height - 130)
    platform_group.empty()
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()
    coin_group.add(score_coin)
    world_data = load_world(level)
    world = World(world_data, blob_group, lava_group, exit_group, coin_group, platform_group)
    return world
