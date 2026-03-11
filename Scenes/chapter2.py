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

# ---------------- ASSETS ----------------
player_size = 40
player_image = pygame.image.load(os.path.join("Assets", "Player", "player_idle.png")).convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))
font = pygame.font.SysFont(None, 30)

# ---------------- GLOBAL VARIABLES ----------------
light_radius = 200      # universal torch radius
dim_speed = 0.5         # universal dim speed

# ---------------- UTILITY FUNCTIONS ----------------
def update_player(player_x, player_y, velocity_y, dt, speed=200, gravity=900, ground_y=460):
    """Handles player movement, input, and gravity."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= speed * dt
    if keys[pygame.K_d]:
        player_x += speed * dt
    if keys[pygame.K_w] and player_y >= ground_y:
        velocity_y = -500

    player_x = max(0, min(WIDTH - player_size, player_x))

    # gravity
    velocity_y += gravity * dt
    player_y += velocity_y * dt

    if player_y >= ground_y:
        player_y = ground_y
        velocity_y = 0

    return player_x, player_y, velocity_y

def draw_player_with_light(player_x, player_y):
    """Draws player and surrounding darkness using universal light_radius."""
    screen.blit(player_image, (player_x, player_y))
    darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    darkness.fill((0, 0, 0, 180))
    center = (player_x + player_size // 2, player_y + player_size // 2)
    pygame.draw.circle(darkness, (0, 0, 0, 0), center, int(light_radius))
    screen.blit(darkness, (0, 0))

# ---------------- SCENES ----------------
def scene1():
    global light_radius
    player_x, player_y = 120, -50
    velocity_y = 0
    ground_y = 460
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
                player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
                if player_rect.colliderect(sign_rect):
                    show_dialogue = not show_dialogue

        # Update player
        player_x, player_y, velocity_y = update_player(player_x, player_y, velocity_y, dt, ground_y=ground_y)

        # Draw background
        screen.fill((40, 40, 40))
        pygame.draw.rect(screen, (70, 50, 30), (0, 500, WIDTH, 100))  # ground

        # Scene-specific light cone
        cone_points = [(80, 0), (160, 0), (250, HEIGHT), (0, HEIGHT)]
        cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surface, (255, 255, 200, 120), cone_points)
        screen.blit(cone_surface, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (80, 0, 80, 20))

        # Sign
        pygame.draw.rect(screen, (200, 180, 100), sign_rect)

        # Player + darkness
        draw_player_with_light(player_x, player_y)

        # Interaction hint
        if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(sign_rect):
            hint = font.render("Press E", True, (255, 255, 255))
            screen.blit(hint, (sign_rect.x - 10, sign_rect.y - 30))

        # Dialogue
        if show_dialogue:
            dialogue = font.render("Escape before the light fades.", True, (255, 255, 255))
            screen.blit(dialogue, (player_x - 120, player_y - 40))

        # Universal torch dim
        if light_radius > 10:
            light_radius -= dim_speed * dt

        pygame.display.update()

        # Next scene
        if player_x + player_size >= WIDTH:
            scene2()
            return

def scene2():
    global light_radius
    player_x, player_y = 50, 500
    velocity_y = 0
    ground_y = 580
    platforms = [
        pygame.Rect(0, 200, 150, 20),
        pygame.Rect(650, 200, 150, 20),
        pygame.Rect(650, 400, 150, 20)
    ]
    running = True

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update player
        player_x, player_y, velocity_y = update_player(player_x, player_y, velocity_y, dt, ground_y=ground_y)

        # Platform collisions
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for plat in platforms:
            if player_rect.colliderect(plat) and velocity_y >= 0:
                player_y = plat.top - player_size
                velocity_y = 0

        # Draw background & platforms
        screen.fill((50, 50, 100))
        for plat in platforms:
            pygame.draw.rect(screen, (150, 100, 50), plat)

        # Player + darkness
        draw_player_with_light(player_x, player_y)

        # Universal torch dim
        if light_radius > 10:
            light_radius -= dim_speed * dt

        pygame.display.update()

def scene3():
    global light_radius
    player_x, player_y = 100, -50
    velocity_y = 0
    ground_y = 460
    monster_size = 40
    monster_x = player_x - 100
    monster_y = -50
    monster_speed = 150

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player update
        player_x, player_y, velocity_y = update_player(player_x, player_y, velocity_y, dt, ground_y=ground_y)

        # Monster falling & chasing
        if monster_y < ground_y:
            monster_y += 900 * dt
        else:
            if monster_x < player_x:
                monster_x += monster_speed * dt
            elif monster_x > player_x:
                monster_x -= monster_speed * dt

        # Draw
        screen.fill((40, 40, 40))
        pygame.draw.rect(screen, (70, 50, 30), (0, 500, WIDTH, 100))  # ground

        # Scene-specific light cone
        cone_points = [(80, 0), (160, 0), (250, HEIGHT), (0, HEIGHT)]
        cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surface, (255, 255, 200, 120), cone_points)
        screen.blit(cone_surface, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (80, 0, 80, 20))

        # Player + darkness
        draw_player_with_light(player_x, player_y)

        # Monster
        monster_rect = pygame.Rect(monster_x, monster_y, monster_size, monster_size)
        pygame.draw.rect(screen, (200, 50, 50), monster_rect)

        # Universal torch dim
        if light_radius > 10:
            light_radius -= dim_speed * dt

        pygame.display.update()

        # Next scene
        if player_x + player_size >= WIDTH:
            scene4()
            return

def scene4():
    global light_radius
    player_x, player_y = 50, 460
    velocity_y = 0
    ground_y = 460
    running = True

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player update
        player_x, player_y, velocity_y = update_player(player_x, player_y, velocity_y, dt, ground_y=ground_y)

        # Draw background
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (70, 50, 30), (0, 500, WIDTH, 100))  # ground

        # Scene-specific light cone
        cone_points = [
            (WIDTH, 100),
            (WIDTH-100, 0),
            (WIDTH-200, HEIGHT),
            (WIDTH, HEIGHT-100)
        ]
        cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surface, (255, 255, 200, 120), cone_points)
        screen.blit(cone_surface, (0, 0))

        # Player + darkness
        draw_player_with_light(player_x, player_y)

        # Universal torch dim
        if light_radius > 10:
            light_radius -= dim_speed * dt

        pygame.display.update()

        # Exit through light cone
        if player_x + player_size >= WIDTH-200:
            print("Player exited through the light! Scene complete!")
            return

# ---------------- MAIN ----------------
scene1()
pygame.quit()
sys.exit()