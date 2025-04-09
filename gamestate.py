# These variables are used to store the game state and are updated frequently by other modules

# Import required modules
import pygame
import constants
import asteroids
import asteroidfield
import bullets

# Is the game active and the player is playing?
running = True # This variable is used to control the main game loop and all other game loops
paused = False # Is the game active but paused? This variable is used to control the pause screen and the game loop
main_menu = True # Is the game in the main menu? This variable is used to control the main menu loop
playing = False # Is the game active and the player is playing? This variable is used to control the active game loop
score_menu = False # Is the game in the high score menu? This variable is used to control the high score menu loop


# Define the ship here.  This will be changed when the player creates a ship and starts a game mode
ship = None

# Define the screen here
screen = None

# Define the clock here
clock = None
dt = 0 # This is the delta time variable

# Define the asteroid field here.  This will be changed when the player creates a ship and starts a game mode
asteroid_field = None

# Define the high score list here.  It will be loaded from a file when the game starts, it starts as None
high_scores = None
top_player_name = None # This will be the name of the player with the highest score
top_player_score = None # This will be the score of the player with the highest score

# Game Score
score = 0
over_9000_played = False # This variable is used to control the over 9000 sound effect
over_9000_playing = False # This variable is used to detect if the sound effect is currently playing
over_9000_time_started = 0 # This variable is used to store the time the sound effect started playing

# Game Difficulty Variable
difficulty = 1

# Asteroid Variables
asteroid_spawn_rate = 0.8

# Sound Effect Timer
sound_effect_timer = 0

# Key Lock Variables
# These variables are used to control the key lock state
key_lock = 0
key_lock_kp_enter = 0
key_lock_kp_plus = 0
key_lock_t = 0
key_lock_f = 0
key_lock_v = 0
key_lock_1 = 0
key_lock_2 = 0
key_lock_5 = 0
key_lock_spacebar = 0


def game_reset():
    for big_space_rock in constants.UPDATEABLE_GROUP: #reset the asteroids
        if isinstance(big_space_rock, asteroids.Asteroid):
            big_space_rock.kill()
        for asfield in constants.UPDATEABLE_GROUP: #reset the asteroid field
            if isinstance(asfield, asteroidfield.AsteroidField):
                asfield.kill()
        for bullet in constants.UPDATEABLE_GROUP: #reset the asteroid field
            if isinstance(bullet, bullets.Shot):
                bullet.kill()
    asteroid_field = None #reset the asteroid field
    ship.reset()
    score = 0 #reset the score
    ship.lives = constants.PLAYER_STARTING_LIVES #reset the ship lives