import pygame
import sys
from Scenes import chapter1
## from Scenes import chapter2

## Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Good Night, Sleep Tight")

## --- SCENE MANAGER (The Router) ---
current_scene = "CHAPTER1" 

while True:
    if current_scene == "CHAPTER1":
        ## Run your chapter file. It will return "CHAPTER2" or "QUIT" when finished.
        current_scene = chapter1.run(screen)
        
    elif current_scene == "CHAPTER2":
        ## current_scene = chapter2.run(screen)
        print("Transitioning to Chapter 2! (Teammate's file will run here)")
        break ## Stop for now since chapter 2 isn't ready
        
    elif current_scene == "QUIT":
        break

pygame.quit()
sys.exit()