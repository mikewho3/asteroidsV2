# Constants.py is the root file in the import tree
# Import pygame module
import pygame
# Constant values are defined here

# Game Version
VERSION = 2.10
# Set Fonts
pygame.font.init()
title_font = pygame.font.Font(None, 150)
title_font.set_bold(True)
title_font.set_italic(True)
big_font = pygame.font.Font(None, 48)
font = pygame.font.Font(None, 19)
medium_font = pygame.font.Font(None,18)
small_font = pygame.font.Font(None, 16)

# Set Default Containers and Groups(these will be assigned inside the indicated classes)
UPDATEABLE_GROUP = pygame.sprite.Group()
DRAWABLE_GROUP = pygame.sprite.Group()
ASTEROID_GROUP = pygame.sprite.Group()
BULLET_GROUP = pygame.sprite.Group()

PLAYER_CONTAINERS = (UPDATEABLE_GROUP,DRAWABLE_GROUP)
ASTEROID_CONTAINERS = (UPDATEABLE_GROUP,DRAWABLE_GROUP,ASTEROID_GROUP)
ASTEROID_FIELD_CONTAINERS = (UPDATEABLE_GROUP)
BULLET_CONTAINERS = (UPDATEABLE_GROUP,DRAWABLE_GROUP,BULLET_GROUP)

# Screen Constants
# These constants are used to define the dimensions of the game screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_HALF_WIDTH = SCREEN_WIDTH // 2
SCREEN_HALF_HEIGHT = SCREEN_HEIGHT // 2

# Asteroid constants
# These constants are used to define the properties of asteroids in the game
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_LIFESPAN = 20
ASTEROID_VELOCITY_MULTIPLIER = 1.5

# Player Constants
# These constants are used to define the properties of the player in the game
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3
PLAYER_STARTING_LIVES = 3
PLAYER_INVINCIBILITY_TIMER = 5.5
PLAYER_DEATH_TIMER = 3.1
TRI_SHOT_DURATION = 8
KEY_LOCK_TIMER = 1

# Player Ability Cooldowns
# These constants are used to define the cooldowns for various player abilities in the game
# These values are in seconds
DEATH_FLOWER_COOLDOWN = 30
BULLET_STREAM_COOLDOWN = 15
BULLET_STREAM_DURATION = 8
TRI_SHOT_COOLDOWN = 20

# Color Constants
# These constants are used to define the colors used in the game
# The colors are represented as RGB values
PLAYER_COLOR = [255,255,255]
ASTEROID_COLOR = [255,255,255]
GAMEOVER_COLOR = [255,0,0]
SCREEN_COLOR = [0,0,0]
SHOT_COLOR = [155,0,155]
STATUSBAR_COLOR = [255,255,255]
CONTROLBAR_COLOR = [255,255,255]
PAUSED_COLOR = [255,255,0]
TITLE_COLOR = [0,63,255]

# Shot Constants
# These constants are used to define the properties of shots in the game
SHOT_RADIUS = 5
SHOT_LIFESPAN = 3.5
TRI_SHOT_ROTATION = 15

# Bar Locations
# These constants are used to define the locations of various bars in the game
BOTTOM_BAR_LOC_X = 10
BOTTOM_BAR_LOC_Y = SCREEN_HEIGHT - 16

# Sound Delay
# This constant is used to define the delay between sound effects in the game
# This value is in seconds
# Not all sounds will have this delay
SOUND_DELAY = 1.0
