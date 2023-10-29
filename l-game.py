import pygame
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((750, 400))
pygame.display.set_caption("L-GAME")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GRAY2 = (150, 150, 150)
GREEN = (34, 177, 76)
YELLOW = (255, 242, 0)

# Block directions
class Direction(Enum):
    VERTICAL = [{'x': 0, 'y': 0}, {'x': -1, 'y': 0}, {'x': -1, 'y': -1}, {'x': -1, 'y': -2}]
    VERTICAL_MIRROR_X = [{'x': 0, 'y': 0}, {'x': -1, 'y': 0}, {'x': -1, 'y': 1}, {'x': -1, 'y': 2}]
    VERTICAL_MIRROR_Y = [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': -1}, {'x': 1, 'y': -2}]
    VERTICAL_MIRROR_X_Y = [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}, {'x': 1, 'y': 2}]
    HORIZONTAL = [{'x': 0, 'y': 0}, {'x': 0, 'y': 1}, {'x': -1, 'y': 1}, {'x': -2, 'y': 1}]
    HORIZONTAL_MIRROR_X = [{'x': 0, 'y': 0}, {'x': 0, 'y': -1}, {'x': -1, 'y': -1}, {'x': -2, 'y': -1}]
    HORIZONTAL_MIRROR_Y = [{'x': 0, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 1}, {'x': 2, 'y': 1}]
    HORIZONTAL_MIRROR_X_Y = [{'x': 0, 'y': 0}, {'x': 0, 'y': -1}, {'x': 1, 'y': -1}, {'x': 2, 'y': -1}]

# Define grid properties
GRID_SIZE = 4
CELL_SIZE = 100

# Images
img_red_square = pygame.image.load("resources/red_square.png").convert()
img_blue_square = pygame.image.load("resources/blue_square.png").convert()
img_white_square = pygame.image.load("resources/white_square.png").convert()
img_coin1 = pygame.image.load("resources/coin1.png").convert()
img_coin2 = pygame.image.load("resources/coin2.png").convert()

# Game control variables
class GameState(Enum):
    RED_TO_MOVE_BLOCK = 1
    RED_TO_MOVE_COIN = 2
    BLUE_TO_MOVE_BLOCK = 3
    BLUE_TO_MOVE_COIN = 4

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 'w'
        self.has_coin = False


game_state = GameState.BLUE_TO_MOVE_COIN

red_player_position = {"start": {"x": 0, "y": 1}, "direction": Direction.HORIZONTAL_MIRROR_Y}
blue_player_position = {"start":  {"x": 3, "y": 2}, "direction": Direction.HORIZONTAL_MIRROR_X}
coin1_position = {"x": 0, "y": 0}
coin2_position = {"x": 3, "y": 3}

#draw start on screen

message_text = "Vez do jogador vermelho"
def advanceState():
    global game_state
    global message_text
    match game_state:
        case GameState.RED_TO_MOVE_BLOCK:
            game_state = GameState.RED_TO_MOVE_COIN
            message_text = "Vez do jogador vermelho mexer a moeda"
        case GameState.RED_TO_MOVE_COIN:
            game_state = GameState.BLUE_TO_MOVE_BLOCK
            message_text = "Vez do jogador azul mexer o L"
        case GameState.BLUE_TO_MOVE_BLOCK:
            game_state = GameState.BLUE_TO_MOVE_COIN
            message_text = "Vez do jogador azul mexer a moeda"
        case GameState.BLUE_TO_MOVE_COIN:
            game_state = GameState.RED_TO_MOVE_BLOCK
            message_text = "Vez do jogador vermelho mexer o L"

advanceState()

# Create 16 cells
cells = [[Cell(0, 0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
img_cells = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

for i in range(len(cells)):
    for j in range(len(cells[i])):
        cells[i][j].x = i
        cells[i][j].y = j


# Function to load an image onto a cell
def load_image(cell_x, cell_y, image):
    img_cells[cell_x][cell_y] = image

# Function to draw the grid
def draw_grid():
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, CELL_SIZE * GRID_SIZE), 2)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (CELL_SIZE * GRID_SIZE, i * CELL_SIZE), 2)

