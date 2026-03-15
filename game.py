import pygame
import sys
from Scenes import chapter1
from Scenes import chapter2
from Scenes import chapter3
from Scenes import game_state_manager as gsm
from Scenes import main_menu

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Christmas Alone")
        self.clock = pygame.time.Clock()

        self.gameStateManager = gsm.GameStateManager("menu")
        self.start = Start(self.screen, self.gameStateManager)
        self.chapter1 = chapter1.Chapter1(self.screen, self.gameStateManager)
        self.chapter2 = chapter2.Chapter2(self.screen, self.gameStateManager)
        self.chapter3 = chapter3.Chapter3(self.screen, self.gameStateManager)
        self.mainMenu = main_menu.MainMenu(self.screen, self.gameStateManager, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.states = {"menu": self.mainMenu, 
                       "chapter1": self.chapter1, 
                       "chapter2": self.chapter2, 
                       "chapter3": self.chapter3}

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.gameStateManager.get_state()].run(events)    

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()