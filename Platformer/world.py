"""
The world module: contains game classes
"""

import pygame
from pygame.locals import *
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


class Player():
    """
    A class used to represent the player

    Attributes:
        x : float
            x coordinate
        y : float
            y coordinate
        world : class World
            the world in which you want to draw the player
        blob_group : pygame.sprite.Group()

        lava_group : pygame.sprite.Group()

        exit_group : pygame.sprite.Group()

        coin_group : pygame.sprite.Group()

        platform_group : pygame.sprite.Group()

    """

    def __init__(self, x, y, world, blob_group, lava_group, exit_group, coin_group, platform_group):
        self.images_right = []
        self.images_left = []
        self.world = world
        self.blob_group = blob_group
        self.lava_group = lava_group
        self.exit_group = exit_group
        self.coin_group = coin_group
        self.platform_group = platform_group
        try:
            for num in range(1, 5):
                img_right = pygame.image.load(f'img/guy{num}.png').convert_alpha()
                img_right = pygame.transform.scale(img_right, (int(0.8*tile_size), int(1.6*tile_size)))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
            self.dead_image = pygame.image.load('img/ghost.png').convert_alpha()
        except pygame.error as err:
            raise SystemExit(err)
        self.sprite_index = 0
        self.image = self.images_right[self.sprite_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.walk_counter = 0
        self.in_air = True
        self.jump_vel_y = 0
        self.jumped = False
        self.direction = 1
        self.walk_cooldown = 5
        self.col_thresh = 20

    def change_world(self, new_world):
        """
        Change world for player

        Args: 
            new_world(two-dimensional array)

        Returns: 
            None
        """

        self.world = new_world

    def reset(self, x, y):
        """
        Reset player's condition
        Moves the player's sprite to the starting position and resets the effects

        Args: 
            x : float
                new x position
            y : float
                new y position

        Returns: 
            None
        """

        self.sprite_index = 0
        self.image = self.images_right[self.sprite_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.walk_counter = 0
        self.in_air = True
        self.jump_vel_y = 0
        self.jumped = False
        self.direction = 1
        self.walk_cooldown = 5
        self.col_thresh = 20

    def update(self, game_over, score, game_completed, sounds):
        """
        Updates the state on each frame of the player: tracks movement and collision with objects

        Args: 
            game_over : bool
                flag for determining the progress status of the game
            score : int
                Uses the current score counter
            game_complited : bool
                flag for determining the victory in the game
            sounds : dict[str, fx]
                dictionary with sounds for different situations

        Returns: 
            new conditions of game_over and score
        """

        dx, dy = 0, 0

        if not game_over and not game_completed:
            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                sounds['jump'].play()
                self.jump_vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                self.direction = -1
                dx -= 5
                self.walk_counter += 1
            if key[pygame.K_RIGHT]:
                self.direction = 1
                self.walk_counter += 1
                dx += 5
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.walk_counter = 0
                self.sprite_index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.sprite_index]
                if self.direction == -1:
                    self.image = self.images_left[self.sprite_index]

            # handle animation
            if self.walk_counter > self.walk_cooldown:
                self.walk_counter = 0
                self.sprite_index += 1
                if self.sprite_index >= len(self.images_right):
                    self.sprite_index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.sprite_index]
                if self.direction == -1:
                    self.image = self.images_left[self.sprite_index]

            # add gravity
            self.jump_vel_y += 1
            if self.jump_vel_y > 10:
                self.jump_vel_y = 10
            dy += self.jump_vel_y

            self.in_air = True
            # checking collisions with ground
            for tile in self.world.tile_list:
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground (collision with head) i.e jumping
                    if self.jump_vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.jump_vel_y = 0
                    # check if falling on ground
                    elif self.jump_vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.jump_vel_y = 0
                        self.in_air = False
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
            # checking collisions with platforms
            for platform in self.platform_group:
                # collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    if abs((self.rect.top + dy) - platform.rect.bottom) < self.col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # falling collision
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < self.col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # move sideqays with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, self.blob_group, False):
                game_over = True
                sounds['game_over'].play()
            if pygame.sprite.spritecollide(self, self.lava_group, False):
                game_over = True
                sounds['game_over'].play()
            # check for collision with exit
            if pygame.sprite.spritecollide(self, self.exit_group, False):
                self.world.level_completed = True
            # check for collision with coin
            if pygame.sprite.spritecollide(self, self.coin_group, True):
                score += 1
                sounds['coin'].play()
                # update player's coordinates
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0
        elif game_over:
            self.image = self.dead_image
            if self.rect.y > 4*tile_size:
                self.rect.y -= 5

        # draw player onto screen
        screen.blit(self.image, self.rect)

        return game_over, score


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
