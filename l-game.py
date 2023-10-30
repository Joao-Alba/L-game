import pygame
import sys
from enum import Enum

pygame.init()

# Display
screen = pygame.display.set_mode((750, 400))
pygame.display.set_caption("L-GAME")
GRID_SIZE = 4
CELL_SIZE = 100

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GRAY2 = (150, 150, 150)
GREEN = (34, 177, 76)
YELLOW = (255, 242, 0)

# Formatos do L
class Direction(Enum):
    VERTICAL = [{'x': 0, 'y': 0}, {'x': -1, 'y': 0}, {'x': -1, 'y': -1}, {'x': -1, 'y': -2}]
    VERTICAL_MIRROR_X = [{'x': 0, 'y': 0}, {'x': -1, 'y': 0}, {'x': -1, 'y': 1}, {'x': -1, 'y': 2}]
    VERTICAL_MIRROR_Y = [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': -1}, {'x': 1, 'y': -2}]
    VERTICAL_MIRROR_X_Y = [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}, {'x': 1, 'y': 2}]
    HORIZONTAL = [{'x': 0, 'y': 0}, {'x': 0, 'y': 1}, {'x': -1, 'y': 1}, {'x': -2, 'y': 1}]
    HORIZONTAL_MIRROR_X = [{'x': 0, 'y': 0}, {'x': 0, 'y': -1}, {'x': -1, 'y': -1}, {'x': -2, 'y': -1}]
    HORIZONTAL_MIRROR_Y = [{'x': 0, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 1}, {'x': 2, 'y': 1}]
    HORIZONTAL_MIRROR_X_Y = [{'x': 0, 'y': 0}, {'x': 0, 'y': -1}, {'x': 1, 'y': -1}, {'x': 2, 'y': -1}]

# Imagens
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

# Posições iniciais
red_player_position = {"start": {"x": 0, "y": 1}, "direction": Direction.HORIZONTAL_MIRROR_Y}
blue_player_position = {"start":  {"x": 3, "y": 2}, "direction": Direction.HORIZONTAL_MIRROR_X}
coin1_position = {"x": 0, "y": 0}
coin2_position = {"x": 3, "y": 3}

#red_player_position = {"start": {"x": 1, "y": 2}, "direction": Direction.VERTICAL}
#blue_player_position = {"start":  {"x": 2, "y": 0}, "direction": Direction.VERTICAL_MIRROR_X_Y}
#coin1_position = {"x": 2, "y": 1}
#coin2_position = {"x": 3, "y": 3}

# Manter o estado atual do jogo
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

# Matrizes de controle
cells = [[Cell(0, 0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
img_cells = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

for i in range(len(cells)):
    for j in range(len(cells[i])):
        cells[i][j].x = i
        cells[i][j].y = j

# Carrega uma imagem em uma celula
def load_image(cell_x, cell_y, image):
    img_cells[cell_x][cell_y] = image

# Desenha matriz
def draw_grid():
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, CELL_SIZE * GRID_SIZE), 2)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (CELL_SIZE * GRID_SIZE, i * CELL_SIZE), 2)

# Desenha botões e mensagem
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

# Recebe os inputs do jogador e atualiza as variáveis de controles
inputs = []
def register_inputs(game_state):
    global inputs
    if(game_state == GameState.RED_TO_MOVE_BLOCK):
        remove_previous_block('r')
        for _input in inputs:
            cells[_input['x']][_input['y']].color = 'r'
            load_image(_input['x'], _input['y'], img_red_square)
        new_player_position = get_new_block_position()
        red_player_position['start']['x'] = new_player_position['start']['x']
        red_player_position['start']['y'] = new_player_position['start']['y']
        red_player_position['direction'] = new_player_position['direction']
    elif(game_state == GameState.BLUE_TO_MOVE_BLOCK):
        remove_previous_block('b')
        for _input in inputs:
            cells[_input['x']][_input['y']].color = 'b'
            load_image(_input['x'], _input['y'], img_blue_square)
        new_player_position = get_new_block_position()
        blue_player_position['start']['x'] = new_player_position['start']['x']
        blue_player_position['start']['y'] = new_player_position['start']['y']
        blue_player_position['direction'] = new_player_position['direction']
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
        
