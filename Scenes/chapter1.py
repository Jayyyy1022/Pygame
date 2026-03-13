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

class Chapter1:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.isInitialized = False
        

    def setup_level(self):
        """Handles all initialization, asset loading, and variable resetting."""
        self.FPS = 60
        self.SCREEN_WIDTH = self.screen.get_width()
        self.SCREEN_HEIGHT = self.screen.get_height()
        self.GRAVITY = 0.75
        self.MOVEMENT_SPEED = 3

        self.BG_ROOM_COLOR = (40, 40, 40)   
        self.BG_FOREST_COLOR = (10, 15, 30) 
        self.current_bg_color = self.BG_ROOM_COLOR 

        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        ## --- 1. Load Sounds & UI Font ---
        pygame.mixer.init()
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        pygame.font.init()
        
        self.ui_font = pygame.font.SysFont("Arial", 22, bold=True)
        
        try:
            door_path = os.path.join(self.ROOT_DIR, "Assets", "SFX", "door_open.mp3")
            self.door_sfx = pygame.mixer.Sound(door_path) 
            self.door_sfx.set_volume(0.3)
        except:
            self.door_sfx = None

        try:
            jumpscare_path = os.path.join(self.ROOT_DIR, "Assets", "SFX", "jumpscare.wav")
            self.jumpscare_sfx = pygame.mixer.Sound(jumpscare_path)
            self.jumpscare_sfx.set_volume(0.1)
        except:
            self.jumpscare_sfx = None

        try:
            room_bgm_path = os.path.join(self.ROOT_DIR, "Assets", "SFX", "room_bgm.wav")
            pygame.mixer.music.load(room_bgm_path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1) 
        except:
            pass

        ## --- 2. Initialize Entities ---
        self.player = Player.Player_Child(100, 450, 0.1, self.MOVEMENT_SPEED, self.GRAVITY)
        self.enemy = Enemy.Enemy_Krampus(-600, 400, 0.15, self.MOVEMENT_SPEED * 1.1, self.GRAVITY)
        self.enemies_group = pygame.sprite.Group()
        self.enemies_group.add(self.enemy)

        ## --- 3. Build the Level ---
        self.platforms = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        
        wood_floor_img = os.path.join(self.ROOT_DIR, "Assets", "Miscellaneous", "wood_floor.png")
        woods_platform_img = os.path.join(self.ROOT_DIR, "Assets", "Miscellaneous", "woods_platform.png")
        rock_img = os.path.join(self.ROOT_DIR, "Assets", "Miscellaneous", "rock.png")
        snow_floor_img = os.path.join(self.ROOT_DIR, "Assets", "Miscellaneous", "snow_floor.png")
        room_img = os.path.join(self.ROOT_DIR, "Assets", "Miscellaneous", "room.png")
        wood_platform2_img = os.path.join(self.ROOT_DIR, "Assets", "Miscellaneous", "wood_platform2.png")
        wood_platform_img = os.path.join(self.ROOT_DIR, "Assets", "Miscellaneous", "wood_platform.png")
        wood_platform3_img = os.path.join(self.ROOT_DIR, "Assets", "Miscellaneous", "wood_platform3.png")
        
        forest_bg_img = os.path.join(self.ROOT_DIR, "Assets", "Miscellaneous", "forest_bg.png")
        try:
            bg_surface = pygame.image.load(forest_bg_img).convert_alpha()
            self.bg_surface = pygame.transform.scale(bg_surface, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        except:
            self.bg_surface = None

        ## --- Build Room Walls ---
        left_wall = BackgroundDecoration(0, 150, room_img, width=40, height=350)
        right_pillar = BackgroundDecoration(500, 150, room_img, width=60, height=200)
        self.decorations.add(left_wall, right_pillar)

        ## --- Physical Foundations ---
        self.platforms.add(Platform(0, 500, 500, 100, color=(45, 25, 15))) 
        self.platforms.add(Platform(0, 500, 500, 30, image_path=wood_floor_img)) 

        self.door = Platform(500, 350, 60, 150, image_path=room_img)
        self.platforms.add(self.door)
        
        self.is_door_opened = False
        self.is_door_transitioning = False
        self.door_fade_state = "none"
        self.door_fade_alpha = 0
        
        self.platforms.add(Platform(500, 520, 4000, 80, color=(30, 30, 40))) 
        self.platforms.add(Platform(500, 500, 4000, 30, image_path=snow_floor_img)) 
        self.platforms.add(Platform(1000, 430, 120, 70, image_path=woods_platform_img))
        self.platforms.add(Platform(1500, 450, 150, 50, image_path=rock_img))
        self.platforms.add(Platform(1900, 450, 150, 50, image_path=rock_img)) 
        self.platforms.add(Platform(2000, 400, 120, 70, image_path=wood_platform2_img))
        self.platforms.add(Platform(2200, 350, 120, 70, image_path=wood_platform_img)) 
        self.platforms.add(Platform(2700, 450, 150, 50, image_path=rock_img))
        self.platforms.add(Platform(2750, 400, 150, 50, image_path=wood_floor_img))
        self.platforms.add(Platform(2800, 350, 150, 50, image_path=wood_platform3_img))
        self.platforms.add(Platform(3300, 430, 120, 70, image_path=wood_platform_img))
        self.platforms.add(Platform(3480, 430, 120, 70, image_path=woods_platform_img))
        
        ## --- Particle Systems & Trackers ---
        self.camera_scroll = 0
        self.chase_started = False
        
        self.snowflakes = []
        for i in range(300):
            self.snowflakes.append([random.randrange(0, self.SCREEN_WIDTH), random.randrange(0, self.SCREEN_HEIGHT), random.randrange(3, 7), random.randrange(1, 4)])

        self.room_x = 0  
        self.smoke_particles = [] 

        ## --- Cinematic Triggers & Timers ---
        self.fade_alpha = 255                
        self.intro_state = 1                 
        self.intro_timer = 200               
        self.chase_text_timer = 200          

    def draw_floating_text(self, text_string):
        """Helper method to draw text above the player."""
        text_surf = self.ui_font.render(text_string, True, (255, 255, 255))
        shadow_surf = self.ui_font.render(text_string, True, (0, 0, 0)) 
        x = self.player.rect.centerx - text_surf.get_width() // 2
        y = self.player.rect.top - 35
        self.screen.blit(shadow_surf, (x + 2, y + 2)) 
        self.screen.blit(text_surf, (x, y))

    def run(self, events):
        """Main update loop called every frame by game.py"""
        if not self.isInitialized:
            self.setup_level() # This includes loading assets and starting music
            self.isInitialized = True

        # Quit logic is handled by game.py now, but we loop through events to clear the queue
        for event in events:
            pass 

        keys = pygame.key.get_pressed()
        
        ## --- Door Interaction Trigger ---
        if not self.is_door_opened and not self.is_door_transitioning:
            interaction_area = self.player.rect.inflate(40, 0) 
            if interaction_area.colliderect(self.door.rect):
                self.is_door_transitioning = True
                self.door_fade_state = "fading_out"
                self.door_fade_alpha = 0
                pygame.mixer.music.stop()
                if self.door_sfx:
                    self.door_sfx.play()

        ## --- Door Transition State Machine ---
        if self.is_door_transitioning:
            if self.door_fade_state == "fading_out":
                self.door_fade_alpha += 4  
                if self.door_fade_alpha >= 255:
                    self.door_fade_alpha = 255
                    self.door_fade_state = "snapping"
            
            elif self.door_fade_state == "snapping":
                self.is_door_opened = True
                self.current_bg_color = self.BG_FOREST_COLOR 

                snap_amount = 250
                for p in self.platforms: p.rect.x -= snap_amount
                for d in self.decorations: d.rect.x -= snap_amount
                self.enemy.rect.x -= snap_amount
                self.camera_scroll += snap_amount
                
                self.room_x -= snap_amount 
                for smoke in self.smoke_particles: smoke[0] -= snap_amount
                
                self.player.rect.x = 330
                self.door_fade_state = "fading_in"
            
            elif self.door_fade_state == "fading_in":
                self.door_fade_alpha -= 4 
                if self.door_fade_alpha <= 0:
                    self.door_fade_alpha = 0
                    self.door_fade_state = "done"
                    self.is_door_transitioning = False

        ## Update player physics
        self.player.move(self.platforms)

        ## --- Invisible Barriers ---
        if self.player.rect.left < 0:
            self.player.rect.left = 0
            
        if self.is_door_opened:
            if self.player.rect.left < self.room_x + 480:
                self.player.rect.left = self.room_x + 480

        ## --- Camera following logic ---
        if self.player.rect.right > self.SCREEN_WIDTH // 2:
            scroll_amount = self.player.rect.right - (self.SCREEN_WIDTH // 2)
            self.player.rect.right = self.SCREEN_WIDTH // 2 
            self.camera_scroll += scroll_amount
            
            for p in self.platforms: p.rect.x -= scroll_amount
            for d in self.decorations: d.rect.x -= scroll_amount
            self.enemy.rect.x -= scroll_amount
            
            self.room_x -= scroll_amount
            for smoke in self.smoke_particles: smoke[0] -= scroll_amount

        ## --- Enemy chase logic ---
        if self.camera_scroll > 1500:
            if not self.chase_started:
                self.enemy.rect.x = -200 
                self.enemy.rect.y = self.player.rect.y - 150 
                self.chase_started = True
            
            if self.enemy.rect.centerx < self.player.rect.centerx:
                self.enemy.rect.x += 6  
            elif self.enemy.rect.centerx > self.player.rect.centerx:
                self.enemy.rect.x -= 3
    
            if self.enemy.rect.centery < self.player.rect.centery:
                self.enemy.rect.y += 2  
            elif self.enemy.rect.centery > self.player.rect.centery:
                self.enemy.rect.y -= 2  

        if pygame.sprite.spritecollideany(self.player, self.enemies_group):
            pygame.mixer.music.stop()
            if self.jumpscare_sfx: self.jumpscare_sfx.play()
            try:
                if hasattr(self.enemy, 'shriek'): self.enemy.shriek()
            except: pass
            pygame.time.delay(1500) 
            
            ## RESTART LOGIC: Just call setup_level() to instantly reset everything!
            self.setup_level()
            return  ## Stop processing this frame immediately

        ## --- Transition to Chapter 2 when player falls ---
        if self.player.rect.y > self.SCREEN_HEIGHT + 100:
            # pygame.mixer.music.fadeout(500)
            self.door_sfx.fadeout(500)
            self.isInitialized = False
            self.gameStateManager.set_state("chapter2")
            return

        ## --- 5. RENDERING ---
        self.screen.fill(self.current_bg_color) 
        
        if self.bg_surface:
            scroll_offset = (self.camera_scroll * 0.3) % self.SCREEN_WIDTH
            self.screen.blit(self.bg_surface, (-scroll_offset, 0))
            self.screen.blit(self.bg_surface, (-scroll_offset + self.SCREEN_WIDTH, 0))
                
        for flake in self.snowflakes:
            flake[1] += flake[2] 
            flake[0] += random.choice([-2, -1, 0, 1, 2]) 
            if flake[1] > self.SCREEN_HEIGHT:
                flake[1] = random.randrange(-50, -10)
                flake[0] = random.randrange(0, self.SCREEN_WIDTH)
            pygame.draw.circle(self.screen, (255, 255, 255), (flake[0], flake[1]), flake[3])
        
        self.decorations.draw(self.screen)

        wall_color = (130, 95, 65) 
        pygame.draw.rect(self.screen, wall_color, (self.room_x + 40, 150, 460, 30))
        pygame.draw.rect(self.screen, wall_color, (self.room_x + 40, 470, 460, 30))
        pygame.draw.rect(self.screen, wall_color, (self.room_x + 40, 180, 60, 290))
        pygame.draw.rect(self.screen, wall_color, (self.room_x + 250, 180, 50, 290))
        pygame.draw.rect(self.screen, wall_color, (self.room_x + 450, 180, 50, 290))

        glass_surface = pygame.Surface((150, 290), pygame.SRCALPHA)
        glass_surface.fill((150, 200, 255, 25)) 
        self.screen.blit(glass_surface, (self.room_x + 100, 180)) 
        self.screen.blit(glass_surface, (self.room_x + 300, 180)) 
        
        frame_color = (80, 50, 30) 
        pygame.draw.rect(self.screen, frame_color, (self.room_x + 100, 180, 150, 290), 4)
        pygame.draw.rect(self.screen, frame_color, (self.room_x + 300, 180, 150, 290), 4)
        pygame.draw.line(self.screen, frame_color, (self.room_x + 175, 180), (self.room_x + 175, 470), 4)
        pygame.draw.line(self.screen, frame_color, (self.room_x + 375, 180), (self.room_x + 375, 470), 4)
        pygame.draw.line(self.screen, frame_color, (self.room_x + 100, 325), (self.room_x + 250, 325), 4)
        pygame.draw.line(self.screen, frame_color, (self.room_x + 300, 325), (self.room_x + 450, 325), 4)

        pygame.draw.rect(self.screen, (70, 30, 30), (self.room_x + 380, 40, 40, 110))

        pygame.draw.polygon(self.screen, (50, 30, 20), [
            (self.room_x - 50, 150),    
            (self.room_x + 600, 150),   
            (self.room_x + 275, 10)     
        ])

        if random.random() < 0.15: 
            self.smoke_particles.append([self.room_x + 400, 30, 4]) 

        for smoke in self.smoke_particles[:]:
            smoke[0] += random.uniform(-0.5, 1.5) 
            smoke[1] -= random.uniform(1, 2)      
            smoke[2] += 0.3                       
            
            if smoke[1] < -50 or smoke[2] > 25:
                self.smoke_particles.remove(smoke)
            else:
                pygame.draw.circle(self.screen, (120, 120, 120), (int(smoke[0]), int(smoke[1])), int(smoke[2]))

        self.platforms.draw(self.screen)
        
        door_shade = pygame.Surface((self.door.rect.width, self.door.rect.height), pygame.SRCALPHA)
        door_shade.fill((0, 0, 0, 80)) 
        self.screen.blit(door_shade, (self.door.rect.x, self.door.rect.y))
        pygame.draw.rect(self.screen, (60, 35, 20), self.door.rect, 4)
        pygame.draw.circle(self.screen, (220, 180, 50), (self.door.rect.x + 15, self.door.rect.y + 80), 6)
        pygame.draw.circle(self.screen, (120, 80, 20), (self.door.rect.x + 15, self.door.rect.y + 80), 6, 2)

        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        ## --- OVERLAY EFFECTS & UI TEXT ---
        darkness_filter = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        darkness_filter.fill((0, 5, 15, 110)) 
        self.screen.blit(darkness_filter, (0, 0))

        if self.fade_alpha > 0:
            self.fade_alpha -= 2   
            fade_surf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surf, (0, 0))
        else:
            if self.intro_state == 1:
                self.draw_floating_text("Is it a dream...?")
                self.intro_timer -= 1
                if self.intro_timer <= 0:
                    self.intro_state = 2     
                    self.intro_timer = 180   
            elif self.intro_state == 2:
                self.draw_floating_text("Press A / D to Move")
                self.intro_timer -= 1
                if self.intro_timer <= 0:
                    self.intro_state = 3     
                    self.intro_timer = 180   
            elif self.intro_state == 3:
                self.draw_floating_text("Press SPACE to Jump")
                self.intro_timer -= 1
                if self.intro_timer <= 0:
                    self.intro_state = 0     

        if self.chase_started and self.chase_text_timer > 0:
            self.draw_floating_text("Hold LEFT SHIFT to RUN!")
            self.chase_text_timer -= 1
            
        if self.camera_scroll > 2800 and self.player.rect.y < 600:
            self.draw_floating_text("No way out... I must jump!")

        if self.is_door_transitioning:
            door_fade_surf = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            door_fade_surf.fill((0, 0, 0))
            door_fade_surf.set_alpha(self.door_fade_alpha)
            self.screen.blit(door_fade_surf, (0, 0))

## --- Allow chapter1.py to be run as a standalone script ---
# if __name__ == "__main__":
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     pygame.display.set_caption("Good Night, Sleep Tight - Chapter 1")
#     run(screen)
#     pygame.quit()