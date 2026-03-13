import pygame
import sys
import os
import random


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Entities.Player.player_child import Player_Child as Player
from Entities.Enemy.enemy_krampus import Enemy_Krampus as Krampus
from Entities.Obstacle.platform import Platform
from Scenes import game_state_manager

pygame.init()
pygame.mixer.init()

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
cave_platform = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Cave_platforms_1.png")).convert_alpha()
key_image = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Key.png")).convert_alpha()
key_image = pygame.transform.scale(key_image, (30, 30))
door_image = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Cave_door.png")).convert_alpha()
door_image = pygame.transform.scale(door_image, (50, 80))  # match the rectangle size

fall_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Fall_down.mp3"))
ghost_whisper = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Ghost_whisper.mp3"))
ghost_whisper.set_volume(0)  # start muted
ghost_playing = False
door_appear_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Door_appear.mp3"))
jumpscare_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "jumpscare.wav"))
krampus_spawn_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "E_spawn.mp3"))
exit_scream = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Exit_scream.mp3"))

# ---------------- GLOBAL TORCH ----------------
light_radius = 200
dim_speed = 2


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

    global ghost_playing

    # Start ghost whisper when radius <= 150
    if light_radius <= 150:
        if not ghost_playing:
            ghost_whisper.play(loops=-1)
            ghost_playing = True

        # Gradually increase volume as light dims (150 -> 10 maps to 0 -> 1)
        volume = max(0, min(1, (150 - light_radius) / (150 - 10)))
        ghost_whisper.set_volume(volume)

