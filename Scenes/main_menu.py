import pygame
import sys
import random

from Scenes import particles


class MainMenu:
    def __init__(self, display, gameStateManager, screen_width, screen_height):
        self.display = display
        self.gameStateManager = gameStateManager
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.isInitialised = False

        self.current_off_x = 0
        self.current_off_y = 0
        self.lerp_speed = 0.05

        # Fonts
        self.button_font = pygame.font.SysFont(None, 45)
        self.hover_font = pygame.font.SysFont(None , 60)
        self.title_font_primary = pygame.font.SysFont("Georgia", 70, bold=True)
        self.title_font_secondary = pygame.font.SysFont("Georgia", 60, bold=True)
        
        # Parallax Layers
        self.layers = []
        try:
            base_path = "Assets\\Menu\\"
            layer_names = [
                "snowy_landscape_layer_4.png", # Furthest
                "snowy_landscape_layer_3.png",
                "snowy_landscape_layer_2.png",
                "snowy_landscape_layer_1.png"  # Closest
            ]
            for name in layer_names:
                img = pygame.image.load(base_path + name).convert_alpha()
                self.layers.append(img)
        except pygame.error:
            for i in range(4):
                surf = pygame.Surface((400, 600))
                surf.fill((20, 20, 40 + i*20))
                self.layers.append(surf)

        # Window Frame
        self.window_rect = pygame.Rect(450, 50, 300, 500)
        self.window_surface = pygame.Surface((self.window_rect.width, self.window_rect.height))
        
        # Snow Particles for the window
        self.snow_particles = []
        for _ in range(50):
            self.snow_particles.append(particles.Snow(self.window_rect.width, self.window_rect.height, drift_offset = -0.1))

        # Buttons
        self.buttons = [
            {"text": "Chapter 1", "state": "chapter1", "position": (50, 255)},
            {"text": "Chapter 2", "state": "chapter2", "position": (50, 335)},
            {"text": "Chapter 3", "state": "chapter3", "position": (50, 415)},
        ]
        self.exit_button = {"text": "Exit", "position": (self.SCREEN_WIDTH - 120, self.SCREEN_HEIGHT - 60)}

    def setup(self):
        self.isInitialised = True

        pygame.mixer.stop()
        pygame.mixer.music.stop()

        pygame.mixer.music.load("Assets\\SFX\\Silksong.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def run(self, events):
        if not self.isInitialised:
            self.setup()

        self.display.fill((10, 10, 15)) 
        self.draw_parallax_window()
        
        # Window Frame & Glass
        pygame.draw.rect(self.display, (60, 40, 30), self.window_rect, 15)
        glass = pygame.Surface((self.window_rect.width, self.window_rect.height), pygame.SRCALPHA)
        glass.fill((200, 230, 255, 40)) 
        self.display.blit(glass, self.window_rect)

        # Title
        self.draw_title()

        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    if self.get_btn_rect(btn).collidepoint(mouse_pos):
                        pygame.mixer.music.fadeout(500)
                        self.gameStateManager.set_state(btn["state"])
                        self.isInitialised = False # Reset for when we return to menu
                
                # Check Exit
                if self.get_btn_rect(self.exit_button).collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        for btn in self.buttons:
            self.draw_menu_button(btn, mouse_pos)
        self.draw_menu_button(self.exit_button, mouse_pos)

    def get_btn_rect(self, btn):
        surf = self.button_font.render(btn["text"], True, (255, 255, 255))
        return surf.get_rect(topleft=btn["position"])

    def draw_parallax_window(self):
        self.window_surface.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()

        target_x = max(0, min(self.SCREEN_WIDTH, mx)) - self.SCREEN_WIDTH // 2
        target_y = max(0, min(self.SCREEN_HEIGHT, my)) - self.SCREEN_HEIGHT // 2

        self.current_off_x += (target_x - self.current_off_x) * self.lerp_speed
        self.current_off_y += (target_y - self.current_off_y) * self.lerp_speed

        for i, layer in enumerate(self.layers):
            depth = (i + 1) * 0.02
            
            off_x = self.current_off_x * depth
            off_y = self.current_off_y * depth
            
            lx = (self.window_rect.width - layer.get_width()) // 2 - off_x
            ly = (self.window_rect.height - layer.get_height()) // 2 - off_y
            self.window_surface.blit(layer, (lx, ly))

        for p in self.snow_particles:
            p.update()
            p.draw(self.window_surface)

        self.display.blit(self.window_surface, self.window_rect)

    def draw_menu_button(self, btn, mouse_pos):
        text = btn["text"]
        x, y = btn["position"]
        
        base_surf = self.button_font.render(text, True, (255, 255, 255))
        base_rect = base_surf.get_rect(topleft=(x, y))
        
        is_hover = base_rect.collidepoint(mouse_pos)
        
        if is_hover:
            color = (255, 100, 100) 
            font = self.hover_font
        else:
            color = (255, 255, 255)
            font = self.button_font
            
        text_surf = font.render(text, True, color)
        
        rect = text_surf.get_rect(midleft=(x, y + base_rect.height // 2))
        
        self.display.blit(text_surf, rect)
        return is_hover
    
    def draw_title(self):
        if random.randint(0, 100) > 95:
            title_color = (100, 0, 0) # Dim red
        else:
            title_color = (200, 0, 0) # Bright red

        title_surface_1 = self.title_font_primary.render("Christmas", True, (200, 0, 0))
        title_surface_2 = self.title_font_secondary.render("Alone", True, title_color)

        self.display.blit(title_surface_1, (50, 70))
        self.display.blit(title_surface_2, (50, 150))