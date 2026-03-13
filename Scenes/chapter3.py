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
pygame.mixer.music.set_volume(0.1) ## bgm

interact_sound = pygame.mixer.Sound("Assets\\SFX\\interact_sound.mp3")
interact_sound.set_volume(0.7)

knocking_door = pygame.mixer.Sound("Assets\\SFX\\knocking_door.mp3")
knocking_door.set_volume(0.7)

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

props = pygame.sprite.Group()
# props.add(platform.Platform((RIGHT_WALL_X - 275), (GROUND_Y - 50), 50, 50, PRESENT_COLOR)) ## present
# props.add(platform.Platform(LEFT_WALL_X, (GROUND_Y - 80), 170, 80, RED_OBJECT)) ## bed
# props.add(platform.Platform((LEFT_WALL_X + 210), 240, 220, 200, RED_OBJECT)) ## window
# props.add(platform.Platform((RIGHT_WALL_X - 245), (GROUND_Y - 300), 180, 300, RED_OBJECT)) ## tree
# props.add(platform.Platform((RIGHT_WALL_X - 15), (GROUND_Y - 175), 15, 175, RED_OBJECT)) ## door

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
font = pygame.font.SysFont(None, 25)

default_hint = "[J] Interact"
present_text = "Merry Christmas! ~Mom and Dad"
window_text = "I can't reach the windowsill..."
tree_text = "I wonder how they got this tree in."
bed_text = "        I'd rather stay awake for now..."

# room_objects = pygame.sprite.OrderedUpdates(bed, christmas_tree) ## no particular order ## use ordered updates 

class Chapter3:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.activeInteractable = None
        self.interactableDialogue = False

        self.interactables = [
            {"name": "present", "rect": present, "hint": "[J] Open", "text": present_text, "sound": interact_sound, "position": ((present.x + 25), (present.y - 10))},
            {"name": "window", "rect": window, "hint": "[J] Look outside", "text": window_text, "sound": interact_sound, "position": ((window.x + 110), (window.y - 10))},
            {"name": "tree", "rect": christmas_tree, "hint": default_hint, "text": tree_text, "sound": interact_sound, "position": ((christmas_tree.x + 90), (christmas_tree.y - 10))},
            {"name": "bed", "rect": bed, "hint": "[J] Sleep", "text": bed_text, "sound": interact_sound, "position": ((bed.x + 85), (bed.y - 10))},
            {"name": "door", "rect": door, "hint": "[J] Open", "text": "Who's there?", "sound": knocking_door, "position": ((door.x - 25), (door.y - 10))}
        ]

        # self.platforms = pygame.sprite.Group()
        # self.platforms.add(platform.Platform(-50, GROUND_Y, 900, 120, BROWN_FLOOR))

        self.player = player_child.Player_Child(PLAYER_X, (GROUND_Y - 60), PLAYER_SIZE_SCALE, MOVEMENT_SPEED, GRAVITY)
        

    def run(self, events):

        self.draw_scene_house_final()

        ## self.player.isCutscene = True ## need to set this too true during final jumpscare
        if not self.player.isCutscene:
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
                    if event.key == pygame.K_f:
                        self.gameStateManager.set_state("level")
                        pygame.mixer.music.fadeout(1000)
                    if event.key == pygame.K_j and current_touching_object:
                        if not self.interactableDialogue:
                            current_touching_object["sound"].play()
                        self.interactableDialogue = True
                        self.activeInteractable = current_touching_object["rect"]
            
            if current_touching_object:
                if self.interactableDialogue and self.activeInteractable == current_touching_object["rect"]:
                    display_text = current_touching_object["text"]
                else:
                    display_text = current_touching_object["hint"]
                    
                self.draw_text(display_text, WHITE, current_touching_object["position"][0], current_touching_object["position"][1])

        # self.object_interactions(present, (RIGHT_WALL_X - 255), (GROUND_Y - 80),  present_text)
        # self.object_interactions(window, 345, 260, window_text)
        # self.object_interactions(christmas_tree, 620, (GROUND_Y - 320), tree_text)
        # self.object_interactions(bed, (LEFT_WALL_X + 85), (GROUND_Y - 100), bed_text)
            

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
        # props.draw(self.display)

        self.draw_props_rect(BROWN_FLOOR, ceiling)
        self.draw_props_rect(RED_OBJECT, bed)
        self.draw_props_rect(RED_OBJECT, window)
        self.draw_props_rect(RED_OBJECT, christmas_tree)
        self.draw_props_rect(RED_OBJECT, door)
        self.draw_props_rect(PRESENT_COLOR, present)


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


    def draw_text(self, text, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midbottom = (x, y)
        self.display.blit(text_surface, text_rect)
    