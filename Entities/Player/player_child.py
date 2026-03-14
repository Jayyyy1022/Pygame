import pygame

class Player_Child(pygame.sprite.Sprite):

    def __init__(self, x, y, scale, speed, gravity):
        super().__init__()
        
        img = pygame.image.load("Assets\\Player\\player_idle.png").convert_alpha()
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

        self.idleFrames = []
        self.walkingFrames = []
        self.jumpingFrames = []

        self.frameIndex = 0 
        self.updateTime = pygame.time.get_ticks() 

        self.baseSpeed = speed 
        self.speedMultiplier = 1
        self.direction = 0  
        self.facingRight = True
        self.isRunning = False
        self.velocityY = 0  
        self.gravity = gravity
        self.isJumping = False
        self.onGround = False
        self.action = 0  

        self.isAlive = True
        self.isCutscene = False

    def move(self, platforms):
        if self.isCutscene or not self.isAlive:
            return
        keys = pygame.key.get_pressed()
        
        self.direction = 0
        self.isRunning = False
        self.speedMultiplier = 1.0
        dx = 0
        dy = 0

        
        if keys[pygame.K_a]:
            self.direction = -1
            self.facingRight = False
        if keys[pygame.K_d]:
            self.direction = 1
            self.facingRight = True
        if (keys[pygame.K_k] or keys[pygame.K_LSHIFT]) and self.direction != 0: 
            self.isRunning = True
            self.speedMultiplier = 2
        if keys[pygame.K_SPACE] and self.onGround:
            self.velocityY = -12
            self.isJumping = True
            self.onGround = False

        if not self.onGround:
            self.update_action(3) 
        elif self.direction == 0:
            self.update_action(0) 
        elif self.isRunning:
            self.update_action(2) 
        else:
            self.update_action(1) 

        if self.direction == -1:    
            dx = int(-(self.baseSpeed * self.speedMultiplier))
        if self.direction == 1:
            dx = int(self.baseSpeed * self.speedMultiplier)
        
        self.velocityY += self.gravity
        if self.velocityY > 10:  
            self.velocityY = 10
        dy = int(self.velocityY)

        ## --- DYNAMIC COLLISION DETECTION ---
        
        ## X-axis collision
        self.rect.x += dx
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if self.rect.bottom > platform.rect.top + 2:
                    if dx > 0: 
                        self.rect.right = platform.rect.left
                    if dx < 0: 
                        self.rect.left = platform.rect.right

        ## Y-axis collision
        self.rect.y += dy
        self.onGround = False 
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if dy >= 0: 
                    self.rect.bottom = platform.rect.top
                    self.velocityY = 0
                    self.onGround = True
                    self.isJumping = False
                elif dy < 0: 
                    self.rect.top = platform.rect.bottom
                    self.velocityY = 0

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
            
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frameIndex = 0 
            self.updateTime = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, not self.facingRight, False), self.rect)