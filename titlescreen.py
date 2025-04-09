# This is the module for the title screen in the game. It handles the display of the title screen and its functionality.

# Import required modules
import pygame
import constants
import gamestate

def draw_title_line():
    # This function will draw the title line on the screen
    title_line = constants.title_font.render(f"---Asteroids---",True, constants.TITLE_COLOR)
    gamestate.screen.blit(title_line,(10,20)) # Blit the title text to the screen at the top left corner

def draw_text_line1():
    # This function will draw the first text line on the screen
    title_text_line = constants.font.render(f"A Boot.Dev Project by MikeWho3",True, constants.TITLE_COLOR)
    gamestate.screen.blit(title_text_line,(250, 20 + constants.title_font.get_linesize() - 20))

def draw_text_line2():
    # This function will draw the second text line on the screen
    title_text_line = constants.big_font.render(f"Play the Game | Press -ENTER-",True, constants.TITLE_COLOR)
    gamestate.screen.blit(title_text_line,(10, 164))

def draw_menu_option_high_score():
    # This function will draw the high score option on the screen
    menu_option_high_score = constants.big_font.render(f"High Scores | Press -H-",True, constants.HIGH_SCORE_COLOR)
    gamestate.screen.blit(menu_option_high_score,(10,200))

def draw_menu_option_game_mode():
    # This function will draw the game mode option on the screen
    menu_option_game_mode = constants.big_font.render(f"Game Mode | Press -G-",True, constants.GAME_MODE_COLOR)
    gamestate.screen.blit(menu_option_game_mode,(10,236))

def title_screen():
    # This function will display the title screen
    draw_title_line() # Call the function to draw the title line
    draw_text_line1() # Call the function to draw the first text line
    draw_text_line2() # Call the function to draw the second text line
    draw_menu_option_high_score() # Call the function to draw the high score option
    draw_menu_option_game_mode() # Call the function to draw the game mode option