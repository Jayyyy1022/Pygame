import pygame
import sys
from Scenes import chapter1
##from Scenes import chapter2
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
        self.chapter1 = chapter1.Chapter1(self.screen, self.gameStateManager)
        ##self.chapter2 = chapter2.run(self.screen, self.gameStateManager)
        self.chapter3 = chapter3.Chapter3(self.screen, self.gameStateManager)

        self.states = {"menu": self.start, "chapter1": self.chapter1, "chapter2": self.level, "chapter3": self.chapter3, 
                       "ending": self.level, "level": self.level}

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

# ignore these, placeholder for testing
class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        # self.music_stopped = False
    
    def run(self, events):
    #     if not self.music_stopped:
    #         pygame.mixer.music.stop()
    #         pygame.mixer.music.unload()
    #         pygame.mixer.stop()
    #         self.music_stopped = True

        self.display.fill("blue")
        font = pygame.font.SysFont(None, 50)
        text = font.render("CHAPTER 2 - CAVE", True, (255, 255, 255))
        draw_text(self.display, "[p] chapter 3", (255,255,255), 400, 400)
        self.display.blit(text, (200, 250))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.gameStateManager.set_state("chapter3")


class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    
    def run(self, event):
        self.display.fill("red")
        draw_text(self.display, "[a] chapter 1", (255,255,255), 400, 250)
        draw_text(self.display, "[b] chapter 2 (not yet implemented)", (255,255,255), 400, 275)
        draw_text(self.display, "[c] chapter 3", (255,255,255), 400, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.gameStateManager.set_state("chapter1")
        if keys[pygame.K_b]:
            self.gameStateManager.set_state("chapter2")
        if keys[pygame.K_c]:
            self.gameStateManager.set_state("chapter3")

def draw_text(display, text, color, x, y):
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midbottom = (x, y)
        display.blit(text_surface, text_rect)


if __name__ == "__main__":
    game = Game()
    game.run()