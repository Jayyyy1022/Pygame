import os
import pygame


class FallingRock(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, fall_speed=300):
        super().__init__()
        if os.path.exists(image_path):
            img = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(img, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill((150, 75, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.fall_speed = fall_speed
        self.active = True  # still falling

    def update(self, dt, platforms):
        if self.active:
            self.rect.y += self.fall_speed * dt
            # Stop falling on platforms
            for p in platforms:
                if self.rect.colliderect(p.rect):
                    self.rect.bottom = p.rect.top
                    self.active = False