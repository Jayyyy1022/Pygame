import pygame
from Entities.Obstacle.platform import Platform

class Chapter1:
    def __init__(self):
        # Group to hold all ground and rocks
        self.platforms = pygame.sprite.Group()
        
        # Level Colors for Greyboxing
        WHITE = (255, 255, 255)
        GROUND_COLOR = (34, 139, 34) # Green forest
        ROCK_COLOR = (128, 128, 128) # Gray rocks
        
        # --- Build Chapter 1 Level ---
        # Scene 1: House floor
        self.platforms.add(Platform(0, 500, 600, 100, WHITE))
        
        # Scene 2 & 3: Forest floor and rocks
        self.platforms.add(Platform(600, 500, 2000, 100, GROUND_COLOR))
        self.platforms.add(Platform(1200, 450, 60, 50, ROCK_COLOR)) # Rock 1
        self.platforms.add(Platform(1600, 420, 80, 80, ROCK_COLOR)) # Rock 2

        self.camera_scroll = 0

    def update(self, player, enemy, screen_width):
        # Camera logic: scroll level to the left when player moves past the middle
        if player.rect.right > screen_width // 2:
            scroll_amount = player.rect.right - (screen_width // 2)
            player.rect.right = screen_width // 2 # Keep player in the middle
            self.camera_scroll += scroll_amount
            
            # Move all platforms left to simulate camera moving right
            for p in self.platforms:
                p.rect.x -= scroll_amount
                
            # Move enemy left so it stays in relative position
            enemy.rect.x -= scroll_amount

        # Krampus chase logic (Scene 4 Trigger)
        if self.camera_scroll > 800:
            enemy.rect.x += 4 # Krampus starts running

    def draw(self, screen):
        # Draw all level objects
        self.platforms.draw(screen)