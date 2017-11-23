import pygame
import sys

from pygame.locals import *


pygame.init()

DISPLAYSURFACE = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Drawing')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED_ALPHA = (255, 0, 0, 20)

DISPLAYSURFACE.fill(WHITE)
pygame.draw.polygon(DISPLAYSURFACE, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
pygame.draw.line(DISPLAYSURFACE, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(DISPLAYSURFACE, BLUE, (120, 60), (60, 120))
pygame.draw.line(DISPLAYSURFACE, BLUE, (60, 120), (120, 120), 4)
pygame.draw.circle(DISPLAYSURFACE, BLUE, (300, 50), 20, 0)
pygame.draw.ellipse(DISPLAYSURFACE, RED, (300, 250, 40, 80), 1)
pygame.draw.rect(DISPLAYSURFACE, RED_ALPHA, (200, 150, 100, 50))

pix_obj = pygame.PixelArray(DISPLAYSURFACE)
pix_obj[480][380] = BLACK
pix_obj[482][382] = BLACK
pix_obj[484][384] = BLACK
pix_obj[486][386] = BLACK
pix_obj[488][388] = BLACK
del pix_obj

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

