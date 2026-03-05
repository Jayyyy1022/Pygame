import pygame

WHITE = (255, 255, 255)
RED = (199, 40, 78)

def drawBG(screen):
    screen.fill(WHITE)
    pygame.draw.line(screen, RED, (0, 500), (800, 500))