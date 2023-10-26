import pygame
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("L-GAME")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Block directions
class Direction(Enum):
    VERTICAL = 1
    VERTICAL_MIRROR_X = 2
    VERTICAL_MIRROR_Y = 3
    VERTICAL_MIRROR_X_Y = 4
    HORIZONTAL = 5
    HORIZONTAL_MIRROR_X = 6
    HORIZONTAL_MIRROR_Y = 7
    HORIZONTAL_MIRROR_X_Y = 8

# Define grid properties
GRID_SIZE = 4
CELL_SIZE = 100

# Images
img_red_square = pygame.image.load("resources/red_square.png").convert()
img_blue_square = pygame.image.load("resources/blue_square.png").convert()

# Game control variables
game_state = GameState.RED_TO_MOVE_BLOCK

red_player_position = {"start": {0, 1}, "direction": Direction.HORIZONTAL_MIRROR_Y}
blue_player_position = {"start": {3, 2}, "direction": Direction.HORIZONTAL_MIRROR_X}

class GameState(Enum):
    RED_TO_MOVE_BLOCK = "Vermelho mexe L"
    RED_TO_MOVE_COIN = "Vermelho mexe moeda"
    BLUE_TO_MOVE_BLOCK = "Azul mexe L"
    BLUE_TO_MOVE_COIN = "Azul mexe moeda"

def advanceState():
    match game_state:
        case GameState.RED_TO_MOVE_BLOCK:
            game_state = GameState.RED_TO_MOVE_COIN
        case GameState.RED_TO_MOVE_COIN:
            game_state = GameState.BLUE_TO_MOVE_BLOCK
        case GameState.BLUE_TO_MOVE_BLOCK:
            game_state = GameState.BLUE_TO_MOVE_COIN
        case GameState.BLUE_TO_MOVE_COIN:
            game_state = GameState.RED_TO_MOVE_BLOCK


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

def click(cell_x, cell_y):
    print(str(cell_x) + ' - ' + str(cell_y))
    paintCell(cell_x, cell_y, img_red_square)

def paintCell(cell_x, cell_y, img)
    
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
                click(grid_x, grid_y)

    screen.fill(WHITE)
    draw_grid()
    draw_buttons()

    pygame.display.flip()