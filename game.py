import pygame
import sys
from Scenes import chapter3
from Scenes import game_state_manager as gsm

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Good Night, Sleep Tight")
        self.clock = pygame.time.Clock()

        self.gameStateManager = gsm.GameStateManager("menu")
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager)
        self.chapter3 = chapter3.Chapter3(self.screen, self.gameStateManager)

        self.states = {"menu": self.start, "chapter1": self.level, "chapter2": self.level, "chapter3": self.chapter3, 
                       "ending": self.level, "level": self.level}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.gameStateManager.get_state()].run()    

            pygame.display.flip()
            self.clock.tick(FPS)


class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    
    def run(self):
        self.display.fill("blue")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state("menu")


class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    
    def run(self):
        self.display.fill("red")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.gameStateManager.set_state("chapter3")


if __name__ == "__main__":
    game = Game()
    game.run()