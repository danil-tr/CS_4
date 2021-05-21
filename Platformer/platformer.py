"""
The platformer module: contains the initialization of the main game objects and the game loop

Run this script to start the game
"""

import pygame
import pickle
from pygame import mixer
from pygame.locals import *
from world import *
from constants import *
from functions import *
from debug import draw_grid


pygame.mixer.pre_init(48000, -16, 1, 1024)
mixer.init()
pygame.init()

# load sounds
pygame.mixer.music.load('sounds/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)

coin_fx = pygame.mixer.Sound('sounds/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('sounds/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('sounds/game_over.wav')
game_over_fx.set_volume(0.5)
sounds = {
    'coin': coin_fx,
    'jump': jump_fx,
    'game_over': game_over_fx
}

# define font
font_score = pygame.font.Font('fonts/BAUHS93.ttf', 30)
font = pygame.font.Font('fonts/BAUHS93.ttf', 70)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 50, 'img/restart_btn.png')
start_button = Button(screen_width // 2 - 350, screen_height // 2, 'img/start_btn.png')
exit_button = Button(screen_width // 2 + 150, screen_height // 2, 'img/exit_btn.png')
score_coin = Coin(tile_size // 2, tile_size // 2)

platform_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
coin_group.add(score_coin)

world = World(load_world(level), blob_group, lava_group, exit_group, coin_group, platform_group)
player = Player(100, screen_height - (50 + 80), world, blob_group, lava_group, exit_group, coin_group, platform_group)
background = Background(('img/sky.png', (0, 0)), ('img/sun.png', (100, 100)))

# game event loop
run = True
while run:
    clock.tick(fps)
    background.draw()

    if main_menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()
        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        if not game_over:
            blob_group.update()
            platform_group.update()
        lava_group.update()
        game_over, score = player.update(game_over, score, game_completed, sounds)
        draw_text(f'X {score}', font_score, white, tile_size - 10, 10)

        # if player has died
        if game_over:
            draw_text('GAME OVER', font, blue, (screen_width // 2) - 180, screen_height // 2 - 50)
            if restart_button.draw():
                reset_level(level, player, blob_group, lava_group, exit_group, coin_group, score_coin, platform_group)
                game_over = False
                score = 0

        # if player has completed the level
        if world.level_completed:
            level += 1
            if level <= max_levels:
                world = reset_level(level, player, blob_group, lava_group, exit_group, coin_group, score_coin,
                                    platform_group)
                player.change_world(world)
            else:
                game_completed = True
                draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2 - 50)
                if restart_button.draw():
                    game_completed = False
                    level = 0
                    score = 0
                    world = reset_level(level, player, blob_group, lava_group, exit_group, coin_group, score_coin,
                                        platform_group)
                    player.change_world(world)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
