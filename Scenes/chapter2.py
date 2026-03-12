import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Entities.Player.player_child import Player_Child as Player

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Christmas Alone - Chapter 2")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)

# ---------------- GLOBAL VARIABLES ----------------
light_radius = 200
dim_speed = 20


# ---------------- PLATFORM CLASS ----------------
class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 100, 50), self.rect)


# ---------------- LIGHT SYSTEM ----------------
def draw_darkness(player):
    darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    darkness.fill((0, 0, 0, 200))

    center = (player.rect.centerx, player.rect.centery)

    pygame.draw.circle(darkness, (0, 0, 0, 0), center, int(light_radius))

    screen.blit(darkness, (0, 0))


# ---------------- SCENE 1 ----------------
def scene1():
    global light_radius

    player = Player(120, -50, 1, 4, 0.5)
    ground = Platform(0, 500, WIDTH, 100)
    platforms = [ground]

    sign_rect = pygame.Rect(380, 440, 40, 60)
    show_dialogue = False

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:

                if player.rect.colliderect(sign_rect):
                    show_dialogue = not show_dialogue

        player.move(platforms)

        screen.fill((40, 40, 40))

        ground.draw(screen)

        pygame.draw.rect(screen, (200, 180, 100), sign_rect)

        player.draw(screen)

        draw_darkness(player)

        if player.rect.colliderect(sign_rect):
            hint = font.render("Press E", True, (255, 255, 255))
            screen.blit(hint, (sign_rect.x - 10, sign_rect.y - 30))

        if show_dialogue:
            dialogue = font.render("Escape before the light fades.", True, (255, 255, 255))
            screen.blit(dialogue, (player.rect.x - 120, player.rect.y - 40))

        if light_radius > 20:
            light_radius -= dim_speed * dt

        pygame.display.update()

        if player.rect.right >= WIDTH:
            scene2()
            return


# ---------------- SCENE 2 ----------------
def scene2():
    global light_radius

    player = Player(50, 400, 1, 4, 0.5)

    platforms = [
        Platform(0, 200, 150, 20),
        Platform(650, 200, 150, 20),
        Platform(650, 400, 150, 20),
        Platform(0, 580, WIDTH, 20)
    ]

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move(platforms)

        screen.fill((50, 50, 100))

        for p in platforms:
            p.draw(screen)

        player.draw(screen)

        draw_darkness(player)

        if light_radius > 20:
            light_radius -= dim_speed * dt

        pygame.display.update()

        if player.rect.right >= WIDTH:
            scene3()
            return


# ---------------- SCENE 3 ----------------
def scene3():
    global light_radius

    player = Player(100, -50, 1, 4, 0.5)

    ground = Platform(0, 500, WIDTH, 100)
    platforms = [ground]

    monster_size = 40
    monster_x = player.rect.x - 100
    monster_y = -50
    monster_speed = 2

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move(platforms)

        if monster_y < 460:
            monster_y += 5
        else:
            if monster_x < player.rect.x:
                monster_x += monster_speed
            elif monster_x > player.rect.x:
                monster_x -= monster_speed

        screen.fill((40, 40, 40))

        ground.draw(screen)

        player.draw(screen)

        pygame.draw.rect(screen, (200, 50, 50), (monster_x, monster_y, monster_size, monster_size))

        draw_darkness(player)

        if light_radius > 20:
            light_radius -= dim_speed * dt

        pygame.display.update()

        if player.rect.right >= WIDTH:
            scene4()
            return


# ---------------- SCENE 4 ----------------
def scene4():
    global light_radius

    player = Player(50, 460, 1, 4, 0.5)

    ground = Platform(0, 500, WIDTH, 100)
    platforms = [ground]

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move(platforms)

        screen.fill((30, 30, 30))

        ground.draw(screen)

        player.draw(screen)

        draw_darkness(player)

        if light_radius > 20:
            light_radius -= dim_speed * dt

        pygame.display.update()

        if player.rect.right >= WIDTH - 200:
            print("Player escaped through the light!")
            return


# ---------------- START GAME ----------------
scene1()

pygame.quit()
sys.exit()