# Remove da tela o bloco da cor especificada
def remove_previous_block(color):
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if(cells[i][j].color == color):
                cells[i][j].color = 'w'
                load_image(i, j, img_white_square)

# Remove da tela a moeda especificada
def remove_previous_coin(chosen_coin):
    if(chosen_coin == 1):
        coin = coin1_position
    elif(chosen_coin == 2):
        coin = coin2_position

    cells[coin['x']][coin['y']].has_coin = False
    load_image(coin['x'], coin['y'], img_white_square)

# Verifica se o input é valido
def input_invalid(target_x, target_y):
    current_color = ''

    if(game_state == GameState.RED_TO_MOVE_BLOCK or game_state == GameState.RED_TO_MOVE_COIN):
        current_color = 'r'
    else:
        current_color = 'b'

    if(game_state == GameState.RED_TO_MOVE_COIN or game_state == GameState.BLUE_TO_MOVE_COIN):
        if(cells[target_x][target_y].has_coin or cells[target_x][target_y].color != 'w'):
            return True
    else:
        if(cells[target_x][target_y].has_coin or (cells[target_x][target_y].color != 'w' and cells[target_x][target_y].color != current_color)):
            return True

    for _input in inputs:
        if(_input['x'] == target_x and _input['y'] == target_y):
            return True
    
# Verifica se o L desenhado está completamente em cima de um L já existente
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

# Retorna todos as posições possíveis (célula inicial e direção) para a cor especificada 
def check_possible_moves_for(target_color):
    possible_moves = []
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            for direction in Direction:
                direction_possible = True
                cell_overlap_number = 0
                for move in direction.value:
                    target_x = i + move['x']
                    target_y = j + move['y']

                    if(target_x < 0 or target_x > 3 or target_y < 0 or target_y > 3):
                        direction_possible = False
                        break

                    if(cells[target_x][target_y].has_coin or (cells[target_x][target_y].color != 'w' and cells[target_x][target_y].color != target_color)):
                        direction_possible = False
                        break

                    if(cells[target_x][target_y].color == target_color):
                            cell_overlap_number += 1

                if(direction_possible and cell_overlap_number < 4):
                    possible_moves.append({"start": {"x": i, "y": j}, "direction": direction})
                cell_overlap_number = 0
    return possible_moves

# Retorna a posição do bloco novo baseado nos inputs
def get_new_block_position():
    for possible_start_cell in inputs:
        found_direction = get_block_direction(possible_start_cell['x'], possible_start_cell['y'])
        if(found_direction != None):
            return {"start": {"x": possible_start_cell['x'], "y": possible_start_cell['y']}, "direction": found_direction}
    return None

# Calcula a direção de um block
def get_block_direction(start_x, start_y):
    direction_valid = False
    for direction in Direction:
        found_moves = 0
        for move in direction.value:
            target_x = start_x + move['x']
            target_y = start_y + move['y']

            if(target_x < 0 or target_x > 3 or target_y < 0 or target_y > 3):
                break

            found_move = False
            for _input in inputs:
                if(_input['x'] == target_x and _input['y'] == target_y):
                    found_move = True
                    found_moves += 1
                    break
            
            if(not found_move):
                break
        if(found_moves == 4):
            direction_valid = True
            break
    if(direction_valid):
        return direction
    return None

# Desenha os objetos iniciais na tela pelas suas posições
def draw_starting_objects():
    draw_from_position(red_player_position, 'r', img_red_square)
    draw_from_position(blue_player_position, 'b', img_blue_square)
    cells[coin1_position['x']][coin1_position['y']].has_coin = True
    load_image(coin1_position['x'], coin1_position['y'], img_coin1)
    cells[coin2_position['x']][coin2_position['y']].has_coin = True
    load_image(coin2_position['x'], coin2_position['y'], img_coin2)
    return

# Atualiza as variáveis de controle pela posição especificada
def draw_from_position(player_position, player_color, player_color_img):
    for move in player_position['direction'].value:
        x = player_position['start']['x'] + move['x']
        y = player_position['start']['y'] + move['y']
        cells[x][y].color = player_color
        load_image(x, y, player_color_img)

