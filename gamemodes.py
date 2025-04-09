# This is where we will define the game modes (difficulty) for the game

# Import the required modules
import pygame
import constants
import gamestate
import music
import titlescreen




# This function will handle the game mode selection screen
def game_mode_screen():
    # Draw the game title and author line
    titlescreen.draw_title_line()
    titlescreen.draw_text_line1()

    # Draw the game mode header
    header = constants.header_font_notbold.render("Game Modes", True, constants.GAME_MODE_COLOR)
    gamestate.screen.blit(header, (10, 200))

    # Draw the game mode options
    # Each game mode will be displayed with its description and the key to select it

    if gamestate.difficulty == 1:
        easy_text = constants.big_font.render(f"Easy | Press -E-  <---Selected",True, constants.GAMEOVER_COLOR)
    else:
        easy_text = constants.big_font.render(f"Easy | Press -E-",True, constants.GAME_MODE_COLOR)

    gamestate.screen.blit(easy_text,(10, 300))
    easy_description = constants.font.render("Extra Lives: 5 | Player Speed: 1.2x | Use Abilities: Yes | Asteroids: 1 / 1-seconds",True, constants.GAME_MODE_COLOR)
    gamestate.screen.blit(easy_description,(10, 300 + constants.big_font.get_linesize()))


    if gamestate.difficulty == 2:
        normal_text = constants.big_font.render(f"Normal | Press -N-  <---Selected",True, constants.GAMEOVER_COLOR)
    else:
        normal_text = constants.big_font.render(f"Normal | Press -N-",True, constants.GAME_MODE_COLOR)

    gamestate.screen.blit(normal_text,(10, 336 + constants.font.get_linesize()))
    normal_description = constants.font.render("Extra Lives: 3 | Player Speed: 1.0x | Use Abilities: Yes | Asteroids: 1 / 0.8-seconds",True, constants.GAME_MODE_COLOR)
    gamestate.screen.blit(normal_description,(10, 336 + constants.big_font.get_linesize() + constants.font.get_linesize()))


    if gamestate.difficulty == 3:
        hard_text = constants.big_font.render(f"Hard | Press -H-  <---Selected",True, constants.GAMEOVER_COLOR)
    else:
        hard_text = constants.big_font.render(f"Hard | Press -H-",True, constants.GAME_MODE_COLOR)

    gamestate.screen.blit(hard_text,(10, 372 + constants.big_font.get_linesize()))
    hard_description = constants.font.render("Extra Lives: 2 | Player Speed: 0.8x | Use Abilities: Yes | Asteroids: 1 / 0.5-seconds",True, constants.GAME_MODE_COLOR)
    gamestate.screen.blit(hard_description,(10, 372 + constants.big_font.get_linesize()*2))


    if gamestate.difficulty == 4:
        insane_text = constants.big_font.render(f"Insane | Press -I-  <---Selected",True, constants.GAMEOVER_COLOR)
    else:
        insane_text = constants.big_font.render(f"Insane | Press -I-",True, constants.GAME_MODE_COLOR)

    gamestate.screen.blit(insane_text,(10, 408 + constants.big_font.get_linesize() + constants.font.get_linesize()))
    insane_description = constants.font.render("Extra Lives: 1 | Player Speed: 0.6x | Use Abilities: Yes | Asteroids: 1 / 0.3-seconds",True, constants.GAME_MODE_COLOR)
    gamestate.screen.blit(insane_description,(10, 408 + constants.big_font.get_linesize() + constants.font.get_linesize()*3.5))


    if gamestate.difficulty == 5:
        impossible_text = constants.big_font.render(f"I Want to Die | Press -O-  <---Selected",True, constants.GAMEOVER_COLOR)
    else:
        impossible_text = constants.big_font.render(f"I Want to Die | Press -O-",True, constants.GAME_MODE_COLOR)

    gamestate.screen.blit(impossible_text,(10, 444 + constants.big_font.get_linesize()*2))
    die_description = constants.font.render("Extra Lives: -!-ZERO-!- | Player Speed: 0.4x | Use Abilities: DISABLED | Asteroids: 1 / 0.1-seconds",True, constants.GAME_MODE_COLOR)
    gamestate.screen.blit(die_description,(10, 444 + constants.big_font.get_linesize() + constants.font.get_linesize()*4.5))

    # Draw the instructions for returning to the menu
    return_to_menu_text = constants.big_font.render(f"Return to Menu | Press -Any Other Keys-",True, constants.GAME_MODE_COLOR)
    gamestate.screen.blit(return_to_menu_text,(constants.SCREEN_WIDTH//2 - return_to_menu_text.get_width()//2, 588 + constants.big_font.get_linesize()*4))