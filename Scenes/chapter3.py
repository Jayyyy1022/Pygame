import pygame

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
WHITE = (255, 255, 255)

## Items, Props or any Objects
# bed = prop() gonna be using props for beds
# christmas_tree = prop()

## placeholder
floor = pygame.Rect(-50, GROUND_Y, 900, 120)
left_wall = pygame.Rect(-10, -50, 35, 600)
right_wall = pygame.Rect(775, -50, 35, 600)
ceiling = pygame.Rect(-50, -50, 900, 80)

bed = pygame.Rect(LEFT_WALL_X, (GROUND_Y - 80), 170, 80)
window = pygame.Rect((LEFT_WALL_X + 210), 240, 220, 200)
christmas_tree = pygame.Rect((RIGHT_WALL_X - 245), (GROUND_Y - 300), 180, 300)
door = pygame.Rect((RIGHT_WALL_X - 15), (GROUND_Y - 175), 15, 175)

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



# room_objects = pygame.sprite.OrderedUpdates(bed, christmas_tree) ## no particular order ## use ordered updates 

class Chapter3:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        # self.platforms = pygame.sprite.Group()
        # self.platforms.add(platform.Platform(-50, GROUND_Y, 900, 120, BROWN_FLOOR))

        self.player = player_child.Player_Child(PLAYER_X, (GROUND_Y - 60), PLAYER_SIZE_SCALE, MOVEMENT_SPEED, GRAVITY)
        

    def run(self):
        self.display.fill(BLIZZARD_NIGHT)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            self.gameStateManager.set_state("level")
        
        self.draw_scene_house_final()

        self.player.draw(self.display)
        self.player.move(platforms)




    def draw_scene_house_final(self):
        # pygame.draw.rect(self.display, BROWN_FLOOR, floor)
        platforms.draw(self.display)
        # self.draw_props_rect(BROWN_FLOOR, left_wall)
        # self.draw_props_rect(BROWN_FLOOR, right_wall)
        self.draw_props_rect(BROWN_FLOOR, ceiling)
        self.draw_props_rect(RED_OBJECT, bed)
        self.draw_props_rect(RED_OBJECT, window)
        self.draw_props_rect(RED_OBJECT, christmas_tree)
        self.draw_props_rect(RED_OBJECT, door)


    

    def draw_props_rect(self, color, dimensions):
        pygame.draw.rect(self.display, color, dimensions)
    
    