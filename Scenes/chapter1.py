import pygame
import os
import sys
import subprocess
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Entities.Player import player_child as Player
from Entities.Enemy import enemy_krampus as Enemy
from Entities.Obstacle.platform import Platform
from Entities.Decoration.prop import BackgroundDecoration

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

    ## --- 1. Load Sounds ---
    pygame.mixer.init()
    pygame.mixer.stop()
    pygame.mixer.music.stop()
    
    try:
        door_path = os.path.join(ROOT_DIR, "Assets", "SFX", "door_open.mp3")
        door_sfx = pygame.mixer.Sound(door_path) 
        door_sfx.set_volume(0.3)
    except:
        door_sfx = None

    try:
        jumpscare_path = os.path.join(ROOT_DIR, "Assets", "SFX", "jumpscare.wav")
        jumpscare_sfx = pygame.mixer.Sound(jumpscare_path)
        jumpscare_sfx.set_volume(0.1)
    except:
        jumpscare_sfx = None

    try:
        room_bgm_path = os.path.join(ROOT_DIR, "Assets", "SFX", "room_bgm.wav")
        pygame.mixer.music.load(room_bgm_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1) 
    except:
        print("Warning: Room BGM not found.")

    ## --- 2. Initialize Entities ---
    player = Player.Player_Child(100, 300, 0.1, MOVEMENT_SPEED, GRAVITY)
    enemy = Enemy.Enemy_Krampus(-600, 400, 0.15, MOVEMENT_SPEED * 1.1, GRAVITY)
    enemies_group = pygame.sprite.Group()
    enemies_group.add(enemy)

    ## --- 3. Build the Level ---
    platforms = pygame.sprite.Group()
    decorations = pygame.sprite.Group()
    
    wood_floor_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "wood_floor.png")
    woods_platform_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "woods_platform.png")
    rock_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "rock.png")
    snow_floor_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "snow_floor.png")
    room_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "room.png")
    wood_platform2_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "wood_platform2.png")
    wood_platform_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "wood_platform.png")
    wood_platform3_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "wood_platform3.png")
    
    forest_bg_img = os.path.join(ROOT_DIR, "Assets", "Miscellaneous", "forest_bg.png")
    try:
        bg_surface = pygame.image.load(forest_bg_img).convert_alpha()
        bg_surface = pygame.transform.scale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        bg_surface = None

    ## --- Build Room Walls (Decoration Layer) ---
    left_wall = BackgroundDecoration(0, 150, room_img, width=40, height=350)
    right_pillar = BackgroundDecoration(500, 150, room_img, width=60, height=200)
    decorations.add(left_wall, right_pillar)

    ## --- Physical Foundations ---
    platforms.add(Platform(0, 500, 500, 100, color=(45, 25, 15))) 
    platforms.add(Platform(0, 500, 500, 30, image_path=wood_floor_img)) 

    ## This makes it perfectly match the wall. We will draw a frame over it later.
    door = Platform(500, 350, 60, 150, image_path=room_img)
    platforms.add(door)
    is_door_opened = False
    
    platforms.add(Platform(500, 520, 4000, 80, color=(30, 30, 40))) 
    platforms.add(Platform(500, 500, 4000, 30, image_path=snow_floor_img)) 
    platforms.add(Platform(1000, 430, 120, 70, image_path=woods_platform_img))
    platforms.add(Platform(1500, 450, 150, 50, image_path=rock_img))

    platforms.add(Platform(1900, 450, 150, 50, image_path=rock_img)) 
    platforms.add(Platform(2000, 400, 120, 70, image_path=wood_platform2_img))
    platforms.add(Platform(2200, 350, 120, 70, image_path=wood_platform_img)) 

    platforms.add(Platform(2700, 450, 150, 50, image_path=rock_img))
    platforms.add(Platform(2750, 400, 150, 50, image_path=wood_floor_img))
    platforms.add(Platform(2800, 350, 150, 50, image_path=wood_platform3_img))

    platforms.add(Platform(3300, 430, 120, 70, image_path=wood_platform_img))
    platforms.add(Platform(3480, 430, 120, 70, image_path=woods_platform_img))
      
    ## --- Particle Systems & Trackers ---
    camera_scroll = 0
    chase_started = False
    
    snowflakes = []
    for i in range(100):
        snowflakes.append([random.randrange(0, SCREEN_WIDTH), random.randrange(0, SCREEN_HEIGHT), random.randrange(1, 4), random.randrange(1, 3)])

    room_x = 0  
    smoke_particles = [] 

    ## --- 4. MAIN GAME LOOP ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT" 

        keys = pygame.key.get_pressed()
        
        ## Door opening & Camera Snap logic
        if not is_door_opened:
            interaction_area = player.rect.inflate(40, 0) 
            if interaction_area.colliderect(door.rect):
                door.kill() 
                is_door_opened = True
                current_bg_color = BG_FOREST_COLOR 
                pygame.mixer.music.stop()
                if door_sfx:
                    door_sfx.play()

                ## Camera Snap
                snap_amount = 500
                for p in platforms: p.rect.x -= snap_amount
                for d in decorations: d.rect.x -= snap_amount
                enemy.rect.x -= snap_amount
                camera_scroll += snap_amount
                
                room_x -= snap_amount 
                for smoke in smoke_particles: smoke[0] -= snap_amount
                
                player.rect.x = 100

        player.move(platforms)

        ## Camera following logic
        if player.rect.right > SCREEN_WIDTH // 2:
            scroll_amount = player.rect.right - (SCREEN_WIDTH // 2)
            player.rect.right = SCREEN_WIDTH // 2 
            camera_scroll += scroll_amount
            
            for p in platforms: p.rect.x -= scroll_amount
            for d in decorations: d.rect.x -= scroll_amount
            enemy.rect.x -= scroll_amount
            
            room_x -= scroll_amount
            for smoke in smoke_particles: smoke[0] -= scroll_amount

        ## Enemy chase logic
        if camera_scroll > 1500:
            if not chase_started:
                enemy.rect.x = -200 
                enemy.rect.y = player.rect.y - 150 
                chase_started = True
            
            ## Homing Logic (Enemy follows player smoothly)
            if enemy.rect.centerx < player.rect.centerx:
                enemy.rect.x += 5  
            elif enemy.rect.centerx > player.rect.centerx:
                enemy.rect.x -= 3
    
            if enemy.rect.centery < player.rect.centery:
                enemy.rect.y += 2  
            elif enemy.rect.centery > player.rect.centery:
                enemy.rect.y -= 2  

        if pygame.sprite.spritecollideany(player, enemies_group):
            pygame.mixer.music.stop()
            if jumpscare_sfx: jumpscare_sfx.play()
            try:
                if hasattr(enemy, 'shriek'): enemy.shriek()
            except: pass
            pygame.time.delay(1500) 
            return "CHAPTER1" 

        ## --- Transition to Chapter 2 when player falls ---
        if player.rect.y > SCREEN_HEIGHT + 100:
            print("Player fell! Transitioning to Chapter 2...")
            pygame.mixer.music.stop() 
            
            ## 1. Quit the current Chapter 1 window
            pygame.quit() 
            
            ## 2. Locate and launch teammate's chapter2.py
            chapter2_path = os.path.join(ROOT_DIR, "Scenes", "chapter2.py")
            subprocess.run([sys.executable, chapter2_path])
            
            ## 3. Exit this script completely once Chapter 2 finishes
            sys.exit()

        ## --- 5. RENDERING ---
        screen.fill(BG_FOREST_COLOR) 
        
        ## Draw parallax background
        if bg_surface:
            scroll_offset = (camera_scroll * 0.3) % SCREEN_WIDTH
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
        
        ## 1. Draw wood walls (Decoration Group)
        decorations.draw(screen)

        ## --- TRUE HOLLOW WALLS FOR WINDOWS ---
        wall_color = (130, 95, 65) 
        pygame.draw.rect(screen, wall_color, (room_x + 40, 150, 460, 30))
        pygame.draw.rect(screen, wall_color, (room_x + 40, 470, 460, 30))
        pygame.draw.rect(screen, wall_color, (room_x + 40, 180, 60, 290))
        pygame.draw.rect(screen, wall_color, (room_x + 250, 180, 50, 290))
        pygame.draw.rect(screen, wall_color, (room_x + 450, 180, 50, 290))

        ## 2. Draw transparent glass
        glass_surface = pygame.Surface((150, 290), pygame.SRCALPHA)
        glass_surface.fill((150, 200, 255, 25)) 
        screen.blit(glass_surface, (room_x + 100, 180)) 
        screen.blit(glass_surface, (room_x + 300, 180)) 
        
        ## Window frames
        frame_color = (80, 50, 30) 
        pygame.draw.rect(screen, frame_color, (room_x + 100, 180, 150, 290), 4)
        pygame.draw.rect(screen, frame_color, (room_x + 300, 180, 150, 290), 4)
        pygame.draw.line(screen, frame_color, (room_x + 175, 180), (room_x + 175, 470), 4)
        pygame.draw.line(screen, frame_color, (room_x + 375, 180), (room_x + 375, 470), 4)
        pygame.draw.line(screen, frame_color, (room_x + 100, 325), (room_x + 250, 325), 4)
        pygame.draw.line(screen, frame_color, (room_x + 300, 325), (room_x + 450, 325), 4)

        ## 3. Draw the chimney
        pygame.draw.rect(screen, (70, 30, 30), (room_x + 380, 40, 40, 110))

        ## 4. Draw the triangular roof
        pygame.draw.polygon(screen, (50, 30, 20), [
            (room_x - 50, 150),    
            (room_x + 600, 150),   
            (room_x + 275, 10)     
        ])

        ## 5. Generate and update smoke particles
        if random.random() < 0.15: 
            smoke_particles.append([room_x + 400, 30, 4]) 

        for smoke in smoke_particles[:]:
            smoke[0] += random.uniform(-0.5, 1.5) 
            smoke[1] -= random.uniform(1, 2)      
            smoke[2] += 0.3                       
            
            if smoke[1] < -50 or smoke[2] > 25:
                smoke_particles.remove(smoke)
            else:
                pygame.draw.circle(screen, (120, 120, 120), (int(smoke[0]), int(smoke[1])), int(smoke[2]))

        ## 6. Draw platforms, player, and enemy
        platforms.draw(screen)
        
        ## This only runs if the door hasn't been opened yet!
        if not is_door_opened:
            ## Add a semi-transparent dark shadow to make the door look recessed
            door_shade = pygame.Surface((door.rect.width, door.rect.height), pygame.SRCALPHA)
            door_shade.fill((0, 0, 0, 80)) ## 80 is the transparency (0-255)
            screen.blit(door_shade, (door.rect.x, door.rect.y))
            
            ## Draw a thick, dark wood frame around the door
            pygame.draw.rect(screen, (60, 35, 20), door.rect, 4)
            
            ## Draw a shiny golden doorknob on the left side
            pygame.draw.circle(screen, (220, 180, 50), (door.rect.x + 15, door.rect.y + 80), 6)
            ## Doorknob outline for extra detail
            pygame.draw.circle(screen, (120, 80, 20), (door.rect.x + 15, door.rect.y + 80), 6, 2)

        player.draw(screen)
        enemy.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

## --- Allow chapter1.py to be run as a standalone script ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Good Night, Sleep Tight - Chapter 1")
    run(screen)
    pygame.quit()