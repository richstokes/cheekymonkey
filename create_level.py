"""
This code creates the layout of level one.
"""
import pymunk
import arcade
import random
import sys
import logging
from random import randint
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

from physics_utility import (
    PymunkSprite,
)
# from constants import *
import constants
from k8s_kill_pod import count_pods

def create_floor(space, sprite_list):
    """ Create a bunch of blocks for the floor. """
    for x in range(-1200, 2200, constants.SPRITE_SIZE):
        y = constants.SPRITE_SIZE / 2
        sprite = PymunkSprite("./images/tiles/grassMid.png", x, y, scale=0.5, body_type=pymunk.Body.STATIC)
        sprite_list.append(sprite)
        space.add(sprite.body, sprite.shape)

    for x in range(-1200, 2200, constants.SPRITE_SIZE):
        y = constants.SPRITE_SIZE / 2 - constants.SPRITE_SIZE
        sprite = PymunkSprite("./images/tiles/grassCenter.png", x, y, scale=0.5, body_type=pymunk.Body.STATIC)
        sprite_list.append(sprite)
        space.add(sprite.body, sprite.shape)

def create_walls(space, sprite_list):
    """ Create side walls """
    # Left wall
    for y in range(96, 2000, constants.SPRITE_SIZE): # was 96 - constants.SPRITE_SIZE
        # x = constants.SPRITE_SIZE / 4
        x = -1000 - constants.SPRITE_SIZE
        sprite = PymunkSprite("./images/tiles/brickBrown.png", x, y, scale=0.5, body_type=pymunk.Body.STATIC)
        sprite_list.append(sprite)
        space.add(sprite.body, sprite.shape)
    # Right wall
    for y in range(96, 2000, constants.SPRITE_SIZE):
        # x = constants.SPRITE_SIZE / 4
        x = 1960 - constants.SPRITE_SIZE
        sprite = PymunkSprite("./images/tiles/brickBrown.png", x, y, scale=0.5, body_type=pymunk.Body.STATIC)
        sprite_list.append(sprite)
        space.add(sprite.body, sprite.shape)

def create_platform(space, sprite_list, start_x, y, count):
    """ Create a platform """
    for x in range(start_x, start_x + count * constants.SPRITE_SIZE + 1, constants.SPRITE_SIZE):
        sprite = PymunkSprite("./images/tiles/grassMid.png", x, y, scale=0.5, body_type=pymunk.Body.STATIC)
        sprite_list.append(sprite)
        space.add(sprite.body, sprite.shape)

def decorate_cactus(sprite_list, start_x, y, count):
    """ Create a cactus """
    for x in range(0, count):
        # print(x)
        X_POSITION = randint(-1000, 2000) # Initial random position
        POSITION_OK = False
        while POSITION_OK == False:
            if any(X_POSITION in range(s.center_x - 40, s.center_x + 40) for s in sprite_list):
                # print(X_POSITION, s)
                X_POSITION = randint(-1000, 2000)
            else:
                # print("Outside of if any, cactus position good!")
                POSITION_OK = True
                sprite = arcade.Sprite("./images/tiles/cactus.png", 0.5)
                sprite.center_y = y
                sprite.center_x = X_POSITION # Randomly place cacti 
                sprite_list.append(sprite)
                # print(len(sprite_list))

def decorate_cactus_large(sprite_list, start_x, y, count):
    """ Create a cactus """
    for x in range(0, count):
        # print(x)
        X_POSITION = randint(-1000, 2000) # Initial random position
        POSITION_OK = False
        while POSITION_OK == False:
            if any(X_POSITION in range(s.center_x - 100, s.center_x + 100) for s in sprite_list):
                # print(X_POSITION, s)
                X_POSITION = randint(-1000, 2000)
            else:
                # print("Outside of if any, cactus position good!")
                POSITION_OK = True
                sprite = arcade.Sprite("./images/tiles/cactus.png", 1)
                sprite.center_y = y
                sprite.center_x = X_POSITION # Randomly place cacti 
                sprite_list.append(sprite)                

def decorate_grass(sprite_list, start_x, y, count):
    """ Create some grass """
    for x in range(0, count):
        X_POSITION = randint(-1000, 2000) # Initial random position
        POSITION_OK = False
        while POSITION_OK == False:
                    if any(X_POSITION in range(s.center_x - 20, s.center_x + 20) for s in sprite_list):
                        # print(X_POSITION, s)
                        X_POSITION = randint(-1000, 2000)        
                    else:
                            # print("Outside of if any, grass position good!")
                            POSITION_OK = True 
                            sprite = arcade.Sprite("./images/tiles/grass_sprout.png", 0.5)
                            sprite.center_y = y
                            sprite.center_x = X_POSITION # Randomly place grass 
                            sprite_list.append(sprite)

