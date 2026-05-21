import pygame
import math
import random
import time
import os
from src.core.spritesheet import Spritesheet

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================
MAP_SIZE = (4000, 3000)
TILE_SIZE = 256
PATH_COLOR = (139, 115, 85)
GRASS_COLOR_1 = (34, 139, 34)
GRASS_COLOR_2 = (30, 120, 30)

# =============================================================================
# VISUAL & PARTICLE CLASSES
# =============================================================================

class Particle:
    """Simple particle for fire or dust effects."""
    def __init__(self, x, y, color):
        self.pos = [x, y]
        self.vel = [random.uniform(-0.5, 0.5), random.uniform(-1, -2)]
        self.life = 1.0
        self.decay = random.uniform(0.01, 0.03)
        self.color = color

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.life -= self.decay
        return self.life > 0

    def draw(self, screen, camera):
        draw_pos = camera.apply(self.pos)
        size = int(self.life * 6)
        p_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(p_surf, (*self.color, int(self.life * 255)), (size, size), size)
        screen.blit(p_surf, (draw_pos[0]-size, draw_pos[1]-size))

class SanctuaryVisuals:
    @staticmethod
    def draw_shadow(screen, camera, pos, radius=12):
        draw_pos = camera.apply(pos)
        shadow_surf = pygame.Surface((radius * 4, radius * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 80), shadow_surf.get_rect())
        screen.blit(shadow_surf, (draw_pos[0] - radius*2, draw_pos[1] - radius))

    @staticmethod
    def draw_speech_bubble(screen, camera, pos, text, font):
        text_surf = font.render(text, True, (255, 255, 255))
        padding = 8
        bubble_rect = pygame.Rect(0, 0, text_surf.get_width() + padding*2, text_surf.get_height() + padding*2)
        draw_pos = camera.apply(pos)
        bubble_rect.centerx = draw_pos[0]
        bubble_rect.bottom = draw_pos[1] - 55
        
        pygame.draw.rect(screen, (30, 30, 30, 230), bubble_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 200, 150), bubble_rect, width=1, border_radius=10)
        pygame.draw.polygon(screen, (30, 30, 30), [(bubble_rect.centerx, bubble_rect.bottom + 10), (bubble_rect.centerx - 6, bubble_rect.bottom), (bubble_rect.centerx + 6, bubble_rect.bottom)])
        screen.blit(text_surf, (bubble_rect.x + padding, bubble_rect.y + padding))

# =============================================================================
# ENVIRONMENT OBJECTS
# =============================================================================

class SanctuaryObject:
    def __init__(self, name, pos, obj_type):
        self.name = name
        self.pos = pos
        self.type = obj_type
        self.particles = []
        
    def update(self):
        if self.type == "FIRE":
            if random.random() < 0.2:
                self.particles.append(Particle(self.pos[0], self.pos[1], (255, 150, 50)))
        
        for p in self.particles[:]:
            if not p.update():
                self.particles.remove(p)

    def draw(self, screen, camera, font=None):
        draw_pos = camera.apply(self.pos)
        if self.type == "FIRE":
            # Glow
            glow = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 150, 50, 50), (50, 50), 40 + random.randint(0, 5))
            screen.blit(glow, (draw_pos[0]-50, draw_pos[1]-50))
            # Base logs
            pygame.draw.rect(screen, (80, 50, 30), (draw_pos[0]-15, draw_pos[1]-5, 30, 10), border_radius=2)
            for p in self.particles: p.draw(screen, camera)
        elif self.type == "BENCH":
            pygame.draw.rect(screen, (100, 70, 40), (draw_pos[0]-30, draw_pos[1]-10, 60, 20), border_radius=3)
            pygame.draw.rect(screen, (60, 40, 20), (draw_pos[0]-30, draw_pos[1]-10, 60, 20), width=2, border_radius=3)

# =============================================================================
# POPULATION MANAGER (UNIVERSAL ASSET LOADER)
# =============================================================================

