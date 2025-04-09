# This is the file where I will create the status bars for the game.
# Import the required modules
import gamestate
import constants

def status_bar(color):


    if gamestate.ship.invincible_timer <= 0:  #Lets not display negative values on the timer shall we?
        formatted_timer = "0"


    else:
        formatted_timer = f"{gamestate.ship.invincible_timer:.1f}"  #Format the timer to only show 1 decimal place
    status_text = f"Score: {gamestate.score} | Extra Lives: {gamestate.ship.lives} | High Score: {gamestate.top_player_score} by {gamestate.top_player_name} | Death Blossom: {gamestate.ship.death_flower}" # Format the score and lives
    
    
    if gamestate.ship.spin_cooldown > 0: # Check if the spin cooldown is greater than 0
        formatted_death_flower = f"{gamestate.ship.spin_cooldown:.1f}" # Format the spin cooldown to only show 1 decimal place
        status_text += f" {formatted_death_flower}" # Add the spin cooldown to the status text
    status_text += f" | Bullet Stream: "
    
    
    if gamestate.ship.bullet_stream_cooldown > 0: # Check if the bullet stream cooldown is greater than 0
        formatted_bullet_stream = f"{gamestate.ship.bullet_stream_msg}{gamestate.ship.bullet_stream_cooldown:.1f}/s" # Format the bullet stream cooldown to only show 1 decimal place
        status_text += formatted_bullet_stream # Add the bullet stream cooldown to the status text
    
    
    if gamestate.ship.is_bullet_stream: # Check if the ship is in bullet stream mode
        formatted_bullet_stream_a = f"{gamestate.ship.bullet_stream_msg}{gamestate.ship.shot_timer_bypass:.1f}/s" # Format the bullet stream duration to only show 1 decimal place
        status_text += formatted_bullet_stream_a # Add the bullet stream duration to the status text
    
    
    if gamestate.ship.bullet_stream_cooldown <= 0 and gamestate.ship.is_bullet_stream == False: # Check if the bullet stream cooldown is less than or equal to 0 and the ship is not in bullet stream mode
        formatted_bullet_stream_b = f"{gamestate.ship.bullet_stream_msg}" # Add the bullet stream message to the status text
        status_text += formatted_bullet_stream_b 
    status_text += f" | Triple Shot: "
    
    
    if gamestate.ship.tri_shot_cooldown > 0: # Check if the triple shot cooldown is greater than 0
        formatted_tri_shot = f"{gamestate.ship.tri_shot_msg}{gamestate.ship.tri_shot_cooldown:.1f}/s"   # Format the triple shot cooldown to only show 1 decimal place
        status_text += formatted_tri_shot # Add the triple shot cooldown to the status text
    
    
    if gamestate.ship.is_tri_shot: # Check if the ship is in triple shot mode
        formatted_tri_shot_a = f"{gamestate.ship.tri_shot_msg}{gamestate.ship.tri_shot_bypass:.1f}/s" # Format the triple shot duration to only show 1 decimal place
        status_text += formatted_tri_shot_a # Add the triple shot duration to the status text
    
    
    if gamestate.ship.tri_shot_cooldown <= 0 and gamestate.ship.is_tri_shot == False: # Check if the triple shot cooldown is less than or equal to 0 and the ship is not in triple shot mode
        formatted_tri_shot_b = f"{gamestate.ship.tri_shot_msg}" # Add the triple shot message to the status text
        status_text += formatted_tri_shot_b
    
    
    if gamestate.ship.invincible_timer > 0: # Check if the invincible timer is greater than 0
        status_text += f" | Invincible for {formatted_timer}/s" # Add the invincible timer to the status text
    
    
    render = constants.font.render(status_text, True, color) # Render the status text

    gamestate.screen.blit(render, (5, 5))  # Draw the status bar at the top left corner of the screen



def control_bar(color):
    control_text = f"Controls | Move: -W- -A- -S- -D- | Fire: -SPACEBAR- | Death Blossom: -F- | Bullet Stream: -V- THEN -SPACEBAR- | Triple Shot: -T-" # Format the control text
    render = constants.font.render(control_text, True, color) # Render the control text
    gamestate.screen.blit(render, (5, 5 + constants.font.get_linesize()))  # Draw the control bar at the bottom left corner of the screen


def over_9000():
    text = f"---SCORE: {gamestate.score}---" # Format the over 9000 text
    text2 = "ITS OVER 9,000!!!!!" # Format the over 9000 text
    render = constants.big_font.render(text, True, constants.HIGH_SCORE_COLOR)  # Render the over 9000 text
    render2 = constants.big_font.render(text2, True, constants.HIGH_SCORE_COLOR)  # Render the over 9000 text
    gamestate.screen.blit(render, (constants.SCREEN_HALF_WIDTH,constants.SCREEN_HALF_HEIGHT))
    gamestate.screen.blit(render2, (constants.SCREEN_HALF_WIDTH,constants.SCREEN_HALF_HEIGHT + constants.big_font.get_linesize()))  # Draw the over 9000 text at the center of the screen
