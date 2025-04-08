# import required modules
import pygame

def load_music(file="asteroids.mp3",volume=0.5,play_time=-1,set_pos=None):
    # Initialize the mixer
    pygame.mixer.init()

    # Load the music file
    pygame.mixer.music.load(file)

    # Set the volume (0.0 to 1.0)
    pygame.mixer.music.set_volume(volume)  

    # Play the music for the specified time (in seconds)
    pygame.mixer.music.play(play_time)  

def stop_music():
    # Stop the music
    pygame.mixer.music.stop()