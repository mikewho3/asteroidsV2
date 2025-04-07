# These variables are used to store the game state and are updated frequently by other modules

# Import required modules
import pygame

# Is the game active and the player is playing?
running = True
paused = False


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