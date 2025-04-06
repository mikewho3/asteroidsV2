# This is where I will create the high score system for the game

# Import the required modules
import pygame
import constants


# This will get the player name for the high score
def get_player_name(screen, font):
    name = ""
    input_active = True
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Exit the game if the window is closed
                return None
            elif event.type == pygame.KEYDOWN: # Check for key presses
                if event.key == pygame.K_RETURN: # Check for the enter key
                    input_active = False
                elif event.key == pygame.K_BACKSPACE: # Check for the backspace key
                    name = name[:-1]
                else:
                    # Limit name length to prevent overflow
                    if len(name) < 18:
                        name += event.unicode
        
        # Draw input box and text
        screen.fill((0, 0, 0)) # Clear the screen
        text_surface = font.render("New High Score! Enter your name:", True, (255, 255, 255))
        name_surface = font.render(name, True, (255, 255, 255))
        screen.blit(text_surface, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(text_surface)//2, constants.SCREEN_HEIGHT//2 - 50))
        screen.blit(name_surface, (constants.SCREEN_WIDTH//2 - pygame.Surface.get_width(name_surface)//2, constants.SCREEN_HEIGHT//2))
        pygame.display.flip()
        
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
            file.write(f"MikeWho3,0001\n")
        print("No high scores file found. Creating a new one.")
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
        return "No one yet", 0  # Default values if no high scores exist



