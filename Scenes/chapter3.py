import pygame
import sys
import random

from Entities.Obstacle import platform
from Entities.Decoration import prop
from Entities.Player import player_child
from Entities.Enemy import enemy_krampus
from Scenes import game_state_manager
from Scenes import particles

## Game variables
GROUND_Y = 550
LEFT_WALL_X = 25
RIGHT_WALL_X = 775
CEILING_Y = 30
GRAVITY = 0.75

## colors
BLIZZARD_NIGHT = (24, 29, 74)
BLIZZARD_FILTER = (68, 76, 148)
BEIGE_WALL = (227, 205, 163)
WARM = (189, 128, 108)
BROWN_FLOOR = (115, 65, 41)
RED_OBJECT = (210, 34, 21)
PRESENT_COLOR = (150, 20, 240)
WINDOW_GLASS_COLOR = (200, 230, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
XMAS_CONFETTI_COLORS = [(210, 34, 21), (34, 139, 34), (255, 215, 0), (255, 255, 255)]

## Music
# pygame.mixer.init()
# pygame.mixer.music.load("Assets\\SFX\\christmas_piano.wav")
# pygame.mixer.music.set_volume(0.1) ## bgm

# interact_sound = pygame.mixer.Sound("Assets\\SFX\\interact_sound.mp3")
# interact_sound.set_volume(0.7)

# knocking_door = pygame.mixer.Sound("Assets\\SFX\\knocking_door.mp3")
# knocking_door.set_volume(0.7)

# jumpscare_sound = pygame.mixer.Sound("Assets\\SFX\\jumpscare.wav")
# jumpscare_sound.set_volume(0.4)

# tension_horror_buildup = pygame.mixer.Sound("Assets\\SFX\\horror_tension_buildup.mp3")
# tension_horror_buildup.set_volume(0.4)

## placeholder props
# floor = pygame.Rect(-50, GROUND_Y, 900, 120)
# left_wall = pygame.Rect(-10, -50, 35, 600)
# right_wall = pygame.Rect(775, -50, 35, 600)
# ceiling = pygame.Rect(-50, -50, 900, 80)

# bed = pygame.Rect(LEFT_WALL_X, (GROUND_Y - 80), 170, 80)
# window = pygame.Rect((LEFT_WALL_X + 210), 240, 220, 200)
# christmas_tree = pygame.Rect((RIGHT_WALL_X - 245), (GROUND_Y - 300), 180, 300)
# door = pygame.Rect((RIGHT_WALL_X - 15), (GROUND_Y - 175), 15, 175)
# present = pygame.Rect((RIGHT_WALL_X - 275), (GROUND_Y - 50), 50, 50)

# window_glass = pygame.Surface((window.width, window.height))

# props = pygame.sprite.Group()
# props.add(platform.Platform((RIGHT_WALL_X - 275), (GROUND_Y - 50), 50, 50, PRESENT_COLOR)) ## present
# props.add(platform.Platform(LEFT_WALL_X, (GROUND_Y - 80), 170, 80, RED_OBJECT)) ## bed
# props.add(platform.Platform((LEFT_WALL_X + 210), 240, 220, 200, RED_OBJECT)) ## window
# props.add(platform.Platform((RIGHT_WALL_X - 245), (GROUND_Y - 300), 180, 300, RED_OBJECT)) ## tree
# props.add(platform.Platform((RIGHT_WALL_X - 15), (GROUND_Y - 175), 15, 175, RED_OBJECT)) ## door

## platforms and walls
# platforms = pygame.sprite.Group()
# platforms.add(platform.Platform(-50, GROUND_Y, 900, 120, BROWN_FLOOR))
# platforms.add(platform.Platform(-10, -50, 35, 600, BROWN_FLOOR))
# platforms.add(platform.Platform(775, -50, 35, 600, BROWN_FLOOR))

## Players and entities
MOVEMENT_SPEED = 3
PLAYER_X = 60
PLAYER_SIZE_SCALE = 0.1
## player = player_child.Player_Child(PLAYER_X, (GROUND_Y - 60), PLAYER_SIZE_SCALE, MOVEMENT_SPEED, GRAVITY)

## Fonts and Text
# pygame.font.init()
# font = pygame.font.SysFont(None, 25)

default_hint = "[J] Interact"
present_text = "Merry Christmas!\n Love, Mom and Dad"
window_text = "I can't reach the windowsill..."
tree_text = "I wonder how they got this tree in."
bed_text = "I'd rather stay awake for now..."
door_text = "Maybe later..."
dialogue_text = ["Oh...", ".. a nightmare..?", "Mom and dad left presents...", "I should check them out."]
thank_you_dialogue = "Thanks mom... Thanks dad..."

# room_objects = pygame.sprite.OrderedUpdates(bed, christmas_tree) ## no particular order ## use ordered updates 

class Chapter3:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.isInitialized = False
        # self.activeInteractable = None
        # self.interactableDialogue = False
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 25)
        self.large_font = pygame.font.SysFont(None, 50)

        pygame.mixer.init()
        pygame.mixer.stop()
        # pygame.mixer.music.load("Assets\\SFX\\christmas_piano.wav")
        # pygame.mixer.music.set_volume(0.1) ## bgm
        self.interact_sound = pygame.mixer.Sound("Assets\\SFX\\interact_sound.mp3")
        self.interact_sound.set_volume(0.65)
        self.knocking_door = pygame.mixer.Sound("Assets\\SFX\\knocking_door.mp3")
        self.knocking_door.set_volume(0.7)
        self.jumpscare_sound = pygame.mixer.Sound("Assets\\SFX\\jumpscare.wav")
        self.jumpscare_sound.set_volume(0.4)
        self.tension_horror_buildup = pygame.mixer.Sound("Assets\\SFX\\horror_tension_buildup.mp3")
        self.tension_horror_buildup.set_volume(0.4)
        self.door_breaking_sound = pygame.mixer.Sound("Assets\\SFX\\door_breaking.flac")
        self.door_breaking_sound.set_volume(0.6)
        self.present_confetti_sound = pygame.mixer.Sound("Assets\\SFX\confetti.mp3")

        self.interactChannel = pygame.mixer.Channel(0)
        self.knockingChannel = pygame.mixer.Channel(1)
        self.horrorTensionChannel = pygame.mixer.Channel(2)
        self.jumpscareChannel = pygame.mixer.Channel(3)
        self.doorbreakingChannel = pygame.mixer.Channel(4)
        self.presentConfettiChannel = pygame.mixer.Channel(5)

        self.floor = pygame.Rect(-50, GROUND_Y, 900, 120)
        self.left_wall = pygame.Rect(-10, -50, 35, 600)
        self.right_wall = pygame.Rect(775, -50, 35, 600)
        self.ceiling = pygame.Rect(-50, -50, 900, 80)

        self.bed = pygame.Rect(LEFT_WALL_X, (GROUND_Y - 112), 238, 112)
        self.window = pygame.Rect((LEFT_WALL_X + 210), 240, 220, 200)
        self.christmas_tree = pygame.Rect((RIGHT_WALL_X - 245), (GROUND_Y - 300), 180, 300)
        self.door = pygame.Rect((RIGHT_WALL_X - 15), (GROUND_Y - 175), 15, 175)
        self.present = pygame.Rect((RIGHT_WALL_X - 275), (GROUND_Y - 50), 50, 50)

        self.bed_prop = prop.BackgroundDecoration(self.bed.left - 3, self.bed.top + 2, "Assets\\Objects\\house_bed.png", 238, 112)
        self.window_prop = prop.BackgroundDecoration(self.window.left - 22, self.window.top - 28, "Assets\\Objects\\window_small.png", 264, 240)
        self.christmas_tree_prop = prop.BackgroundDecoration(self.christmas_tree.left, self.christmas_tree.top, "Assets\\Objects\\green_christmas_tree.png", 180, 300)
        self.door_prop = prop.BackgroundDecoration(self.door.left - 15, self.door.top, "Assets\\Objects\\house_door.png", 31, 175)
        self.present_prop = prop.BackgroundDecoration(self.present.left, self.present.top + 5, "Assets\\Objects\\present_unopened.png", 50, 50)
        self.photo_frame_prop = prop.BackgroundDecoration(self.bed.left - 1, self.bed.top - 220, "Assets\\Objects\\house_photo_frame.png", 23, 136)
        self.star_prop = prop.BackgroundDecoration(self.christmas_tree.left + 79, self.christmas_tree.top - 22, "Assets\\Objects\\star.png", 23.5, 24.4)
        
        

        self.window_glass = pygame.Surface((self.window.width, self.window.height)).convert_alpha()
        self.outside_window = pygame.image.load("Assets\\Backgrounds\\snowy_landscape_3.png").convert_alpha()


        self.interactables = [
            {"name": "present", "rect": self.present, "hint": "[J] Open", "text": present_text, "sound": self.interact_sound, "position": ((self.present.x + 25), (self.present.y - 25))},
            {"name": "window", "rect": self.window, "hint": "[J] Look outside", "text": window_text, "sound": self.interact_sound, "position": ((self.window.x + 110), (self.window.y - 40))},
            {"name": "tree", "rect": self.christmas_tree, "hint": default_hint, "text": tree_text, "sound": self.interact_sound, "position": ((self.christmas_tree.x + 90), (self.christmas_tree.y - 30))},
            {"name": "bed", "rect": self.bed, "hint": "[J] Sleep", "text": bed_text, "sound": self.interact_sound, "position": ((self.bed.x + 119), (self.bed.y))},
            {"name": "door", "rect": self.door, "hint": "[J] Open", "text": door_text, "sound": self.interact_sound, "position": ((self.door.x - 25), (self.door.y - 10))}
        ]

        # self.doorParticles = []
        # self.isDoorBroken = False
        # self.starSparkles = []
        # self.starSparkles.append(particles.Sparkle((self.christmas_tree.centerx + 4), (self.christmas_tree.top - 8))) ## have to change the pos so that it matches assets ltr
        # self.starSparkles.append(particles.Sparkle((self.christmas_tree.centerx + 7), (self.christmas_tree.top - 4)))
        # self.starSparkles.append(particles.Sparkle((self.christmas_tree.centerx - 6), (self.christmas_tree.top - 1)))
        # self.snowParticles = []
        # for _ in range(200):
        #     self.snowParticles.append(particles.Snow(800, 600, 2, -4))

        self.fade_in_alpha = 255
        self.fade_speed = 3
        # self.start_time = pygame.time.get_ticks()
        self.trigger_delay = 15000 # seconds delay b4 knocking phase
        self.knocking_interval = 3000 # 3 seconds between knocks
        # self.last_knock_time = 0

        # self.state = "NORMAL" # cutscene states, NORMAL, KNOCKING, BREAKING, INCHING, RUSH, BLACKOUT, CREDITS 
        # self.inching_count = 0
        # self.inching_timer = 0
        # self.black_bar_height = 0
        # self.red_filter_alpha = 0
        
        self.player_target_x = 0
        self.enemy_target_x = 0
        self.move_speed = 2 # Speed of smooth movement during inching
        self.fall_speed = 5

        # self.player = player_child.Player_Child(PLAYER_X, (GROUND_Y - 60), PLAYER_SIZE_SCALE, MOVEMENT_SPEED, GRAVITY)
        # self.krampus = enemy_krampus.Enemy_Krampus((self.door.centerx + 70), self.door.centery, 0.2, 2)
        

    def setup_level(self):
        self.state = "FADE_IN"
        self.start_time = pygame.time.get_ticks()
        self.last_knock_time = 0
        self.inching_count = 0
        self.inching_timer = 0
        self.black_bar_height = 0
        self.red_filter_alpha = 0
        self.activeInteractable = None
        self.interactableDialogue = False
        self.isDoorBroken = False

        self.dialogueTimer = pygame.time.get_ticks()
        self.dialogueStage = 0
        self.waitTimer = 0

        self.hasOpenedPresent = False
        self.presentDialogStart = 0
        self.presentDialogDuration = 3000

        pygame.mixer.music.load("Assets\\SFX\\christmas_piano.wav")
        pygame.mixer.music.set_volume(0.18)

        self.player = player_child.Player_Child(PLAYER_X, (GROUND_Y - 50), PLAYER_SIZE_SCALE, MOVEMENT_SPEED, GRAVITY)
        self.krampus = enemy_krampus.Enemy_Krampus((self.door.centerx + 70), self.door.centery, 0.2, 2)
        self.props = pygame.sprite.OrderedUpdates()
        self.props.add(self.window_prop, self.bed_prop, self.photo_frame_prop, 
                       self.christmas_tree_prop, self.star_prop, self.present_prop, self.door_prop)
        self.platforms = pygame.sprite.Group()
        self.platforms.add(platform.Platform(-50, GROUND_Y, 900, 120, BROWN_FLOOR))
        self.platforms.add(platform.Platform(-10, -50, 35, 600, BROWN_FLOOR))
        self.platforms.add(platform.Platform(775, -50, 35, 600, BROWN_FLOOR))
        self.platforms.add(platform.Platform(-50, -50, 900, 80, BROWN_FLOOR))

        self.doorParticles = []
        self.isDoorBroken = False

        self.starSparkles = []
        self.starSparkles.append(particles.Sparkle((self.christmas_tree.centerx + 14), (self.christmas_tree.top - 25))) ## have to change the pos so that it matches assets ltr
        self.starSparkles.append(particles.Sparkle((self.christmas_tree.centerx + 12), (self.christmas_tree.top - 18)))
        self.starSparkles.append(particles.Sparkle((self.christmas_tree.centerx - 11), (self.christmas_tree.top - 1)))

        self.snowParticles = []
        for _ in range(200):
            self.snowParticles.append(particles.Snow(800, 600, 2, -4))
        self.endingSnowParticles = []
        for _ in range(120):
            self.endingSnowParticles.append(particles.Snow(800, 600, start_at_top = True))

        self.confettiParticles = []
        

    def run(self, events):
        if not self.isInitialized:
            self.setup_level()
            self.isInitialized = True

        current_time = pygame.time.get_ticks()

        if self.state != "CREDITS":
            self.draw_room()
        
        if self.fade_in_alpha > 0:
            self.fade_in_alpha -= self.fade_speed
            if self.fade_in_alpha < 0:
                self.fade_in_alpha = 0

        if self.state == "FADE_IN":
            if self.fade_in_alpha <= 0:
                self.state = "DIALOGUE"
                
        elif self.state == "DIALOGUE":
            if self.dialogueStage < len(dialogue_text):
                self.draw_text(dialogue_text[self.dialogueStage], WHITE, self.player.rect.x + 80, self.player.rect.y - 10)

                if current_time - self.dialogueTimer > 2500:
                    self.dialogueStage += 1
                    self.dialogueTimer = current_time
            else:
                self.state = "BRIEF_PAUSE"
                self.wait_timer = current_time
        
        elif self.state == "BRIEF_PAUSE":
            if current_time - self.wait_timer > 500:
                self.state = "NORMAL"
                self.start_time = pygame.time.get_ticks() 

        elif self.state == "NORMAL":
            if current_time - self.start_time > self.trigger_delay:
                self.state = "KNOCKING"
                self.last_knock_time = current_time
            
            if self.hasOpenedPresent:
                if current_time - self.presentDialogStart < self.presentDialogDuration:
                    self.draw_text(thank_you_dialogue, WHITE, self.player.rect.x + 15, self.player.rect.y - 10)

        elif self.state == "KNOCKING":
            if current_time - self.last_knock_time > self.knocking_interval:
                pygame.mixer.music.fadeout(500)
                self.knockingChannel.play(self.knocking_door)
                self.last_knock_time = current_time
            
        elif self.state == "BREAKING":
            pygame.mixer.music.stop()
            if not self.doorParticles and not self.isDoorBroken:
                self.isDoorBroken = True
                for _ in range(50):
                    spawn_y = random.randint(self.door.top, self.door.bottom)
                    self.doorParticles.append(particles.Splinter(self.door.left, spawn_y, (150, 210)))

            self.knockingChannel.stop()
            self.interactChannel.stop()

            if self.player.rect.bottom < GROUND_Y: ## edge case for when you jump and start flying during cutscene
                self.player.rect.y += self.fall_speed 
            
            if self.black_bar_height < 100:
                self.black_bar_height += 2
            if self.red_filter_alpha < 100:
                self.red_filter_alpha += 2
            
            if self.inching_timer == 0:
                self.inching_timer = current_time
                self.player_target_x = self.player.rect.x - 220
                self.player.isCutscene = True
            
            if self.player.rect.x > self.player_target_x:
                self.player.rect.x -= 2

            if current_time - self.inching_timer > 1500:
                self.state = "INCHING"
                self.inching_timer = current_time

                if self.krampus.rect.x > self.door.x:
                    self.krampus.rect.x -= self.move_speed

                self.player_target_x = self.player.rect.x
                self.enemy_target_x = self.krampus.rect.x

        elif self.state == "INCHING":
            if self.player.rect.x > self.player_target_x:
                self.player.rect.x -= self.move_speed
            if self.krampus.rect.x > self.enemy_target_x:
                self.krampus.rect.x -= self.move_speed + 1 ## krampus will be slightly faster

            if current_time - self.inching_timer > 1500:
                self.inching_count += 1
                move_dist = 40 + (self.inching_count * 30)
                self.player_target_x = self.player.rect.x - move_dist
                self.enemy_target_x = self.krampus.rect.x - (move_dist + 20) ## krampus will be slightly faster
                self.inching_timer = current_time
                
                if self.inching_count >= 4:
                    self.state = "RUSH"
                    self.inching_timer = current_time

        elif self.state == "RUSH":
            self.horrorTensionChannel.fadeout(1000)
            self.player.rect.x -= 2
            self.krampus.rect.x -= 15
            if self.krampus.rect.colliderect(self.player.rect):
                self.state = "BLACKOUT"
                self.jumpscareChannel.play(self.jumpscare_sound)
                self.inching_timer = current_time

        elif self.state == "BLACKOUT":
            self.display.fill(BLACK)
            if current_time - self.inching_timer > 5000:
                self.state = "CREDITS"

        elif self.state == "CREDITS":
            self.display.fill(BLACK)
            self.play_bgm(58, 0) ## absolute cinema
            self.draw_text("MERRY BELATED CHRISTMAS", WHITE, 400, 260, True)
            self.draw_text("AND", WHITE, 400, 295, True)
            self.draw_text("THANK YOU FOR PLAYING", WHITE, 400, 330, True)
            self.draw_text("Press any key to return to menu", (150, 150, 150), 400, 380, True)
            self.draw_snow(self.endingSnowParticles)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    pygame.mixer.music.fadeout(500)
                    self.gameStateManager.set_state("menu")
                    self.isInitialized = False
                    return

        if self.state in ["NORMAL", "KNOCKING"]:
            self.handle_interactions(events)
            self.player.move(self.platforms)
        
        if self.state not in ["BLACKOUT", "CREDITS"]:
            self.player.draw(self.display)
            if self.krampus:
                self.krampus.draw(self.display)
            self.draw_vfx()
        
        self.draw_broken_door()
        self.draw_confetti()

        ## self.player.isCutscene = True ## need to set this too true during final jumpscare
        # if not self.player.isCutscene:
        #     self.handle_interactions(events)
        #     for event in events:
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_f:
        #                 self.gameStateManager.set_state("level")
        #                 pygame.mixer.music.fadeout(1000)
            
        # self.player.draw(self.display)
        # self.player.move(self.platforms)


    def handle_interactions(self, events):
        current_touching_object = None
        for obj in self.interactables:
            if self.player.rect.colliderect(obj["rect"]):
                current_touching_object = obj
                break
        if current_touching_object:
            if self.activeInteractable != current_touching_object["rect"]:
                self.interactableDialogue = False
                self.activeInteractable = None
        else:
            self.interactableDialogue = False
            self.activeInteractable = None

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j and current_touching_object:
                    if not self.interactableDialogue:
                        self.interactChannel.play(current_touching_object["sound"])

                    self.interactableDialogue = True
                    self.activeInteractable = current_touching_object["rect"]

                    if current_touching_object["name"] == "present" and not self.hasOpenedPresent:
                        self.hasOpenedPresent = True
                        self.presentConfettiChannel.play(self.present_confetti_sound)
                        self.presentDialogStart = pygame.time.get_ticks()
                        for _ in range(40):
                            self.confettiParticles.append(particles.Confetti(self.present.centerx, self.present.centery))

                    if self.activeInteractable == self.door and self.state == "KNOCKING":
                        self.state = "BREAKING"
                        self.doorbreakingChannel.play(self.door_breaking_sound)
                        self.horrorTensionChannel.play(self.tension_horror_buildup)
                        self.player.isCutscene = True
                        return

        if current_touching_object:
                if self.interactableDialogue and self.activeInteractable == current_touching_object["rect"]:
                    display_text = current_touching_object["text"]
                else:
                    display_text = current_touching_object["hint"]
                
                self.draw_text(display_text, WHITE, current_touching_object["position"][0], current_touching_object["position"][1])

    def draw_room(self):
        self.display.fill(WARM)
        self.play_bgm(0, 3000)

        self.window_glass.blit(self.outside_window, (0, 0))
        self.apply_color_filter(self.window_glass, BLIZZARD_FILTER)
        self.display.blit(self.window_glass, (self.window.x, self.window.y))

        ## snow thru window
        self.display.set_clip(self.window) 
        self.draw_snow(self.snowParticles)
        self.display.set_clip(None)

        self.props.draw(self.display)
        self.platforms.draw(self.display)
        # self.draw_props_rect(BROWN_FLOOR, self.ceiling)
        # self.draw_props_rect(RED_OBJECT, self.bed)
        # # self.draw_props_rect(RED_OBJECT, window)
        # self.draw_props_rect(RED_OBJECT, self.christmas_tree)
        # self.draw_props_rect(PRESENT_COLOR, self.present)
        
        # if self.state not in ["BREAKING", "INCHING", "RUSH"]:
        #     self.draw_props_rect(RED_OBJECT, self.door)

        if self.state in ["BREAKING", "INCHING", "RUSH"]:
            pygame.sprite.Sprite.kill(self.door_prop)

        self.draw_sparkles()

    # def object_interactions(self, interactedObject, x, y, interactText, hintText = default_hint):
    #     if self.player.rect.colliderect(interactedObject):
    #         if self.interactableDialogue:
    #             self.draw_text(interactText, WHITE, x, y)
    #         else:
    #             self.draw_text(hintText, WHITE, x, y)
    #     else:
    #         self.interactableDialogue = False


    def draw_props_rect(self, color, dimensions):
        pygame.draw.rect(self.display, color, dimensions)

    def draw_vfx(self):
        # Black bars
        if self.black_bar_height > 0:
            pygame.draw.rect(self.display, BLACK, (0, 0, 800, self.black_bar_height))
            pygame.draw.rect(self.display, BLACK, (0, 600 - self.black_bar_height, 800, self.black_bar_height))
        
        # Red filter
        if self.red_filter_alpha > 0:
            s = pygame.Surface((800, 600))
            s.set_alpha(self.red_filter_alpha)
            s.fill("RED")
            self.display.blit(s, (0,0))

        # White fade in
        if self.fade_in_alpha > 0:
            s = pygame.Surface((800, 600))
            s.set_alpha(self.fade_in_alpha)
            s.fill(WHITE)
            self.display.blit(s, (0,0))


    # def draw_text(self, text, color, x, y, large = False):
    #     font = self.large_font if large else self.font
    #     text_surface = font.render(text, True, color)
    #     text_rect = text_surface.get_rect()
    #     text_rect.midbottom = (x, y)
    #     self.display.blit(text_surface, text_rect)

    def draw_text(self, text, color, x, y, large=False):
        font = self.large_font if large else self.font
        lines = text.split('\n')
        line_height = font.get_linesize()
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_rect = text_surface.get_rect()
            text_rect.midbottom = (x, y + (i * line_height))
            self.display.blit(text_surface, text_rect)

    def play_bgm(self, startTime, fadeIn):
        if not pygame.mixer.music.get_busy() and self.state in ["BRIEF_PAUSE", "CREDITS"]:
            pygame.mixer.music.play(-1, startTime, fadeIn)

    def apply_color_filter(self, surface, color):
        filter = pygame.Surface(surface.get_size()).convert_alpha()
        filter.fill(color)
        surface.blit(filter, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

    def draw_broken_door(self):
        for particle in self.doorParticles[:]:
            particle.update()
            particle.draw(self.display)
            if particle.life <= 0:
                self.doorParticles.remove(particle)
    
    def draw_sparkles(self):
        for sparkle in self.starSparkles:
            sparkle.update()
            sparkle.draw(self.display)

    def draw_snow(self, particles):
        for snow in particles:
            snow.update()
            snow.draw(self.display)
    
    def draw_confetti(self):
        for particle in self.confettiParticles[:]:
            particle.update()
            particle.draw(self.display)
            if particle.life <= 0:
                self.confettiParticles.remove(particle)