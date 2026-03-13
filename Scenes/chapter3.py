import pygame
import sys

from Entities.Obstacle import platform
from Entities.Decoration import prop
from Entities.Player import player_child
from Scenes import game_state_manager

## Game variables
GROUND_Y = 550
LEFT_WALL_X = 25
RIGHT_WALL_X = 775
CEILING_Y = 30
GRAVITY = 0.75

## colors
BLIZZARD_NIGHT = (24, 29, 74)
BROWN_FLOOR = (115, 65, 41)
RED_OBJECT = (210, 34, 21)
PRESENT_COLOR = (150, 20, 240)
WHITE = (255, 255, 255)

## Music
pygame.mixer.init()
pygame.mixer.music.load("Assets\\SFX\\christmas_piano.wav")
pygame.mixer.music.set_volume(0.2) ## bgm

interact_sound = pygame.mixer.Sound("Assets\\SFX\\interact_sound.mp3")
interact_sound.set_volume(0.7)

## placeholder props
floor = pygame.Rect(-50, GROUND_Y, 900, 120)
left_wall = pygame.Rect(-10, -50, 35, 600)
right_wall = pygame.Rect(775, -50, 35, 600)
ceiling = pygame.Rect(-50, -50, 900, 80)

bed = pygame.Rect(LEFT_WALL_X, (GROUND_Y - 80), 170, 80)
window = pygame.Rect((LEFT_WALL_X + 210), 240, 220, 200)
christmas_tree = pygame.Rect((RIGHT_WALL_X - 245), (GROUND_Y - 300), 180, 300)
door = pygame.Rect((RIGHT_WALL_X - 15), (GROUND_Y - 175), 15, 175)

present = pygame.Rect((RIGHT_WALL_X - 275), (GROUND_Y - 50), 50, 50)

# props = pygame.sprite.Group()
# props.add(prop.BackgroundDecoration((RIGHT_WALL_X - 275), (GROUND_Y - 50), 50, 50))

## platforms and walls
platforms = pygame.sprite.Group()
platforms.add(platform.Platform(-50, GROUND_Y, 900, 120, BROWN_FLOOR))
platforms.add(platform.Platform(-10, -50, 35, 600, BROWN_FLOOR))
platforms.add(platform.Platform(775, -50, 35, 600, BROWN_FLOOR))

## Players and entities
MOVEMENT_SPEED = 3
PLAYER_X = 60
PLAYER_SIZE_SCALE = 0.1
## player = player_child.Player_Child(PLAYER_X, (GROUND_Y - 60), PLAYER_SIZE_SCALE, MOVEMENT_SPEED, GRAVITY)

## Fonts and Text
pygame.font.init()
font = pygame.font.SysFont(None, 30)

hint = "Press J to interact"
present_text = "Merry Christmas!"

# room_objects = pygame.sprite.OrderedUpdates(bed, christmas_tree) ## no particular order ## use ordered updates 

class Chapter3:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.interactableDialogue = False

        # self.platforms = pygame.sprite.Group()
        # self.platforms.add(platform.Platform(-50, GROUND_Y, 900, 120, BROWN_FLOOR))

        self.player = player_child.Player_Child(PLAYER_X, (GROUND_Y - 60), PLAYER_SIZE_SCALE, MOVEMENT_SPEED, GRAVITY)
        

    def run(self, events):

        self.draw_scene_house_final()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.gameStateManager.set_state("level")
                    pygame.mixer.music.fadeout(1000)
                if event.key == pygame.K_j and self.player.rect.colliderect(present):
                    interact_sound.play(0)
                    self.interactableDialogue = True
        
        if self.player.rect.colliderect(present):
            if self.interactableDialogue:
                self.draw_text(present_text, WHITE, (RIGHT_WALL_X - 255), (GROUND_Y - 80))
            else:
                self.draw_text(hint, WHITE, (RIGHT_WALL_X - 255), (GROUND_Y - 80))
        else:
            self.interactableDialogue = False
            

        self.player.draw(self.display)
        self.player.move(platforms)




    def draw_scene_house_final(self):
        self.display.fill(BLIZZARD_NIGHT)

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1, 0, 4000)

        # pygame.draw.rect(self.display, BROWN_FLOOR, floor)
        # self.draw_props_rect(BROWN_FLOOR, left_wall)
        # self.draw_props_rect(BROWN_FLOOR, right_wall)

        platforms.draw(self.display)

        self.draw_props_rect(BROWN_FLOOR, ceiling)
        self.draw_props_rect(RED_OBJECT, bed)
        self.draw_props_rect(RED_OBJECT, window)
        self.draw_props_rect(RED_OBJECT, christmas_tree)
        self.draw_props_rect(RED_OBJECT, door)
        self.draw_props_rect(PRESENT_COLOR, present)

    

    def draw_props_rect(self, color, dimensions):
        pygame.draw.rect(self.display, color, dimensions)

    def draw_text(self, text, color, x, y):
        text_surface = font.render(text, False, color)
        text_rect = text_surface.get_rect()
        text_rect.midbottom = (x, y)
        self.display.blit(text_surface, text_rect)
    