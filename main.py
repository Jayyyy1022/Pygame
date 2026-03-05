import pygame

from Entities.Player import player_child as Player

## Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGTH = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption("Good Night, Sleep Tight")

## Colors
WHITE = (255, 255, 255)

# player and player states
player = Player.Player_Child(100, 550, 0.1, 3)
# moving_left = False
# moving_right = False

## set framrate
clock = pygame.time.Clock()
FPS = 60

def drawbg():
    screen.fill(WHITE)

running = True
while running:
    drawbg()

    for event in pygame.event.get():
        ## Quit game
        if event.type == pygame.QUIT:
            running = False
        # ## Keyboard movement WASD
        # if event.type == pygame.K_a:
        #     moving_left = True
        # if event.type == pygame.K_d:
        #     moving_right = True


    player.draw(screen)
    player.move()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
