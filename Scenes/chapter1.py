import pygame
import os
import random
from Entities.Player import player_child as Player
from Entities.Enemy import enemy_krampus as Enemy
from Entities.Obstacle.platform import Platform

def run(screen):
    clock = pygame.time.Clock()
    FPS = 60

    ## --- 1. Basic Setup & Colors ---
    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()
    GRAVITY = 0.75
    MOVEMENT_SPEED = 3

    ## Background Colors for Scene Transition
    BG_ROOM_COLOR = (40, 40, 40)   ## Dark gray for the starting room
    BG_FOREST_COLOR = (10, 15, 30) ## Creepy dark blue for the forest
    current_bg_color = BG_ROOM_COLOR ## Start in the room

    ## --- 2. Load Sounds (Safe Loading) ---
    pygame.mixer.init()
    try:
        sound_path = os.path.join("Assets", "SFX", "jumpscare.wav")
        jingle_sfx = pygame.mixer.Sound(sound_path) 
        jingle_sfx.set_volume(0.05)
    except:
        jingle_sfx = None
        print("Warning: SFX file not found, skipping audio.")

    ## --- 3. Initialize Entities ---
    player = Player.Player_Child(100, 300, 0.1, MOVEMENT_SPEED, GRAVITY)
    enemy = Enemy.Enemy_Krampus(-600, 400, 0.15, MOVEMENT_SPEED * 1.1, GRAVITY)
    
    enemies_group = pygame.sprite.Group()
    enemies_group.add(enemy)

    ## --- 4. Build the Level (Platforms) ---
    platforms = pygame.sprite.Group()
    
    wood_floor_img = os.path.join("Assets", "wood_floor.png")
    woods_platform_img = os.path.join("Assets", "woods_platform.png")
    rock_img = os.path.join("Assets", "rock.png")

    ## --- Scene 1:  ---
    platforms.add(Platform(0, 500, 500, 100, image_path=wood_floor_img)) 

    door = Platform(500, 350, 40, 150, (139, 69, 19))
    platforms.add(door)
    is_door_opened = False
    
    ## --- Scene 2 & 3:  ---
    platforms.add(Platform(540, 500, 2000, 100, color=(34, 139, 34))) 
    
    platforms.add(Platform(1000, 400, 160, 100, image_path=woods_platform_img))
    
    platforms.add(Platform(1500, 450, 150, 50, image_path=rock_img))
    
    ## Scene 4: Cliff (The forest floor ends at x=2540)
    camera_scroll = 0
    chase_started = False

    ## --- Initialize Snowflakes Array ---
    snowflakes = []
    for i in range(200):
        x = random.randrange(0, SCREEN_WIDTH)
        y = random.randrange(0, SCREEN_HEIGHT) 
        speed = random.randrange(1, 4) 
        size = random.randrange(1, 3) 
        snowflakes.append([x, y, speed, size])

    ## --- 5. THE MAIN GAME LOOP FOR CHAPTER 1 ---
    running = True
    while running:
        ## A. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT" 

        ## B. Player Input & Interaction
        keys = pygame.key.get_pressed()
        
        ## AUTO-OPEN DOOR (Proximity based)
        if not is_door_opened:
            interaction_area = player.rect.inflate(40, 0) 
            if interaction_area.colliderect(door.rect):
                door.kill() 
                is_door_opened = True
                
                ## DYNAMIC SCENE TRANSITION!
                current_bg_color = BG_FOREST_COLOR 
                print("Scene 2: Entered the Forest!")
                if jingle_sfx:
                    jingle_sfx.play() 

        ## C. Movement & Physics
        player.move(platforms)

        ## D. Camera Scrolling Logic
        if player.rect.right > SCREEN_WIDTH // 2:
            scroll_amount = player.rect.right - (SCREEN_WIDTH // 2)
            player.rect.right = SCREEN_WIDTH // 2 
            camera_scroll += scroll_amount
            
            for p in platforms:
                p.rect.x -= scroll_amount
            enemy.rect.x -= scroll_amount

        ## E. Enemy Chase Logic
        if camera_scroll > 1000:
            if not chase_started:
                enemy.rect.x = -150 
                chase_started = True
                print("Krampus is right behind you!!")
                
                if jingle_sfx: jingle_sfx.play()
            
            enemy.rect.x += 6

        ## F. GAME OVER & RESTART LOGIC
        if pygame.sprite.spritecollideany(player, enemies_group):
            print("Caught by Krampus! Restarting Chapter 1...")
            
            ## Try to play enemy shriek if it exists
            try:
                if hasattr(enemy, 'shriek'):
                    enemy.shriek()
            except:
                pass
                
            ## Freeze the game for 1 second before restarting
            pygame.time.delay(1000) 
            
            ## Return to main router to reload Chapter 1
            return "CHAPTER1" 

        ## G. Exit Condition (Falling off the cliff at the end)
        if player.rect.y > SCREEN_HEIGHT + 100:
            print("Player fell! Transitioning to Chapter 2...")
            return "CHAPTER2" 

        ## --- H. RENDERING ---
        screen.fill(current_bg_color)

        ## NDraw and update Snowflakes (ONLY IF IN THE FOREST)
        if is_door_opened:
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