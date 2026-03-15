import pygame

class Player_Child(pygame.sprite.Sprite):

    def __init__(self, x, y, scale, speed = 3, gravity = 0.75):
        super().__init__()
        self.baseSpeed = speed  
        self.speedMultiplier = 1
        self.direction = 0              ## Movement direction | Left = -1 | Idle = 0 | Right = 1 |
        self.facingRight = True
        self.isRunning = False
        self.velocityY = 0              ## jump height
        self.gravity = gravity
        self.isJumping = False
        self.onGround = False
        self.action = 0                 ## Player action | Idle = 0 | Walk = 1 | Run = 2 | Jump = 3 | 

        self.isAlive = True
        self.isCutscene = False


        self.animationList = []
        self.idleFrames = []
        for i in range(14):
            img_frame = self.load_and_crop_image(
                f"Assets\\Player\\Idle\\Idle ({i+1}).png", 
                scale
            )
            self.idleFrames.append(img_frame)
        self.animationList.append(self.idleFrames)

        self.walkingFrames = []
        for i in range(14):
            img_frame = self.load_and_crop_image(
                f"Assets\\Player\\Walk\\Walk ({i+1}).png", 
                scale
            )
            self.walkingFrames.append(img_frame)
        self.animationList.append(self.walkingFrames)

        self.runningFrames = []
        for i in range(14):
            img_frame = self.load_and_crop_image(
                f"Assets\\Player\\Run\\Run ({i+1}).png", 
                scale,
                crop_right = 258
            )            
            self.runningFrames.append(img_frame)
        self.animationList.append(self.runningFrames)
        
        self.jumpingFrames = []
        for i in range(14):
            img_frame = self.load_and_crop_image(
                f"Assets\\Player\\Jump\\Jump ({i+1}).png", 
                scale,
                crop_bottom = 82, 
                crop_right = 250
            )            
            self.jumpingFrames.append(img_frame)
        self.animationList.append(self.jumpingFrames)


        
        self.frameIndex = 0 
        self.image = self.animationList[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.updateTime = pygame.time.get_ticks() 



    def move(self, platforms):
        if self.isCutscene or not self.isAlive:
            return
        keys = pygame.key.get_pressed()
        
        ## enter idle state when no key presses / Resetting speed
        self.direction = 0
        self.isRunning = False
        self.speedMultiplier = 1.0
        dx = 0
        dy = 0

        ## A - D Movement | Space for jump | K for run | J for interact
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

        if not self.onGround and self.velocityY >= 0:
            self.rect.y += 1
            for platform in platforms:
                if platform.rect.colliderect(self.rect):
                    self.onGround = True
                    self.isJumping = False
                    break
            self.rect.y -= 1
        
        if not self.onGround:
            self.update_action(3)       ## jump
        elif self.direction == 0:
            self.update_action(0)       ## idle
        elif self.isRunning:
            self.update_action(2)       ## run
        else:
            self.update_action(1)       ## walk


    def update_animation(self):
        ANIMATION_COOLDOWN = 50

        self.image = self.animationList[self.action][self.frameIndex]

        if pygame.time.get_ticks() - self.updateTime > ANIMATION_COOLDOWN:
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
        
        if self.frameIndex >= len(self.animationList[self.action]):
            self.frameIndex = 0 

            
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frameIndex = 0 
            self.updateTime = pygame.time.get_ticks()


    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, not self.facingRight, False), self.rect)


    def load_and_crop_image(self, path, scale, crop_top = 20, crop_bottom = 58, crop_left = 11, crop_right = 311):
        img = pygame.image.load(path).convert_alpha()
        
        new_width = img.get_width() - crop_left - crop_right
        new_height = img.get_height() - crop_top - crop_bottom
        
        crop_rect = pygame.Rect(crop_left, crop_top, new_width, new_height)
    
        img = img.subsurface(crop_rect)
        return pygame.transform.scale(img, (int(new_width * scale), int(new_height * scale)))
