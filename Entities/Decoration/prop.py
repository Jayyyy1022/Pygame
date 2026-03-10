import pygame

class BackgroundDecoration(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, width=None, height=None):
        super().__init__()
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            if width and height:
                self.image = pygame.transform.scale(self.image, (width, height))
        except:
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 0, 255)) 
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    