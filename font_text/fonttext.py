import pygame
import sys
from pygame.locals import *


pygame.init()
DISPLAY_SURFACE = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello font world!')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

font_object = pygame.font.Font('freesansbold.ttf', 32)
text_surface_object = font_object.render('Hello, font world!', True, GREEN, BLUE)
text_rect = text_surface_object.get_rect()
text_rect.center = (200, 150)

while True:
    DISPLAY_SURFACE.fill(WHITE)
    DISPLAY_SURFACE.blit(text_surface_object, text_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
