# Size of the window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# How many hits can the containers take before being destroyed?
CONTAINER_HEALTH = 1

# Container multiplication factor
# Will create (Actual number of running pods * CONTAINER_FACTOR) crates in game. Each crate represents one pod
CONTAINER_FACTOR = 1

# How many containers to spawn in offline mode
OFFLINE_CRATE_COUNT = 30

# Default friction used for sprites, unless otherwise specified
DEFAULT_FRICTION = 0.4

# Default mass used for sprites
DEFAULT_MASS = 1.2

# Gravity
GRAVITY = (0.0, -900.0)

# Player forces
PLAYER_FRICTION = 0.5
PLAYER_MOVE_FORCE = 700
PLAYER_JUMP_IMPULSE = 600
PLAYER_PUNCH_IMPULSE = 1100
PLAYER_SPEED_LIMIT = 800

# Grid-size
SPRITE_SIZE = 64

WORLD_SIZE = 4480 # Size of world
MAP_SIZE = 5760 # Size of map

# How close we get to the edge before scrolling
VIEWPORT_MARGIN = SPRITE_SIZE * 2

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
TEXTURE_LEFT_3 = 11
TEXTURE_RIGHT_3 = 12
TEXTURE_LEFT_4 = 13
TEXTURE_RIGHT_4 = 14

SPRITE_SCALING = 0.5
SCREEN_TITLE = 'Cheeky Monkey'

# Emitter stuffs
CENTER_POS = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
DEFAULT_SCALE = 0.3
DEFAULT_ALPHA = 96
DEFAULT_PARTICLE_LIFETIME = 3.0
PARTICLE_SPEED_FAST = 1.0
PARTICLE_SPEED_SLOW = 0.3
DEFAULT_EMIT_INTERVAL = 0.003
DEFAULT_EMIT_DURATION = 1.5
E_TEXTURE = "./images/misc/boom.png"

# Online/offline selector
## Set this via the command line argument: --offline yes
OFFLINE_MODE = False

# Namespace exclusions
## Set this via the command line argument: --excludes
EXCLUDES_LIST = []