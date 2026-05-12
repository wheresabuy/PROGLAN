import pygame

class VisualEffects:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.darkness_surf = pygame.Surface((width, height))
        self.flash_surf = pygame.Surface((width, height))
        self.flash_surf.fill((255, 255, 255))
        self.flash_timer = 0
        self.flash_duration = 60
        self.shake_amount = 0

    def draw_darkness(self, screen, player_pos, camera, flashlight_on, battery_level, is_injured):
        dark_color = (15, 15, 25)
        if is_injured:
            pulse = int(abs(math.sin(pygame.time.get_ticks() * 0.003)) * 40)
            dark_color = (25+pulse, 15, 15)
        
        self.darkness_surf.fill(dark_color)
        if flashlight_on and battery_level > 0:
            light_radius = 200
            screen_pos = camera.apply(player_pos)
            for r in range(light_radius, 0, -8):
                alpha = int(255 * (r / light_radius))
                pygame.draw.circle(self.darkness_surf, (0, 0, 0, alpha), (int(screen_pos[0] + 32), int(screen_pos[1] + 32)), r)
        
        screen.blit(self.darkness_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    def trigger_flash(self, duration=120):
        self.flash_timer = duration
        self.flash_duration = duration
        self.shake_amount = 15 # Guncangan kuat di awal

    def draw_flash(self, screen):
        # Handle Screen Shake
        shake_offset = (0, 0)
        if self.shake_amount > 0:
            shake_offset = (random.randint(-self.shake_amount, self.shake_amount), 
                            random.randint(-self.shake_amount, self.shake_amount))
            self.shake_amount = max(0, self.shake_amount - 1)

        # Handle Flash Overlay
        if self.flash_timer > 0:
            alpha = int((self.flash_timer / self.flash_duration) * 255)
            self.flash_surf.set_alpha(alpha)
            screen.blit(self.flash_surf, shake_offset)
            self.flash_timer -= 1
        return shake_offset

import random
import math
