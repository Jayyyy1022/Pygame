import pygame
import os

class Platform(pygame.sprite.Sprite):
    ## Added 'image_path' parameter, default is None
    def __init__(self, x, y, width, height, color=(100, 100, 100), image_path=None):
        super().__init__()
        
        ## If an image path is provided and the file exists, use the image!
        if image_path and os.path.exists(image_path):
            original_image = pygame.image.load(image_path).convert_alpha()
            ## Scale the image to fit the width and height we set in chapter1.py
            self.image = pygame.transform.scale(original_image, (width, height))
        else:
            ## Fallback: If no image is provided, create a simple solid color rectangle
            print(f"⚠️ 警告: 找不到图片文件 -> {image_path}")
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)