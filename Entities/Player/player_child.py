import pygame

class Player_Child(pygame.sprite.Sprite):

    def __init__(self, x, y, scale, speed, gravity):
        pygame.sprite.Sprite.__init__(self)
        
        ## Frames
        img = pygame.image.load("Assets\\Player\\player_idle.png")
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

        self.idleFrames = []
        self.walkingFrames = []
        self.jumpingFrames = []

        self.frameIndex = 0 ## starts from first img in array, will be used for looping player frames
        self.updateTime = pygame.time.get_ticks() ## times how long has passed since last animation update, used for animation cycles

        ## Stats and states
        self.baseSpeed = speed ## Can change base speed (how many pixels to move)
        self.speedMultiplier = 1
        self.direction = 0  ## Movement direction | Left = -1 | Idle = 0 | Right = 1 |
        self.facingRight = True
        self.isRunning = False
        self.velocityY = 0  ## jump height
        self.gravity = gravity
        self.isJumping = False
        self.onGround = False
        self.action = 0     ## Player action | Idle = 0 | Walk = 1 | Run = 2 | Jump = 3 | can add more actions if necessary
        #self.isAlive = True


## Added 'platforms' parameter to receive level obstacles
    def move(self, platforms):
        keys = pygame.key.get_pressed()
        
        ## enter idle state when no key presses / Resetting speed
        self.direction = 0
        self.isRunning = False
        self.speedMultiplier = 1.0

        ## reset movement variables - to be used for collision
        dx = 0
        dy = 0

        ## A - D Movement | Space for jump | K for run | J for interact
        if keys[pygame.K_a]:
            self.direction = -1
            self.facingRight = False
        if keys[pygame.K_d]:
            self.direction = 1
            self.facingRight = True
        if keys[pygame.K_k] and self.direction != 0:
            self.isRunning = True
            self.speedMultiplier = 2
        if keys[pygame.K_SPACE] and self.onGround:
            self.velocityY = -12
            self.isJumping = True
            self.onGround = False

        if not self.onGround:
            self.update_action(3) # jump
        elif self.direction == 0:
            self.update_action(0) # idle
        elif self.isRunning:
            self.update_action(2) # run
        else:
            self.update_action(1) # walk


        ## assign movement variables if moving left or right
        if self.direction == -1:    
            dx = int(-(self.baseSpeed * self.speedMultiplier))
        if self.direction == 1:
            dx = int(self.baseSpeed * self.speedMultiplier)
        
        ## jumping mechanism
        self.velocityY += self.gravity
        if self.velocityY > 10:  ## limiting terminal velocity 
            self.velocityY = 10
        
        ## apply gravity to dy
        dy += self.velocityY

        ## --- NEW DYNAMIC COLLISION DETECTION ---
        
        ## 1. X-axis collision
        self.rect.x += dx
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if dx > 0: # Moving right, hit left side of platform
                    self.rect.right = platform.rect.left
                if dx < 0: # Moving left, hit right side of platform
                    self.rect.left = platform.rect.right

        ## 2. Y-axis collision
        self.rect.y += dy
        self.onGround = False # Reset ground state before checking
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if dy > 0: # Falling down, hit top of platform
                    self.rect.bottom = platform.rect.top
                    self.velocityY = 0
                    self.onGround = True
                    self.isJumping = False
                elif dy < 0: # Jumping up, hit bottom of platform (ceiling)
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