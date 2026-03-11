import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Entities.Player.player_child import Player_Child as Player


pygame.init()

# ---------------- SETTINGS ----------------
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Christmas Alone - Chapter 2")

clock = pygame.time.Clock()

# ---------------- ASSETS ----------------
player_size = 40

player_image = pygame.image.load(
    os.path.join("Assets","Player","player_idle.png")
).convert_alpha()

player_image = pygame.transform.scale(player_image,(player_size,player_size))


font = pygame.font.SysFont(None,30)

# ---------------- SCENE 1 ----------------
def scene1():

    # -------- Player --------
    player_x = 120
    player_y = -50
    player_speed = 200

    # -------- Physics --------
    velocity_y = 0
    gravity = 900
    ground_y = 460

    # -------- Torch Light --------
    light_radius = 200
    dim_speed = 0.5

    # -------- Sign --------
    sign_rect = pygame.Rect(380,440,40,60)

    # -------- Dialogue --------
    show_dialogue = False

    running = True

    while running:

        dt = clock.tick(60)/1000

        # -------- EVENTS --------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_e:

                    player_rect = pygame.Rect(player_x,player_y,player_size,player_size)

                    if player_rect.colliderect(sign_rect):
                        show_dialogue = not show_dialogue

        # -------- INPUT --------
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player_x -= player_speed * dt

        if keys[pygame.K_d]:
            player_x += player_speed * dt
            
        # Jumping
        if keys[pygame.K_w] and player_y >= ground_y:
            velocity_y = -500  # adjust jump strength here

        player_x = max(0,min(WIDTH-player_size,player_x))

        # -------- GRAVITY --------
        velocity_y += gravity * dt
        player_y += velocity_y * dt

        if player_y >= ground_y:
            player_y = ground_y
            velocity_y = 0

        player_rect = pygame.Rect(player_x,player_y,player_size,player_size)

        # -------- BACKGROUND --------
        screen.fill((40,40,40))

        pygame.draw.rect(screen,(70,50,30),(0,500,WIDTH,100))

        # -------- LIGHT CONE --------
        cone_points = [(80,0), (160,0), (250,HEIGHT), (0,HEIGHT)]

        cone_surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surface,(255,255,200,120),cone_points)

        screen.blit(cone_surface,(0,0))

        pygame.draw.rect(screen,(0,0,0),(80,0,80,20))

        # -------- SIGN --------
        pygame.draw.rect(screen,(200,180,100),sign_rect)

        # -------- PLAYER --------
        screen.blit(player_image,(player_x,player_y))

        # -------- INTERACTION HINT --------
        if player_rect.colliderect(sign_rect):

            hint = font.render("Press E",True,(255,255,255))
            screen.blit(hint,(sign_rect.x-10,sign_rect.y-30))

        # -------- DIALOGUE --------
        if show_dialogue:

            dialogue = font.render(
                "Escape before the light fades.",
                True,(255,255,255)
            )

            screen.blit(dialogue,(player_x-120,player_y-40))

        # -------- DARKNESS --------
        darkness = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        darkness.fill((0,0,0,180))

        center = (player_x+player_size//2,player_y+player_size//2)

        pygame.draw.circle(darkness,(0,0,0,0),center,int(light_radius))

        screen.blit(darkness,(0,0))

        # -------- TORCH DIM --------
        if light_radius > 60:
            light_radius -= dim_speed * dt

        pygame.display.update()
        
        # -------- NEXT SCENE --------
        if player_x + player_size >= WIDTH:
            scene2()
            return

def scene2():
    # -------- Player --------
    player_x = 50
    player_y = 500
    player_speed = 200
    player_size = 40

    velocity_y = 0
    gravity = 900

    # -------- Platforms --------
    platforms = [
        pygame.Rect(0, 200, 150, 20),    # Top-left
        pygame.Rect(650, 200, 150, 20),   # Top-right
        pygame.Rect(650, 400, 150, 20)     # Right
        #(x, y, width, height)
    ]

    running = True

    while running:
        dt = clock.tick(60)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # -------- INPUT --------
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= player_speed * dt
        if keys[pygame.K_d]:
            player_x += player_speed * dt
        if keys[pygame.K_w] and velocity_y == 0:  # jump if on platform or ground
            velocity_y = -500

        # -------- GRAVITY --------
        velocity_y += gravity * dt
        player_y += velocity_y * dt

        # -------- COLLISION WITH PLATFORMS --------
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        on_platform = False

        for plat in platforms:
            if player_rect.colliderect(plat) and velocity_y >= 0:
                player_y = plat.top - player_size
                velocity_y = 0
                on_platform = True

        # -------- FLOOR LIMIT --------
        if player_y + player_size >= 580:
            player_y = 580 - player_size
            velocity_y = 0

        player_rect.topleft = (player_x, player_y)

        # -------- DRAWING --------
        screen.fill((50,50,100))

        # Draw platforms
        for plat in platforms:
            pygame.draw.rect(screen, (150,100,50), plat)

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        pygame.display.update()
        
def scene3():
    print("Scene 3 started!")

    # -------- Player --------
    player_size = 40
    player_x = 100
    player_y = -50          # Start above the screen (falling from hole)
    player_speed = 200

    # -------- Physics --------
    velocity_y = 0
    gravity = 900
    ground_y = 460

    # -------- Torch Light --------
    light_radius = 200
    dim_speed = 0.5

    # -------- Monster --------
    monster_size = 40
    monster_x = player_x - 100  # Start behind player
    monster_y = -50
    monster_speed = 150

    running = True

    while running:
        dt = clock.tick(60)/1000

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # -------- INPUT --------
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= player_speed * dt
        if keys[pygame.K_d]:
            player_x += player_speed * dt
        if keys[pygame.K_w] and player_y >= ground_y:
            velocity_y = -500

        player_x = max(0, min(WIDTH - player_size, player_x))

        # -------- GRAVITY --------
        velocity_y += gravity * dt
        player_y += velocity_y * dt

        if player_y >= ground_y:
            player_y = ground_y
            velocity_y = 0

        # -------- MONSTER MOVEMENT --------
        # Monster falls from same hole
        if monster_y < ground_y:
            monster_y += gravity * dt

        # Monster follows player horizontally after landing
        if monster_y >= ground_y:
            if monster_x < player_x:
                monster_x += monster_speed * dt
            elif monster_x > player_x:
                monster_x -= monster_speed * dt

        # -------- DRAWING --------
        screen.fill((40,40,40))
        pygame.draw.rect(screen, (70,50,30), (0,500,WIDTH,100))  # ground

        # -------- LIGHT CONE --------
        cone_points = [(80,0), (160,0), (250,HEIGHT), (0,HEIGHT)]
        cone_surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surface,(255,255,200,120),cone_points)
        screen.blit(cone_surface,(0,0))
        pygame.draw.rect(screen,(0,0,0),(80,0,80,20))

        # -------- PLAYER --------
        screen.blit(player_image,(player_x,player_y))

        # -------- MONSTER --------
        monster_rect = pygame.Rect(monster_x, monster_y, monster_size, monster_size)
        pygame.draw.rect(screen, (200,50,50), monster_rect)  # simple red square for monster

        # -------- DARKNESS --------
        darkness = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        darkness.fill((0,0,0,180))
        center = (player_x+player_size//2,player_y+player_size//2)
        pygame.draw.circle(darkness,(0,0,0,0),center,int(light_radius))
        screen.blit(darkness,(0,0))

        # -------- TORCH DIM --------
        if light_radius > 60:
            light_radius -= dim_speed * dt

        pygame.display.update()

        # -------- NEXT SCENE --------
        if player_x + player_size >= WIDTH:
            scene4()
            return
        
def scene4():
    print("Scene 4 started!")

    # -------- Player --------
    player_size = 40
    player_x = 50
    player_y = 460
    player_speed = 200

    # -------- Physics --------
    velocity_y = 0
    gravity = 900
    ground_y = 460

    # -------- Torch Light --------
    light_radius = 200
    dim_speed = 0.5

    running = True

    while running:
        dt = clock.tick(60)/1000

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # -------- INPUT --------
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= player_speed * dt
        if keys[pygame.K_d]:
            player_x += player_speed * dt
        if keys[pygame.K_w] and player_y >= ground_y:
            velocity_y = -500

        player_x = max(0, min(WIDTH - player_size, player_x))

        # -------- GRAVITY --------
        velocity_y += gravity * dt
        player_y += velocity_y * dt

        if player_y >= ground_y:
            player_y = ground_y
            velocity_y = 0

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        # -------- DRAWING --------
        screen.fill((30,30,30))   # background
        pygame.draw.rect(screen, (70,50,30), (0,500,WIDTH,100))  # ground

        # -------- LIGHT CONE (right → left diagonal) --------
        cone_points = [
            (WIDTH, 100),         # top-right
            (WIDTH-100, 0),       # top-left of cone
            (WIDTH-200, HEIGHT),  # bottom-left of cone
            (WIDTH, HEIGHT-100)   # bottom-right
        ]
        cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surface, (255,255,200,120), cone_points)
        screen.blit(cone_surface, (0,0))

        # -------- PLAYER --------
        screen.blit(player_image,(player_x,player_y))

        # -------- DARKNESS --------
        darkness = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        darkness.fill((0,0,0,180))
        center = (player_x+player_size//2, player_y+player_size//2)
        pygame.draw.circle(darkness, (0,0,0,0), center, int(light_radius))
        screen.blit(darkness,(0,0))

        # -------- TORCH DIM --------
        if light_radius > 60:
            light_radius -= dim_speed * dt

        pygame.display.update()

        # -------- EXIT THROUGH LIGHT CONE --------
        # Check if player is inside the cone (approximation using diagonal bounds)
        # Simple version: if player's x > WIDTH-200 and y is within cone slope
        if player_x + player_size >= WIDTH-200:
            # Optional: check y between the diagonal lines for more precision
            print("Player exited through the light! Scene complete!")
            return
        
# ---------------- MAIN ----------------
scene1()

pygame.quit()
sys.exit()