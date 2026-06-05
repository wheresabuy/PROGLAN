import pygame
from src.core.spritesheet import Spritesheet

class Player:
    def __init__(self, x, y):
        self.pos = [x, y]
        # Base skin
        self.sheet = Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v00.png", 8, 8, scale=2.0)
        
        # Clothing / Outfit
        self.clothing_sheet = Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v01.png", 8, 8, scale=2.0)
        self.clothing_active = True # Start with default clothes active
        
        # Hair (Default: Dapper Hair Brown/v08)
        self.hair_sheet = Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_dap1_v08.png", 8, 8, scale=2.0)
        
        # Hat (Default: None)
        self.hat_sheet = None
        
        self.direction = 'down'
        self.state = 'stand'
        self.current_col = 0
        self.frame_timer = 0
        self.anim_speed = 8
        self.health = 100
        self.injured = True
        self.speed_multiplier = 0.4
        self.adrenaline_timer = 0

    def update(self, keys, collision_mask=None, map_size=None):
        adrenaline_bonus = 2.0 if self.adrenaline_timer > 0 else 1.0
        if self.adrenaline_timer > 0: self.adrenaline_timer -= 1

        base_speed = (5.0 if keys[pygame.K_LSHIFT] else 3.0) * adrenaline_bonus
        speed = float(base_speed * self.speed_multiplier)
        moving = False

        if keys[pygame.K_RIGHT]: self.pos[0] += speed; self.direction = 'right'; moving = True
        if keys[pygame.K_LEFT]:  self.pos[0] -= speed; self.direction = 'left'; moving = True
        if keys[pygame.K_UP]:    self.pos[1] -= speed; self.direction = 'up'; moving = True
        if keys[pygame.K_DOWN]:  self.pos[1] += speed; self.direction = 'down'; moving = True

        # Clamp position to map size if provided
        if map_size:
            self.pos[0] = max(0, min(self.pos[0], map_size[0] - 32))
            self.pos[1] = max(0, min(self.pos[1], map_size[1] - 32))

        if keys[pygame.K_LSHIFT] and moving: self.state = 'run'
        elif moving: self.state = 'walk'
        else: self.state = 'stand'

        self.frame_timer += 1
        if self.frame_timer >= self.anim_speed:
            self.frame_timer = 0
            if self.state == 'stand': self.current_col = 0
            elif self.state == 'walk': self.current_col = (self.current_col + 1) % 6
            elif self.state == 'run': self.current_col = 6 + (self.current_col + 1) % 2

    def draw(self, screen, camera=None):
        dir_map = {'down': 0, 'up': 1, 'right': 2, 'left': 3}
        row = dir_map[self.direction] + (0 if self.state == 'stand' else 4)
        
        draw_pos = self.pos
        if camera:
            draw_pos = camera.apply(self.pos)
            
        # Layer 1: Skin Base
        screen.blit(self.sheet.get_frame(row, self.current_col), draw_pos)
        
        # Layer 2: Outfit / Clothing
        if self.clothing_active and self.clothing_sheet:
            screen.blit(self.clothing_sheet.get_frame(row, self.current_col), draw_pos)
            
        # Layer 3: Hair
        if self.hair_sheet:
            screen.blit(self.hair_sheet.get_frame(row, self.current_col), draw_pos)
            
        # Layer 4: Hat
        if self.hat_sheet:
            screen.blit(self.hat_sheet.get_frame(row, self.current_col), draw_pos)
