##############################################################################################################
# Asteroids Version 2 which started as V1.xx, a guided Project by Mike Wylder                                #
# Using Pygame and Boot.dev                                                                                  #
# https://www.boot.dev/u/mikewho3                                                                            #
#                                                                                                            #
# All Music/Sound used with permission under license from http://pixabay.com/service/license-summary/        #
##############################################################################################################

# import required modules and libraries
import pygame
import sys
import music
import gamestate
import player
import asteroidfield
import constants
import asteroids
import bullets
import statusbars
import shipdeath
import highscore
import pausescreen

def main():
    # Initialize Pygame
    pygame.init()
    # Start the game music
    music.load_music(file="asteroids.mp3", volume=0.5, play_time=-1)
    # Set the screen size and create the game window
    gamestate.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    # Set the game clock
    gamestate.clock = pygame.time.Clock()
    # Start the Game
    print(f"Starting Asteroids Version {constants.VERSION}")


    # This is where I defined status bars in the old version
    # Saving this spot for now.  I intend to make the status bars inside their own module


    # Temp home for ship and asteroid field creation
    # Create the asteroid field
    asfield = asteroidfield.AsteroidField()
    # Create the player ship
    gamestate.ship = player.Player.create_ship()

    # Begin the main game loop
    while gamestate.running:
        for event in pygame.event.get():  #for loop that stops the process if the game windows gets closed
            if event.type == pygame.QUIT:
                print("Game Over!")
                print(f"Game Score: {gamestate.score}")
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #if the escape key is pressed
                    if gamestate.ship.dead_timer > 0: #if the ship is dead, don't do anything
                        pass
                    else:
                        gamestate.paused = not gamestate.paused  # Pause/Unpause the game if the escape key is pressed
        # Fill the screen with the background color
        gamestate.screen.fill(constants.SCREEN_COLOR)
        # Initialize the high score list if it is None
        if gamestate.high_scores is None:
            gamestate.high_scores = highscore.load_high_scores()
            gamestate.high_scores = gamestate.high_scores[:10]  # Limit to top 10 scores
            gamestate.top_player_name = gamestate.high_scores[0][0]
            gamestate.top_player_score = gamestate.high_scores[0][1]
        # Create the player ship
        if gamestate.ship is None:
            gamestate.ship = player.Player.create_ship()
        if gamestate.asteroid_field is None:
            gamestate.asteroid_field = asteroidfield.AsteroidField()
        # Don't let the ship go off the screen
        if not gamestate.paused:
            if gamestate.ship.position.x < 0:
                gamestate.ship.position.x = constants.SCREEN_WIDTH
            if gamestate.ship.position.x > constants.SCREEN_WIDTH:
                gamestate.ship.position.x = 0
            if gamestate.ship.position.y < 0:
                gamestate.ship.position.y = constants.SCREEN_HEIGHT
            if gamestate.ship.position.y > constants.SCREEN_HEIGHT:
                gamestate.ship.position.y = 0
        # Update the game state
        if not gamestate.paused: #if the game is not paused, update the game state
            for x in constants.UPDATEABLE_GROUP:
                x.update(gamestate.dt)
        else:
            # If the game is paused, stop updating the game state
            # Display the pause screen
            pausescreen.pause_screen()

        for x in constants.DRAWABLE_GROUP:
            if isinstance(x, asteroids.Asteroid):
                #print(f"Debug: drawablegroup: draw asteroid")
                x.draw(gamestate.screen,constants.ASTEROID_COLOR)  #set the default color for asteroids
            elif isinstance(x, player.Player):
                #print(f"Debug: drawablegroup: draw player")
                x.draw(gamestate.screen,constants.PLAYER_COLOR)  #set the default color for the player ship
            elif isinstance(x, bullets.Shot):
                #print(f"Debug: drawablegroup: draw bullet")
                x.draw(gamestate.screen,constants.SHOT_COLOR)  #set the default color for the player ship
            else:
                #print(f"Debug: drawablegroup: draw ELSE")
                x.draw(gamestate.screen,[255,255,255]) #if I missed anything, draw it and make it white

        # Draw the status bar
        status_bar = statusbars.status_bar(constants.STATUSBAR_COLOR)
        gamestate.screen.blit(status_bar, (5, 5))  # Draw the status bar at the top left corner of the screen
        control_bar = statusbars.control_bar(constants.CONTROLBAR_COLOR)
        gamestate.screen.blit(control_bar, (5, 5 + constants.font.get_linesize()))  # Draw the control bar at the bottom left corner of the screen
        pygame.display.flip()  #updates the display



        # For Loop to check asteroids, bullets, and player collisions
        for space_rock in constants.ASTEROID_GROUP:
            #print(f"Debug: Entered space_rock asteroid group")
            for bullet in constants.BULLET_GROUP: #for loop to check for collisions between bullets and asteroids
                if space_rock.collision(bullet):  #if a bullet collides with the asteroid
                    bullet.kill()  #delete the bullet
                    space_rock.split()  #delete or split the asteroid
                    if space_rock.radius >= 60:
                        gamestate.score += 1 # add 1 point for a large asteroid
                    if space_rock.radius == 40:
                        gamestate.score += 2 # add 2 points for a medium asteroid
                    if space_rock.radius == 20:
                        gamestate.score += 3 # add 3 points for a small asteroid

            # This is where we check for collisions between the ship and asteroids
            if space_rock.collision(gamestate.ship):
                if gamestate.ship.invincible_timer > 0: #if the ship is invincible, don't do anything
                    continue # skip the rest of the loop
                continue_game = shipdeath.check_ship_death()  #check if the ship is dead
                if continue_game == True: # ship is dead but has lives left, continue the game
                    gamestate.ship.reset()  # reset the ship
                else:
                    if gamestate.score > gamestate.top_player_score: #if the score is greater than the top player score, save the high score
                        name = highscore.get_player_name(gamestate.screen, constants.font) #get the player name
                        highscore.save_high_score(name, gamestate.score) #save the high score
                    print("Game Over!")
                    print(f"Game Score: {gamestate.score}")
                    print(f"Current High Score: {gamestate.top_player_score} by {gamestate.top_player_name}")
                    sys.exit()

        gamestate.dt = gamestate.clock.tick(60) / 1000  #make the clock tick
        




if __name__ == "__main__":
    main()