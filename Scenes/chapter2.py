import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Entities.Player.player_child import Player_Child as Player
from Entities.Enemy.enemy_krampus import Enemy_Krampus as Krampus
from Entities.Obstacle.platform import Platform


pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chapter 2")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)

# ---------------- ASSETS ----------------
ice_cave_bg = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Ice_cave_1.png")).convert()
ice_cave_bg = pygame.transform.scale(ice_cave_bg, (WIDTH, HEIGHT))
ice_cave_bg2 = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Ice_cave_2.png")).convert_alpha()
ice_cave_bg2 = pygame.transform.scale(ice_cave_bg2, (WIDTH, HEIGHT))
ice_cave_bg3 = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Ice_cave_exit.png")).convert_alpha()
ice_cave_bg3 = pygame.transform.scale(ice_cave_bg3, (WIDTH, HEIGHT))
sign = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Wooden_Sign.png")).convert_alpha()
sign = pygame.transform.scale(sign, (40, 60))

# ---------------- GLOBAL TORCH ----------------
light_radius = 200
dim_speed = 1.5


# ---------------- LIGHT SYSTEM ----------------
def draw_player_with_light(player):
    global light_radius

    player.draw(screen)

    darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    center = player.rect.center

    # ---- Flicker based on torch size ----
    min_radius = 20
    max_radius = 200

    # normalize radius
    radius_ratio = max(0, min(1, (light_radius - min_radius) / (max_radius - min_radius)))
    
    # darker environment when torch is weak
    darkness_alpha = 220 - (radius_ratio * 120)

    darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    darkness.fill((0, 0, 0, int(darkness_alpha)))

    # flicker speed increases as light gets smaller
    flicker_speed = 5 + (1 - radius_ratio) * 25

    flicker = (pygame.time.get_ticks() * flicker_speed / 1000) % 8 - 4

    radius = max(10, light_radius + flicker)
    
    if light_radius < 40 and pygame.time.get_ticks() % 500 < 40:
        radius = 5

    pygame.draw.circle(darkness, (0, 0, 0, 0), center, int(radius))

    screen.blit(darkness, (0, 0))
    
# ---------------- KRAMPUS DANGER ----------------
def draw_krampus_danger(player, krampus):

    # distance between player and krampus
    distance = abs(player.rect.centerx - krampus.rect.centerx)

    danger_range = 200

    if distance < danger_range:

        # stronger red when closer
        intensity = int((1 - distance / danger_range) * 120)

        red_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, intensity))

        screen.blit(red_overlay, (0, 0))


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

        screen.blit(ice_cave_bg, (0, 0))

        for p in platforms:
            screen.blit(p.image, p.rect)

        screen.blit(sign, sign_rect)
        
        cone_points = [(80, 0), (160, 0), (250, HEIGHT), (0, HEIGHT)]
        
        cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        pygame.draw.polygon(
            cone_surface,
            (255, 255, 200, 120),
            cone_points)
        
        screen.blit(cone_surface, (0, 0))

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

    player = Player(10, 430, 0.1, 4, 0.5)

    platforms = [
        Platform(0, 500, 150, 20),
        Platform(300, 420, 200, 20),
        Platform(650, 500, 150, 20),
        Platform(650, 200, 150, 20),
        Platform(0, 0, 0, 0),  # Placeholder
        Platform(0, 0, 0, 0)  # Placeholder
    ]

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move(platforms)

        screen.blit(ice_cave_bg2, (0, 0))

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

    player = Player(10, 430, 0.1, 4, 0.5)

    platforms = [
        Platform(0, 500, WIDTH, 100)
    ]

    krampus = Krampus(player.rect.x, -50, 0.2, 2, 0.5)

    monster_speed = 150

    # --- Spawn delay ---
    spawn_delay = 0.5
    spawn_timer = 0
    krampus_active = False
    krampus_on_ground = False

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move(platforms)

        # --- Spawn timer ---
        spawn_timer += dt

        if spawn_timer >= spawn_delay:
            krampus_active = True

        # --- Krampus behaviour ---
        if krampus_active:

            # --- Falling ---
            if not krampus_on_ground:

                krampus.rect.y += 900 * dt

                for p in platforms:

                    if krampus.rect.bottom >= p.rect.top:
                        krampus.rect.bottom = p.rect.top
                        krampus_on_ground = True

            # --- Chase after landing ---
            else:

                if krampus.rect.x < player.rect.x:
                    krampus.rect.x += monster_speed * dt
                    krampus.facingRight = True

                elif krampus.rect.x > player.rect.x:
                    krampus.rect.x -= monster_speed * dt
                    krampus.facingRight = False

        # --- Draw background ---
        screen.blit(ice_cave_bg2, (0, 0))

        for p in platforms:
            screen.blit(p.image, p.rect)
        
        # --- Player torch ---
        draw_player_with_light(player)

        # --- Draw Krampus ---
        if krampus_active:
            krampus.draw(screen)
            draw_krampus_danger(player, krampus)

        # --- Collision ---
        if krampus_active and player.rect.colliderect(krampus.rect):

            text = font.render("You were caught...", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))

            pygame.display.update()
            pygame.time.delay(2000)

            return

        # --- Torch dim ---
        if light_radius > 10:
            light_radius -= dim_speed * dt

        pygame.display.update()

        # --- Scene transition ---
        if player.rect.right >= WIDTH:
            scene4()
            return


# ---------------- SCENE 4 EXIT ----------------
def scene4():

    global light_radius

    player = Player(10, 430, 0.1, 4, 0.5)

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

        screen.blit(ice_cave_bg3, (0, 0))

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

        if player.rect.right >= WIDTH:
            ##Credits or next chapter here
            return


# ---------------- START ----------------
scene1()

pygame.quit()
sys.exit()