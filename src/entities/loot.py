import pygame
import math

class Loot:
    def __init__(self, name, x, y, item_type, image_path=None, prompt=None):
        self.name = name
        self.pos = (x, y)
        self.item_type = item_type
        self.prompt = prompt or f"Tekan ENTER untuk ambil {name}"
        self.collected = False
        self.hover_offset = 0
        
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image.set_colorkey((255, 255, 255))
                self.image = pygame.transform.scale(self.image, (64, 64))
            except Exception as e:
                print(f"Debug: Error loading {image_path}: {e}")
                self.image = pygame.Surface((40, 40))
                self.image.fill((255, 0, 0))
        else:
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 215, 0))
            
        self.rect = self.image.get_rect(topleft=(x, y))

    def check_interaction(self, player_pos):
        dx = self.pos[0] - player_pos[0]
        dy = self.pos[1] - player_pos[1]
        return (dx**2 + dy**2)**0.5 < 100

    def get_interaction_prompt(self):
        return self.prompt

    def draw(self, screen, player_pos, camera=None):
        if not self.collected:
            self.hover_offset = math.sin(pygame.time.get_ticks() * 0.005) * 10
            draw_pos = self.pos
            if camera:
                draw_pos = camera.apply(self.pos)
            screen.blit(self.image, (draw_pos[0], draw_pos[1] + self.hover_offset))
