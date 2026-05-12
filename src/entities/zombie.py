import pygame
import math
from src.core.spritesheet import Spritesheet

class ZombieNPC:
    def __init__(self, x, y):
        self.pos = [x, y]
        # Menggunakan spritesheet zombie baru
        self.sheet = Spritesheet("assets/enemies/zombie_new.png", 8, 8, scale=1.6)
        self.direction = 'down'
        self.state = 'stand'
        self.current_col = 0
        self.frame_timer = 0
        self.anim_speed = 10
        self.speed = 3.5

    def update(self, player_pos, player_state):
        if player_state == 'run':
            # Mengejar pemain
            dx = player_pos[0] - self.pos[0]
            dy = player_pos[1] - self.pos[1]
            dist = math.hypot(dx, dy)
            
            if dist > 30:
                self.pos[0] += (dx / dist) * self.speed
                self.pos[1] += (dy / dist) * self.speed
                self.state = 'walk'
                
                # Update arah berdasarkan vektor gerak
                if abs(dx) > abs(dy):
                    self.direction = 'right' if dx > 0 else 'left'
                else:
                    self.direction = 'down' if dy > 0 else 'up'
            else:
                self.state = 'stand'
        else:
            self.state = 'stand'

        # Animasi
        self.frame_timer += 1
        if self.frame_timer >= self.anim_speed:
            self.frame_timer = 0
            if self.state == 'stand': self.current_col = 0
            else: self.current_col = (self.current_col + 1) % 6

    def draw(self, screen, camera=None):
        dir_map = {'down': 0, 'up': 1, 'right': 2, 'left': 3}
        row = dir_map[self.direction] + (0 if self.state == 'stand' else 4)
        
        draw_pos = self.pos
        if camera:
            draw_pos = camera.apply(self.pos)
            
        screen.blit(self.sheet.get_frame(row, self.current_col), draw_pos)
