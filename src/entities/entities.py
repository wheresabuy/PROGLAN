import pygame, math, random
from src.core.engine import Spritesheet

class Player:
    def __init__(self, x, y):
        self.pos, self.direction, self.state, self.current_col = [x, y], 'down', 'stand', 0
        self.sheet = Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v00.png", 8, 8, scale=2.0)
        self.clothing_sheet = Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v01.png", 8, 8, scale=2.0)
        self.clothing_active, self.hair_sheet, self.hat_sheet = True, Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_dap1_v08.png", 8, 8, scale=2.0), None
        self.frame_timer, self.anim_speed, self.health, self.injured, self.speed_multiplier, self.adrenaline_timer = 0, 8, 100, True, 0.4, 0
    def update(self, keys, collision_mask=None, map_size=None):
        ad_bonus = 2.0 if self.adrenaline_timer > 0 else 1.0
        if self.adrenaline_timer > 0: self.adrenaline_timer -= 1
        speed = float((5.0 if keys[pygame.K_LSHIFT] else 3.0) * ad_bonus * self.speed_multiplier)
        moving = False
        if keys[pygame.K_RIGHT]: self.pos[0] += speed; self.direction = 'right'; moving = True
        if keys[pygame.K_LEFT]:  self.pos[0] -= speed; self.direction = 'left'; moving = True
        if keys[pygame.K_UP]:    self.pos[1] -= speed; self.direction = 'up'; moving = True
        if keys[pygame.K_DOWN]:  self.pos[1] += speed; self.direction = 'down'; moving = True
        if map_size:
            self.pos[0] = max(0, min(self.pos[0], map_size[0] - 32))
            self.pos[1] = max(0, min(self.pos[1], map_size[1] - 32))
        self.state = 'run' if (keys[pygame.K_LSHIFT] and moving) else 'walk' if moving else 'stand'
        self.frame_timer += 1
        if self.frame_timer >= self.anim_speed:
            self.frame_timer = 0
            self.current_col = 0 if self.state == 'stand' else (self.current_col + 1) % 6 if self.state == 'walk' else 6 + (self.current_col + 1) % 2
    def draw(self, screen, camera=None):
        row = {'down': 0, 'up': 1, 'right': 2, 'left': 3}[self.direction] + (0 if self.state == 'stand' else 4)
        dp = camera.apply(self.pos) if camera else self.pos
        screen.blit(self.sheet.get_frame(row, self.current_col), dp)
        if self.clothing_active and self.clothing_sheet: screen.blit(self.clothing_sheet.get_frame(row, self.current_col), dp)
        if self.hair_sheet: screen.blit(self.hair_sheet.get_frame(row, self.current_col), dp)
        if self.hat_sheet: screen.blit(self.hat_sheet.get_frame(row, self.current_col), dp)

class NPC:
    def __init__(self, name, x, y, role, base_path, outfit_path=None, hair_path=None):
        self.name, self.pos, self.role = name, [x, y], role
        self.sheet = Spritesheet(base_path, 8, 8, scale=2.0)
        self.outfit_sheet = Spritesheet(outfit_path, 8, 8, scale=2.0) if outfit_path else None
        self.hair_sheet = Spritesheet(hair_path, 8, 8, scale=2.0) if hair_path else None
        self.direction, self.state, self.current_col, self.frame_timer, self.anim_speed = 'down', 'stand', 0, 0, 8
        self.wander_timer, self.target_dir, self.speed, self.spawn_pos, self.max_wander_dist = random.randint(30, 90), [0, 0], 1.0, [x, y], 100
    def update(self, map_size=None):
        self.wander_timer -= 1
        if self.wander_timer <= 0:
            self.wander_timer = random.randint(60, 180)
            if random.random() < 0.5:
                self.state, self.target_dir = 'stand', [0, 0]
            else:
                angle = random.uniform(0, 2 * math.pi)
                self.target_dir = [math.cos(angle), math.sin(angle)]
                self.state = 'walk'
                dx, dy = self.target_dir
                self.direction = ('right' if dx > 0 else 'left') if abs(dx) > abs(dy) else ('down' if dy > 0 else 'up')
        if self.state == 'walk':
            nx, ny = self.pos[0] + self.target_dir[0]*self.speed, self.pos[1] + self.target_dir[1]*self.speed
            if math.hypot(nx - self.spawn_pos[0], ny - self.spawn_pos[1]) < self.max_wander_dist:
                self.pos = [nx, ny]
            else:
                self.state, self.target_dir, self.wander_timer = 'stand', [0, 0], 15
        if map_size:
            self.pos[0] = max(0, min(self.pos[0], map_size[0] - 32))
            self.pos[1] = max(0, min(self.pos[1], map_size[1] - 32))
        self.frame_timer += 1
        if self.frame_timer >= self.anim_speed:
            self.frame_timer = 0
            self.current_col = 0 if self.state == 'stand' else (self.current_col + 1) % 6
    def draw(self, screen, camera=None):
        row = {'down': 0, 'up': 1, 'right': 2, 'left': 3}[self.direction] + (0 if self.state == 'stand' else 4)
        dp = camera.apply(self.pos) if camera else self.pos
        screen.blit(self.sheet.get_frame(row, self.current_col), dp)
        if self.outfit_sheet: screen.blit(self.outfit_sheet.get_frame(row, self.current_col), dp)
        if self.hair_sheet: screen.blit(self.hair_sheet.get_frame(row, self.current_col), dp)

