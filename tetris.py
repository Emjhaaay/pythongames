import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
BLOCK_SIZE = 30
ROWS, COLS = SCREEN_HEIGHT // BLOCK_SIZE, SCREEN_WIDTH // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)  # Grid color
EXPLOSION_COLOR = (255, 165, 0)  # Explosion color (orange)
COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (0, 255, 255),  # Cyan
]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]],  # J shape
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * COLS for _ in range(ROWS)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.explosion_rows = []

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {'shape': shape, 'color': color, 'x': COLS // 2 - len(shape[0]) // 2, 'y': 0}

    def draw_grid(self):
        for y in range(ROWS):
            for x in range(COLS):
                if self.grid[y][x]:
                    self.draw_block(x, y, self.grid[y][x])

    def draw_background_grid(self):
        for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))

    def draw_block(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self):
        shape = self.current_piece['shape']
        color = self.current_piece['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(self.current_piece['x'] + x, self.current_piece['y'] + y, color)

    def merge_piece(self):
        shape = self.current_piece['shape']
        color = self.current_piece['color']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = color

    def check_collision(self):
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if (self.current_piece['x'] + x < 0 or
                            self.current_piece['x'] + x >= COLS or
                            self.current_piece['y'] + y >= ROWS or
                            self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x]):
                        return True
        return False

    def clear_lines(self):
        lines_to_clear = [i for i in range(ROWS) if all(self.grid[i])]
        self.explosion_rows = lines_to_clear  # Store rows for explosion effect
        if lines_to_clear:
            self.score += len(lines_to_clear) * 100  # Increase score based on cleared lines

    def draw_explosions(self):
        for row in self.explosion_rows:
            for x in range(COLS):
                pygame.draw.rect(self.screen, EXPLOSION_COLOR, (x * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()
        self.clock.tick(10)  # Delay to make explosion visible
        time.sleep(0.1)
        for row in self.explosion_rows:
            del self.grid[row]
            self.grid.insert(0, [0] * COLS)
        self.explosion_rows = []  # Reset explosion rows

    def rotate_piece(self):
        self.current_piece['shape'] = [list(row) for row in zip(*self.current_piece['shape'][::-1])]

    def drop_piece(self):
        self.current_piece['y'] += 1
        if self.check_collision():
            self.current_piece['y'] -= 1
            self.merge_piece()
            self.clear_lines()
            self.current_piece = self.new_piece()
            if self.check_collision():
                self.game_over = True

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        text = self.font.render("Game Over - Press R to Retry", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def reset_game(self):
        self.grid = [[0] * COLS for _ in range(ROWS)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif not self.game_over:
                        if event.key == pygame.K_LEFT:
                            self.current_piece['x'] -= 1
                            if self.check_collision():
                                self.current_piece['x'] += 1
                        elif event.key == pygame.K_RIGHT:
                            self.current_piece['x'] += 1
                            if self.check_collision():
                                self.current_piece['x'] -= 1
                        elif event.key == pygame.K_DOWN:
                            self.drop_piece()
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                            if self.check_collision():
                                self.rotate_piece()

            self.screen.fill(BLACK)
            self.draw_background_grid()
            if not self.game_over:
                self.drop_piece()
            self.draw_grid()
            self.draw_piece()
            self.draw_score()

            if self.explosion_rows:
                self.draw_explosions()  # Trigger explosion effect

            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(5)

if __name__ == '__main__':
    Tetris().run()