def decorate_rock(sprite_list, start_x, y, count):
    """ Create some rocks """
    for x in range(0, count):
        X_POSITION = randint(-1000, 2000) # Initial random position
        POSITION_OK = False
        while POSITION_OK == False:
                    if any(X_POSITION in range(s.center_x - 10, s.center_x + 10) for s in sprite_list):
                        # print(X_POSITION, s)
                        X_POSITION = randint(-1000, 2000)        
                    else:
                            # print("Outside of if any, rock position good!")
                            POSITION_OK = True 
                            sprite = arcade.Sprite("./images/tiles/rock.png", 0.5)
                            sprite.center_y = y
                            sprite.center_x = X_POSITION # Randomly place rock 
                            sprite_list.append(sprite)

def decorate_rock_small(sprite_list, start_x, y, count):
    """ Create some rocks """
    for x in range(0, count):
        X_POSITION = randint(-1000, 2000) # Initial random position
        POSITION_OK = False
        while POSITION_OK == False:
                    if any(X_POSITION in range(s.center_x - 10, s.center_x + 10) for s in sprite_list):
                        # print(X_POSITION, s)
                        X_POSITION = randint(-1000, 2000)        
                    else:
                            # print("Outside of if any, rock position good!")
                            POSITION_OK = True 
                            sprite = arcade.Sprite("./images/tiles/rock.png", 0.2)
                            sprite.center_y = y
                            sprite.center_x = X_POSITION # Randomly place rock 
                            sprite_list.append(sprite)                            

def decorate_clouds(sprite_list, count):
    """ Create some clouds """
    for x in range(0, count):
        sprite = arcade.Sprite("./images/tiles/snow_pile.png", 3)
        sprite.center_y = randint(700, 1500)
        sprite.center_x = randint(-1500, 1500)
        sprite_list.append(sprite)

def create_level_1(space, static_sprite_list, dynamic_sprite_list, bg_sprite_list, fg_sprite_list):
    """ Create level one. """
    create_floor(space, static_sprite_list)
    create_walls(space, static_sprite_list)
    create_platform(space, static_sprite_list, 200, constants.SPRITE_SIZE * 3, 3)
    create_platform(space, static_sprite_list, 500, constants.SPRITE_SIZE * 6, 3)
    create_platform(space, static_sprite_list, 200, constants.SPRITE_SIZE * 9, 3)
    create_platform(space, static_sprite_list, -300, constants.SPRITE_SIZE * 3, 3)
    create_platform(space, static_sprite_list, -600, constants.SPRITE_SIZE * 6, 2)
    create_platform(space, static_sprite_list, -900, constants.SPRITE_SIZE * 9, 3)
    create_platform(space, static_sprite_list, -900, constants.SPRITE_SIZE * 3, 1)
    create_platform(space, static_sprite_list, -840, constants.SPRITE_SIZE * 13, 1)
    create_platform(space, static_sprite_list, 0, constants.SPRITE_SIZE * 13, 3)

    # Add some more to the right
    create_platform(space, static_sprite_list, 1040, constants.SPRITE_SIZE * 4, 5)
    create_platform(space, static_sprite_list, 1440, constants.SPRITE_SIZE * 6, 2)
    create_platform(space, static_sprite_list, 1640, constants.SPRITE_SIZE * 8, 1)
    create_platform(space, static_sprite_list, 800, constants.SPRITE_SIZE * 8, 1)

    # Add decorations
    decorate_cactus(bg_sprite_list, 0, 96, 8) # Cacti along ground
    decorate_cactus_large(bg_sprite_list, 0, 127, 3)
    decorate_grass(bg_sprite_list, 0, 95, 20)
    decorate_rock(bg_sprite_list, 0, 95, 3)
    decorate_rock_small(fg_sprite_list, 0, 73, 10)
    # decorate_clouds(bg_sprite_list, 10)

    # Create the stacks of boxes based on number of running pods or create random ones if offline mode
    # print(constants.OFFLINE_MODE)
    if constants.OFFLINE_MODE == True:
        CRATE_COUNT = constants.OFFLINE_CRATE_COUNT
    else:
        logging.info("Attempting to connect to Kubernetes API host..")
        try:
            CRATE_COUNT = count_pods()
        except:
            logging.error("Unable to connect to Kubernetes API host")
            logging.error("Check your Kubernetes environement/kubeconfig")
            logging.error("Or feel free to start with --offline yes set")
            sys.exit(1)

    logging.info("Creating %s crates", int(CRATE_COUNT * constants.CONTAINER_FACTOR))
    
    # Create crates in random locations, based on number of pods * CONTAINER_FACTOR
    i = 0
    while i < int(CRATE_COUNT * constants.CONTAINER_FACTOR):
        x = random.randrange(-1000, 1900)
        y = random.randrange(200, 7000) # Drop crates in from random heights
        # print(x)
        # print(y)    
        sprite = PymunkSprite("./images/tiles/boxCrate_double.png", x, y, scale=constants.SPRITE_SCALING, friction=0.6)
        dynamic_sprite_list.append(sprite)
        space.add(sprite.body, sprite.shape)
        # fall_sound = arcade.load_sound("./sounds/wooddrop.wav")
        # arcade.play_sound(fall_sound)
        i += 1

    logging.info("Number of crates created: %s", len(dynamic_sprite_list))