class ZombieNPC:
    def __init__(self, x, y):
        self.pos, self.sheet = [x, y], Spritesheet("assets/enemies/zombie_new.png", 8, 8, scale=2.0)
        self.direction, self.state, self.current_col, self.frame_timer, self.anim_speed, self.speed, self.stun_timer, self.health = 'down', 'stand', 0, 0, 10, 2.5, 0, 100
    def update(self, player_pos, player_state, tactical_items=[]):
        if self.stun_timer > 0:
            self.stun_timer -= 1; self.state = 'stand'; return
        t_pos, agg = player_pos, (player_state == 'run')
        for item in tactical_items:
            if item.item_type == "Decoy" and item.active and item.reached_target and math.hypot(item.pos[0] - self.pos[0], item.pos[1] - self.pos[1]) < 400:
                t_pos, agg = item.pos, True; break
        for item in tactical_items:
            if item.item_type == "Molotov" and item.reached_target and item.active and math.hypot(item.pos[0] - self.pos[0], item.pos[1] - self.pos[1]) < 50:
                self.health -= 2; self.stun_timer = 20
        if agg and self.health > 0:
            dx, dy = t_pos[0] - self.pos[0], t_pos[1] - self.pos[1]
            dist = math.hypot(dx, dy)
            if dist > 10:
                self.pos[0] += (dx / dist) * self.speed
                self.pos[1] += (dy / dist) * self.speed
                self.state = 'walk'
                self.direction = ('right' if dx > 0 else 'left') if abs(dx) > abs(dy) else ('down' if dy > 0 else 'up')
            else: self.state = 'stand'
        else: self.state = 'stand'
        self.frame_timer += 1
        if self.frame_timer >= self.anim_speed:
            self.frame_timer = 0
            self.current_col = 0 if self.state == 'stand' else (self.current_col + 1) % 6
    def draw(self, screen, camera=None):
        row = {'down': 0, 'up': 1, 'right': 2, 'left': 3}[self.direction] + (0 if self.state == 'stand' else 4)
        dp = camera.apply(self.pos) if camera else self.pos
        screen.blit(self.sheet.get_frame(row, self.current_col), dp)

class Loot:
    def __init__(self, name, x, y, item_type, image=None, prompt=None):
        self.name, self.pos, self.item_type = name, (x, y), item_type
        self.prompt, self.collected, self.hover_offset = prompt or f"Tekan [ENTER] untuk ambil {name}", False, 0
        if image:
            if isinstance(image, str):
                try:
                    self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (64, 64))
                except:
                    self.image = pygame.Surface((40, 40)); self.image.fill((255, 0, 0))
            else: self.image = pygame.transform.scale(image, (64, 64))
        else:
            self.image = pygame.Surface((40, 40)); self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
    def check_interaction(self, player_pos):
        return math.hypot(self.pos[0] - player_pos[0], self.pos[1] - player_pos[1]) < 100
    def get_interaction_prompt(self): return self.prompt
    def draw(self, screen, player_pos, camera=None):
        if not self.collected:
            self.hover_offset = math.sin(pygame.time.get_ticks() * 0.005) * 10
            dp = camera.apply(self.pos) if camera else self.pos
            screen.blit(self.image, (dp[0], dp[1] + self.hover_offset))

class TacticalItem:
    def __init__(self, x, y, item_type, target_pos=None):
        self.pos, self.item_type, self.timer, self.active, self.target_pos, self.speed = [x, y], item_type, 0, True, target_pos, 8
        self.reached_target = False if target_pos else True
    def update(self):
        if not self.reached_target and self.target_pos:
            dx, dy = self.target_pos[0] - self.pos[0], self.target_pos[1] - self.pos[1]
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.pos, self.reached_target = list(self.target_pos), True
            else:
                self.pos[0] += (dx / dist) * self.speed
                self.pos[1] += (dy / dist) * self.speed
        self.timer += 1
        dur = {"Molotov": 180, "Decoy": 600, "Taser": 10}.get(self.item_type, 100)
        if self.timer > dur: self.active = False
    def draw(self, screen, camera):
        dp = camera.apply(self.pos)
        if self.item_type == "Molotov" and self.reached_target:
            pygame.draw.circle(screen, (255, 100, 0) if self.timer % 10 < 5 else (255, 200, 0), dp, 50)
        elif self.item_type == "Decoy":
            c = (0, 0, 255) if self.timer % 20 < 10 else (100, 100, 255)
            pygame.draw.circle(screen, c, dp, 10)
            pygame.draw.circle(screen, c, dp, (self.timer % 40) * 2, 1)
        elif self.item_type == "Taser":
            pygame.draw.line(screen, (255, 255, 255), dp, (dp[0]+10, dp[1]-10), 2)
