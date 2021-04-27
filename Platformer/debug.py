import pygame
from game_constants import *
# draw primary blocks of world
def draw_grid():
	grids_number = screen_width//tile_size
	for line in range(0, grids_number):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
