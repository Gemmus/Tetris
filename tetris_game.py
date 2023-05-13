import pygame
import random

pygame.font.init()

#######################
#   Global Variable   #
#######################
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

###############################
#   Blocks and their shapes   #
###############################

RhodeIsland_Z = [['.....',
                  '......',
                  '..00..',
                  '.00...',
                  '.....'],
                 ['.....',
                  '..0..',
                  '..00.',
                  '...0.',
                  '.....']]

Cleveland_Z = [['.....',
                '.....',
                '.00..',
                '..00.',
                '.....'],
               ['.....',
                '..0..',
                '.00..',
                '.0...',
                '.....']]

Hero = [['..0..',
         '..0..',
         '..0..',
         '..0..',
         '.....'],
        ['.....',
         '0000.',
         '.....',
         '.....',
         '.....']]

Smashboy = [['.....',
             '.....',
             '.00..',
             '.00..',
             '.....']]

BlueRicky = [['.....',
              '.0...',
              '.000.',
              '.....',
              '.....'],
             ['.....',
              '..00.',
              '..0..',
              '..0..',
              '.....'],
             ['.....',
              '.....',
              '.000.',
              '...0.',
              '.....'],
             ['.....',
              '..0..',
              '..0..',
              '.00..',
              '.....']]

OrangeRicky = [['.....',
                '...0.',
                '.000.',
                '.....',
                '.....'],
               ['.....',
                '..0..',
                '..0..',
                '..00.',
                '.....'],
               ['.....',
                '.....',
                '.000.',
                '.0...',
                '.....'],
               ['.....',
                '.00..',
                '..0..',
                '..0..',
                '.....']]

Teewee = [['.....',
           '..0..',
           '.000.',
           '.....',
           '.....'],
          ['.....',
           '..0..',
           '..00.',
           '..0..',
           '.....'],
          ['.....',
           '.....',
           '.000.',
           '..0..',
           '.....'],
          ['.....',
           '..0..',
           '.00..',
           '..0..',
           '.....']]

shapes = [RhodeIsland_Z, Cleveland_Z, Hero, Smashboy, BlueRicky, OrangeRicky, Teewee]
shape_colors = [(0, 240, 1), (240, 35, 0), (2, 240, 240), (240, 240, 0), (4, 47, 240), (240, 160, 0), (159, 52, 240)]

############################
#   Classes and Functions  #
############################


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for ii in range(len(grid[i])):
            if (ii, i) in locked_positions:
                c = locked_positions[(ii, i)]
                grid[i][ii] = c
    return grid


def convert_shape_format(shape):
    positions = []
    formation = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(formation):
        row = list(line)
        for ii, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + ii, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions


def valid_space(shape, grid):
    accepted_position = [[(ii, i) for ii in range(10) if grid[i][ii] == (0, 0, 0)] for i in range(20)]
    accepted_position = [ii for sub in accepted_position for ii in sub]

    formatted = convert_shape_format(shape)

    for position in formatted:
        if position not in accepted_position:
            if position[1] > -1:
                return False
    return True


def check_lost(positions):
    for position in positions:
        x, y = position
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('arial', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width()/2), (top_left_y + play_height / 2 - label.get_height() / 2) - 100))


def draw_grid(surface, grid):
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x, top_left_y + i * block_size), (top_left_x + play_width, top_left_y + i * block_size))
        for ii in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (top_left_x + ii * block_size, top_left_y), (top_left_x + ii * block_size, top_left_y + play_height))


def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for ii in range(len(row)):
                try:
                    del locked[(ii, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1]) [::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    x_position = top_left_x + play_width - 500
    y_position = top_left_y + play_height / 2 - 250
    formation = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(formation):
        row = list(line)
        for ii, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (x_position + ii * block_size, y_position + i * block_size, block_size, block_size), 0)

    surface.blit(label, (x_position + 10, y_position - 50))


def draw_window(surface, grid, score, time):
    highest_score = display_max_score()

    x_position = top_left_x + play_width - 500
    y_position = top_left_y + play_height / 2

    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('arial', 60)
    game_label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(game_label, (top_left_x + play_width / 2 - game_label.get_width() / 2, 20))

    font = pygame.font.SysFont('arial', 30)
    score_label1 = font.render('Score: ', 1, (255, 255, 255))
    score_label2 = font.render(str(score), 1, (255, 255, 255))
    time_label1 = font.render('Time: ', 1, (255, 255, 255))
    time_label2 = font.render(str(time), 1, (255, 255, 255))
    highest_score_label1 = font.render('Highest Score: ', 1, (255, 255, 255))
    highest_score_label2 = font.render(str(highest_score), 1, (255, 255, 255))

    surface.blit(score_label1, (x_position + 10, y_position + 20))
    surface.blit(score_label2, (x_position + 10, y_position + 52))
    surface.blit(time_label1, (x_position + 535, y_position + 20))
    surface.blit(time_label2, (x_position + 535, y_position + 52))
    surface.blit(highest_score_label1, (x_position + 535, y_position - 300))
    surface.blit(highest_score_label2, (x_position + 535, y_position - 268))

    for i in range(len(grid)):
        for ii in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][ii], (top_left_x + ii * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)


def time_converter(raw_time):
    second = 0
    second += int(raw_time / 1000)
    minute = 0
    hour = 0
    if second >= 60:
        second = 0
        minute += 1
    if minute >= 60:
        minute = 0
        hour += 1
    return f'{hour} h {minute} min {second} s'


def scoring_table(new_score):
    score = display_max_score()

    with open('scores.txt', 'w') as f:
        if int(score) < new_score:
            f.write(str(new_score))
        else:
            f.write(str(score))


def display_max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def main(go):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    level_time = 0
    score = 0
    raw_time = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        raw_time += clock.get_rawtime()
        time = time_converter(raw_time)
        clock.tick()

        if level_time/1000 > 5 :
            level_time = 0
            if fall_speed > 0.15:
                fall_time = 0.15

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_position = convert_shape_format(current_piece)

        for i in range(len(shape_position)):
            x, y = shape_position[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            score += 15
            for position in shape_position:
                p = (position[0], position[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 100

        draw_window(go, grid, score, time)
        draw_next_shape(next_piece, go)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(go, "You lost", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            scoring_table(score)


def main_menu(steady):
    run = True
    while run:
        steady.fill((0, 0, 0))
        draw_text_middle(steady, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(steady)

    pygame.display.quit()


ready = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu(ready)
