import pygame

class Enemy_Krampus(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, gravity=0.75):
        pygame.sprite.Sprite.__init__(self)

        ## Frames
        img = pygame.image.load("Assets\\Enemy\\enemy_idle.png").convert_alpha()
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

        self.frameIndex = 0 ## starts from first img in array, will be used for looping player frames
        self.updateTime = pygame.time.get_ticks() ## times how long has passed since last animation update, used for animation cycles

        ## Stats and states
        self.baseSpeed = speed ## Can change base speed (how many pixels to move)
        self.speedMultiplier = 1
        self.direction = 0  ## Movement direction | Left = -1 | Idle = 0 | Right = 1 |
        self.facingRight = True
        self.isRunning = False
        # self.gravity = gravity
        # self.isJumping = False
        # self.onGround = False
        self.action = 0     ## Enemy actions | Idle = 0 | Walk = 1 | Run = 2 | can add more actions if necessary

    
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, not self.facingRight, False), self.rect)

    def shriek(self):
        ## sound test
        pygame.mixer.init()
        scare = pygame.mixer.Sound("Assets\\SFX\\jumpscare.wav")
        scare.set_volume(0.16)
        scare.play()