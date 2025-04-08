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
import gamestate
import player
import music
import asteroidfield
import constants
import asteroids
import bullets
import statusbars
import shipdeath
import highscore
import pausescreen
import titlescreen

def main():
    # Initialize Pygame
    pygame.init()
    # Set the game clock
    gamestate.clock = pygame.time.Clock()
    # Start the Game
    print(f"Starting Asteroids Version {constants.VERSION}")
    gamestate.high_scores = highscore.load_high_scores()
    gamestate.high_scores = gamestate.high_scores[:10]  # Limit to top 10 scores
    gamestate.top_player_name = gamestate.high_scores[0][0]
    gamestate.top_player_score = gamestate.high_scores[0][1]
    while gamestate.running:
        # Start the game music
        if pygame.mixer.music.get_busy() == 0: #if the music is not playing, play the music
            music.load_music(file="title.mp3", volume=0.5, play_time=-1)
        while gamestate.main_menu:
            if gamestate.screen is None: #if the screen is None, create the screen
                gamestate.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            gamestate.screen.fill(constants.SCREEN_COLOR) #fill the screen with the background color
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() #if the game window is closed, exit the game
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        music.stop_music() #stop the music
                        gamestate.playing = True #set the running variable to True to start the game
                        gamestate.main_menu = False
            titlescreen.title_screen() #display the title screen
            pygame.display.flip() #update the display

        # Begin the main game loop (active game loop)
        while gamestate.playing:
            # Start the game music
            if pygame.mixer.music.get_busy() == 0: #if the music is not playing, play the music
                music.load_music(file="asteroids.mp3", volume=0.5, play_time=-1)
            for event in pygame.event.get():  #for loop that stops the process if the game windows gets closed
                if event.type == pygame.QUIT:
                    print("Game Over!")
                    print(f"Game Score: {gamestate.score}")
                    sys.exit() #if the game window is closed, exit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #if the escape key is pressed
                        if gamestate.ship.dead_timer > 0: #if the ship is dead, don't do anything
                            pass
                        else:
                            gamestate.paused = not gamestate.paused  # Pause/Unpause the game if the escape key is pressed
            if gamestate.screen is None: #if the screen is None, create the screen
                gamestate.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            # Fill the screen with the background color
            gamestate.screen.fill(constants.SCREEN_COLOR)
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
                if gamestate.running:
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
                        music.stop_music() #stop the music
                        for big_space_rock in constants.UPDATEABLE_GROUP: #reset the asteroids
                            if isinstance(big_space_rock, asteroids.Asteroid):
                                big_space_rock.kill()
                        for asfield in constants.UPDATEABLE_GROUP: #reset the asteroid field
                            if isinstance(asfield, asteroidfield.AsteroidField):
                                asfield.kill()
                        gamestate.asteroid_field = None #reset the asteroid field
                        gamestate.ship.reset()
                        gamestate.score = 0 #reset the score
                        gamestate.ship.lives = constants.PLAYER_STARTING_LIVES #reset the ship lives
                        gamestate.playing = False
                        gamestate.main_menu = True

            gamestate.dt = gamestate.clock.tick(60) / 1000  #make the clock tick
        




if __name__ == "__main__":
    main()