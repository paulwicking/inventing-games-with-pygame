"""
Memory puzzle.
http://inventwithpython.com/pygame
"""
import pygame
import random
import sys
from pygame.locals import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
REVEAL_SPEED = 8
BOX_SIZE = 40
GAP_SIZE = 10
BOARD_WIDTH = 10
BOARD_HEIGHT = 7

assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'

X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)

GRAY = (100, 100, 100)
NAVY_BLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

BG_COLOR = NAVY_BLUE
LIGHT_BG_COLOR = GRAY
BOX_COLOR = WHITE
HIGHLIGHT_COLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= BOARD_WIDTH * BOARD_HEIGHT, \
    "Board is too big for the number of shapes/colors."


def main():
    global FPS_CLOCK, DISPLAY_SURFACE
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    mouse_x = 0
    mouse_y = 0
    pygame.display.set_caption('Memory Game')

    game_board = get_randomized_board()
    revealed_boxes = generate_revealed_boxes_data(False)

    first_selection = None

    DISPLAY_SURFACE.fill(BG_COLOR)
    start_game_animation(game_board)

    while True:
        mouse_clicked = False

        DISPLAY_SURFACE.fill(BG_COLOR)
        draw_board(game_board, revealed_boxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True

        box_x, box_y = get_box_at_pixel(mouse_x, mouse_y)
        if box_x is not None and box_y is not None:  # The mouse is over a box
            if not revealed_boxes[box_x][box_y]:
                draw_highlight_box(box_x, box_y)
            if not revealed_boxes[box_x][box_y] and mouse_clicked:
                reveal_boxes_animation(game_board, [(box_x, box_y)])
                revealed_boxes[box_x][box_y] = True  # set the box as revealed

                if first_selection is None:
                    first_selection = (box_x, box_y)
                else:
                    icon1shape, icon1color = get_shape_and_color(game_board, first_selection[0], first_selection[1])
                    icon2shape, icon2color = get_shape_and_color(game_board, box_x, box_y)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)  # milliseconds
                        cover_boxes_animation(game_board, [(first_selection[0], first_selection[1]), (box_x, box_y)])
                        revealed_boxes[first_selection[0]][first_selection[1]] = False
                        revealed_boxes[box_x][box_y] = False
                    elif has_won(revealed_boxes):
                        game_won_animation(game_board)
                        pygame.time.wait(2000)

                        game_board = get_randomized_board()
                        revealed_boxes = generate_revealed_boxes_data(False)

                        draw_board(game_board, revealed_boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        start_game_animation(game_board)
                    first_selection = None

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def generate_revealed_boxes_data(value):
    revealed_boxes = []
    for i in range(BOARD_WIDTH):
        revealed_boxes.append([value] * BOARD_HEIGHT)
    return revealed_boxes


def get_randomized_board():
    """Get a list of every possible shape in every possible color."""
    icons = []
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            icons.append((shape, color))

    random.shuffle(icons)
    number_of_icons_used = int(BOARD_WIDTH * BOARD_HEIGHT / 2)
    icons = icons[:number_of_icons_used] * 2
    random.shuffle(icons)

    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)

    return board


def split_into_groups_of(group_size, the_list):
    """Splits a list into a list of lists, where the inner list have at most group_size number of items."""
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i:i + group_size])

    return result


def left_top_coords_of_box(box_x, box_y):
    """Convert board coordinates to pixel coordinates."""
    left = box_x * (BOX_SIZE + GAP_SIZE) + X_MARGIN
    top = box_y * (BOX_SIZE + GAP_SIZE) + Y_MARGIN

    return left, top


def get_box_at_pixel(x, y):
    for box_x in range(BOARD_WIDTH):
        for box_y in range(BOARD_HEIGHT):
            left, top = left_top_coords_of_box(box_x, box_y)
            box_rect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if box_rect.collidepoint(x, y):
                return box_x, box_y

    return None, None