class SanctuaryPopulation:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.body_types = ["char_a_p1", "char_a_pONE1", "char_a_pONE2", "char_a_pONE3"]
        self.asset_cache = {}
        self._load_all_available_assets()

    def _load_all_available_assets(self):
        for b_type in self.body_types:
            type_path = os.path.join(self.base_dir, b_type)
            if not os.path.exists(type_path): continue
            
            body_file = f"{b_type}_0bas_humn_v00.png"
            body_path = os.path.join(type_path, body_file)
            if os.path.exists(body_path):
                self.asset_cache[f"{b_type}_base"] = Spritesheet(body_path, 8, 8, scale=1.6)
            
            outfit_dir = os.path.join(type_path, "1out")
            if os.path.exists(outfit_dir):
                for o_type in ["fstr", "pfpn", "boxr"]:
                    o_file = f"{b_type}_1out_{o_type}_v01.png"
                    o_path = os.path.join(outfit_dir, o_file)
                    if os.path.exists(o_path):
                        self.asset_cache[f"{b_type}_{o_type}"] = Spritesheet(o_path, 8, 8, scale=1.6)

    def generate_random_npc(self, role, name, pos):
        b_type = random.choice(list(self.body_types))
        if f"{b_type}_base" not in self.asset_cache: b_type = "char_a_p1" 
        base_sheet = self.asset_cache[f"{b_type}_base"]
        
        outfit_key = "boxr"
        if role == "Guard" or role == "Worker": outfit_key = "fstr"
        elif role in ["Merchant", "Elite"]: outfit_key = "pfpn"
        
        clothing_sheet = self.asset_cache.get(f"{b_type}_{outfit_key}")
        return AdvancedNPC(name, role, pos, base_sheet, clothing_sheet)

# =============================================================================
# NPC AI & LOGIC
# =============================================================================

class AdvancedNPC:
    def __init__(self, name, role, pos, base_sheet, clothing_sheet):
        self.name, self.role, self.pos = name, role, list(pos)
        self.base_sheet, self.clothing_sheet = base_sheet, clothing_sheet
        self.dir, self.frame, self.state = random.randint(0, 3), 0, "IDLE"
        self.target, self.timer = None, random.randint(100, 300)
        self.speed = 1.2 if role == "Child" else 0.8
        self.chatter, self.chatter_timer = None, 0
        self.is_panicked = False

    def update(self, player_pos, is_alarm_active):
        self.timer -= 1
        if is_alarm_active and not self.is_panicked:
            self.is_panicked = True; self.state = "RUN"
            self.target = [2000, 500] if self.role == "Guard" else [2000, 2800]
            self.speed *= 1.6

        if self.timer <= 0 and not self.is_panicked:
            self.state = "WALK" if self.state == "IDLE" else "IDLE"
            if self.state == "WALK": self.target = [random.randint(200, 3800), random.randint(200, 2800)]
            self.timer = random.randint(200, 500)

        if self.state in ["WALK", "RUN"] and self.target:
            dx, dy = self.target[0] - self.pos[0], self.target[1] - self.pos[1]
            d = math.hypot(dx, dy)
            if d > 5:
                self.pos[0] += (dx/d) * self.speed; self.pos[1] += (dy/d) * self.speed
                if abs(dx) > abs(dy): self.dir = 2 if dx > 0 else 3
                else: self.dir = 0 if dy > 0 else 1
                if pygame.time.get_ticks() % 120 < 20: self.frame = (self.frame + 1) % 6
            else: self.state = "IDLE"; self.frame = 0

        dist_p = math.hypot(self.pos[0] - player_pos[0], self.pos[1] - player_pos[1])
        if dist_p < 120 and self.state == "IDLE":
            dx, dy = player_pos[0] - self.pos[0], player_pos[1] - self.pos[1]
            if abs(dx) > abs(dy): self.dir = 2 if dx > 0 else 3
            else: self.dir = 0 if dy > 0 else 1

        if self.chatter_timer > 0: self.chatter_timer -= 1
        elif random.random() < 0.0005:
            self.chatter = "Selamat datang!" if not self.is_panicked else "LARI!"
            self.chatter_timer = 150

    def draw(self, screen, camera, font):
        SanctuaryVisuals.draw_shadow(screen, camera, self.pos)
        draw_pos = camera.apply(self.pos)
        row = self.dir + (4 if self.state != "IDLE" else 0)
        screen.blit(self.base_sheet.get_frame(row, self.frame), (draw_pos[0]-16, draw_pos[1]-16))
        if self.clothing_sheet: screen.blit(self.clothing_sheet.get_frame(row, self.frame), (draw_pos[0]-16, draw_pos[1]-16))
        if self.chatter_timer > 0: SanctuaryVisuals.draw_speech_bubble(screen, camera, self.pos, self.chatter, font)

# =============================================================================
# MAIN MISSION LOGIC
# =============================================================================

from src.core.ai_backend import DialogueAI
from src.ui.text_input import TextInput

