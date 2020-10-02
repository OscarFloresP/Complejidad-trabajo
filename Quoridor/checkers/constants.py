import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 17, 17
SQUARE_SIZE = WIDTH//COLS

# rgb

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
GREEN = (142,16,90)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
