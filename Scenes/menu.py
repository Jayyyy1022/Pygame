# Scenes/menu.py
import pygame
import subprocess
import sys
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

# Buttons
ch1_button = pygame.Rect(300, 200, 200, 60)
ch2_button = pygame.Rect(300, 300, 200, 60)
font = pygame.font.SysFont(None, 40)

def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect)
    txt = font.render(text, True, WHITE)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)

# Get absolute path to the Scenes folder
scenes_folder = os.path.dirname(os.path.abspath(__file__))

running = True
while running:
    screen.fill(BLACK)
    draw_button(ch1_button, "Chapter 1", BLUE)
    draw_button(ch2_button, "Chapter 2", RED)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ch1_button.collidepoint(event.pos):
                # Open chapter1 and close menu
                subprocess.Popen([sys.executable, os.path.join(scenes_folder, "chapter1.py")])
                running = False
            elif ch2_button.collidepoint(event.pos):
                # Open chapter2 and close menu
                subprocess.Popen([sys.executable, os.path.join(scenes_folder, "chapter2.py")])
                running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()