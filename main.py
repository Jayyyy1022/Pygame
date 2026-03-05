import pygame

from Entities.Player import player_child as Player
from Entities.Enemy import enemy_krampus as Enemy
from Scenes import testscene

## Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGTH = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption("Good Night, Sleep Tight")

## Colors
WHITE = (255, 255, 255)

## game variables
GRAVITY = 0.75

## player variables
MOVEMENT_SPEED = 3
PLAYER_X = 100
PLAYER_Y = 100
PLAYER_SIZE_SCALE = 0.1

player = Player.Player_Child(PLAYER_X, PLAYER_Y, PLAYER_SIZE_SCALE, MOVEMENT_SPEED, GRAVITY)
# moving_left = False
# moving_right = False

## enemy variabls 
ENEMY_X = 700
ENEMY_Y = 450
ENEMY_SIZE_SCALE = 0.15

enemy = Enemy.Enemy_Krampus(ENEMY_X, ENEMY_Y, ENEMY_SIZE_SCALE, MOVEMENT_SPEED, GRAVITY)

## set framrate
clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    testscene.drawBG(screen)

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

    enemy.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
