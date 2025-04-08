# This is the module for the pause screen in the game. It handles the display of the pause screen and its functionality.

# Import required modules
import constants
import gamestate
import pygame

def pause_screen():
    # This function will display the pause screen and handle the functionality of the pause screen
    paused_text = constants.paused_font.render(f"---PAUSED---",True, constants.PAUSED_COLOR)
    paused_text_line2 = constants.big_font.render(f"Press -ESCAPE- to continue",True, constants.PAUSED_COLOR)
    paused_text_quit = constants.big_font.render(f"Press -Q- to return to the Title and lose all progress",True, constants.PAUSED_COLOR)
    gamestate.screen.blit(paused_text,(constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(paused_text)//2, constants.SCREEN_HEIGHT//2 - 50))
    gamestate.screen.blit(paused_text_line2,(constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(paused_text_line2)//2, constants.SCREEN_HALF_HEIGHT - 50 + constants.paused_font.get_linesize()))
    gamestate.screen.blit(paused_text_quit,(constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(paused_text_quit)//2, constants.SCREEN_HALF_HEIGHT - 50 + constants.paused_font.get_linesize() + constants.big_font.get_linesize()))