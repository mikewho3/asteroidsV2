# This is where I will create the high score system for the game

# Import the required modules
import pygame
import constants
import gamestate
import music
import titlescreen
import sys


# This will get the player name for the high score
def get_player_name(screen, font,score):
    name = ""
    input_active = True
    music.stop_music() # Stop the music when the input box is active
    music.load_music("score.mp3",set_pos=1) # Play the high score music
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Exit the game if the window is closed
                sys.exit()
            elif event.type == pygame.KEYDOWN: # Check for key presses
                if event.key == pygame.K_RETURN: # Check for the enter key
                    if len(name) < 1:
                        name = "Unknown Player" # Default name if none is entered
                    input_active = False
                elif event.key == pygame.K_BACKSPACE: # Check for the backspace key
                    name = name[:-1]
                else:
                    # Limit name length to prevent overflow
                    if len(name) < 18:
                        name += event.unicode
        
        # Draw input box and text
        screen.fill((0, 0, 0)) # Clear the screen
        text_surface2 = None # Initialize text_surface2 to None
        if score > 9000:
            text_surface = font.render(f"Your Score.... ITS OVER 9000!!", True, constants.HIGH_SCORE_COLOR)
            text_surface2 = font.render(" Enter your name:", True, constants.HIGH_SCORE_COLOR)
        else:
            text_surface = font.render("Top Ten High Score! Enter your name:", True, constants.HIGH_SCORE_COLOR)
        control_surface = font.render("Press -ENTER- to continue", True, constants.HIGH_SCORE_COLOR)
        name_surface = font.render(name, True, (255, 255, 255))
        if text_surface2 is not None:
            screen.blit(text_surface, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(text_surface)//2, constants.SCREEN_HEIGHT//2 - 50 - (font.get_linesize() * 3)))
            screen.blit(text_surface2, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(text_surface2)//2, constants.SCREEN_HEIGHT//2 - 50 - (font.get_linesize() * 2)))
            screen.blit(control_surface, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(control_surface)//2, constants.SCREEN_HEIGHT//2 - 50 - font.get_linesize()))
            screen.blit(name_surface, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(name_surface)//2, constants.SCREEN_HEIGHT//2 - 50 + font.get_linesize()))
        else:
            screen.blit(text_surface, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(text_surface)//2, constants.SCREEN_HEIGHT//2 - 50 - (font.get_linesize() * 2)))
            screen.blit(control_surface, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(control_surface)//2, constants.SCREEN_HEIGHT//2 - 50 - font.get_linesize()))
            screen.blit(name_surface, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(name_surface)//2, constants.SCREEN_HEIGHT//2 - 50 + font.get_linesize()))

        pygame.display.flip()
    music.stop_music() # Stop the high score music
        
    return name

def save_high_score(name, score):
    diff = None
    if gamestate.difficulty == 1:
        diff = "Easy"
    elif gamestate.difficulty == 2:
        diff = "Normal"
    elif gamestate.difficulty == 3:
        diff = "Hard"
    elif gamestate.difficulty == 4:
        diff = "Insane"
    elif gamestate.difficulty == 5:
        diff = "I Want to Die"
    with open("high_scores.txt", "a") as file:
        file.write(f"{name},{score},{diff}\n")

def load_high_scores():
    high_scores = []
    try:
        with open("high_scores.txt", "r") as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    name, score, diff = line.strip().split(",")
                    high_scores.append((name, int(score), str(diff)))
        # Sort high scores by score (highest first)
        high_scores.sort(key=lambda x: x[1], reverse=True)
    except FileNotFoundError:
        with open("high_scores.txt", "a") as file:
            file.write(f"No One Yet...,1,Easy\n")
        print("No high scores file found.")
        with open("high_scores.txt", "r") as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    name, score, diff = line.strip().split(",")
                    high_scores.append((name, int(score), str(diff)))
        # Sort high scores by score (highest first)
        high_scores.sort(key=lambda x: x[1], reverse=True)
        high_scores = high_scores[:10]  # Limit to top 10 scores
    except Exception as e:
        # Handle other potential errors
        print(f"Error loading high scores: {e}")
    
    return high_scores

def get_top_player():
    high_scores = load_high_scores()
    if high_scores:  # Check if the list is not empty
        top_player_name = high_scores[0][0]  # First tuple's first element (name)
        top_score = high_scores[0][1]        # First tuple's second element (score)
        return top_player_name, top_score
    else:
        return "No One Yet...", 1  # Default values if no high scores exist

def display_high_scores(screen, font):
    load_high_scores()  # Ensure high scores are updated before displaying
    titlescreen.draw_title_line()  # Draw the title line
    titlescreen.draw_text_line1()  # Draw the first text line
    y_position = 300
    
    # Title
    title = constants.header_font.render("HIGH SCORES", True, constants.HIGH_SCORE_COLOR)
    screen.blit(title, (100, 200))
    
    # List of scores
    for i, (name, score, diff) in enumerate(gamestate.high_scores[:10]):  # Display top 10
        if score > 9000:
            text = font.render(f"{i+1}. Name: {name} | Score: {score} | Difficulty: {diff}>>> ITS OVER 9,000!!!!! <<<", True, constants.GAMEOVER_COLOR)
        else:
            text = font.render(f"{i+1}. Name: {name} | Score: {score} | Difficulty: {diff}", True, constants.HIGH_SCORE_COLOR)
        screen.blit(text, (100, y_position))
        y_position += 30  # Move down for next score
    
    # Instructions to continue
    if y_position > 300:  # If any scores were displayed
        continue_text = constants.big_font.render("Press any key to continue", True, constants.HIGH_SCORE_COLOR)
        screen.blit(continue_text, (constants.SCREEN_WIDTH//2 - continue_text.get_width()//2, y_position + 30))


def add_high_scores(new_score):
    # Load existing high scores
    high_scores = load_high_scores()
    
    # Flag to track if we've added the new score
    score_added = False
    
    # Create a new list for updated scores
    updated_scores = []
    diff = None
    if gamestate.difficulty == 1:
        diff = "Easy"
    elif gamestate.difficulty == 2:
        diff = "Normal"
    elif gamestate.difficulty == 3:
        diff = "Hard"
    elif gamestate.difficulty == 4:
        diff = "Insane"
    elif gamestate.difficulty == 5:
        diff = "I Want to Die"
    
    # Check if the new score matches or beats any existing scores
    for i, (name, score, internal_diff) in enumerate(high_scores):
        if new_score >= score and not score_added and score > 0:
            player_name = get_player_name(gamestate.screen, constants.big_font,new_score)
            # Add the new score here (replacing the equal score or inserting before lower score)
            updated_scores.append((player_name, new_score, diff))
            score_added = True
            
            # If scores are equal, skip the old entry (effectively replacing it)
            if new_score == score:
                continue
                
        # Add the existing score to our updated list
        updated_scores.append((name, score, internal_diff))
    
    # If the score hasn't been added yet (lower than all existing scores)
    # and we have fewer than 10 scores, add it at the end
    if not score_added and len(high_scores) < 10 and new_score > 0:
        updated_scores.append((player_name, new_score, diff))
    
    # Sort again just to be safe
    updated_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Keep only top 10
    updated_scores = updated_scores[:10]
    
    # Save the updated high scores back to the file
    with open("high_scores.txt", "w") as file:  # Note: "w" mode overwrites the file
        for name, score, diff in updated_scores:
            file.write(f"{name},{score},{diff}\n")
    update_high_scores()  # Update the gamestate with new high scores
    return


def update_high_scores():
    # Load high scores from the file
    gamestate.high_scores = load_high_scores()
    
    # Limit to top 10 scores (shouldn't be necessary, but just in case)
    gamestate.high_scores = gamestate.high_scores[:10]
    
    # Get the top player name and score
    gamestate.top_player_name, gamestate.top_player_score = get_top_player()  # get the top player score and name