# Function to draw buttons and message
def draw_buttons_and_message():
    button_height = 80
    button_width = 300
    button_padding = 20
    button_start_x = GRID_SIZE * CELL_SIZE + button_padding

    button_texts = ["Moeda 1", "Moeda 2", "Não mexer moeda"]

    for i, color in enumerate([YELLOW, GREEN, BLACK]):
        button_y = i * (button_height + button_padding)
        pygame.draw.rect(screen, color, (button_start_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 24)
        text = font.render(button_texts[i], True, WHITE)
        text_rect = text.get_rect(center=(button_start_x + button_width/2, button_y + button_height/2))
        screen.blit(text, text_rect)

    message_height = 30
    message_y = 3 * (button_height + button_padding) + button_padding
    pygame.draw.rect(screen, WHITE, (button_start_x, message_y, button_width, message_height))

    font = pygame.font.Font(None, 24)
    message = font.render(message_text, True, BLACK)
    screen.blit(message, (button_start_x + 10, message_y + 5))

inputs = []
def register_inputs(game_state):
    global inputs
    if(game_state == GameState.RED_TO_MOVE_BLOCK):
        remove_previous_block('r')
        for _input in inputs:
            cells[_input['x']][_input['y']].color = 'r'
            load_image(_input['x'], _input['y'], img_red_square)
            #Arrumar positions
            red_player_position['start']['x'] = _input['x']
            red_player_position['start']['y'] = _input['y']
            red_player_position['direction'] = Direction.HORIZONTAL_MIRROR_Y
    elif(game_state == GameState.BLUE_TO_MOVE_BLOCK):
        remove_previous_block('b')
        for _input in inputs:
            cells[_input['x']][_input['y']].color = 'b'
            load_image(_input['x'], _input['y'], img_blue_square)
            #Arrumar positions
            blue_player_position['start']['x'] = _input['x']
            blue_player_position['start']['y'] = _input['y']
            blue_player_position['direction'] = Direction.HORIZONTAL_MIRROR_Y
    elif(game_state == GameState.RED_TO_MOVE_COIN or game_state == GameState.BLUE_TO_MOVE_COIN):
        remove_previous_coin(chosen_coin)
        for _input in inputs:
            cells[_input['x']][_input['y']].has_coin = True
            if(chosen_coin == 1):
                coin1_position['x'] = _input['x']
                coin1_position['y'] = _input['y']
                load_image(_input['x'], _input['y'], img_coin1)
            else:
                coin2_position['x'] = _input['x']
                coin2_position['y'] = _input['y']
                load_image(_input['x'], _input['y'], img_coin2)
        
def remove_previous_block(color):
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if(cells[i][j].color == color):
                cells[i][j].color = 'w'
                load_image(i, j, img_white_square)

def remove_previous_coin(chosen_coin):
    if(chosen_coin == 1):
        coin = coin1_position
    elif(chosen_coin == 2):
        coin = coin2_position

    cells[coin['x']][coin['y']].has_coin = False
    load_image(coin['x'], coin['y'], img_white_square)

def input_invalid(x, y):
    current_color = ''

    if(game_state == GameState.RED_TO_MOVE_BLOCK):
        current_color = 'r'
    else:
        current_color = 'b'

    if(cells[cell_x][cell_y].has_coin or (cells[cell_x][cell_y].color != 'w' and cells[cell_x][cell_y].color != current_color)):
        return True

    for _input in inputs:
        if(_input['x'] == x and _input['y'] == y):
            return True
    
def has_full_block_overlap():
    current_color = ''

    if(game_state == GameState.RED_TO_MOVE_BLOCK):
        current_color = 'r'
    else:
        current_color = 'b'

    current_block = []
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if(cells[i][j].color == current_color):
                current_block.append({'x': i, 'y': j})
    

    for _input in inputs:
        found_match = False
        for block_piece in current_block:
            if(_input['x'] == block_piece['x'] and _input['y'] == block_piece['y']):
                found_match = True
                break
        if(not found_match):
            return False
    return True

def is_block_valid():
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if(cells[i][j].color == current_color):
                current_block.append({'x': i, 'y': j})

def check_win():
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            for direction in Direction:
                direction_possible = True
                for move in direction.value:
                    target_x = i + move['x']
                    target_y = j + move['y']

                    if(target_x < 0 or target_y < 0):
                        continue

                    if(cells[target_x][target_y].has_coin or cells[target_x][target_y].color != 'w'):
                        direction_possible = False
                        break

                if(direction_possible):
                    return False
    return True

def draw_starting_objects():
    for move in red_player_position['direction'].value:
        x = red_player_position['start']['x'] + move['x']
        y = red_player_position['start']['y'] + move['y']
        cells[x][y].color = 'r'
        load_image(x, y, img_red_square)
    for move in blue_player_position['direction'].value:
        x = blue_player_position['start']['x'] + move['x']
        y = blue_player_position['start']['y'] + move['y']
        cells[x][y].color = 'b'
        load_image(x, y, img_blue_square)
    cells[coin1_position['x']][coin1_position['y']].has_coin = True
    load_image(coin1_position['x'], coin1_position['y'], img_coin1)
    cells[coin2_position['x']][coin2_position['y']].has_coin = True
    load_image(coin2_position['x'], coin2_position['y'], img_coin2)
    return

message_before_invalid = ''
chosen_coin = 9
draw_starting_objects()
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
                    chosen_coin = 1
                elif y < 2 * CELL_SIZE:
                    chosen_coin = 2
                elif y < 3 * CELL_SIZE:
                    chosen_coin = 0
                    advanceState()

            else:
                cell_x = x // CELL_SIZE
                cell_y = y // CELL_SIZE

                if((game_state == GameState.RED_TO_MOVE_COIN or game_state == GameState.BLUE_TO_MOVE_COIN) and chosen_coin == 9):
                    message_before_invalid = message_text
                    message_text = "Escolha uma moeda primeiro"
                    continue

                if(input_invalid(cell_x, cell_y)):
                    message_before_invalid = message_text
                    message_text = "Input inválido"
                    continue

                inputs.append({"x": cell_x, "y": cell_y})

                print(str(cell_x) + " - " + str(cell_y))

                if(game_state == GameState.RED_TO_MOVE_BLOCK or game_state == GameState.BLUE_TO_MOVE_BLOCK):
                    if(len(inputs) == 4):
                        if(has_full_block_overlap()):
                            # or is_block_invalid()
                            message_text = "Bloco inválido"
                            inputs = []
                            continue
                        register_inputs(game_state)
                        if(check_win()):
                            pygame.quit()
                        advanceState()
                        inputs = []
                elif(game_state == GameState.RED_TO_MOVE_COIN or game_state == GameState.BLUE_TO_MOVE_COIN):
                    register_inputs(game_state)
                    if(check_win()):
                        pygame.quit()
                    advanceState()
                    inputs = []

    screen.fill(WHITE)
    draw_grid()
    draw_buttons_and_message()
    
    # Draw cells
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if img_cells[x][y]:
                screen.blit(img_cells[x][y], ((x * CELL_SIZE) + 2, (y * CELL_SIZE) + 2))

    pygame.display.flip()