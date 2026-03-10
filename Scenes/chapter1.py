import pygame
import os
import random
from Entities.Player import player_child as Player
from Entities.Enemy import enemy_krampus as Enemy
from Entities.Obstacle.platform import Platform

def run(screen):
    clock = pygame.time.Clock()
    FPS = 60

    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()
    GRAVITY = 0.75
    MOVEMENT_SPEED = 3

    BG_ROOM_COLOR = (40, 40, 40)   
    BG_FOREST_COLOR = (10, 15, 30) 
    current_bg_color = BG_ROOM_COLOR 

    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    ## --- Load Sounds ---
    pygame.mixer.init()
    try:
        sound_path = os.path.join(ROOT_DIR, "Assets", "SFX", "jumpscare.wav")
        jingle_sfx = pygame.mixer.Sound(sound_path) 
        jingle_sfx.set_volume(0.2)
    except:
        jingle_sfx = None

    ## --- Initialize Entities ---
    player = Player.Player_Child(100, 300, 0.1, MOVEMENT_SPEED, GRAVITY)
    enemy = Enemy.Enemy_Krampus(-600, 400, 0.15, MOVEMENT_SPEED * 1.1, GRAVITY)
    enemies_group = pygame.sprite.Group()
    enemies_group.add(enemy)

    ## --- Build the Level (Platforms) ---
    platforms = pygame.sprite.Group()
    
    wood_floor_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "wood_floor.png")
    woods_platform_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "woods_platform.png")
    rock_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "rock.png")
    
    ## Load forest background image
    forest_bg_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "forest_bg.png")
    try:
        bg_surface = pygame.image.load(forest_bg_img).convert_alpha()
        ## Scale the background image to fit the screen
        bg_surface = pygame.transform.scale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        bg_surface = None

    ## --- Scene 1: Starting Room ---
    ## Foundation for the room floor (fills the bottom gap)
    platforms.add(Platform(0, 530, 500, 70, color=(45, 25, 15))) 
    ## Surface wood floor image
    platforms.add(Platform(0, 500, 500, 30, image_path=wood_floor_img)) 

    ## The door
    door = Platform(500, 350, 40, 150, (139, 69, 19))
    platforms.add(door)
    is_door_opened = False
    
    ## --- Scene 2 & 3: Forest ---
    ## Base forest floor
    platforms.add(Platform(540, 500, 4000, 100, color=(34, 139, 34))) 
    ## Forest obstacles
    platforms.add(Platform(1000, 430, 120, 70, image_path=woods_platform_img))
    platforms.add(Platform(1500, 450, 150, 50, image_path=rock_img))
      
    ## --- Initialize Snowflakes ---
    camera_scroll = 0
    chase_started = False
    snowflakes = []
    for i in range(100):
        x = random.randrange(0, SCREEN_WIDTH)
        y = random.randrange(0, SCREEN_HEIGHT)
        speed = random.randrange(1, 4)
        size = random.randrange(1, 3)
        snowflakes.append([x, y, speed, size])

    ## --- MAIN GAME LOOP ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT" 

        keys = pygame.key.get_pressed()
        
        ## Auto-open door logic
        if not is_door_opened:
            interaction_area = player.rect.inflate(40, 0) 
            if interaction_area.colliderect(door.rect):
                door.kill() 
                is_door_opened = True
                current_bg_color = BG_FOREST_COLOR 
                if jingle_sfx:
                    jingle_sfx.play() 

        player.move(platforms)

        ## Camera scrolling logic
        if player.rect.right > SCREEN_WIDTH // 2:
            scroll_amount = player.rect.right - (SCREEN_WIDTH // 2)
            player.rect.right = SCREEN_WIDTH // 2 
            camera_scroll += scroll_amount
            
            for p in platforms:
                p.rect.x -= scroll_amount
            enemy.rect.x -= scroll_amount

        ## Enemy chase logic
        if camera_scroll > 1500:
            if not chase_started:
                enemy.rect.x = -150 
                chase_started = True
            enemy.rect.x += 6 

        ## Game over & restart logic
        if pygame.sprite.spritecollideany(player, enemies_group):
            print("Caught by Krampus! Restarting Chapter 1...")
            try:
                if hasattr(enemy, 'shriek'):
                    enemy.shriek()
            except:
                pass
            pygame.time.delay(1000) 
            return "CHAPTER1" 

        ## Transition to Chapter 2
        if player.rect.y > SCREEN_HEIGHT + 100:
            print("Player fell! Transitioning to Chapter 2...")
            return "CHAPTER2" 

        ## --- RENDERING ---
        screen.fill(current_bg_color) 
        
        if is_door_opened:
            ## Draw the forest background with parallax scrolling
            if bg_surface:
                ## 0.3 is the scroll ratio for parallax effect
                scroll_offset = (camera_scroll * 0.3) % SCREEN_WIDTH
                ## Draw two images side by side for infinite seamless scrolling
                screen.blit(bg_surface, (-scroll_offset, 0))
                screen.blit(bg_surface, (-scroll_offset + SCREEN_WIDTH, 0))
                
            ## Draw snowflakes
            for flake in snowflakes:
                flake[1] += flake[2] 
                flake[0] += random.choice([-1, 0, 1]) 
                if flake[1] > SCREEN_HEIGHT:
                    flake[1] = random.randrange(-50, -10)
                    flake[0] = random.randrange(0, SCREEN_WIDTH)
                pygame.draw.circle(screen, (255, 255, 255), (flake[0], flake[1]), flake[3])
        
        platforms.draw(screen)
        player.draw(screen)
        enemy.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)