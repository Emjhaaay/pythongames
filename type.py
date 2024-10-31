import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typewriting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 35)

# Game variables
words = ["python", "java", "react", "javascript", "docker", "linux", "tensor", "typing", "keyboard", "pygame","nigger","missyou balik kana","gago"]
current_word = ""
word_y_pos = 0
word_speed = 2
user_input = ""
score = 0
lives = 5

# Functions
def display_text(text, font, color, x, y):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def reset_word():
    """Reset only the current word and its position"""
    global current_word, word_y_pos
    current_word = random.choice(words)
    word_y_pos = -50  # Start the word above the screen

def reset_game():
    """Reset the entire game state"""
    global score, lives, word_speed, user_input
    score = 0
    lives = 5
    word_speed = 2
    user_input = ""
    reset_word()

# Start with a random word
reset_word()

# Main game loop
running = True
game_over = False

while running:
    screen.fill(BLACK)
    
    if not game_over:
        # Events handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check if the typed word matches
                    if user_input == current_word:
                        score += 1  # Increment score for correct word
                        reset_word()
                        word_speed += 0.1  # Increase difficulty
                    else:
                        lives -= 1  # Decrement lives for incorrect word
                    user_input = ""  # Reset user input
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]  # Remove last character
                else:
                    user_input += event.unicode  # Add typed character
        
        # Move the word down
        word_y_pos += word_speed
        
        # Check if word hits the bottom of the screen
        if word_y_pos > HEIGHT:
            lives -= 1
            reset_word()
        
        # Draw elements
        display_text(f"Score: {score}", small_font, WHITE, 10, 10)
        display_text(f"Lives: {lives}", small_font, WHITE, WIDTH - 150, 10)
        display_text(current_word, font, RED, WIDTH // 2 - len(current_word) * 10, word_y_pos)
        display_text(user_input, font, GREEN, WIDTH // 2 - len(user_input) * 10, HEIGHT - 50)
        
        # Game over condition
        if lives <= 0:
            game_over = True
            display_text("Game Over", font, RED, WIDTH // 2 - 100, HEIGHT // 2)
            display_text("Press R to Try Again or Q to Quit", small_font, WHITE, WIDTH // 2 - 180, HEIGHT // 2 + 50)
            pygame.display.flip()
            pygame.time.delay(500)
    
    else:
        # Waiting for the player to restart or quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    reset_game()
                    game_over = False
                elif event.key == pygame.K_q:  # Quit the game
                    running = False

    pygame.display.flip()
    pygame.time.delay(30)  # Frame rate

# Quit pygame
pygame.quit()
sys.exit()
