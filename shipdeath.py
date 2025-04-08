# This file will be where we handle the player ship death and death screen

# Import required modules
import gamestate
import soundeffects
import constants
import pygame
import statusbars

def check_ship_death():
    # Check if the ship is dead
    if gamestate.ship.lives > 0:
        status_bar = statusbars.status_bar(constants.GAMEOVER_COLOR)
        gamestate.screen.blit(status_bar, (5, 5))  # Draw the status bar at the top left corner of the screen
        control_bar = statusbars.control_bar(constants.GAMEOVER_COLOR)
        gamestate.screen.blit(control_bar, (5, 5 + constants.font.get_linesize()))  # Draw the control bar at the bottom left corner of the screen
        soundeffects.play_soundeffect("lostlife.mp3",1,1500)
        gamestate.ship.lives -= 1
        gamestate.ship.invincible_timer = constants.PLAYER_INVINCIBILITY_TIMER
        gamestate.ship.dead_timer = constants.PLAYER_DEATH_TIMER
        died = constants.big_font.render(f"You Died! Extra Lives: {gamestate.ship.lives}",True, constants.GAMEOVER_COLOR)
        gamestate.screen.blit(died,(constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(died)//2, constants.SCREEN_HEIGHT//2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)
        return True  # Ship is dead but has lives left, return True to continue the game
    else:
        status_bar = statusbars.status_bar(constants.GAMEOVER_COLOR)
        gamestate.screen.blit(status_bar, (5, 5))  # Draw the status bar at the top left corner of the screen
        control_bar = statusbars.control_bar(constants.GAMEOVER_COLOR)
        gamestate.screen.blit(control_bar, (5, 5 + constants.font.get_linesize()))  # Draw the control bar at the bottom left corner of the screen
        soundeffects.play_soundeffect("gameover.mp3",1,1500)
        died = constants.big_font.render(f"----GAME OVER ----",True, constants.GAMEOVER_COLOR)
        gamestate.screen.blit(died,(constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(died)//2, constants.SCREEN_HEIGHT//2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)
        return False  # Ship is dead and no lives left, return False to end the game

