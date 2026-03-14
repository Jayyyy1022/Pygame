import pygame
import sys
import os
import random


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Entities.Player.player_child import Player_Child as Player
from Entities.Enemy.enemy_krampus import Enemy_Krampus as Krampus
from Entities.Obstacle.platform import Platform
from Scenes import game_state_manager
from Entities.Obstacle.falling_rock import FallingRock

pygame.init()
pygame.mixer.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chapter 2")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)

landing_dialogue_shown = False
scene2_entry_dialogue_shown = False  # for "Is that a key..."
scene2_key_dialogue_shown = False    # for "A door appeared..."

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
rock_path = os.path.join("Assets", "Miscellaneous", "rock.png")  # Add this line

fall_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Fall_down.mp3"))
ghost_whisper = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Ghost_whisper.mp3"))
ghost_whisper.set_volume(0)  # start muted
ghost_playing = False
door_appear_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Door_appear.mp3"))
jumpscare_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "jumpscare.wav"))
krampus_spawn_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "E_spawn.mp3"))
exit_scream = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Exit_scream.mp3"))
collision_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Collision.mp3"))
collision_sound.set_volume(0.6)
rumble_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Rumble.mp3"))
rumble_sound.set_volume(0.5)
rumble2_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Rumble_2.mp3"))
rumble2_sound.set_volume(0.8)

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

    flicker = random.randint(-5,5)

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
    global current_bgm  # optional: reset current bgm tracker

    # stop ghost whisper
    ghost_whisper.stop()
    ghost_playing = False
    ghost_whisper.set_volume(0)

    # stop background music
    pygame.mixer.music.stop()
    current_bgm = None  # reset so BGM can start fresh next scene

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

# ---------------- GLOBAL BGM ----------------
bgm_scene1_2_path = os.path.join("Assets", "SFX", "Scene_1n2bgm.mp3")
bgm_scene3_4_path = os.path.join("Assets", "SFX", "Scene_3n4bgm.mp3")
current_bgm = None  # keep track of which music is playing

def play_bgm(scene_name, volume=0.5):
    """Play the correct BGM based on scene. Only switches if needed."""
    global current_bgm

    # Determine which BGM to play
    if scene_name in ["scene1", "scene2"]:
        bgm_to_play = bgm_scene1_2_path
    elif scene_name in ["scene3", "scene4"]:
        bgm_to_play = bgm_scene3_4_path
    else:
        return  # no music for unknown scenes

    # Only reload/play if different from current
    if current_bgm != bgm_to_play and os.path.exists(bgm_to_play):
        pygame.mixer.music.load(bgm_to_play)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=-1)
        current_bgm = bgm_to_play


