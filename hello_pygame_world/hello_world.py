import pygame
import sys

from pygame.locals import *


pygame.init()
DISPLAYSURFACE = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Hello world!')
while True:  # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
