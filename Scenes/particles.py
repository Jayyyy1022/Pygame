import pygame
import random
import math

BROWN_DOOR = (115, 65, 41)

class Particles(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, 
                 position: list, 
                 color: str, 
                 direction: pygame.math.Vector2, 
                 speed: int):
        super().__init__(groups,)
        self.position = position
        self.color = color
        self.direction - direction
        self.speed = speed


    def create_surf(self):
        self.image = pygame.Surface((4, 4)).convert_alpha
        self.image.set_colorkey("black")
        pygame.draw.circle(self.image, self.color, (2, 2), 2)
        self.rect = self.image.get_rect(center = self.position)

    def move(self, dt):
        self.position += self.speed * dt
        self.rect.center = self.position

    def update(self, dt):
        self.move(dt)



class Splinter:
    def __init__(self, x, y, angle_range):
        self.rect = pygame.Rect(x, y, random.randint(8, 12), random.randint(6, 8))
        self.color = BROWN_DOOR
        
        angle = math.radians(random.uniform(angle_range[0], angle_range[1]))
        speed = random.uniform(4, 10)
        
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.gravity = 0.2
        self.life = 255

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += self.gravity
        self.life -= 5

    def draw(self, surface):
        if self.life > 0:
            surf = pygame.Surface((self.rect.width, self.rect.height))
            surf.set_alpha(self.life)
            surf.fill(self.color)
            surface.blit(surf, (self.rect.x, self.rect.y))



class Sparkle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_size = random.randint(5, 10)
        self.color = [255, 215, 0]
        self.timer = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(0.03, 0.07)
        
    def update(self):
        self.timer += self.speed
        self.scale = 0.5 + (math.sin(self.timer) * 0.5)
        
        flicker = random.randint(-20, 20)
        self.current_color = (
            max(0, min(255, self.color[0] + flicker)),
            max(0, min(255, self.color[1] + flicker)),
            0
        )

    def draw(self, surface):
        s = self.base_size * self.scale
        if s <= 0.1: 
            return
        
        pygame.draw.polygon(surface, self.current_color, [
            (self.x, self.y - s), (self.x + s/3, self.y), 
            (self.x, self.y + s), (self.x - s/3, self.y)
        ])
        pygame.draw.polygon(surface, self.current_color, [
            (self.x - s, self.y), (self.x, self.y - s/3), 
            (self.x + s, self.y), (self.x, self.y + s/3)
        ])

class Snow:
    def __init__(self, screen_width, screen_height, speed_offset = 0, drift_offset = 0):
        self.sw = screen_width
        self.sh = screen_height
        self.speed_offset = speed_offset
        self.drift_offset = drift_offset
        self.reset(True)

    def reset(self, first_time=False):
        self.x = random.randint(0, self.sw)
        self.y = random.randint(0, self.sh) if first_time else random.randint(-50, -10)
        
        self.size = random.randint(2, 4)
        self.fall_speed = random.uniform(1.5, 3.5) + self.speed_offset
        self.drift = random.uniform(-0.5, 0.5) + self.drift_offset
        self.alpha = random.randint(150, 255) 

    def update(self):
        self.y += self.fall_speed
        self.x += self.drift
        
        if self.y > self.sh or self.x < 0 or self.x > self.sw:
            self.reset()

    def draw(self, surface):
        pygame.draw.circle(surface, "white", (int(self.x), int(self.y)), self.size)