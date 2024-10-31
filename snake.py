import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)  # Snake color
GREEN = (0, 255, 0)  # Food color
BLUE = (50, 153, 213)  # Background color

WIDTH = 600
HEIGHT = 400
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Set up display
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Set the clock
clock = pygame.time.Clock()

# Font styles
font_style = pygame.font.SysFont("poppins", 25)
score_font = pygame.font.SysFont("poppins", 35)

def draw_snake(snake_block, snake_list):
    """Draw the snake on the screen."""
    for segment in snake_list:
        pygame.draw.rect(dis, RED, [segment[0], segment[1], snake_block, snake_block])  # Change color to RED

def display_score(score):
    """Display the current score on the screen."""
    value = score_font.render("Score: " + str(score), True, BLACK)
    dis.blit(value, [0, 0])

def display_message(msg, color):
    """Display a message on the screen."""
    message = font_style.render(msg, True, color)
    dis.blit(message, [WIDTH / 6, HEIGHT / 3])

def draw_food(foodx, foody):
    """Draw the food on the screen."""
    pygame.draw.rect(dis, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

def get_random_food_position():
    """Generate random food position."""
    return (round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0,
            round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0)

def game_loop():
    """Main function for the game."""
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    foodx, foody = get_random_food_position()

    while not game_over:
        while game_close:
            dis.fill(BLUE)
            display_message("You Lost! Press C-Play Again or Q-Quit", RED)
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Check for boundaries
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        # Update snake's position
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLUE)
        draw_food(foodx, foody)

        # Create snake's head
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        # Remove tail segment if snake length exceeds
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for self-collision
        if snake_head in snake_list[:-1]:
            game_close = True

        draw_snake(SNAKE_BLOCK, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        # Check if the snake has eaten the food
        if x1 == foodx and y1 == foody:
            foodx, foody = get_random_food_position()
            snake_length += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()

# Start the game
if __name__ == "__main__":
    game_loop()
