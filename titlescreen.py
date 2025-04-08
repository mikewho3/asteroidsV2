# This is the module for the title screen in the game. It handles the display of the title screen and its functionality.

# Import required modules
import pygame
import constants
import gamestate
def title_screen():
    # This function will display the title screen and handle the functionality of the title screen
    title_text = constants.title_font.render(f"---Asteroids---",True, constants.TITLE_COLOR)
    title_text_line2 = constants.font.render(f"A Boot.Dev Project by MikeWho3",True, constants.TITLE_COLOR)
    title_text_line3 = constants.font.render(f"        Press -ENTER- to start",True, constants.TITLE_COLOR)
    menu_option_high_score = constants.big_font.render(f"High Scores | Press -H-",True, constants.HIGH_SCORE_COLOR)
    gamestate.screen.blit(title_text,(10,0)) # Blit the title text to the screen at the top left corner
    gamestate.screen.blit(title_text_line2,(0 + pygame.Surface.get_width(title_text)//2-100, 0 + constants.title_font.get_linesize())) # Blit the title text to the screen at the top left corner
    gamestate.screen.blit(title_text_line3,(0 + pygame.Surface.get_width(title_text)//2-100, 0 + constants.title_font.get_linesize() + constants.font.get_linesize())) # Blit the title text to the screen at the top left corner
    gamestate.screen.blit(menu_option_high_score,(10,200))