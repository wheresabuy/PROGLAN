import pygame
import math
from src.core.spritesheet import Spritesheet

class ZombieNPC:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.sheet = Spritesheet("assets/enemies/zombie_new.png", 8, 8, scale=2.0)
        self.direction = 'down'
        self.state = 'stand'
        self.current_col = 0
        self.frame_timer = 0
        self.anim_speed = 10
        self.speed = 2.5
        self.stun_timer = 0
        self.health = 100

    def update(self, player_pos, player_state, tactical_items=[]):
        if self.stun_timer > 0:
            self.stun_timer -= 1
            self.state = 'stand'
            return

        # Prioritas: Cek apakah ada Decoy aktif
        target_pos = player_pos
        is_aggressive = (player_state == 'run')
        
        for item in tactical_items:
            if item.item_type == "Decoy" and item.active and item.reached_target:
                dx = item.pos[0] - self.pos[0]
                dy = item.pos[1] - self.pos[1]
                if math.hypot(dx, dy) < 400: # Radius dengar decoy
                    target_pos = item.pos
                    is_aggressive = True
                    break

        # Cek apakah terkena api Molotov
        for item in tactical_items:
            if item.item_type == "Molotov" and item.reached_target and item.active:
                dx = item.pos[0] - self.pos[0]
                dy = item.pos[1] - self.pos[1]
                if math.hypot(dx, dy) < 50:
                    self.health -= 2 # Terbakar!
                    self.stun_timer = 20 # Panik kena api

        if is_aggressive and self.health > 0:
            dx = target_pos[0] - self.pos[0]
            dy = target_pos[1] - self.pos[1]
            dist = math.hypot(dx, dy)
            
            if dist > 10:
                self.pos[0] += (dx / dist) * self.speed
                self.pos[1] += (dy / dist) * self.speed
                self.state = 'walk'
                if abs(dx) > abs(dy): self.direction = 'right' if dx > 0 else 'left'
                else: self.direction = 'down' if dy > 0 else 'up'
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
