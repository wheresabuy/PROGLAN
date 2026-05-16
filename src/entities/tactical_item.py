import pygame
import math

class TacticalItem:
    def __init__(self, x, y, item_type, target_pos=None):
        self.pos = [x, y]
        self.item_type = item_type
        self.timer = 0
        self.active = True
        self.target_pos = target_pos # Untuk item yang dilempar
        self.speed = 8
        self.reached_target = False if target_pos else True

    def update(self):
        if not self.reached_target and self.target_pos:
            dx = self.target_pos[0] - self.pos[0]
            dy = self.target_pos[1] - self.pos[1]
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.pos = list(self.target_pos)
                self.reached_target = True
            else:
                self.pos[0] += (dx / dist) * self.speed
                self.pos[1] += (dy / dist) * self.speed

        self.timer += 1
        
        # Durasi item
        if self.item_type == "Molotov":
            if self.timer > 180: self.active = False # 3 detik api
        elif self.item_type == "Decoy":
            if self.timer > 600: self.active = False # 10 detik umpan
        elif self.item_type == "Taser":
            if self.timer > 10: self.active = False # Sekejap

    def draw(self, screen, camera):
        draw_pos = camera.apply(self.pos)
        if self.item_type == "Molotov" and self.reached_target:
            # Gambar api (lingkaran berkedip)
            color = (255, 100, 0) if self.timer % 10 < 5 else (255, 200, 0)
            pygame.draw.circle(screen, color, draw_pos, 50, 0)
        elif self.item_type == "Decoy":
            # Gambar gadget berkedip biru
            color = (0, 0, 255) if self.timer % 20 < 10 else (100, 100, 255)
            pygame.draw.circle(screen, color, draw_pos, 10, 0)
            # Gelombang suara
            pygame.draw.circle(screen, color, draw_pos, (self.timer % 40) * 2, 1)
        elif self.item_type == "Taser":
            # Efek setrum petir
            pygame.draw.line(screen, (255, 255, 255), draw_pos, (draw_pos[0]+10, draw_pos[1]-10), 2)