# ---------------- SCENE 1 ----------------
def scene1():
    global light_radius
    global landing_dialogue_shown   # persists across scene reloads

    play_bgm("scene1")

    player = Player(120, -50, 0.1, 4, 0.5) 
    
    show_sign_dialogue = False
    sign_dialogue_timer = 0
    
    player_landed = False
    dialogue_stage = 0      # 0 = no dialogue, 1 = first line, 2 = second line
    dialogue_timer = 0      # to time the second line
    
    prev_on_ground = False

    platforms = [
        Platform(0, 500, WIDTH, 100)
    ]

    sign_rect = pygame.Rect(380, 440, 40, 60)

    running = True

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    if player.rect.colliderect(sign_rect):
                        show_sign_dialogue = True
                        sign_dialogue_timer = 0  # reset timer

        player.move(platforms)

        # --- Check if player landed ---
        on_ground = any(player.rect.bottom == p.rect.top for p in platforms)

        # Play landing SFX every time player lands, but show dialogue only once
        if on_ground and not player_landed and not prev_on_ground:
            fall_sound.play()  # landing SFX
            player_landed = True

            if not landing_dialogue_shown:
                dialogue_stage = 1
                dialogue_timer = 0
                landing_dialogue_shown = True  # lock dialogue permanently

        prev_on_ground = on_ground

        # --- Draw background and platforms ---
        screen.blit(ice_cave_bg, (0, 0))
        for p in platforms:
            screen.blit(p.image, p.rect)
        screen.blit(sign, sign_rect)

        # --- Torch/light cone overlay ---
        cone_points = [(80, 0), (160, 0), (250, HEIGHT), (0, HEIGHT)]
        cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surface, (255, 255, 200, 120), cone_points)
        screen.blit(cone_surface, (0, 0))

        # --- Dialogue handling ---
        if dialogue_stage > 0:
            dialogue_timer += dt

            if dialogue_stage == 1:
                # First line
                text = font.render("Ouff! Where am I....", True, (255, 255, 255))
                padding = 6
                box_width = text.get_width() + padding*2
                box_height = text.get_height() + padding*2
                box_x = player.rect.centerx - box_width//2
                box_y = player.rect.y - 60
                pygame.draw.rect(screen, (0,0,0), (box_x, box_y, box_width, box_height))
                screen.blit(text, (box_x + padding, box_y + padding))

                if dialogue_timer >= 1.5:  # after 1.5 seconds
                    dialogue_stage = 2
                    dialogue_timer = 0

            elif dialogue_stage == 2:
                # Second line
                text = font.render("I need to get out of here!", True, (255, 255, 255))
                padding = 6
                box_width = text.get_width() + padding*2
                box_height = text.get_height() + padding*2
                box_x = player.rect.centerx - box_width//2
                box_y = player.rect.y - 60
                pygame.draw.rect(screen, (0,0,0), (box_x, box_y, box_width, box_height))
                screen.blit(text, (box_x + padding, box_y + padding))

                if dialogue_timer >= 2:   # show for 2 seconds
                    dialogue_stage = 0

        # --- Sign interaction ---
        if player.rect.colliderect(sign_rect):
            # Draw black box
            hint_text = "Press J"
            text_surface = font.render(hint_text, True, (255, 255, 255))
            padding = 6
            box_width = text_surface.get_width() + padding*2
            box_height = text_surface.get_height() + padding*2
            box_x = sign_rect.x - 10
            box_y = sign_rect.y - 35
            pygame.draw.rect(screen, (0,0,0), (box_x, box_y, box_width, box_height))
            screen.blit(text_surface, (box_x + padding, box_y + padding))

        # --- Show sign dialogue if activated ---
        if show_sign_dialogue:
            sign_dialogue_timer += dt
            text = font.render("Escape before the light fades. What does that mean...", True, (255, 255, 255))
            padding = 6
            box_width = text.get_width() + padding*2
            box_height = text.get_height() + padding*2
            box_x = player.rect.centerx - box_width//2
            box_y = player.rect.y - 60
            pygame.draw.rect(screen, (0,0,0), (box_x, box_y, box_width, box_height))
            screen.blit(text, (box_x + padding, box_y + padding))

            if sign_dialogue_timer >= 2:  # display 2 seconds
                show_sign_dialogue = False

        # --- Draw player on top ---
        draw_player_with_light(player)

        # --- Torch dimming ---
        if light_radius > 0:
            light_radius -= dim_speed * dt
        else:
            game_over()

        pygame.display.update()

        # --- Scene transition ---
        if player.rect.right >= WIDTH:
            scene2()
            return


