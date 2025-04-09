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
import gamemodes

def main():
    # Initialize Pygame
    pygame.init()
    # Set the game clock
    gamestate.clock = pygame.time.Clock()
    # Start the Game
    print(f"Starting Asteroids Version {constants.VERSION}")
    # Load the high scores
    highscore.update_high_scores() # attempt to load the high scores from the file
    

    # Begin the MAIN loop.  This loop runs EVERYTHING, the game and all menus.  Each is it's own seperate loop
    while gamestate.running:

        # Here is the main menu loop.  This loop will run when gamestate.main_menu is True and will display the title screen and handle all functionality of the title screen
        while gamestate.main_menu:
            # Start the game music
            if pygame.mixer.music.get_busy() == 0: #if the music is not playing, play the music
                music.load_music(file="title.mp3", volume=0.5, play_time=-1)
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
                    if event.key == pygame.K_h:
                        music.stop_music() #stop the music
                        gamestate.score_menu = True #set the score menu variable to True to start the high score menu
                        gamestate.main_menu = False
                    if event.key == pygame.K_g:
                        #music.stop_music() #stop the music # commented out to allow the music to play in the game mode menu
                        gamestate.mode_menu = True #set the score menu variable to True to start the game mode menu
                        gamestate.main_menu = False
                    if event.key == pygame.K_KP_ENTER:
                        #debuginfo = constants.big_font.get_linesize()
                        #print(f"Debug: big_font.get_linesize() = {debuginfo}")
                        pass
            titlescreen.title_screen()
            #titlescreen.title_screen() #display the title screen
            pygame.display.flip() #update the display

        # Here is the game mode menu loop.
        while gamestate.mode_menu:
            #if pygame.mixer.music.get_busy() == 0: #if the music is not playing, play the music # currently just playing main menu music
                #music.load_music(file="gamemode.mp3", volume=0.5, play_time=-1, set_pos=1) # currently there is no game mode music file, if the comment is removed it will crash the game
            if gamestate.screen is None:  # if the screen is None, create the screen
                gamestate.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            gamestate.screen.fill(constants.SCREEN_COLOR)  # fill the screen with the background color
            gamemodes.game_mode_screen()  # display the game mode menu
            pygame.display.flip()  # update the display
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # if the game window is closed, exit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        gamestate.difficulty = 1  # set the difficulty to easy
                    elif event.key == pygame.K_n:
                        gamestate.difficulty = 2 # set the difficulty to normal
                    elif event.key == pygame.K_h:
                        gamestate.difficulty = 3 # set the difficulty to hard
                    elif event.key == pygame.K_i:
                        gamestate.difficulty = 4 # set the difficulty to insane
                    elif event.key == pygame.K_o:
                        gamestate.difficulty = 5 # set the difficulty to I Want to Die
                    else: # if any other key is pressed, go back to the main menu
                        #music.stop_music()  # stop the music # commented out to allow the music to play in the game mode menu
                        gamestate.main_menu = True  # set the main menu variable to True to start the main menu loop
                        gamestate.mode_menu = False  # exit the high score menu
                    



        # Here is the high score menu loop.  This loop will run when gamestate.score_menu is True and will display the top 10 high scores from gamestate.high_scores using the highscore module with highscore.display_high_scores()
        while gamestate.score_menu:
            if pygame.mixer.music.get_busy() == 0: #if the music is not playing, play the music
                music.load_music(file="score.mp3", volume=0.5, play_time=-1, set_pos=1)
            if gamestate.screen is None:  # if the screen is None, create the screen
                gamestate.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            gamestate.screen.fill(constants.SCREEN_COLOR)  # fill the screen with the background color
            highscore.display_high_scores(gamestate.screen, constants.font)  # display the high scores
            pygame.display.flip()  # update the display
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # if the game window is closed, exit the game
                if event.type == pygame.KEYDOWN:
                    music.stop_music()  # stop the music
                    gamestate.main_menu = True  # set the main menu variable to True to start the main menu loop
                    gamestate.score_menu = False  # exit the high score menu

        # Begin the main game loop (active game loop)
        while gamestate.playing:
            if gamestate.screen is None: #if the screen is None, create the screen
                gamestate.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            # Fill the screen with the background color
            gamestate.screen.fill(constants.SCREEN_COLOR)
            # Set the difficulty
            if gamestate.is_difficulty_set == False: #if the difficulty is not set, set the difficulty
                if gamestate.difficulty == 1:
                    gamestate.player_starting_lives = 5
                    if gamestate.ship is not None:
                        gamestate.ship.lives = 5
                    gamestate.player_speed = 300
                    gamestate.asteroid_spawn_rate = 1
                    gamestate.player_can_use_abilities = True
                elif gamestate.difficulty == 2:
                    gamestate.player_starting_lives = 3
                    if gamestate.ship is not None:
                        gamestate.ship.lives = 3
                    gamestate.player_speed = 250
                    gamestate.asteroid_spawn_rate = 0.8
                    gamestate.player_can_use_abilities = True
                elif gamestate.difficulty == 3:
                    gamestate.player_starting_lives = 2
                    if gamestate.ship is not None:
                        gamestate.ship.lives = 2
                    gamestate.player_speed = 200
                    gamestate.asteroid_spawn_rate = 0.5
                    gamestate.player_can_use_abilities = True
                elif gamestate.difficulty == 4:
                    gamestate.player_starting_lives = 1
                    if gamestate.ship is not None:
                        gamestate.ship.lives = 1
                    gamestate.player_speed = 150
                    gamestate.asteroid_spawn_rate = 0.3
                    gamestate.player_can_use_abilities = True
                else:
                    gamestate.player_starting_lives = 0
                    if gamestate.ship is not None:
                        gamestate.ship.lives = 0
                    gamestate.player_speed = 100
                    gamestate.asteroid_spawn_rate = 0.1
                    gamestate.player_can_use_abilities = False
                gamestate.is_difficulty_set = True #set the difficulty to True so it doesn't set again
            # Create the player ship
            if gamestate.ship is None:
                gamestate.ship = player.Player.create_ship()
            # Create the asteroid field
            if gamestate.asteroid_field is None:
                gamestate.asteroid_field = asteroidfield.AsteroidField()
            # Start the game music
            if pygame.mixer.music.get_busy() == 0: #if the music is not playing, play the music
                music.load_music(file="asteroids.mp3", volume=0.5, play_time=-1)
            # Check the timer for the special music effect
            if gamestate.over_9000_playing == True:
                if gamestate.paused == False: #if the game is not paused, draw the over 9000 status bar
                    statusbars.over_9000() #display the over 9000 status bar
                if pygame.time.get_ticks() - gamestate.over_9000_time_started >= 7500:
                    pygame.mixer.music.fadeout(1500) #fade out the music
                    gamestate.over_9000_playing = False #set the over 9000 music to not playing
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
                    if event.key == pygame.K_q and gamestate.paused == True:
                        music.stop_music() # stop the music
                        gamestate.game_reset() #reset the game
                        gamestate.is_difficulty_set = False #reset the difficulty
                        gamestate.main_menu = True # if the game is paused and the Q key is pressed, go to the main menu
                        gamestate.playing = False # set the playing variable to False to exit the game loop
                        gamestate.paused = False # reset the paused variable to false before we exit the loop
                        break # exit the game loop NOW
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
                    x.draw(gamestate.screen,constants.ASTEROID_COLOR)  #set the default color for asteroids
                elif isinstance(x, player.Player):
                    x.draw(gamestate.screen,constants.PLAYER_COLOR)  #set the default color for the player ship
                elif isinstance(x, bullets.Shot):
                    x.draw(gamestate.screen,constants.SHOT_COLOR)  #set the default color for the player ship
                else:
                    x.draw(gamestate.screen,[255,255,255]) #if I missed anything, draw it and make it white

            # Draw the status bar and control bar
            statusbars.status_bar(constants.STATUSBAR_COLOR)
            statusbars.control_bar(constants.CONTROLBAR_COLOR)
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
                        if gamestate.score > 9000 and gamestate.over_9000_played == False: #if the score is over 9000 and the over 9000 music has not been played yet
                            music.stop_music() #stop the music
                            music.load_music(file="9000.mp3", volume=1, play_time=1, set_pos=5) #play the over 9000 music
                            gamestate.over_9000_playing = True #set the over 9000 music to playing
                            gamestate.over_9000_time_started = pygame.time.get_ticks() #set the time the over 9000 music started playing
                            pygame.mixer.music.queue("asteroids.mp3",loops=-1) #queue the asteroids music to play after the over 9000 music
                            gamestate.over_9000_played = True

                # This is where we check for collisions between the ship and asteroids
                if space_rock.collision(gamestate.ship):
                    if gamestate.ship.invincible_timer > 0: # if the ship is invincible, don't do anything
                        continue # skip the rest of the loop
                    continue_game = shipdeath.check_ship_death()  # check if the ship is dead
                    if continue_game == True: # ship is dead but has lives left, continue the game
                        gamestate.ship.reset()  # reset the ship
                    else: # ship is dead and no lives left, end the game
                        highscore.add_high_scores(gamestate.score) # update the high scores
                        print("Game Over!")
                        print(f"Game Score: {gamestate.score}")
                        print(f"Current High Score: {gamestate.top_player_score} by {gamestate.top_player_name}")
                        gamestate.game_reset() #reset the game
                        gamestate.is_difficulty_set = False #reset the difficulty
                        music.stop_music() #stop the music
                        gamestate.playing = False
                        gamestate.main_menu = True

            gamestate.dt = gamestate.clock.tick(60) / 1000  #make the clock tick
        




if __name__ == "__main__":
    main()