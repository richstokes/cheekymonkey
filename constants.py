# Size of the window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# How many hits can the containers take before being destroyed?
CONTAINER_HEALTH = 4

# Container multiplication factor
# Will create (Actual number of running pods * CONTAINER_FACTOR) crates in game. Each crate represents one pod
CONTAINER_FACTOR = 0.4

# Default friction used for sprites, unless otherwise specified
DEFAULT_FRICTION = 0.2

# Default mass used for sprites
DEFAULT_MASS = 1.2

# Gravity
GRAVITY = (0.0, -900.0)

# Player forces
PLAYER_FRICTION = 10
PLAYER_MOVE_FORCE = 700 # was 700
PLAYER_JUMP_IMPULSE = 600
PLAYER_PUNCH_IMPULSE = 1000

# Grid-size
SPRITE_SIZE = 64

# How close we get to the edge before scrolling
VIEWPORT_MARGIN = 120

# Player textures
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_JUMP_RIGHT = 2
TEXTURE_JUMP_LEFT = 3
TEXTURE_JUMP_UP = 4
TEXTURE_IDLE = 5
TEXTURE_PUNCH_LEFT = 6
TEXTURE_PUNCH_RIGHT = 7
TEXTURE_IDLE_2 = 8
TEXTURE_LEFT_2 = 9
TEXTURE_RIGHT_2 = 10

SPRITE_SCALING = 0.5
SCREEN_TITLE = 'Cheeky Monkey'

# Online/offline selector
## Set this via the command line argument: --offline yes
OFFLINE_MODE = False