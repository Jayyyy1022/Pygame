import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Entities.Player.player_child import Player_Child as Player
from Entities.Obstacle.platform import Platform

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Christmas Alone - Chapter 2")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)

# ---------------- GLOBAL TORCH ----------------
light_radius = 200
dim_speed = 1


# ---------------- LIGHT SYSTEM ----------------
def draw_player_with_light(player):
    global light_radius

    player.draw(screen)

    darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    darkness.fill((0, 0, 0, 180))

    center = player.rect.center

    # ---- Flicker based on torch size ----
    min_radius = 20
    max_radius = 200

    # normalize radius
    radius_ratio = max(0, min(1, (light_radius - min_radius) / (max_radius - min_radius)))

    # flicker speed increases as light gets smaller
    flicker_speed = 5 + (1 - radius_ratio) * 25

    flicker = (pygame.time.get_ticks() * flicker_speed / 1000) % 8 - 4

    radius = max(10, light_radius + flicker)
    
    if light_radius < 40 and pygame.time.get_ticks() % 500 < 40:
        radius = 5

    pygame.draw.circle(darkness, (0, 0, 0, 0), center, int(radius))

    screen.blit(darkness, (0, 0))


# ---------------- SCENE 1 ----------------
def scene1():

    global light_radius

    player = Player(120, -50, 0.1, 4, 0.5)

    platforms = [
        Platform(0, 500, WIDTH, 100)
    ]

    sign_rect = pygame.Rect(380, 440, 40, 60)
    show_dialogue = False

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_e:
                    if player.rect.colliderect(sign_rect):
                        show_dialogue = not show_dialogue

        player.move(platforms)

        screen.fill((40, 40, 40))

        for p in platforms:
            screen.blit(p.image, p.rect)

        pygame.draw.rect(screen, (200, 180, 100), sign_rect)
        
        cone_points = [(80, 0), (160, 0), (250, HEIGHT), (0, HEIGHT)]
        
        cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        pygame.draw.polygon(
            cone_surface,
            (255, 255, 200, 120),
            cone_points)
        
        screen.blit(cone_surface, (0, 0))
        
        pygame.draw.rect(screen, (0, 0, 0), (80, 0, 80, 20))

        draw_player_with_light(player)

        if player.rect.colliderect(sign_rect):

            hint = font.render("Press E", True, (255, 255, 255))
            screen.blit(hint, (sign_rect.x - 10, sign_rect.y - 30))

        if show_dialogue:

            text = font.render("Escape before the light fades.", True, (255, 255, 255))
            screen.blit(text, (player.rect.x - 120, player.rect.y - 40))

        if light_radius > 10:
            light_radius -= dim_speed * dt

        pygame.display.update()

        if player.rect.right >= WIDTH:
            scene2()
            return


# ---------------- SCENE 2 PLATFORM LEVEL ----------------
def scene2():

    global light_radius

    player = Player(120, -50, 0.1, 4, 0.5)

    platforms = [
        Platform(0, 500, 150, 20),
        Platform(300, 420, 200, 20),
        Platform(650, 500, 150, 20),
        Platform(650, 200, 150, 20)
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
            screen.blit(p.image, p.rect)

        draw_player_with_light(player)

        if light_radius > 10:
            light_radius -= dim_speed * dt

        pygame.display.update()

        if player.rect.right >= WIDTH:
            scene3()
            return


# ---------------- SCENE 3 MONSTER CHASE ----------------
def scene3():

    global light_radius

    player = Player(120, -50, 0.1, 4, 0.5)

    platforms = [
        Platform(0, 500, WIDTH, 100)
    ]

    monster_size = 40
    monster_x = player.rect.x - 200
    monster_y = -50
    monster_speed = 150

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move(platforms)

        if monster_y < 460:
            monster_y += 900 * dt

        else:

            if monster_x < player.rect.x:
                monster_x += monster_speed * dt

            if monster_x > player.rect.x:
                monster_x -= monster_speed * dt

        screen.fill((40, 40, 40))

        for p in platforms:
            screen.blit(p.image, p.rect)

        draw_player_with_light(player)

        monster_rect = pygame.Rect(monster_x, monster_y, monster_size, monster_size)
        pygame.draw.rect(screen, (200, 50, 50), monster_rect)

        if player.rect.colliderect(monster_rect):

            text = font.render("You were caught...", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            return

        if light_radius > 10:
            light_radius -= dim_speed * dt

        pygame.display.update()

        if player.rect.right >= WIDTH:
            scene4()
            return


# ---------------- SCENE 4 EXIT ----------------
def scene4():

    global light_radius

    player = Player(120, -50, 0.1, 4, 0.5)

    platforms = [
        Platform(0, 500, WIDTH, 100)
    ]

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move(platforms)

        screen.fill((30, 30, 30))

        for p in platforms:
            screen.blit(p.image, p.rect)

        cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        pygame.draw.polygon(
            cone_surface,
            (255, 255, 200, 120),
            [
                (WIDTH, 100),
                (WIDTH - 100, 0),
                (WIDTH - 200, HEIGHT),
                (WIDTH, HEIGHT - 100)
            ]
        )

        screen.blit(cone_surface, (0, 0))

        draw_player_with_light(player)

        if light_radius > 10:
            light_radius -= dim_speed * dt

        pygame.display.update()

        if player.rect.right >= WIDTH - 200:

            text = font.render("You escaped the forest...", True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(3000)

            return


# ---------------- START ----------------
scene1()

pygame.quit()
sys.exit()