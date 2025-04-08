# This is the module for the title screen in the game. It handles the display of the title screen and its functionality.

# Import required modules
import pygame
import constants
import gamestate
def title_screen():
    # This function will display the title screen and handle the functionality of the title screen
    title_text = constants.big_font.render(f"---Asteroids---",True, constants.TITLE_COLOR)
    title_text_line2 = constants.font.render(f"A Boot.Dev Project by MikeWho3",True, constants.TITLE_COLOR)
    title_text_line3 = constants.font.render(f"        Press -ENTER- to start",True, constants.TITLE_COLOR)
    gamestate.screen.blit(title_text,(constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(title_text)//2, constants.SCREEN_HEIGHT//2 - 50))
    gamestate.screen.blit(title_text_line2,(constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(title_text_line2)//2, constants.SCREEN_HALF_HEIGHT + constants.big_font.get_linesize()))
    gamestate.screen.blit(title_text_line3,(constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(title_text_line2)//2, constants.SCREEN_HALF_HEIGHT + constants.big_font.get_linesize() + constants.font.get_linesize()))