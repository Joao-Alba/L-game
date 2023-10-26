import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Grid Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Define grid properties
GRID_SIZE = 4
CELL_SIZE = 100

# Function to draw the grid
def draw_grid():
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, CELL_SIZE * GRID_SIZE), 2)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (CELL_SIZE * GRID_SIZE, i * CELL_SIZE), 2)

# Function to draw buttons
def draw_buttons():
    button_height = 80
    button_width = 80
    button_padding = 20

    for i, color in enumerate([WHITE, GRAY, BLACK]):
        pygame.draw.rect(screen, color, (GRID_SIZE * CELL_SIZE + button_padding, i * (button_height + button_padding), button_width, button_height))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x >= GRID_SIZE * CELL_SIZE:
                if y < CELL_SIZE:
                    # Button 1 clicked
                    print("Button 1 clicked")
                elif y < 2 * CELL_SIZE:
                    # Button 2 clicked
                    print("Button 2 clicked")
                elif y < 3 * CELL_SIZE:
                    # Button 3 clicked
                    print("Button 3 clicked")

            else:
                grid_x = x // CELL_SIZE
                grid_y = y // CELL_SIZE
                # Grid cell clicked
                print(f"Grid cell ({grid_x}, {grid_y}) clicked")

    screen.fill(WHITE)
    draw_grid()
    draw_buttons()

    pygame.display.flip()