class Mission3Logic:
    def __init__(self, journal, dialogue):
        self.journal, self.dialogue = journal, dialogue
        self.phase = "ARRIVAL"
        
        # --- AI & Input Systems ---
        # NOTE: User should set GEMINI_API_KEY environment variable
        self.ai = DialogueAI() 
        self.text_input = TextInput(200, 400, 400)
        self.interacting_npc = None
        
        self.pop_manager = SanctuaryPopulation("FREE Mana Seed Character Base Demo 2.0")
        self.npcs, self.world_objects = [], []
        self._seed_sanctuary()
        self.font_name = pygame.font.SysFont("Arial", 12, bold=True)
        self.font_bubble = pygame.font.SysFont("Arial", 11)
        self.states = {"gate_report": False, "elder_met": False, "tasks_done": 0, "alarm_active": False, "last_key": False}

    def _seed_sanctuary(self):
        # ... (rest of _seed_sanctuary)
        self.npcs.append(self.pop_manager.generate_random_npc("Guard", "Kapten Jaka", (400, 300)))
        self.npcs.append(self.pop_manager.generate_random_npc("Elite", "Penatua Aris", (1200, 800)))
        for i in range(80):
            role = random.choice(["Worker", "Citizen", "Merchant", "Child"])
            self.npcs.append(self.pop_manager.generate_random_npc(role, f"{role} {i+1}", (random.randint(200, 3800), random.randint(200, 2800))))
        self.world_objects.append(SanctuaryObject("Main Fire", (2000, 1500), "FIRE"))
        self.world_objects.append(SanctuaryObject("West Fire", (800, 800), "FIRE"))
        for _ in range(15): self.world_objects.append(SanctuaryObject("Bench", (random.randint(500, 3500), random.randint(500, 2500)), "BENCH"))

    def update(self, player, items, keys, effects=None, events=None):
        # 1. Update Entities & Objects
        for npc in self.npcs: npc.update(player.pos, self.states["alarm_active"])
        for obj in self.world_objects: obj.update()
        
        # 2. Handle Text Input Events
        if events and self.text_input.active:
            for event in events:
                user_msg = self.text_input.handle_event(event)
                if user_msg and self.interacting_npc:
                    # Send to AI
                    self.ai.request_dialogue(self.interacting_npc.name, self.interacting_npc.role, user_msg)
                    self.dialogue.show(["..."], is_thinking=True)
                    self.text_input.active = False
            return # Don't process other updates while typing

        # 3. Check for AI Responses
        ai_resp = self.ai.get_latest_response()
        if ai_resp:
            self.dialogue.is_thinking = False # Reset thinking state
            self.dialogue.show([ai_resp])
            self.interacting_npc = None

        # 4. Interaction Detection
        enter = keys[pygame.K_RETURN]
        if not self.dialogue.active and not self.text_input.active:
            for npc in self.npcs:
                dist = math.hypot(player.pos[0] - npc.pos[0], player.pos[1] - npc.pos[1])
                if dist < 80 and enter and not self.states["last_key"]:
                    self.interacting_npc = npc
                    self.text_input.active = True
                    # Progression flags
                    if npc.name == "Kapten Jaka": self.states["gate_report"] = True
                    elif npc.name == "Penatua Aris": self.states["elder_met"] = True
        
        self.states["last_key"] = enter

    def draw_ground(self, screen, camera):
        cam_r = pygame.Rect(-camera.camera.x, -camera.camera.y, screen.get_width(), screen.get_height())
        for r in range(0, MAP_SIZE[1], TILE_SIZE):
            for c in range(0, MAP_SIZE[0], TILE_SIZE):
                rect = pygame.Rect(c, r, TILE_SIZE, TILE_SIZE)
                if rect.colliderect(cam_r):
                    d_pos = camera.apply((c, r))
                    color = GRASS_COLOR_1 if (r//TILE_SIZE + c//TILE_SIZE) % 2 == 0 else GRASS_COLOR_2
                    pygame.draw.rect(screen, color, (d_pos[0], d_pos[1], TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, PATH_COLOR, camera.apply(pygame.Rect(1900, 0, 200, MAP_SIZE[1])))
        pygame.draw.rect(screen, PATH_COLOR, camera.apply(pygame.Rect(0, 1400, MAP_SIZE[0], 200)))

    def draw_entities(self, screen, camera, player):
        entities = self.npcs + self.world_objects
        for ent in sorted(entities, key=lambda e: e.pos[1]):
            ent.draw(screen, camera, self.font_bubble)
            if hasattr(ent, 'name') and isinstance(ent, AdvancedNPC):
                d_p = camera.apply(ent.pos)
                screen.blit(self.font_name.render(ent.name, True, (255, 255, 255)), (d_p[0] - 20, d_p[1] - 45))
        
        # Draw Text Input Overlay
        if self.text_input.active:
            self.text_input.draw(screen)

    def get_status_text(self, player):
        return "DARURAT!" if self.states["alarm_active"] else "Jelajahi Sanctuary."

    def get_target_pos(self, player, items):
        return (400, 300) if not self.states["gate_report"] else (1200, 800)
