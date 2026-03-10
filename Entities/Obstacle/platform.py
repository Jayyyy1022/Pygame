import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(100, 100, 100)):
        super().__init__()
        # Create a simple solid color rectangle for the platform
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)