# import required modules
import pygame
import gamestate

def play_soundeffect(file,volume=0.6,time_limit=1500):
    # Initialize the mixer
    pygame.mixer.init()
    
    # Load the sound effect file
    sound = pygame.mixer.Sound(file)
    
    # Set the volume (0.0 to 1.0)
    sound.set_volume(volume)
  
    # Play the sound effect
    sound.play(maxtime=time_limit)

def get_sound_timer():
    if gamestate.sound_effect_timer <= 0:
        return True
    else:
        return False