# ---------------- SCENE 2 PLATFORM LEVEL ----------------
def scene2():
    global light_radius
    global scene2_entry_dialogue_shown
    global scene2_key_dialogue_shown

    play_bgm("scene2")

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

    # --- Dialogue timers & stages ---
    entry_dialogue_stage = 0
    entry_dialogue_timer = 0
    key_dialogue_stage = 0
    key_dialogue_timer = 0

    # Show entry dialogue only once
    if not scene2_entry_dialogue_shown:
        entry_dialogue_stage = 1
        entry_dialogue_timer = 0
        scene2_entry_dialogue_shown = True

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

            # Trigger key-collected dialogue once
            if not scene2_key_dialogue_shown:
                key_dialogue_stage = 1
                key_dialogue_timer = 0
                scene2_key_dialogue_shown = True

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

        # --- Draw torch/light ---
        draw_player_with_light(player)

        # --- Entry dialogue ---
        if entry_dialogue_stage > 0:
            entry_dialogue_timer += dt
            if entry_dialogue_stage == 1:
                text = font.render("Is that a key on the top platform?", True, (255, 255, 255))
                padding = 6
                box_width = text.get_width() + padding*2
                box_height = text.get_height() + padding*2
                box_x = player.rect.centerx - box_width//2
                box_y = player.rect.y - 60
                pygame.draw.rect(screen, (0,0,0), (box_x, box_y, box_width, box_height))
                screen.blit(text, (box_x + padding, box_y + padding))

                if entry_dialogue_timer >= 2:  # display 2 seconds
                    entry_dialogue_stage = 0

        # --- Key collected dialogue ---
        if key_dialogue_stage > 0:
            key_dialogue_timer += dt
            if key_dialogue_stage == 1:
                text = font.render("A door appeared out of nowhere...", True, (255, 255, 255))
                padding = 6
                box_width = text.get_width() + padding*2
                box_height = text.get_height() + padding*2
                box_x = player.rect.centerx - box_width//2
                box_y = player.rect.y - 60
                pygame.draw.rect(screen, (0,0,0), (box_x, box_y, box_width, box_height))
                screen.blit(text, (box_x + padding, box_y + padding))

                if key_dialogue_timer >= 2:  # display 2 seconds
                    key_dialogue_stage = 0

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

    player = Player(10, 450, 0.1, 4, 0.5)
    
    first_shake_done = False   # for the first shake
    krampus_shake_done = False # for the Krampus entrance shake

    # ---------------- PLATFORMS ----------------
    platforms = [
        Platform(0, 500, 400, 100),
        Platform(400, 500, 400, 100),
        Platform(800, 500, 400, 100),
        Platform(1200, 500, 400, 100),
        Platform(1600, 500, 400, 100),  # New mid-level platform
        Platform(2000, 500, 400, 100)
    ]

    # ---------------- KRAMPUS ----------------
    krampus = Krampus(player.rect.x, -50, 0.2, 2, 0.5)
    monster_speed = 465

    # ---------------- CEILING PILLARS ----------------
    pillars = []
    pillar_width = 40
    pillar_height = 350  # longer pillar
    pillar_platforms = [
        (400, 0, 2),    # top-left platform area
        (850, 0, 1),   
        (1200, 0, 3),  # middle platform area
        (1600, 0, 2)   # new platform area
    ]
    for plat_x, plat_y, num_pillars in pillar_platforms:
        for i in range(num_pillars):
            spacing = 120
            x_pos = plat_x + i * spacing
            pillar = Platform(x_pos, plat_y, pillar_width, pillar_height)
            # Flip rock image for ceiling
            if os.path.exists(rock_path):
                img = pygame.image.load(rock_path).convert_alpha()
                img = pygame.transform.scale(img, (pillar_width, pillar_height))
                img = pygame.transform.flip(img, False, True)  # upside down
                pillar.image = img
            pillars.append(pillar)

    # ---------------- FALLING ROCKS ----------------
    falling_rocks = []
    rock_widths = [40, 50, 60]
    rock_heights = [40, 50, 60]

    # Ensure rocks spawn below the bottom of the tallest pillar
    lowest_rock_y = pillar_height + 20  # leaves a small gap below pillars
    stack_positions = [700, 1000, 1900, 2200]  # X positions
    for stack_x in stack_positions:
        y_offset = -50  # rocks start off-screen
        for i in range(2):  # max 2 rocks per stack
            width = random.choice(rock_widths)
            height = random.choice(rock_heights)
            rock_y = y_offset - i * height * 1.1
            # Ensure rocks are not overlapping pillar bottom
            if rock_y < lowest_rock_y:
                rock_y = lowest_rock_y + random.randint(0, 30)
            falling_rocks.append(FallingRock(
                stack_x,
                rock_y,
                width,
                height,
                rock_path
            ))
            
    # --- Invisible wall setup ---
    invisible_wall_x = 400 - 10 

    # ---------------- GAME LOOP ----------------
    spawn_delay = 2
    spawn_timer = 0
    krampus_active = False
    krampus_on_ground = False
    shake_timer = 0.8
    shake_strength = 8

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.move(platforms)
        camera_x = max(0, min(player.rect.centerx - WIDTH // 2, platforms[-1].rect.right - WIDTH))
        
        # --- Invisible wall logic ---
        if not krampus_on_ground:  # wall active until Krampus lands
            if player.rect.right > invisible_wall_x:
                player.rect.right = invisible_wall_x

        # --- Krampus spawn ---
        spawn_timer += dt
        if spawn_timer >= spawn_delay and not krampus_active:
            krampus_active = True
            shake_timer = 0.8  # trigger shake
            krampus_spawn_sound.play()

            # Play second rumble sound for Krampus entrance
            if not krampus_shake_done:
                pygame.mixer.Channel(6).play(rumble2_sound)
                krampus_shake_done = True

        # --- Krampus movement ---
        if krampus_active:
            if not krampus_on_ground:
                krampus.rect.y += 900 * dt
                for p in platforms:
                    if krampus.rect.bottom >= p.rect.top:
                        krampus.rect.bottom = p.rect.top
                        krampus_on_ground = True

                        # --- Play scene3 BGM only once when Krampus lands ---
                        play_bgm("scene3", volume=0.5)

            else:
                if krampus.rect.x < player.rect.x:
                    krampus.rect.x += monster_speed * dt
                    krampus.facingRight = True
                elif krampus.rect.x > player.rect.x:
                    krampus.rect.x -= monster_speed * dt
                    krampus.facingRight = False
            
        # --- Screen shake ---
        shake_x = shake_y = 0
        if shake_timer > 0:
            shake_timer -= dt
            shake_x = random.randint(-shake_strength, shake_strength)
            shake_y = random.randint(-shake_strength, shake_strength)

            if not first_shake_done:
                pygame.mixer.Channel(5).play(rumble_sound)  # play first shake rumble
                first_shake_done = True

        # --- Draw background ---
        screen.blit(ice_cave_bg2, (shake_x, shake_y))

        # --- Draw platforms ---
        for p in platforms:
            screen.blit(p.image, (p.rect.x - camera_x + shake_x, p.rect.y + shake_y))

        # --- Draw ceiling pillars ---
        for pillar in pillars:
            screen.blit(pillar.image, (pillar.rect.x - camera_x + shake_x, pillar.rect.y + shake_y))

        # --- Update and draw falling rocks ---
        for rock in falling_rocks:
            rock.update(dt, platforms, falling_rocks)
            rock.draw(screen, camera_x, shake_y)

        # --- Player torch ---
        original_x = player.rect.x
        player.rect.x -= camera_x
        draw_player_with_light(player)
        player.rect.x = original_x

        # --- Draw Krampus ---
        if krampus_active:
            screen.blit(
                pygame.transform.flip(krampus.img, not krampus.facingRight, False),
                (krampus.rect.x - camera_x, krampus.rect.y)
            )
            draw_krampus_danger(player, krampus)

        # --- Collision with krampus ---
        if krampus_active and player.rect.colliderect(krampus.rect):
            game_over()
            return

        # --- Collision with rocks ---
        for rock in falling_rocks:
            if rock.solid and player.rect.colliderect(rock.rect):
                # Move player out of rock
                if player.rect.centerx < rock.rect.centerx:
                    player.rect.right = rock.rect.left
                else:
                    player.rect.left = rock.rect.right

                collision_sound.play()

        # --- Collision with ceiling pillars ---
        for pillar in pillars:
            if player.rect.colliderect(pillar.rect):
                if player.rect.centery < pillar.rect.centery:
                    player.rect.bottom = pillar.rect.top
                else:
                    player.rect.top = pillar.rect.bottom
                    
                collision_sound.play()
                    

        # --- Torch dimming ---
        if light_radius > 0:
            light_radius -= dim_speed * dt
        else:
            game_over()

        pygame.display.update()

        # --- Scene transition ---
        if player.rect.right >= platforms[-1].rect.right:
            scene4()
            return

# ---------------- SCENE 4 EXIT ----------------
def scene4():

    global light_radius, current_bgm

    player = Player(10, 430, 0.1, 2, 0.5)

    platforms = [
        Platform(0, 500, WIDTH, 100)
    ]

    # --- Scene 4 Krampus setup ---
    krampus = Krampus(0, 430, 0.2, 2, 0.5)  # start off-screen left
    krampus_active = False                        # spawn after delay
    krampus_speed = 323                           # pixels per second
    krampus_spawn_delay = 1                       # 1 second delay
    krampus_timer = 0                              # timer to track delay

    running = True

    while running:

        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Player movement ---
        player.move(platforms)

        if player.rect.left < 0:
            player.rect.left = 0

        # --- Krampus spawn delay ---
        if not krampus_active:
            krampus_timer += dt
            if krampus_timer >= krampus_spawn_delay:
                krampus_active = True

        # --- Krampus movement ---
        if krampus_active:
            if krampus.rect.x < player.rect.x - 50:  # stop a little behind player
                krampus.rect.x += krampus_speed * dt
                krampus.facingRight = True
            else:
                krampus.rect.x = player.rect.x - 50  # stop near player

            # Draw Krampus
            screen.blit(
                pygame.transform.flip(krampus.img, not krampus.facingRight, False),
                (krampus.rect.x, krampus.rect.y)
            )

            # Collision triggers game over
            if player.rect.colliderect(krampus.rect):
                game_over()
                return

        # --- Draw background ---
        screen.blit(ice_cave_bg3, (0, 0))

        # --- Draw platforms ---
        for p in platforms:
            screen.blit(p.image, p.rect)

        # --- Draw light cone ---
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

        # --- Draw player with torch ---
        draw_player_with_light(player)
        
        if krampus_active:
            screen.blit(
                pygame.transform.flip(krampus.img, not krampus.facingRight, False),
                (krampus.rect.x, krampus.rect.y)
            )
            
        draw_krampus_danger(player, krampus)

        # --- Torch dimming ---
        if light_radius > 0:
            light_radius -= dim_speed * dt
        else:
            game_over()

        pygame.display.update()

        # --- Scene exit ---
        if player.rect.right >= WIDTH:

            # Stop BGM immediately
            pygame.mixer.stop() 
            pygame.mixer.music.stop()
            current_bgm = None

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

                # draw Krampus during fade
                if krampus_active:
                    screen.blit(
                        pygame.transform.flip(krampus.img, not krampus.facingRight, False),
                        (krampus.rect.x, krampus.rect.y)
                    )

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
scene1()

pygame.quit()
sys.exit()