def draw_icon(shape, color, box_x, box_y):
    quarter = int(BOX_SIZE * 0.25)
    half = int(BOX_SIZE * 0.5)

    left, top = left_top_coords_of_box(box_x, box_y)

    if shape == DONUT:
        pygame.draw.circle(DISPLAY_SURFACE, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAY_SURFACE, BG_COLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAY_SURFACE, color, (left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(
            DISPLAY_SURFACE,
            color,
            (
                (left + half, top),
                (left + BOX_SIZE - 1, top + half),
                (left + half, top + BOX_SIZE - 1),
                (left, top + half)
            ))
    elif shape == LINES:
        for i in range(0, BOX_SIZE, 4):
            pygame.draw.line(DISPLAY_SURFACE, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAY_SURFACE, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAY_SURFACE, color, (left, top + quarter, BOX_SIZE, half))


def get_shape_and_color(board, box_x, box_y):
    """
    Shape value for x, y spot is stored in board[x][y][0].
    Color value for x, y spot is stored in board[x][y][1].
    """
    return board[box_x][box_y][0], board[box_x][box_y][1]


def draw_box_covers(board, boxes, coverage):
    """Draws boxes being covered/revealed. "boxes" is a list of two-item lists, which have the x & y spot of the box."""
    for box in boxes:
        left, top = left_top_coords_of_box(box[0], box[1])
        pygame.draw.rect(DISPLAY_SURFACE, BG_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
        shape, color = get_shape_and_color(board, box[0], box[1])
        draw_icon(shape, color, box[0], box[1])
        if coverage > 0:  # only draw the cover if there is a coverage
            pygame.draw.rect(DISPLAY_SURFACE, BOX_COLOR, (left, top, coverage, BOX_SIZE))

    pygame.display.update()
    FPS_CLOCK.tick(FPS)


def reveal_boxes_animation(board, boxes_to_reveal):
    """Do the "box reveal" animation."""
    for coverage in range(BOX_SIZE, (-REVEAL_SPEED) - 1, - REVEAL_SPEED):
        draw_box_covers(board, boxes_to_reveal, coverage)


def cover_boxes_animation(board, boxes_to_cover):
    """Do the "box cover" animation."""
    for coverage in range(0, BOX_SIZE + REVEAL_SPEED, REVEAL_SPEED):
        draw_box_covers(board, boxes_to_cover, coverage)


def draw_board(board, revealed):
    """Draws all the boxes in their covered or revealed state."""
    for box_x in range(BOARD_WIDTH):
        for box_y in range(BOARD_HEIGHT):
            left, top = left_top_coords_of_box(box_x, box_y)
            if not revealed[box_x][box_y]:
                # draw a covered box
                pygame.draw.rect(DISPLAY_SURFACE, BOX_COLOR, (left, top, BOX_SIZE, BOX_SIZE))
            else:
                shape, color = get_shape_and_color(board, box_x, box_y)
                draw_icon(shape, color, box_x, box_y)


def draw_highlight_box(box_x, box_y):
    left, top = left_top_coords_of_box(box_x, box_y)
    pygame.draw.rect(DISPLAY_SURFACE, HIGHLIGHT_COLOR, (left - 5, top - 5, BOX_SIZE + 10, BOX_SIZE + 10), 4)


def start_game_animation(board):
    """Randomly reveal the boxes 8 at a time."""
    covered_boxes = generate_revealed_boxes_data(False)
    boxes = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    box_groups = split_into_groups_of(8, boxes)

    draw_board(board, covered_boxes)
    for box_group in box_groups:
        reveal_boxes_animation(board, box_group)
        cover_boxes_animation(board, box_group)


def game_won_animation(board):
    """Flash the background color when the player has won."""
    covered_boxes = generate_revealed_boxes_data(True)
    color1 = LIGHT_BG_COLOR
    color2 = BG_COLOR

    for i in range(13):
        color1, color2 = color2, color1
        DISPLAY_SURFACE.fill(color1)
        draw_board(board, covered_boxes)
        pygame.display.update()
        pygame.time.wait(300)


def has_won(revealed_boxes):
    """Returns True if all the boxes have been revealed, otherwise False."""
    for i in revealed_boxes:
        if False in i:
            return False

    return True


if __name__ == '__main__':
    main()
