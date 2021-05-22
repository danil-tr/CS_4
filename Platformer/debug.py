"""
The debug module: contains functions for game development
"""

import pygame
from constants import *


def draw_grid():
    """
    When called, draws a grid of elementary blocks

    Args: None

    Returns: None
    """
    grids_number = screen_width // tile_size
    for line in range(0, grids_number):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
