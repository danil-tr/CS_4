import pygame
#fps option
clock = pygame.time.Clock()
fps = 60

#set size of window
screen_width = 1000
screen_height = 1000 

#make window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

#define colours
white = (255, 255, 255)
blue = (0, 0, 255)

#define game variables
tile_size = 50
level = 1
max_levels = 7
game_over = False
game_completed = False
main_menu = True
score = 0