# Calcula o melhor movimento de bloco para a IA
def get_best_block_move():
    current_color = ''
    enemy_color = ''
    current_player_position = None
    current_color_img = None
    if(game_state == GameState.RED_TO_MOVE_BLOCK or game_state == GameState.RED_TO_MOVE_COIN):
        current_color = 'r'
        enemy_color = 'b'
        current_player_position = red_player_position
        current_color_img = img_red_square
    else:
        current_color = 'b'
        enemy_color = 'r'
        current_player_position = blue_player_position
        current_color_img = img_blue_square

    least_possible_moves_enemy_player = 20
    best_current_player_move = None
    possible_moves_current_player = check_possible_moves_for(current_color)

    for possible_move_current_player in possible_moves_current_player:
        remove_previous_block(current_color)
        draw_from_position(possible_move_current_player, current_color, current_color_img)
        enemy_player_possible_move_number = len(check_possible_moves_for(enemy_color))
        if(enemy_player_possible_move_number < least_possible_moves_enemy_player):
            least_possible_moves_enemy_player = enemy_player_possible_move_number
            best_current_player_move = possible_move_current_player
            if(least_possible_moves_enemy_player == 0):
                break

    remove_previous_block(current_color)
    draw_from_position(current_player_position, current_color, current_color_img)
    return best_current_player_move

# Calcula o melhor movimento de moeda para a IA
def get_best_coin_move():
    current_color = ''
    enemy_color = ''
    if(game_state == GameState.RED_TO_MOVE_BLOCK or game_state == GameState.RED_TO_MOVE_COIN):
        current_color = 'r'
        enemy_color = 'b'
    else:
        current_color = 'b'
        enemy_color = 'r'

    best_position_coin1 = try_every_position_coin(1)

    best_position_coin2 = try_every_position_coin(2)
    
    if(best_position_coin1['move_number'] < best_position_coin2['move_number']):
        return {"coin": 1, "position": {'x': best_position_coin1['x'], 'y': best_position_coin1['y']}}
    else:
        return {"coin": 2, "position": {'x': best_position_coin2['x'], 'y': best_position_coin2['y']}}

# Descobre a melhor escolha de moeda para mexer
def try_every_position_coin(coin):
    least_possible_moves_enemy_player_coin = 20
    return_best_coin_position = None

    global coin1_position
    global coin2_position

    for i in range(len(cells)):
        for j in range(len(cells[i])):
            cell = cells[i][j]
            if(not cell.has_coin and cell.color == 'w'):
                if(coin == 1):
                    original_coin_position = coin1_position
                    remove_previous_coin(1)

                    cells[cell.x][cell.y].has_coin = True
                    load_image(cell.x, cell.y, img_coin1)
                    coin1_position = {'x': cell.x, 'y': cell.y}
                    
                    enemy_player_possible_move_number = len(check_possible_moves_for(enemy_color))

                    if(enemy_player_possible_move_number < least_possible_moves_enemy_player_coin):
                        least_possible_moves_enemy_player_coin = enemy_player_possible_move_number
                        return_best_coin_position = {'x': cell.x, 'y': cell.y, "move_number": least_possible_moves_enemy_player_coin}

                    remove_previous_coin(1)
                    cells[original_coin_position['x']][original_coin_position['y']].has_coin = True
                    load_image(original_coin_position['x'], original_coin_position['y'], img_coin1)
                    coin1_position = {'x': original_coin_position['x'], 'y': original_coin_position['y']}
                else:
                    original_coin_position = coin2_position
                    remove_previous_coin(2)

                    cells[cell.x][cell.y].has_coin = True
                    load_image(cell.x, cell.y, img_coin2)
                    coin2_position = {'x': cell.x, 'y': cell.y}
                    
                    enemy_player_possible_move_number = len(check_possible_moves_for(enemy_color))

                    if(enemy_player_possible_move_number < least_possible_moves_enemy_player_coin):
                        least_possible_moves_enemy_player_coin = enemy_player_possible_move_number
                        return_best_coin_position = {'x': cell.x, 'y': cell.y, "move_number": least_possible_moves_enemy_player_coin}

                    remove_previous_coin(2)
                    cells[original_coin_position['x']][original_coin_position['y']].has_coin = True
                    load_image(original_coin_position['x'], original_coin_position['y'], img_coin2)
                    coin2_position = {'x': original_coin_position['x'], 'y': original_coin_position['y']}

    return return_best_coin_position

