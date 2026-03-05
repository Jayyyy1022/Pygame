import pygame

class Player_Child(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        
        img = pygame.image.load("Assets\\Player\\child_idle.png")
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

        self.speed = speed ## Can change base speed (how many pixels to move)
        self.velocityY = 0
        self.direction = 0  ## Movement direction | Left = -1 | Idle = 0 | Right = 1 |
        self.facingRight = True
        self.onGround = True


    def move(self):
        keys = pygame.key.get_pressed()
        
        # enter idle state when no key presses
        self.direction = 0

        ## reset movement variables
        dx = 0
        dy = 0

        ## WASD Movement | Space for jump
        if keys[pygame.K_a]:
            #self.rect.x -= self.speed
            self.direction = -1
            self.facingRight = False
        if keys[pygame.K_d]:
            #self.rect.x -= self.speed
            self.direction = 1
            self.facingRight = True
        if keys[pygame.K_SPACE] and self.onGround:
            self.velocityY = -15
            self.onGround = False

        ## assign movement variables if moving left or right
        if self.direction == -1:
            dx = -self.speed
        if self.direction == 1:
            dx = self.speed
        
        # update rect position
        self.rect.x += dx
        self.rect.y += dy
            

        

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, not self.facingRight, False), self.rect)