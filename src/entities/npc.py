import pygame
import random
import math
from src.core.spritesheet import Spritesheet

class NPC:
    def __init__(self, name, x, y, role, base_path, outfit_path=None, hair_path=None):
        self.name = name
        self.pos = [x, y]
        self.role = role
        
        # Load sheets
        self.sheet = Spritesheet(base_path, 8, 8, scale=2.0)
        self.outfit_sheet = Spritesheet(outfit_path, 8, 8, scale=2.0) if outfit_path else None
        self.hair_sheet = Spritesheet(hair_path, 8, 8, scale=2.0) if hair_path else None
        
        self.direction = 'down'
        self.state = 'stand'
        self.current_col = 0
        self.frame_timer = 0
        self.anim_speed = 8
        
        # Movement/Wandering AI variables
        self.wander_timer = random.randint(30, 90)
        self.target_dir = [0, 0]
        self.speed = 1.0
        
        # Spawn anchor (for keeping them in a certain area)
        self.spawn_pos = [x, y]
        self.max_wander_dist = 100 # Radius they can wander around their spawn anchor

    def update(self, map_size=None):
        # AI Logic: Wandering around spawn anchor
        self.wander_timer -= 1
        if self.wander_timer <= 0:
            self.wander_timer = random.randint(60, 180)
            if random.random() < 0.5:
                # Stand still
                self.state = 'stand'
                self.target_dir = [0, 0]
            else:
                # Pick a random direction
                angle = random.uniform(0, 2 * math.pi)
                self.target_dir = [math.cos(angle), math.sin(angle)]
                self.state = 'walk'
                
                # Determine animation direction facing
                dx, dy = self.target_dir
                if abs(dx) > abs(dy):
                    self.direction = 'right' if dx > 0 else 'left'
                else:
                    self.direction = 'down' if dy > 0 else 'up'

        # Apply movement
        if self.state == 'walk':
            # Calculate next position
            next_x = self.pos[0] + self.target_dir[0] * self.speed
            next_y = self.pos[1] + self.target_dir[1] * self.speed
            
            # Check anchor distance to stay within boundaries
            dist_to_anchor = math.hypot(next_x - self.spawn_pos[0], next_y - self.spawn_pos[1])
            if dist_to_anchor < self.max_wander_dist:
                self.pos[0] = next_x
                self.pos[1] = next_y
            else:
                # Turn back / stand still if too far
                self.state = 'stand'
                self.target_dir = [0, 0]
                self.wander_timer = 15

        # Clamp position to map size if provided
        if map_size:
            self.pos[0] = max(0, min(self.pos[0], map_size[0] - 32))
            self.pos[1] = max(0, min(self.pos[1], map_size[1] - 32))

        # Update Frame Animation (using same logic as player)
        self.frame_timer += 1
        if self.frame_timer >= self.anim_speed:
            self.frame_timer = 0
            if self.state == 'stand':
                self.current_col = 0
            elif self.state == 'walk':
                self.current_col = (self.current_col + 1) % 6

    def draw(self, screen, camera=None):
        dir_map = {'down': 0, 'up': 1, 'right': 2, 'left': 3}
        row = dir_map[self.direction] + (0 if self.state == 'stand' else 4)
        
        draw_pos = self.pos
        if camera:
            draw_pos = camera.apply(self.pos)
            
        # Draw base character
        screen.blit(self.sheet.get_frame(row, self.current_col), draw_pos)
        
        # Draw outfit
        if self.outfit_sheet:
            screen.blit(self.outfit_sheet.get_frame(row, self.current_col), draw_pos)
            
        # Draw hair
        if self.hair_sheet:
            screen.blit(self.hair_sheet.get_frame(row, self.current_col), draw_pos)