# Variáveis de controle do loop
message_before_invalid = ''
chosen_coin = 9
draw_starting_objects()
game_over = False

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if(game_over):
            continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x >= GRID_SIZE * CELL_SIZE:
                if(game_state == GameState.RED_TO_MOVE_COIN):
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

                if((game_state == GameState.RED_TO_MOVE_COIN) and (chosen_coin == 9 or chosen_coin == 0)):
                    message_before_invalid = message_text
                    message_text = "Escolha uma moeda primeiro"
                    continue

                if(input_invalid(cell_x, cell_y) and (game_state == GameState.RED_TO_MOVE_BLOCK or game_state == GameState.RED_TO_MOVE_COIN)):
                    message_before_invalid = message_text
                    message_text = "Input inválido"
                    continue

                inputs.append({"x": cell_x, "y": cell_y})

                if(game_state == GameState.RED_TO_MOVE_BLOCK or game_state == GameState.RED_TO_MOVE_COIN):
                    enemy_color = 'b'
                else:
                    enemy_color = 'r'

                if(game_state == GameState.RED_TO_MOVE_BLOCK):
                    if(len(inputs) == 4):
                        if(has_full_block_overlap() or get_new_block_position() == None):
                            message_text = "Bloco inválido"
                            inputs = []
                            continue
                        register_inputs(game_state)

                        advanceState()
                        inputs = []
                elif(game_state == GameState.BLUE_TO_MOVE_BLOCK):
                    best_block_move_ai = get_best_block_move()
                    blue_player_position = best_block_move_ai
                    remove_previous_block('b')
                    draw_from_position(best_block_move_ai, 'b', img_blue_square)

                    advanceState()
                    inputs = []
                elif(game_state == GameState.RED_TO_MOVE_COIN):
                    register_inputs(game_state)

                    if(game_state == GameState.RED_TO_MOVE_COIN):
                        enemy_color = 'b'
                    else:
                        enemy_color = 'r'
                
                    advanceState()
                    inputs = []
                    chosen_coin = 9
                elif(game_state == GameState.BLUE_TO_MOVE_COIN):
                    best_coin_move_ai = get_best_coin_move()
                    if(best_coin_move_ai['coin'] == 1):
                        remove_previous_coin(1)
                        cells[best_coin_move_ai['position']['x']][best_coin_move_ai['position']['y']].has_coin = True
                        load_image(best_coin_move_ai['position']['x'], best_coin_move_ai['position']['y'], img_coin1)
                        coin1_position = {'x': best_coin_move_ai['position']['x'], 'y': best_coin_move_ai['position']['y']}
                    else:
                        remove_previous_coin(2)
                        cells[best_coin_move_ai['position']['x']][best_coin_move_ai['position']['y']].has_coin = True
                        load_image(best_coin_move_ai['position']['x'], best_coin_move_ai['position']['y'], img_coin2)
                        coin2_position = {'x': best_coin_move_ai['position']['x'], 'y': best_coin_move_ai['position']['y']}

                    advanceState()
                    inputs = []
                    chosen_coin = 9

                possible_moves_for_enemy = check_possible_moves_for(enemy_color)
                if(len(possible_moves_for_enemy) == 0):
                    game_over = True
                    if(enemy_color == 'r'):
                        message_text = "Jogador Azul ganhou!"
                    else:
                        message_text = "Jogador Vermelho ganhou!"

    screen.fill(WHITE)
    draw_grid()
    draw_buttons_and_message()
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if img_cells[x][y]:
                screen.blit(img_cells[x][y], ((x * CELL_SIZE) + 2, (y * CELL_SIZE) + 2))

    pygame.display.flip()