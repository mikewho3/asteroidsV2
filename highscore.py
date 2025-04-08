# This is where I will create the high score system for the game

# Import the required modules
import pygame
import constants
import gamestate
import music


# This will get the player name for the high score
def get_player_name(screen, font):
    name = ""
    input_active = True
    music.stop_music() # Stop the music when the input box is active
    music.load_music("score.mp3",set_pos=1) # Play the high score music
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Exit the game if the window is closed
                return None
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
        text_surface = font.render("Top Ten High Score! Enter your name:", True, constants.HIGH_SCORE_COLOR)
        name_surface = font.render(name, True, (255, 255, 255))
        screen.blit(text_surface, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(text_surface)//2, constants.SCREEN_HEIGHT//2 - 50))
        screen.blit(name_surface, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(name_surface)//2, constants.SCREEN_HEIGHT//2))
        pygame.display.flip()
    music.stop_music() # Stop the high score music
        
    return name

def save_high_score(name, score):
    with open("high_scores.txt", "a") as file:
        file.write(f"{name},{score}\n")

def load_high_scores():
    high_scores = []
    try:
        with open("high_scores.txt", "r") as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    name, score = line.strip().split(",")
                    high_scores.append((name, int(score)))
        # Sort high scores by score (highest first)
        high_scores.sort(key=lambda x: x[1], reverse=True)
    except FileNotFoundError:
        with open("high_scores.txt", "a") as file:
            file.write(f"No One Yet...,0\n")
        print("No high scores file found.")
        with open("high_scores.txt", "r") as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    name, score = line.strip().split(",")
                    high_scores.append((name, int(score)))
        # Sort high scores by score (highest first)
        high_scores.sort(key=lambda x: x[1], reverse=True)
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
        return "No One Yet...", 0  # Default values if no high scores exist

def display_high_scores(screen, font):
    #high_scores = load_high_scores()
    y_position = 100
    
    # Title
    title = constants.header_score_font.render("HIGH SCORES", True, constants.HIGH_SCORE_COLOR)
    screen.blit(title, (100, 0))
    
    # List of scores
    for i, (name, score) in enumerate(gamestate.high_scores[:10]):  # Display top 10
        text = font.render(f"{i+1}. Name: {name} | Score: {score}", True, constants.HIGH_SCORE_COLOR)
        screen.blit(text, (100, y_position))
        y_position += 30  # Move down for next score
    
    # Instructions to continue
    if y_position > 100:  # If any scores were displayed
        continue_text = font.render("Press any key to continue", True, constants.HIGH_SCORE_COLOR)
        screen.blit(continue_text, (constants.SCREEN_WIDTH//2 - continue_text.get_width()//2, y_position + 30))


def update_high_scores(new_score):
    # Load existing high scores
    high_scores = load_high_scores()
    
    # Flag to track if we've added the new score
    score_added = False
    
    # Create a new list for updated scores
    updated_scores = []
    
    # Check if the new score matches or beats any existing scores
    for i, (name, score) in enumerate(high_scores):
        if new_score >= score and not score_added:
            player_name = get_player_name(gamestate.screen, constants.big_font)
            # Add the new score here (replacing the equal score or inserting before lower score)
            updated_scores.append((player_name, new_score))
            score_added = True
            
            # If scores are equal, skip the old entry (effectively replacing it)
            if new_score == score:
                continue
                
        # Add the existing score to our updated list
        updated_scores.append((name, score))
    
    # If the score hasn't been added yet (lower than all existing scores)
    # and we have fewer than 10 scores, add it at the end
    if not score_added and len(high_scores) < 10:
        updated_scores.append((player_name, new_score))
    
    # Sort again just to be safe
    updated_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Keep only top 10
    updated_scores = updated_scores[:10]
    
    # Save the updated high scores back to the file
    with open("high_scores.txt", "w") as file:  # Note: "w" mode overwrites the file
        for name, score in updated_scores:
            file.write(f"{name},{score}\n")
    
    return