# ---------------- GAME OVER ----------------
def game_over():

    global light_radius
    global ghost_playing

    # stop ghost whisper
    ghost_whisper.stop()
    ghost_playing = False
    ghost_whisper.set_volume(0)

    # completely dark screen
    screen.fill((0, 0, 0))
    pygame.display.update()

    pygame.time.delay(800)

    # play jumpscare sound
    jumpscare_sound.play()

    # white flash effect
    flash = pygame.Surface((WIDTH, HEIGHT))
    flash.fill((255, 255, 255))
    screen.blit(flash, (0, 0))
    pygame.display.update()

    pygame.time.delay(200)

    # back to darkness
    screen.fill((0, 0, 0))
    pygame.display.update()

    pygame.time.delay(1200)

    # game over text
    text = font.render("You were caught by Krampus...", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - 160, HEIGHT // 2))

    pygame.display.update()

    pygame.time.delay(2000)

    # reset torch
    light_radius = 200

    # restart game
    scene1()

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
        
    player_landed = False

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

        # --- Check if player landed ---
        on_ground = any(player.rect.bottom == p.rect.top for p in platforms)

        if on_ground and not player_landed:
            fall_sound.play()  # play only once
            player_landed = True

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

        if light_radius > 0:
            light_radius -= dim_speed * dt
        else:
            game_over()
        

        pygame.display.update()

        if player.rect.right >= WIDTH:
            scene2()
            return


# ---------------- SCENE 2 PLATFORM LEVEL ----------------
def scene2():

    global light_radius

    player = Player(10, 430, 0.1, 4, 0.5)

    # --- Platforms ---
    platforms = [
        Platform(0, 500, 150, 50),     # starting platform(bottom left)
        Platform(650, 250, 150, 50),   # top right
        Platform(200, 380, 150, 50),   # middle left
        Platform(50, 150, 150, 50),    # top left (key here)
        Platform(350, 150, 150, 50),   # top middle
        Platform(450, 380, 150, 50),   # middle
        Platform(650, 500, 150, 50)    # Exit (bottom right)
    ]

    # --- Key collectible ---
    key_rect = pygame.Rect(80, 110, 30, 30)  # positioned above top-left platform
    key_collected = False

    # --- Exit door ---
    door_rect = pygame.Rect(700, 440, 50, 80)  # exit door on bottom right platform
    door_visible = False

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Player movement ---
        player.move(platforms)

        # --- Check key collection ---
        if not key_collected and player.rect.colliderect(key_rect):
            key_collected = True
            door_visible = True  # door appears after collecting key
            door_appear_sound.play()

        # --- Prevent scene transition until key collected ---
        proceed_to_next_scene = False
        if door_visible and player.rect.colliderect(door_rect):
            proceed_to_next_scene = True

        # --- Check fall off screen ---
        if player.rect.top >= HEIGHT:
            scene1()
            return

        # --- Draw background ---
        screen.blit(ice_cave_bg2, (0, 0))

        # --- Draw platforms ---
        for p in platforms:
            p.image = pygame.transform.scale(cave_platform, (p.rect.width, p.rect.height))
            screen.blit(p.image, p.rect)

        # --- Draw key ---
        if not key_collected:
            screen.blit(key_image, key_rect.topleft)

        # --- Draw exit door ---
        if door_visible:
            screen.blit(door_image, door_rect.topleft)

        # --- Draw player with torch effect ---
        draw_player_with_light(player)

        # --- Torch dimming ---
        if light_radius > 0:
            light_radius -= dim_speed * dt
        else:
            game_over()

        pygame.display.update()

        # --- Scene transition only if player touches the door ---
        if proceed_to_next_scene:
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
    spawn_delay = 10000000000000000000000000
    spawn_timer = 0
    krampus_active = False
    krampus_on_ground = False
    shake_timer = 0
    shake_strength = 8

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move(platforms)
        
        if player.rect.left < 0:
            player.rect.left = 0

        # --- Spawn timer ---
        spawn_timer += dt

        if spawn_timer >= spawn_delay and not krampus_active:
            krampus_active = True
            shake_timer = 0.8
            krampus_spawn_sound.play()

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

        # --- Screen shake offset ---
        shake_x = 0
        shake_y = 0

        if shake_timer > 0:
            shake_timer -= dt
            shake_x = random.randint(-shake_strength, shake_strength)
            shake_y = random.randint(-shake_strength, shake_strength)

        # --- Draw background ---
        screen.blit(ice_cave_bg2, (shake_x, shake_y))

        for p in platforms:
            screen.blit(p.image, (p.rect.x + shake_x, p.rect.y + shake_y))
        
        # --- Player torch ---
        draw_player_with_light(player)

        # --- Draw Krampus ---
        if krampus_active:
            krampus.draw(screen)
            draw_krampus_danger(player, krampus)

        # --- Collision ---
        if krampus_active and player.rect.colliderect(krampus.rect):
            game_over()
            return

        # --- Torch dim ---
        if light_radius > 0:
            light_radius -= dim_speed * dt
        else:
            game_over()

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
        
        if player.rect.left < 0:
            player.rect.left = 0

        screen.blit(ice_cave_bg3, (0, 0))

        for p in platforms:
            screen.blit(p.image, p.rect)

        cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        pygame.draw.polygon(
            cone_surface,
            (255, 255, 200, 120),
            [
                (WIDTH, 260),          # right edge center
                (WIDTH - 60, 200),     # top narrow part
                (WIDTH - 450, 450),    # extend cone far left
                (WIDTH - 450, 520),    # extend cone far left bottom
                (WIDTH - 60, 360)      # bottom narrow part
            ]
        )

        screen.blit(cone_surface, (0, 0))

        draw_player_with_light(player)

        if light_radius > 0:
            light_radius -= dim_speed * dt
        else:
            game_over()

        pygame.display.update()

        if player.rect.right >= WIDTH:

            # play scream
            exit_scream.play()

            # slow white fade
            flash = pygame.Surface((WIDTH, HEIGHT))
            flash.fill((255, 255, 255))

            for alpha in range(0, 255, 5):  # controls speed of fade
                flash.set_alpha(alpha)

                screen.blit(ice_cave_bg3, (0, 0))

                for p in platforms:
                    screen.blit(p.image, p.rect)

                draw_player_with_light(player)

                screen.blit(flash, (0, 0))
                
                if alpha > 180:
                    text = font.render("You hear a loud screeching from Krampus but you escaped...", True, (0, 0, 0))
                    screen.blit(text, (WIDTH // 2 - 300, HEIGHT // 2))

                pygame.display.update()
                pygame.time.delay(30)

            pygame.time.delay(6000)

            from Scenes.chapter3 import Chapter3  # make sure the path is correct
            chapter3 = Chapter3(screen, game_state_manager)  # pass your display and gameStateManager
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                chapter3.run(events)
                pygame.display.update()
                clock.tick(60)


# ---------------- START ----------------
scene3()

pygame.quit()
sys.exit()