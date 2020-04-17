import arcade
import logging
from constants import (
    DEFAULT_FRICTION,
    PLAYER_FRICTION,
    DEFAULT_MASS,
    SPRITE_SIZE,
    SPRITE_SCALING,
    TEXTURE_LEFT,
    TEXTURE_RIGHT,
    TEXTURE_JUMP_RIGHT,
    TEXTURE_JUMP_LEFT,
    TEXTURE_JUMP_UP,
    TEXTURE_IDLE,
    TEXTURE_PUNCH_LEFT,
    TEXTURE_PUNCH_RIGHT,
    TEXTURE_IDLE_2,
    TEXTURE_LEFT_2,
    TEXTURE_RIGHT_2,
    TEXTURE_LEFT_3,
    TEXTURE_RIGHT_3,
    TEXTURE_LEFT_4,
    TEXTURE_RIGHT_4,
    SCREEN_HEIGHT,
    SCREEN_WIDTH
)

import pymunk
import math

class Player(arcade.Sprite):

    def __init__(self,
                 filename,
                 center_x=0,
                 center_y=0,
                 scale=SPRITE_SCALING,
                 mass=DEFAULT_MASS * 2,
                 moment=None,
                 friction=PLAYER_FRICTION, # seeing if its better to use non-default value
                 body_type=pymunk.Body.DYNAMIC):

        super().__init__(filename, scale=scale, center_x=center_x, center_y=center_y)
        width = self.texture.width * scale
        height = self.texture.height * scale

        if moment is None:
            moment = pymunk.moment_for_box(mass, (width, height))

        self.body = pymunk.Body(mass, moment, body_type=body_type)
        self.body.position = pymunk.Vec2d(center_x, center_y)

        self.shape = pymunk.Poly.create_box(self.body, (width * 0.90, height * 0.90,), radius=0.8) # was 0.8
        self.shape.friction = friction
        self.shape.HITCOUNT = -100
        self.shape.name = "Player"
        self.punching = False

        self.set_hit_box([[-22, -60], [22, -60], [22, 50], [-22, 50]]) 
        # self._collision_radius = 0.5

        # Load in monkey textures
        try:
            self.textures = []
            # TEXTURE_LEFT
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_walk_1.png", mirrored=True)
            self.textures.append(texture)
            # TEXTURE_RIGHT
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_walk_1.png")
            self.textures.append(texture)
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_jump_4.png")
            self.textures.append(texture)
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_jump_4.png", mirrored=True)
            self.textures.append(texture)
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_armsup.png")
            self.textures.append(texture)
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_faceforward.png")
            self.textures.append(texture)
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_jump_swing_2.png", mirrored=True)
            self.textures.append(texture)
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_jump_swing_2.png")
            self.textures.append(texture)
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_armsup_happy.png")
            self.textures.append(texture)
            # TEXTURE_LEFT_2
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_walk_2.png", mirrored=True)
            self.textures.append(texture)
            # TEXTURE_RIGHT_2
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_walk_2.png")
            self.textures.append(texture)
            # TEXTURE_LEFT_3
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_walk_3.png", mirrored=True)
            self.textures.append(texture)
            # TEXTURE_RIGHT_3
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_walk_3.png")
            self.textures.append(texture)
            # TEXTURE_LEFT_4
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_walk_4.png", mirrored=True)
            self.textures.append(texture)
            # TEXTURE_RIGHT_4
            texture = arcade.load_texture("./images/Char_Monkey_Free_Images/Animations/monkey_walk_4.png")
            self.textures.append(texture)            

        except:
            logging.error("Unable to load textures")
            quit(1)

        self.scale = SPRITE_SCALING

    def update(self, FRAME_COUNT):
        ''' Updates player animations '''
        # If punching
        if self.punching == True and self.body.velocity[0] < 0:
            # print("punched left")
            # Play punching sound?
            self.texture = self.textures[TEXTURE_PUNCH_LEFT]
            # self.punching = False
            return
        elif self.punching == True and self.body.velocity[0] >= 0:
            # print("punched right")
            # Play punching sound?
            self.texture = self.textures[TEXTURE_PUNCH_RIGHT]
            # self.punching = False
            return

        # If not moving, set idle
        if self.body.velocity[0] == 0 and self.body.velocity[1] == 0:
            # print("Idle")
            if FRAME_COUNT % 30 == 0:
                self.texture = self.textures[TEXTURE_IDLE]
            elif FRAME_COUNT % 15 == 0:
                self.texture = self.textures[TEXTURE_IDLE_2]
            return

        # Figure out if we should animate walking left or right
        if self.body.velocity[0] < -20:
            if FRAME_COUNT % 60 == 0:
                self.texture = self.textures[TEXTURE_LEFT]
            elif FRAME_COUNT % 45 == 0:
                self.texture = self.textures[TEXTURE_LEFT_2]
            elif FRAME_COUNT % 30 == 0:
                self.texture = self.textures[TEXTURE_LEFT_3]
            elif FRAME_COUNT % 15 == 0:
                self.texture = self.textures[TEXTURE_LEFT_4]
            # return
        elif self.body.velocity[0] > 20:
            if FRAME_COUNT % 60 == 0:
                self.texture = self.textures[TEXTURE_RIGHT]
            elif FRAME_COUNT % 45 == 0:
                self.texture = self.textures[TEXTURE_RIGHT_2]
            elif FRAME_COUNT % 30 == 0:
                self.texture = self.textures[TEXTURE_RIGHT_3]
            elif FRAME_COUNT % 15 == 0:
                self.texture = self.textures[TEXTURE_RIGHT_4]
            # return

        # Detect jumping
        if self.body.velocity[1] > 5 and self.body.velocity[0] < 0: # Jumping left
            # print("left jump")
            self.texture = self.textures[TEXTURE_JUMP_LEFT]
        elif self.body.velocity[1] > 5 and self.body.velocity[0] > 0: # Jumping right
            # print("right jump")
            self.texture = self.textures[TEXTURE_JUMP_RIGHT]
        elif self.body.velocity[1] > 5 and self.body.velocity[0] == 0: # Jumping straight up
            # print("up jump")
            self.texture = self.textures[TEXTURE_JUMP_UP]
        elif self.body.velocity[1] < 5 and self.body.velocity[0] == 0: # Falling down
            self.texture = self.textures[TEXTURE_JUMP_UP]
            #TODO: Replace with a falling/downward jump texture
 