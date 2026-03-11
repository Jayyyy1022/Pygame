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
    dim_speed = 15

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

        if keys[pygame.K_LEFT]:
            player_x -= player_speed * dt

        if keys[pygame.K_RIGHT]:
            player_x += player_speed * dt

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
        cone_points = [(80,0),(160,0),(250,400),(0,400)]

        cone_surface = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
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
                "The torch will fade... escape quickly.",
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


# ---------------- MAIN ----------------
scene1()

pygame.quit()
sys.exit()