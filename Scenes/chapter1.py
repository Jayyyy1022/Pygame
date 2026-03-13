import pygame
import os
import sys
import subprocess
import random

## --- Tell Python to look in the parent directory for the Entities module ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Entities.Player import player_child as Player
from Entities.Enemy import enemy_krampus as Enemy
from Entities.Obstacle.platform import Platform
from Entities.Decoration.prop import BackgroundDecoration

def run(screen):
    ## --- FOOLPROOF RESTART LOOP ---
    ## This loop ensures the chapter restarts internally without relying on menu.py or main.py
    while True:
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

        ## --- 1. Load Sounds & UI Font ---
        pygame.mixer.init()
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        pygame.font.init()
        
        ## Load a bold font for floating text
        ui_font = pygame.font.SysFont("Arial", 22, bold=True)
        
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
            pass

        ## --- 2. Initialize Entities ---
        player = Player.Player_Child(100, 450, 0.1, MOVEMENT_SPEED, GRAVITY)
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

        ## --- Build Room Walls ---
        left_wall = BackgroundDecoration(0, 150, room_img, width=40, height=350)
        right_pillar = BackgroundDecoration(500, 150, room_img, width=60, height=200)
        decorations.add(left_wall, right_pillar)

        ## --- Physical Foundations ---
        platforms.add(Platform(0, 500, 500, 100, color=(45, 25, 15))) 
        platforms.add(Platform(0, 500, 500, 30, image_path=wood_floor_img)) 

        door = Platform(500, 350, 60, 150, image_path=room_img)
        platforms.add(door)
        
        is_door_opened = False
        
        ## --- Transition Variables for Door Exiting ---
        is_door_transitioning = False
        door_fade_state = "none"   ## States: "none" -> "fading_out" -> "snapping" -> "fading_in" -> "done"
        door_fade_alpha = 0
        
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
        ## Heavy blizzard effect
        for i in range(300):
            snowflakes.append([random.randrange(0, SCREEN_WIDTH), random.randrange(0, SCREEN_HEIGHT), random.randrange(3, 7), random.randrange(1, 4)])

        room_x = 0  
        smoke_particles = [] 

        ## --- Cinematic Triggers & Timers ---
        fade_alpha = 255                
        intro_state = 1                 ## 1="Dream?", 2="Move", 3="Jump", 0=Done
        intro_timer = 200               
        chase_text_timer = 200          
        
        def draw_floating_text(text_string):
            text_surf = ui_font.render(text_string, True, (255, 255, 255))
            shadow_surf = ui_font.render(text_string, True, (0, 0, 0)) 
            x = player.rect.centerx - text_surf.get_width() // 2
            y = player.rect.top - 35
            screen.blit(shadow_surf, (x + 2, y + 2)) 
            screen.blit(text_surf, (x, y))           

        chapter_action = None ## Stores whether to restart or quit

        ## --- 4. MAIN GAME LOOP ---
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    chapter_action = "QUIT"
                    running = False
                    
            if not running:
                break

            keys = pygame.key.get_pressed()
            
            ## --- Door Interaction Trigger ---
            if not is_door_opened and not is_door_transitioning:
                interaction_area = player.rect.inflate(40, 0) 
                if interaction_area.colliderect(door.rect):
                    ## Start the fade-to-black sequence
                    is_door_transitioning = True
                    door_fade_state = "fading_out"
                    door_fade_alpha = 0
                    pygame.mixer.music.stop()
                    if door_sfx:
                        door_sfx.play()

            ## --- Door Transition State Machine ---
            if is_door_transitioning:
                if door_fade_state == "fading_out":
                    door_fade_alpha += 4  ## Speed of fading out
                    if door_fade_alpha >= 255:
                        door_fade_alpha = 255
                        door_fade_state = "snapping"
                
                elif door_fade_state == "snapping":
                    is_door_opened = True
                    current_bg_color = BG_FOREST_COLOR 

                    ## Move level 250 pixels to keep the house edge visible
                    snap_amount = 250
                    for p in platforms: p.rect.x -= snap_amount
                    for d in decorations: d.rect.x -= snap_amount
                    enemy.rect.x -= snap_amount
                    camera_scroll += snap_amount
                    
                    room_x -= snap_amount 
                    for smoke in smoke_particles: smoke[0] -= snap_amount
                    
                    ## Place the player safely outside the door
                    player.rect.x = 330
                    
                    ## Begin fade in
                    door_fade_state = "fading_in"
                
                elif door_fade_state == "fading_in":
                    door_fade_alpha -= 4  ## Speed of fading in
                    if door_fade_alpha <= 0:
                        door_fade_alpha = 0
                        door_fade_state = "done"
                        is_door_transitioning = False

            ## Update player physics
            player.move(platforms)

            ## --- Invisible Barriers ---
            ## 1. Strictly prevent the player from ever moving past the left edge of the screen
            if player.rect.left < 0:
                player.rect.left = 0
                
            ## 2. Prevent walking back into the void after exiting the house
            if is_door_opened:
                if player.rect.left < room_x + 480:
                    player.rect.left = room_x + 480

            ## --- Camera following logic ---
            if player.rect.right > SCREEN_WIDTH // 2:
                scroll_amount = player.rect.right - (SCREEN_WIDTH // 2)
                player.rect.right = SCREEN_WIDTH // 2 
                camera_scroll += scroll_amount
                
                for p in platforms: p.rect.x -= scroll_amount
                for d in decorations: d.rect.x -= scroll_amount
                enemy.rect.x -= scroll_amount
                
                room_x -= scroll_amount
                for smoke in smoke_particles: smoke[0] -= scroll_amount

            ## --- Enemy chase logic ---
            if camera_scroll > 1500:
                if not chase_started:
                    enemy.rect.x = -200 
                    enemy.rect.y = player.rect.y - 150 
                    chase_started = True
                
                ## Homing Logic: Enemy tracks player coordinates smoothly
                if enemy.rect.centerx < player.rect.centerx:
                    enemy.rect.x += 6  
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
                
                ## Trigger internal restart immediately
                chapter_action = "RESTART"
                running = False  ## Break the inner game loop

            ## --- Transition to Chapter 2 when player falls ---
            if player.rect.y > SCREEN_HEIGHT + 100:
                pygame.mixer.music.stop() 
                pygame.quit() 
                chapter2_path = os.path.join(ROOT_DIR, "Scenes", "chapter2.py")
                subprocess.run([sys.executable, chapter2_path])
                sys.exit()

            ## --- 5. RENDERING ---
            screen.fill(BG_FOREST_COLOR) 
            
            if bg_surface:
                scroll_offset = (camera_scroll * 0.3) % SCREEN_WIDTH
                screen.blit(bg_surface, (-scroll_offset, 0))
                screen.blit(bg_surface, (-scroll_offset + SCREEN_WIDTH, 0))
                    
            ## Render heavy blizzard effect
            for flake in snowflakes:
                flake[1] += flake[2] 
                flake[0] += random.choice([-2, -1, 0, 1, 2]) 
                if flake[1] > SCREEN_HEIGHT:
                    flake[1] = random.randrange(-50, -10)
                    flake[0] = random.randrange(0, SCREEN_WIDTH)
                pygame.draw.circle(screen, (255, 255, 255), (flake[0], flake[1]), flake[3])
            
            decorations.draw(screen)

            ## Draw detailed interior walls
            wall_color = (130, 95, 65) 
            pygame.draw.rect(screen, wall_color, (room_x + 40, 150, 460, 30))
            pygame.draw.rect(screen, wall_color, (room_x + 40, 470, 460, 30))
            pygame.draw.rect(screen, wall_color, (room_x + 40, 180, 60, 290))
            pygame.draw.rect(screen, wall_color, (room_x + 250, 180, 50, 290))
            pygame.draw.rect(screen, wall_color, (room_x + 450, 180, 50, 290))

            ## Draw transparent glass panes
            glass_surface = pygame.Surface((150, 290), pygame.SRCALPHA)
            glass_surface.fill((150, 200, 255, 25)) 
            screen.blit(glass_surface, (room_x + 100, 180)) 
            screen.blit(glass_surface, (room_x + 300, 180)) 
            
            ## Draw window frames
            frame_color = (80, 50, 30) 
            pygame.draw.rect(screen, frame_color, (room_x + 100, 180, 150, 290), 4)
            pygame.draw.rect(screen, frame_color, (room_x + 300, 180, 150, 290), 4)
            pygame.draw.line(screen, frame_color, (room_x + 175, 180), (room_x + 175, 470), 4)
            pygame.draw.line(screen, frame_color, (room_x + 375, 180), (room_x + 375, 470), 4)
            pygame.draw.line(screen, frame_color, (room_x + 100, 325), (room_x + 250, 325), 4)
            pygame.draw.line(screen, frame_color, (room_x + 300, 325), (room_x + 450, 325), 4)

            pygame.draw.rect(screen, (70, 30, 30), (room_x + 380, 40, 40, 110))

            pygame.draw.polygon(screen, (50, 30, 20), [
                (room_x - 50, 150),    
                (room_x + 600, 150),   
                (room_x + 275, 10)     
            ])

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

            platforms.draw(screen)
            
            ## Always render the door details so it looks solid and consistent
            door_shade = pygame.Surface((door.rect.width, door.rect.height), pygame.SRCALPHA)
            door_shade.fill((0, 0, 0, 80)) 
            screen.blit(door_shade, (door.rect.x, door.rect.y))
            pygame.draw.rect(screen, (60, 35, 20), door.rect, 4)
            pygame.draw.circle(screen, (220, 180, 50), (door.rect.x + 15, door.rect.y + 80), 6)
            pygame.draw.circle(screen, (120, 80, 20), (door.rect.x + 15, door.rect.y + 80), 6, 2)

            player.draw(screen)
            enemy.draw(screen)

            ## --- OVERLAY EFFECTS & UI TEXT ---
            
            ## Apply Universal Darkness Filter
            darkness_filter = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            darkness_filter.fill((0, 5, 15, 110)) 
            screen.blit(darkness_filter, (0, 0))

            ## 1. Initial Scene Fade-In
            if fade_alpha > 0:
                fade_alpha -= 2   
                fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surf.fill((0, 0, 0))
                fade_surf.set_alpha(fade_alpha)
                screen.blit(fade_surf, (0, 0))
            else:
                ## UI Sequence
                if intro_state == 1:
                    draw_floating_text("Is it a dream...?")
                    intro_timer -= 1
                    if intro_timer <= 0:
                        intro_state = 2     
                        intro_timer = 180   
                elif intro_state == 2:
                    draw_floating_text("Press A / D to Move")
                    intro_timer -= 1
                    if intro_timer <= 0:
                        intro_state = 3     
                        intro_timer = 180   
                elif intro_state == 3:
                    draw_floating_text("Press SPACE to Jump")
                    intro_timer -= 1
                    if intro_timer <= 0:
                        intro_state = 0     

            ## Chase Text Overlay
            if chase_started and chase_text_timer > 0:
                draw_floating_text("Hold LEFT SHIFT to RUN!")
                chase_text_timer -= 1
                
            ## Cliff Text Overlay
            if camera_scroll > 2800 and player.rect.y < 600:
                draw_floating_text("No way out... I must jump!")

            ## 2. Door Scene Transition Fade (Rendered at the very top)
            if is_door_transitioning:
                door_fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                door_fade_surf.fill((0, 0, 0))
                door_fade_surf.set_alpha(door_fade_alpha)
                screen.blit(door_fade_surf, (0, 0))

            pygame.display.flip()
            clock.tick(FPS)
            
        ## --- Handle post-loop actions (Restart or Quit) ---
        if chapter_action == "RESTART":
            continue  ## Loops back to the start of the `while True:` block and re-initializes everything perfectly!
        elif chapter_action == "QUIT":
            return "QUIT" ## Exits the chapter completely
        else:
            break

## --- Allow chapter1.py to be run as a standalone script ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Good Night, Sleep Tight - Chapter 1")
    run(screen)
    pygame.quit()