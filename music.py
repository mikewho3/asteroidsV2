# import required modules
import pygame

def load_music(file="asteroids.mp3",volume=0.5,play_time=-1,set_pos=None,fadeout=None,fadetimer=None):
    # Initialize the mixer
    pygame.mixer.init()

    # Load the music file
    pygame.mixer.music.load(file)

    # Set the volume (0.0 to 1.0)
    pygame.mixer.music.set_volume(volume)  

    # Play the music for the specified time (in seconds)
    pygame.mixer.music.play(play_time)

    # Set the position in seconds (optional)
    if set_pos is not None:
        # Note: set_pos is in seconds, and pygame.mixer.music.set_pos() expects a float
        # representing the time in seconds to start playing from.
        if isinstance(set_pos, (int, float)):
            pygame.mixer.music.set_pos(float(set_pos))
        else:
            raise ValueError("set_pos must be a float representing seconds.")

    # Fade out the music (optional)
    if fadeout is not None and fadetimer is not None:
        pygame.time.wait(fadetimer)  # Wait for the specified time before fading out
        pygame.mixer.music.fadeout(fadeout)




def stop_music():
    # Stop the music
    pygame.mixer.music.stop()