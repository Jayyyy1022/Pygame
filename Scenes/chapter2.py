import pygame
import sys
import os
import random

# Maintain path appending to find Entities/Scenes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Entities.Player.player_child import Player_Child as Player
from Entities.Enemy.enemy_krampus import Enemy_Krampus as Krampus
from Entities.Obstacle.platform import Platform
from Entities.Obstacle.falling_rock import FallingRock

class Chapter2:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.gameStateManager = game_state_manager
        self.WIDTH, self.HEIGHT = 800, 600
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.PLAYER_SCALE = 0.172
        
        # ---------------- SETTINGS & STATE ----------------
        self.dim_speed = 2
        self.isInitialized = False
        self.current_scene = "scene1"
        self.current_bgm = None
        self.ghost_playing = False

        # ---------------- PERSISTENT DIALOGUE FLAGS ----------------
        self.landing_dialogue_shown = False
        self.scene2_entry_dialogue_shown = False
        self.scene2_key_dialogue_shown = False
        self.scene3_entry_dialogue_shown = False
        self.scene4_entry_dialogue_shown = False

    def load_assets(self):
        """Mimics the ASSETS section of the original file."""
        self.ice_cave_bg = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Ice_cave_1.png")).convert()
        self.ice_cave_bg = pygame.transform.scale(self.ice_cave_bg, (self.WIDTH, self.HEIGHT))
        self.ice_cave_bg2 = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Ice_cave_2.png")).convert_alpha()
        self.ice_cave_bg2 = pygame.transform.scale(self.ice_cave_bg2, (self.WIDTH, self.HEIGHT))
        self.ice_cave_bg3 = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Ice_cave_exit.png")).convert_alpha()
        self.ice_cave_bg3 = pygame.transform.scale(self.ice_cave_bg3, (self.WIDTH, self.HEIGHT))
        
        self.sign = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Wooden_Sign.png")).convert_alpha()
        self.sign = pygame.transform.scale(self.sign, (40, 60))
        self.cave_platform = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Cave_platforms_1.png")).convert_alpha()
        self.key_image = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Key.png")).convert_alpha()
        self.key_image = pygame.transform.scale(self.key_image, (30, 30))
        self.door_image = pygame.image.load(os.path.join("Assets", "Miscellaneous", "Cave_door.png")).convert_alpha()
        self.door_image = pygame.transform.scale(self.door_image, (50, 80))
        self.rock_path = os.path.join("Assets", "Miscellaneous", "rock.png")

        # SFX
        self.fall_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Fall_down.mp3"))
        self.ghost_whisper = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Ghost_whisper.mp3"))
        self.door_appear_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Door_appear.mp3"))
        self.jumpscare_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "jumpscare.wav"))
        self.krampus_spawn_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "E_spawn.mp3"))
        self.exit_scream = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Exit_scream.mp3"))
        self.collision_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Collision.mp3"))
        self.collision_sound.set_volume(0.6)
        self.rumble_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Rumble.mp3"))
        self.rumble2_sound = pygame.mixer.Sound(os.path.join("Assets", "SFX", "Rumble_2.mp3"))

        self.bgm_1_2_path = os.path.join("Assets", "SFX", "Scene_1n2bgm.mp3")
        self.bgm_3_4_path = os.path.join("Assets", "SFX", "Scene_3n4bgm.mp3")

    def setup_scene(self, scene_name):
        # --- Initializse variables for each scene ---
        self.current_scene = scene_name
        self.dialogue_timer = 0     # to time the second line
        self.dialogue_stage = 0     # 0 = no dialogue, 1 = first line, 2 = second line

        if scene_name == "scene1":
            self.play_bgm("scene1")
            if not hasattr(self, "light_radius"):
                self.light_radius = 200
            self.player = Player(120, -50, self.PLAYER_SCALE, 4, 0.5)
            self.platforms = [Platform(0, 500, self.WIDTH, 100)]
            self.sign_rect = pygame.Rect(380, 440, 40, 60)
            self.show_sign_dialogue = False
            self.sign_dialogue_timer = 0
            self.player_landed = False 
            self.prev_on_ground = False 

        elif scene_name == "scene2":
            self.play_bgm("scene2")
            self.player = Player(10, 430, self.PLAYER_SCALE, 4, 0.5)
            self.platforms = [
                Platform(0, 500, 150, 50),      # starting platform(bottom left)
                Platform(650, 250, 150, 50),    # top right
                Platform(200, 380, 150, 50),    # middle left
                Platform(50, 150, 150, 50),     # top left (key here)
                Platform(350, 150, 150, 50),    # top middle
                Platform(450, 380, 150, 50),    # middle
                Platform(650, 500, 150, 50)     # Exit (bottom right)
            ]
            self.key_rect = pygame.Rect(80, 110, 30, 30)
            self.key_collected = False
            self.door_rect = pygame.Rect(700, 440, 50, 80)
            self.door_visible = False

        elif scene_name == "scene3":
            self.player = Player(10, 450, self.PLAYER_SCALE, 4, 0.5)
            self.krampus = Krampus(self.player.rect.x, -50, 0.2, 2, 0.5)
            self.monster_speed = 465
            self.platforms = [
                Platform(0, 500, 400, 100), 
                Platform(400, 500, 400, 100),
                Platform(800, 500, 400, 100), 
                Platform(1200, 500, 400, 100),
                Platform(1600, 500, 400, 100),   # New mid-level platform
                Platform(2000, 500, 400, 100)
            ]
            self.spawn_timer = 0
            self.krampus_active = False
            self.krampus_on_ground = False
            self.shake_timer = 0.8
            self.shake_strength = 8
            self.first_shake_done = False
            self.krampus_shake_done = False
            
            # --- Ceiling Pillars & Falling Rocks ---
            self.pillars = []
            configs = [(400, 0, 2), (850, 0, 1), (1200, 0, 3), (1600, 0, 2)]
            for plat_x, plat_y, num in configs:
                for i in range(num):
                    p = Platform(plat_x + i * 120, plat_y, 40, 350)
                    if os.path.exists(self.rock_path):
                        img = pygame.image.load(self.rock_path).convert_alpha()
                        p.image = pygame.transform.flip(pygame.transform.scale(img, (40, 350)), False, True)
                    self.pillars.append(p)
            self.falling_rocks = []
            for stack_x in [700, 1000, 1900, 2200]:
                for i in range(2):
                    self.falling_rocks.append(FallingRock(stack_x, -50 - (i*60), 50, 50, self.rock_path))

        elif scene_name == "scene4":
            self.play_bgm("scene4")
            self.player = Player(10, 430, self.PLAYER_SCALE, 2, 0.5)
            self.platforms = [Platform(0, 500, self.WIDTH, 100)]
            self.krampus = Krampus(0, 430, 0.2, 2, 0.5)
            self.krampus_active = False         # spawn after delay 
            self.krampus_timer = 0              # timer to track delay
            self.krampus_speed = 280            # pixels per second
            self.krampus_spawn_delay = 1             # 1 second delay

    def play_bgm(self, scene_name, volume=0.5):
        """Mimics play_bgm function. Only switches if needed."""
        bgm_to_play = self.bgm_1_2_path if scene_name in ["scene1", "scene2"] else self.bgm_3_4_path
        if self.current_bgm != bgm_to_play:
            pygame.mixer.music.load(bgm_to_play)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            self.current_bgm = bgm_to_play

    def game_over(self):
        """Mimics the original GAME OVER function exactly (including blocking delays)."""
        self.ghost_whisper.stop()
        self.ghost_playing = False
        self.ghost_whisper.set_volume(0)
        pygame.mixer.music.stop()
        self.current_bgm = None # Force BGM reload on respawn

        self.display.fill((0, 0, 0))
        pygame.display.update()
        pygame.time.delay(800)
        self.jumpscare_sound.play()

        # White flash
        flash = pygame.Surface((self.WIDTH, self.HEIGHT))
        flash.fill((255, 255, 255))
        self.display.blit(flash, (0, 0))
        pygame.display.update()
        pygame.time.delay(200)

        # Black screen and text (Mimicking original red text logic)
        self.display.fill((0, 0, 0))
        pygame.display.update()
        pygame.time.delay(1200)
        text = self.font.render("You were caught by Krampus...", True, (255, 0, 0))
        self.display.blit(text, (self.WIDTH // 2 - 160, self.HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)

        self.light_radius = 200
        self.setup_scene("scene1")

    def draw_player_with_light(self, player):
        """Mimics LIGHT SYSTEM logic."""
        player.draw(self.display)
        darkness = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        center = player.rect.center
        
        ratio = max(0, min(1, (self.light_radius - 20) / 180))
        alpha = 220 - (ratio * 120)
        darkness.fill((0, 0, 0, int(alpha)))
        
        flicker = random.randint(-5, 5)
        rad = max(10, self.light_radius + flicker)
        if self.light_radius < 40 and pygame.time.get_ticks() % 500 < 40: rad = 5
        
        pygame.draw.circle(darkness, (0, 0, 0, 0), center, int(rad))
        self.display.blit(darkness, (0, 0))

        if self.light_radius <= 150:
            if not self.ghost_playing:
                self.ghost_whisper.play(loops=-1)
                self.ghost_playing = True
            vol = max(0, min(1, (150 - self.light_radius) / 140))
            self.ghost_whisper.set_volume(vol)

    def draw_krampus_danger(self, player, krampus):
        dist = abs(player.rect.centerx - krampus.rect.centerx)
        if dist < 200:
            intensity = int((1 - dist / 200) * 120)
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, intensity))
            self.display.blit(overlay, (0, 0))

    def run(self, events):
        """Entry point from game.py."""
        if not self.isInitialized:
            self.load_assets()
            self.setup_scene("scene1")
            self.isInitialized = True

        dt = self.clock.tick(60) / 1000

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j and self.current_scene == "scene1":
                    if self.player.rect.colliderect(self.sign_rect):
                        self.show_sign_dialogue = True
                        self.sign_dialogue_timer = 0

        # Execute scene-specific logic
        if self.current_scene == "scene1": self.update_scene1(dt)
        elif self.current_scene == "scene2": self.update_scene2(dt)
        elif self.current_scene == "scene3": self.update_scene3(dt)
        elif self.current_scene == "scene4": self.update_scene4(dt)

        # Torch Dimming
        if self.player_landed:
            if self.light_radius > 0:
                self.light_radius -= self.dim_speed * dt
            else:
                self.game_over()
        self.draw_ui_esc(events)
        self.player.update_animation()

    def update_scene1(self, dt):
        self.player.move(self.platforms)
        
        # --- Check if player landed ---
        on_ground = any(self.player.rect.bottom == p.rect.top for p in self.platforms)
        
        # Play landing SFX every time player lands, but show dialogue only once
        if on_ground and not self.player_landed and not self.prev_on_ground:
            self.fall_sound.play()
            self.player_landed = True
            if not self.landing_dialogue_shown:
                self.dialogue_stage = 1
                self.landing_dialogue_shown = True      # lock dialogue permanently
        self.prev_on_ground = on_ground

        # --- Draw background and platforms ---
        self.display.blit(self.ice_cave_bg, (0, 0))
        for p in self.platforms: 
            self.display.blit(p.image, p.rect)
        self.display.blit(self.sign, self.sign_rect)

        # --- Scene 1 light cone ---
        cone_surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surface, (255, 255, 200, 120), [(80, 0), (160, 0), (250, self.HEIGHT), (0, self.HEIGHT)])
        self.display.blit(cone_surface, (0, 0))

        # --- Dialogue handling ---
        if self.dialogue_stage > 0:
            self.dialogue_timer += dt
            txt = "Ouff! Where am I...." if self.dialogue_stage == 1 else "I need to get out of here!"
            self.draw_dialogue(txt)
            if self.dialogue_stage == 1 and self.dialogue_timer >= 1.5:
                self.dialogue_stage = 2
                self.dialogue_timer = 0
            elif self.dialogue_stage == 2 and self.dialogue_timer >= 2:
                self.dialogue_stage = 0

        # --- Sign interaction ---
        if self.player.rect.colliderect(self.sign_rect): self.draw_dialogue("Press J", offset=35)
        if self.show_sign_dialogue:
            self.sign_dialogue_timer += dt
            self.draw_dialogue("Escape before the light fades. What does that mean...")
            if self.sign_dialogue_timer >= 2: self.show_sign_dialogue = False
        
        # torch
        self.draw_player_with_light(self.player)
        if self.player.rect.right >= self.WIDTH: self.setup_scene("scene2")


    # ---------------- SCENE 2 PLATFORM LEVEL ----------------
    def update_scene2(self, dt):
        self.player.move(self.platforms)
        
        ## --- Check key collection ---
        if not self.key_collected and self.player.rect.colliderect(self.key_rect):
            self.key_collected = True
            self.door_visible = True
            self.door_appear_sound.play()

            # Trigger key-collected dialogue once
            if not self.scene2_key_dialogue_shown:
                self.dialogue_stage = 1
                self.dialogue_timer = 0 # Timer reset for dialogue logic
                self.scene2_key_dialogue_shown = True

        # --- Check fall off screen ---
        if self.player.rect.top >= self.HEIGHT:
            self.setup_scene("scene1")
            return

        # --- Draw background ---
        self.display.blit(self.ice_cave_bg2, (0, 0))

        # --- Draw platforms ---
        for p in self.platforms:
            p.image = pygame.transform.scale(self.cave_platform, (p.rect.width, p.rect.height))
            self.display.blit(p.image, p.rect)

        # --- Draw key ---
        if not self.key_collected: self.display.blit(self.key_image, self.key_rect.topleft)

        # --- Draw exit door ---
        if self.door_visible: self.display.blit(self.door_image, self.door_rect.topleft)

        # Dialogue
        if not self.scene2_entry_dialogue_shown:
            self.draw_dialogue("Is that a key on the top platform?")
            self.dialogue_timer += dt
            if self.dialogue_timer > 2: 
                self.scene2_entry_dialogue_shown = True
                self.dialogue_timer = 0
        elif self.dialogue_stage == 1:
            self.draw_dialogue("A door appeared out of nowhere...")
            self.dialogue_timer += dt
            if self.dialogue_timer > 2: self.dialogue_stage = 0

        # --- Draw torch/light ---
        self.draw_player_with_light(self.player)

        # --- Scene transition only if player touches the door ---
        if self.door_visible and self.player.rect.colliderect(self.door_rect): 
            self.setup_scene("scene3")
        

    # ---------------- SCENE 3 MONSTER CHASE ----------------
    def update_scene3(self, dt):
        self.player.move(self.platforms)
        cam_x = max(0, min(self.player.rect.centerx - self.WIDTH // 2, self.platforms[-1].rect.right - self.WIDTH))
        
        # Invisible wall before Krampus ground touch
        if not self.krampus_on_ground and self.player.rect.right > 390: self.player.rect.right = 390

        # --- Krampus spawn ---
        self.spawn_timer += dt
        if self.spawn_timer >= 2 and not self.krampus_active:
            self.krampus_active = True
            self.krampus_spawn_sound.play()
            if not self.krampus_shake_done:
                pygame.mixer.Channel(6).play(self.rumble2_sound)
                self.krampus_shake_done = True

        # --- Krampus movement ---
        if self.krampus_active:
            if not self.krampus_on_ground:
                self.krampus.rect.y += 900 * dt
                for p in self.platforms:
                    if self.krampus.rect.bottom >= p.rect.top:
                        self.krampus.rect.bottom = p.rect.top
                        self.krampus_on_ground = True
                        self.play_bgm("scene3")
            else:
                self.krampus.rect.x += (self.monster_speed if self.krampus.rect.x < self.player.rect.x else -self.monster_speed) * dt
                self.krampus.facingRight = self.krampus.rect.x < self.player.rect.x

        # --- Screen shake ---
        sx = sy = 0
        if self.shake_timer > 0:
            self.shake_timer -= dt
            sx, sy = random.randint(-8, 8), random.randint(-8, 8)
            if not self.first_shake_done:
                pygame.mixer.Channel(5).play(self.rumble_sound)
                self.first_shake_done = True

        # --- Draw background ---
        self.display.blit(self.ice_cave_bg2, (sx, sy))

        # --- Draw platforms ---
        for p in self.platforms: 
            self.display.blit(p.image, (p.rect.x - cam_x + sx, p.rect.y + sy))
        
        # --- Draw ceiling pillars + collision logic ---
        for p in self.pillars: 
            self.display.blit(p.image, (p.rect.x - cam_x + sx, p.rect.y + sy))
            if self.player.rect.colliderect(p.rect):
                if self.player.rect.centery < p.rect.centery: self.player.rect.bottom = p.rect.top
                else: self.player.rect.top = p.rect.bottom
                self.collision_sound.play()

        # --- Update and draw falling rocks + collision logic ---
        for r in self.falling_rocks:
            r.update(dt, self.platforms, self.falling_rocks)
            r.draw(self.display, cam_x, sy)
            if r.solid and self.player.rect.colliderect(r.rect):
                if self.player.rect.centerx < r.rect.centerx: self.player.rect.right = r.rect.left
                else: self.player.rect.left = r.rect.right
                self.collision_sound.play()

        # --- Entry dialogue ---
        if not self.scene3_entry_dialogue_shown:
            self.draw_dialogue("What's that noise?!")
            self.dialogue_timer += dt
            if self.dialogue_timer > 2: self.scene3_entry_dialogue_shown = True

        # --- Torch and Krampus drawing --- 
        orig_x = self.player.rect.x
        self.player.rect.x -= cam_x
        self.draw_player_with_light(self.player)
        self.player.rect.x = orig_x

        # --- Krampus Collisions ---
        if self.krampus_active:
            self.display.blit(pygame.transform.flip(self.krampus.img, not self.krampus.facingRight, False), (self.krampus.rect.x - cam_x, self.krampus.rect.y))
            self.draw_krampus_danger(self.player, self.krampus)
            if self.player.rect.colliderect(self.krampus.rect): self.game_over()

        # --- Transition --- 
        if self.player.rect.right >= self.platforms[-1].rect.right: self.setup_scene("scene4")


    # ---------------- SCENE 4 EXIT ----------------
    def update_scene4(self, dt):
        # --- Player movement ---
        self.player.move(self.platforms)
        if self.player.rect.left < 0: self.player.rect.left = 0
        
        # --- Krampus spawn delay ---
        if not self.krampus_active:
            self.krampus_timer += dt
            if self.krampus_timer >= self.krampus_spawn_delay: 
                self.krampus_active = True

        # --- Draw background ---
        self.display.blit(self.ice_cave_bg3, (0, 0))

        # --- Draw platforms ---
        for p in self.platforms: self.display.blit(p.image, p.rect)
        
        # --- Scene 4 Light Cone ---
        cone = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone, (255, 255, 200, 120), [(self.WIDTH, 260), (self.WIDTH-60, 200), (self.WIDTH-450, 450), (self.WIDTH-450, 520), (self.WIDTH-60, 360)])
        self.display.blit(cone, (0, 0))

        # --- Krampus movement and drawing ---
        if self.krampus_active:
            if self.krampus.rect.x < self.player.rect.x - 50:
                self.krampus.rect.x += self.krampus_speed * dt
                self.krampus.facingRight = True
            else: self.krampus.rect.x = self.player.rect.x - 50
            self.display.blit(pygame.transform.flip(self.krampus.img, not self.krampus.facingRight, False), (self.krampus.rect.x, self.krampus.rect.y))
            self.draw_krampus_danger(self.player, self.krampus)
            if self.player.rect.colliderect(self.krampus.rect): self.game_over()

        # --- Draw player, torch, final dialogue ---
        self.draw_player_with_light(self.player)
        if not self.scene4_entry_dialogue_shown:
            self.draw_dialogue("THERE'S THE EXIT!!")
            self.dialogue_timer += dt
            if self.dialogue_timer > 2: self.scene4_entry_dialogue_shown = True

        # --- Final scene exit ---
        if self.player.rect.right >= self.WIDTH:

            # Stop BGM immediately
            pygame.mixer.stop() 
            pygame.mixer.music.stop()
            self.current_bgm = None
            
            # play scream
            self.exit_scream.play()
            
            # slow white fade
            flash = pygame.Surface((self.WIDTH, self.HEIGHT))
            flash.fill((255, 255, 255))
            for alpha in range(0, 255, 5):
                flash.set_alpha(alpha)
                self.display.blit(self.ice_cave_bg3, (0, 0))

                for p in self.platforms: 
                    self.display.blit(p.image, p.rect)

                self.draw_player_with_light(self.player)
                
                if self.krampus_active:
                    self.display.blit(pygame.transform.flip(self.krampus.img, not self.krampus.facingRight, False), (self.krampus.rect.x, self.krampus.rect.y))

                self.display.blit(flash, (0, 0))

                if alpha > 180:
                    txt = self.font.render("You hear a loud screeching from Krampus but you escaped...", True, (0, 0, 0))
                    self.display.blit(txt, (self.WIDTH // 2 - 300, self.HEIGHT // 2))

                pygame.display.update()
                pygame.time.delay(30)
            
            pygame.time.delay(6000)
            self.isInitialized = False # Un-init to allow replays without closing the window
            self.gameStateManager.set_state("chapter3")


    # --- Handles all dialogue related stuff ---
    def draw_dialogue(self, text, offset=60):
        surf = self.font.render(text, True, (255, 255, 255))
        bw, bh = surf.get_width() + 12, surf.get_height() + 12
        bx, by = self.player.rect.centerx - bw//2, self.player.rect.y - offset
        pygame.draw.rect(self.display, (0, 0, 0), (bx, by, bw, bh))
        self.display.blit(surf, (bx + 6, by + 6))

    
    def draw_ui_esc(self, events):
        btn_width, btn_height = 120, 40
        btn_rect = pygame.Rect(20, 20, btn_width, btn_height)
        mouse_pos = pygame.mouse.get_pos()
        
        is_hover = btn_rect.collidepoint(mouse_pos)
        bg_alpha = 200 if is_hover else 150  
        bg_color = (40, 40, 40) if is_hover else (0, 0, 0)
        
        temp_surf = pygame.Surface((btn_width, btn_height), pygame.SRCALPHA)
        
        pygame.draw.rect(temp_surf, (*bg_color, bg_alpha), (0, 0, btn_width, btn_height), border_radius=5)
        
        esc_font = pygame.font.SysFont("Arial", 20, bold=True)
        txt_surf = esc_font.render("[ESC] Menu", True, (255, 255, 255))
        txt_rect = txt_surf.get_rect(center=(btn_width // 2 - 1, btn_height // 2 - 1))
        
        txt_surf.set_alpha(bg_alpha)
        temp_surf.blit(txt_surf, txt_rect)
        
        self.display.blit(temp_surf, (btn_rect.x, btn_rect.y))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if is_hover:
                    self.return_to_menu()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.return_to_menu()

    def return_to_menu(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        
        self.gameStateManager.set_state("menu")
        self.isInitialized = False