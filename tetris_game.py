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


def draw_text_middle(text, size, color, surface):
    pass


def draw_grid(surface, grid):
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x, top_left_y + i * block_size), (top_left_x + play_width, top_left_y + i * block_size))
        for ii in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (top_left_x + ii * block_size, top_left_y), (top_left_x + ii * block_size, top_left_y + play_height))


def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    pass


def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('arial', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, 30))

    for i in range(len(grid)):
        for ii in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][ii], (top_left_x + ii * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)

    pygame.display.update()


def main(go):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

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
                        current_piece -= 1

        shape_position = convert_shape_format(current_piece)

        for i in range(len(shape_position)):
            x, y = shape_position[i]
            if y > -1:
                grid[y][x] =  current_piece.color

        if change_piece:
            for position in shape_position:
                p = (position[0], position[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

        draw_window(go, grid)

        if check_lost(locked_positions):
            run = False

    pygame.display.quit()


def main_menu(steady):
    main(steady)


ready = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu(ready)
