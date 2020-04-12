import timeit
import os
import arcade
from pyglet.gl import GL_NEAREST, GL_LINEAR
import pymunk
import logging
import math
import time
import threading
import argparse
from create_level import create_level_1
from physics_utility import (
    PymunkSprite,
    check_grounding,
    resync_physics_sprites,
)
from player_utility import Player
from constants import *
import constants
from k8s_kill_pod import *

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


class PhysicsSprite(arcade.Sprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(filename, center_x=pymunk_shape.body.position.x, center_y=pymunk_shape.body.position.y)
        self.pymunk_shape = pymunk_shape
        self.HITCOUNT = 0

class CircleSprite(PhysicsSprite):
    def __init__(self, pymunk_shape, filename):
        super().__init__(pymunk_shape, filename)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.DARK_MOSS_GREEN)
        # Sprite list for balls
        self.ball_sprite_list: arcade.SpriteList[PhysicsSprite] = arcade.SpriteList()

        # -- Pymunk
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY

        # Physics joint used for grabbing items
        self.grab_joint = None

        # Lists of sprites
        self.dynamic_sprite_list = arcade.SpriteList[PymunkSprite]()
        self.static_sprite_list = arcade.SpriteList()
        self.static_sprite_list.is_static = True
        self.bg_sprite_list = arcade.SpriteList()
        self.bg_sprite_list.is_static = True
        self.fg_sprite_list = arcade.SpriteList()
        self.fg_sprite_list.is_static = True

        # Used for dragging shapes around with the mouse
        self.shape_being_dragged = None
        self.last_mouse_position = 0, 0

        # Draw and processing timings
        self.draw_time = 0
        self.processing_time = 0

        # Current force applied to the player for movement by keyboard
        self.force = (0, 0)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        # FPS Counter
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None

        # Holds the status message for pods killed
        self.LAST_POD_KILLED = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.is_jumping = False

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Build the level
        create_level_1(self.space, self.static_sprite_list, self.dynamic_sprite_list, self.bg_sprite_list, self.fg_sprite_list)

        # Set up the player
        x = 50
        y = int((SCREEN_HEIGHT / 2))
        # self.player = Player("./images/tiles/grassMid.png", x, y, scale=0.5, moment=pymunk.inf, mass=1)
        self.player = Player("./images/Char_Monkey_Free_Images/Animations/monkey_idle.png", x, y, scale=0.5, moment=pymunk.inf, mass=1)
        # self.player.center_x = SCREEN_WIDTH / 2
        # self.player.center_y = SCREEN_HEIGHT / 2
        self.dynamic_sprite_list.append(self.player)
        self.space.add(self.player.body, self.player.shape)
        # logging.info("Number of dynamic sprites created: %s", len(self.dynamic_sprite_list))

        # Load sounds
        self.jump_sound = arcade.load_sound("./sounds/jump3.wav")
        self.punch_sound = arcade.load_sound("./sounds/woodhit.wav")
        self.explode_sound = arcade.load_sound("./sounds/432668__dxeyes__crate-break-4.wav")
        self.ball_sound = arcade.load_sound("./sounds/laser4.wav")
        

    def on_draw(self):
        """ Render the screen. """
        self.frame_count += 1
        # This command has to happen before we start drawing
        arcade.start_render()

        # for sprite in self.dynamic_sprite_list: # Draw hitboxes for debugging
        #     sprite.draw_hit_box(arcade.color.RED, 3)
        # for sprite in self.static_sprite_list:
        #     sprite.draw_hit_box(arcade.color.BLUE, 3)
        # print("Number of dynamic sprites present:", len(self.dynamic_sprite_list))

        # Start timing how long rendering takes
        draw_start_time = timeit.default_timer()

        # Draw all the sprites
        self.bg_sprite_list.draw(filter=GL_NEAREST)
        self.static_sprite_list.draw(filter=GL_NEAREST)
        self.dynamic_sprite_list.draw(filter=GL_NEAREST)
        self.ball_sprite_list.draw()
        self.fg_sprite_list.draw(filter=GL_NEAREST)

        # Once per split second
        if self.frame_count % 20 == 0:
            self.player.punching = False # Unset the punching animation

        # Display FPS
        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"
        if self.fps_message:
            arcade.draw_text(self.fps_message, self.view_left + 10, self.view_bottom + 60, arcade.color.BLACK, 14)

        if self.frame_count % 60 == 0:
            self.last_time = time.time()

        # Display timings
        # output = f"Processing time: {self.processing_time:.3f}"
        # arcade.draw_text(output, 20 + self.view_left, SCREEN_HEIGHT - 60 + self.view_bottom, arcade.color.WHITE, 12)

        # output = f"Drawing time: {self.draw_time:.3f}"
        # arcade.draw_text(output, 20 + self.view_left, SCREEN_HEIGHT - 80 + self.view_bottom, arcade.color.WHITE, 12)

        # Display instructions
        # output = "Use the mouse to move boxes, space to punch, hold G to grab an item to the right."
        # arcade.draw_text(output, 20 + self.view_left, SCREEN_HEIGHT - 40 + self.view_bottom, arcade.color.WHITE, 12)

        # Display last pod killed
        if self.LAST_POD_KILLED:
            output = f"Last pod killed: {self.LAST_POD_KILLED}"
            arcade.draw_text(output, 20 + self.view_left, SCREEN_HEIGHT - 20 + self.view_bottom, arcade.color.WHITE, 12)

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_mouse_press(self, x, y, button, modifiers):
        """ Handle mouse down events """
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Store where the mouse is clicked. Adjust accordingly if we've
            # scrolled the viewport.
            self.last_mouse_position = (x + self.view_left, y + self.view_bottom)

            # See if we clicked on any physics object
            shape_list = self.space.point_query(self.last_mouse_position, 1, pymunk.ShapeFilter())

            # If we did, remember what we clicked on
            if len(shape_list) > 0:
                self.shape_being_dragged = shape_list[0]

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            # With right mouse button, shoot a heavy coin fast.
            mass = 30
            radius = 10
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            body.position = (x + self.view_left, y + self.view_bottom)
            body.velocity = 2000, 0
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            arcade.play_sound(self.ball_sound)
            self.space.add(body, shape)

            sprite = CircleSprite(shape, "./images/items/coinGold.png")
            self.ball_sprite_list.append(sprite)                

    def on_mouse_release(self, x, y, button, modifiers):
        """ Handle mouse up events """

        if button == arcade.MOUSE_BUTTON_LEFT:
            # Release the item we are holding (if any)
            self.shape_being_dragged = None

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle mouse motion events """

        if self.shape_being_dragged is not None:
            # If we are holding an object, move it with the mouse
            self.last_mouse_position = (x + self.view_left, y + self.view_bottom)
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = dx * 20, dy * 20

    def scroll_viewport(self):
        """ Manage scrolling of the viewport. """

        # Flipped to true if we need to scroll
        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_bndry:
            self.view_left -= left_bndry - self.player.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player.right > right_bndry:
            self.view_left += self.player.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player.top > top_bndry:
            self.view_bottom += self.player.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player.bottom
            changed = True

        if changed:
            arcade.set_viewport(int(self.view_left),
                                int(SCREEN_WIDTH + self.view_left),
                                int(self.view_bottom),
                                int(SCREEN_HEIGHT + self.view_bottom))
            # print(arcade.get_viewport())

    def on_update(self, delta_time):
        """ Update the sprites """

        # Keep track of how long this function takes.
        start_time = timeit.default_timer()
        
        # print(self.player.body.position)
        # # Print key states for debugging
        # logging.info("Left: %s", self.left_pressed)
        # logging.info("Right: %s", self.right_pressed)
        # logging.info("Up: %s", self.up_pressed)
        print(self.force, self.player.shape.friction)    
        print(self.player.body.velocity[0])
                
        # # Debug grounding
        # grounding = check_grounding(self.player) # find out if player is standing on ground
        # if grounding['body'] is not None:
        #     logging.info("Grounding: %s", grounding['normal'].x / grounding['normal'].y)
        # logging.info("Player friction: %s", self.player.shape.friction)

        # See if the player is standing on an item.
        # If she is, apply opposite force to the item below her.
        # So if she moves left, the box below her will have
        # a force to move to the right.
        grounding = check_grounding(self.player)
        if self.force[0] and grounding and grounding['body']:
            grounding['body'].apply_force_at_world_point((-self.force[0], 0), grounding['position'])

        # Apply force to monkey if direction keys pressed
        if self.up_pressed:
            grounding = check_grounding(self.player) # find out if player is standing on ground
            if grounding['body'] is not None and abs(
                grounding['normal'].x / grounding['normal'].y) <= self.player.shape.friction and self.player.body.velocity[1] < 1:
                # She is! Go ahead and jump
                self.player.body.apply_impulse_at_local_point((0, PLAYER_JUMP_IMPULSE))
                arcade.play_sound(self.jump_sound)
            # else:
            #     # print("Not on ground, cant jump")
            #     pass
        elif self.down_pressed and not self.up_pressed:
            # logging.info("Pressed down, not currently doing anything")
            # self.force = (0, 0)
            # self.player.shape.friction = PLAYER_FRICTION * 10 # act as a brake?
            pass

        if self.left_pressed and not self.right_pressed:
            if self.player.body.velocity[0] >= 100: # If player already running right, apply the brakes so we can switch directions faster
                self.force = (-4500, 0)
                self.player.shape.friction = PLAYER_FRICTION * 15
            else: # Add force to the player, and set the player friction to zero
                self.force = (-PLAYER_MOVE_FORCE, 0)
                self.player.shape.friction = 0
        elif self.right_pressed and not self.left_pressed:
            if self.player.body.velocity[0] <= -100: # If player already running left, apply the brakes so we can switch directions faster
                self.force = (4500, 0)
                self.player.shape.friction = PLAYER_FRICTION * 15
            else: # Add force to the player, and set the player friction to zero
                self.force = (PLAYER_MOVE_FORCE, 0)
                self.player.shape.friction = 0
        if not self.right_pressed and not self.left_pressed and not self.up_pressed:
            #If no directions pressed, stop player
            self.force = (0, 0)
            self.player.shape.friction = PLAYER_FRICTION * 15 # Greatly increase friction so player stops instead of sliding

        # print(self.force, self.player.shape.friction, self.player.body.velocity) # Debug physics

        # If we have force to apply to the player (from hitting the arrow
        # keys), apply it.
        self.player.body.apply_force_at_local_point(self.force, (0, 0))
        
        # Update player sprites    
        self.player.update(self.frame_count) # Pass in frame_count so we can decide which frame of animation to use
        
        # Check sprites
        for sprite in self.dynamic_sprite_list:
            if sprite.shape.body.position.y < 0: # Check for sprites that fall off the screen.
                # Remove sprites from physics space
                self.space.remove(sprite.shape, sprite.shape.body)
                # Remove sprites from physics list
                sprite.remove_from_sprite_lists()
            if sprite.shape.name == "Pymunk" and sprite.shape.HITCOUNT >= CONTAINER_HEALTH / 2: # Change texture of crate if 50% damaged
                broken_texture = arcade.load_texture("./images/tiles/boxCrate_single.png")
                sprite.texture = broken_texture
                # print("Damanged crate")
            # if sprite.shape.name:
            #     print(sprite.shape.name)
            if sprite.shape.name == "Pymunk" and sprite.shape.HITCOUNT >= CONTAINER_HEALTH: # Destroy container if hit CONTAINER_HEALTH times
                # logging.info("Destroying shape %s", sprite.shape)
                self.space.remove(sprite.body, sprite.shape)
                sprite.remove_from_sprite_lists()
                # print(len(self.space.shapes))
                arcade.play_sound(self.explode_sound)
                # Kill random pod!
                delete_thread = threading.Thread(target=self.kill_pod)
                delete_thread.start()

        # Check for balls that fall off the screen
        for sprite in self.ball_sprite_list:
            if sprite.pymunk_shape.body.position.y < 0:
                # Remove balls from physics space
                self.space.remove(sprite.pymunk_shape, sprite.pymunk_shape.body)
                # Remove balls from physics list
                sprite.remove_from_sprite_lists()

        # Move ball sprites to where physics objects are
        for sprite in self.ball_sprite_list:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)                     

        # Update physics
        # Use a constant time step, don't use delta_time
        # http://www.pymunk.org/en/latest/overview.html#game-loop-moving-time-forward
        self.space.step(1 / 60.0)

        # If we are dragging an object, make sure it stays with the mouse. Otherwise
        # gravity will drag it down.
        if self.shape_being_dragged is not None:
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = 0, 0

        # Resync the sprites to the physics objects that shadow them
        resync_physics_sprites(self.dynamic_sprite_list)

        # Scroll the viewport if needed
        self.scroll_viewport()

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time

    def kill_pod(self):
        ''' Deletes pod on kubernetes, then removes crate sprite from game '''
        if constants.OFFLINE_MODE == False:
            P1, P2 = list_pods()
            self.LAST_POD_KILLED = delete_pod(P1, P2)
   
    # def delayed_remove(self, sprite):        
    #     time.sleep(2)
    #     sprite.remove_from_sprite_lists()

    def punch(self):
        ''' Punch a crate '''
        # --- Punch left
        # See if we have a physics object to our left
        self.player.punching = True

        check_point = (self.player.right + 40, self.player.center_y)
        shape_list = self.space.point_query(check_point, 1, pymunk.ShapeFilter())
        
        # Apply force to any object to our left
        for shape in shape_list:
            # print(shape.shape.name)
            arcade.play_sound(self.punch_sound)
            shape.shape.body.apply_impulse_at_world_point((PLAYER_PUNCH_IMPULSE, PLAYER_PUNCH_IMPULSE),
                                                          check_point)
            # Hit counter
            shape.shape.HITCOUNT += 1
            # logging.info("Punched shape R%s x %s", shape.shape, shape.shape.HITCOUNT)

        # --- Punch right
        # See if we have a physics object to our left
        check_point = (self.player.left - 40, self.player.center_y)
        shape_list = self.space.point_query(check_point, 1, pymunk.ShapeFilter())

        # Apply force to any object to our right
        for shape in shape_list:
            arcade.play_sound(self.punch_sound)
            shape.shape.body.apply_impulse_at_world_point((-PLAYER_PUNCH_IMPULSE, PLAYER_PUNCH_IMPULSE),
                                                          check_point)
            # Hit counter
            shape.shape.HITCOUNT += 1
            # logging.info("Punched shape L%s x %s", shape.shape, shape.shape.HITCOUNT)

    def grab(self):
        """ Grab something """
        # See if we have a physics object to our right
        check_point = (self.player.right + 40, self.player.center_y)
        shape_list = self.space.point_query(check_point, 1, pymunk.ShapeFilter())

        # Create a joint for an item to our right
        for shape in shape_list:
            self.grab_joint = pymunk.PinJoint(self.player.shape.body, shape.shape.body)
            self.space.add(self.grab_joint)

    def let_go(self):
        """ Let go of whatever we are holding """
        if self.grab_joint:
            self.space.remove(self.grab_joint)
            self.grab_joint = None

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle keyboard presses. """
        if symbol == arcade.key.UP:
            self.up_pressed = True
        elif symbol == arcade.key.DOWN:
            self.down_pressed = True
        elif symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True        
        elif symbol == arcade.key.SPACE:
            self.punch()
        elif symbol == arcade.key.G:
            self.grab()
        # elif symbol == arcade.key.R:
        #     logging.info("Resetting")
        #     self.setup()

    def on_key_release(self, symbol: int, modifiers: int):
        """ Handle keyboard releases. """
        if symbol == arcade.key.UP:
            self.up_pressed = False
        elif symbol == arcade.key.DOWN:
            self.down_pressed = False
        elif symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False        
        # if symbol == arcade.key.RIGHT:
        #     # Remove force from the player, and set the player friction to a high number so she stops
        #     self.force = (0, 0)
        #     self.player.shape.friction = 15
        # elif symbol == arcade.key.LEFT:
        #     # Remove force from the player, and set the player friction to a high number so she stops
        #     self.force = (0, 0)
        #     self.player.shape.friction = 15
        elif symbol == arcade.key.G:
            self.let_go()


def main():
    # Process arguments
    parser = argparse.ArgumentParser(description='A Chaos Monkey for your Kubernetes cluster!')
    parser.add_argument("--offline", default="no", help="Set to yes to enable offline mode")

    args = parser.parse_args()
    offline = args.offline

    if offline != "no":
        logging.info("Starting in offline mode")
        constants.OFFLINE_MODE = True
    else:
        logging.info("Starting in online mode")
        constants.OFFLINE_MODE = False
    # print(constants.OFFLINE_MODE)

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

