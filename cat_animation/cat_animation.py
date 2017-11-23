import pygame
import sys
from pygame.locals import *


pygame.init()

FPS = 60
fps_clock = pygame.time.Clock()

DISPLAYSURFACE = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Cat Animation')

WHITE = (255, 255, 255)
cat_image = pygame.image.load('cat.png')
cat_x = 10
cat_y = 10
direction = 'right'

while True:
    DISPLAYSURFACE.fill(WHITE)

    if direction == 'right':
        cat_x += 5
        if cat_x == 280:
            direction = 'down'
    elif direction == 'down':
        cat_y += 5
        if cat_y == 220:
            direction = 'left'
    elif direction == 'left':
        cat_x -= 5
        if cat_x == 10:
            direction = 'up'
    elif direction == 'up':
        cat_y -= 5
        if cat_y == 10:
            direction = 'right'

    DISPLAYSURFACE.blit(cat_image, (cat_x, cat_y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps_clock.tick(FPS)
