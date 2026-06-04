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

# =============================================================================
# MISSION 3: THE SANCTUARY - CORE DEFENSE & EVOLUTION
# =============================================================================
# This file handles the complex logic for the final sanctuary mission,
# including advanced NPC AI, resource management, and the city-wide alarm system.
# =============================================================================

import pygame
import math
import random
import time
import os
from src.core.spritesheet import Spritesheet
from src.core.ai_backend import DialogueAI
from src.ui.text_input import TextInput

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================
MAP_SIZE = (5000, 4000) # Expanded Map
TILE_SIZE = 256
PATH_COLOR = (120, 100, 70)
GRASS_COLOR_1 = (30, 110, 30)
GRASS_COLOR_2 = (25, 100, 25)
WALL_COLOR = (60, 60, 60)

# =============================================================================
# VISUAL & PARTICLE CLASSES (EXPANDED)
# =============================================================================

class Particle:
    def __init__(self, x, y, color, vel=None, life_decay=None):
        self.pos = [x, y]
        self.vel = vel or [random.uniform(-0.8, 0.8), random.uniform(-1.5, -3)]
        self.life = 1.0
        self.decay = life_decay or random.uniform(0.005, 0.02)
        self.color = color

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.life -= self.decay
        return self.life > 0

    def draw(self, screen, camera):
        draw_pos = camera.apply(self.pos)
        size = int(self.life * 8)
        if size < 1: return
        p_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        alpha = int(self.life * 255)
        pygame.draw.circle(p_surf, (*self.color, alpha), (size, size), size)
        screen.blit(p_surf, (draw_pos[0]-size, draw_pos[1]-size))

class WeatherSystem:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.rain_particles = []
        self.fog_alpha = 0
        self.is_raining = False

    def update(self):
        if self.is_raining:
            if len(self.rain_particles) < 100:
                self.rain_particles.append([random.randint(0, self.width), 0, random.uniform(10, 15)])
            for p in self.rain_particles:
                p[1] += p[2]
            self.rain_particles = [p for p in self.rain_particles if p[1] < self.height]

    def draw(self, screen):
        if self.is_raining:
            for p in self.rain_particles:
                pygame.draw.line(screen, (100, 100, 255, 150), (p[0], p[1]), (p[0]-2, p[1]+10), 1)
        if self.fog_alpha > 0:
            fog_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            fog_surf.fill((100, 100, 120, self.fog_alpha))
            screen.blit(fog_surf, (0, 0))

# =============================================================================
# ADVANCED NPC & AI SYSTEMS
# =============================================================================

class NPCBehavior:
    IDLE = "IDLE"
    WALK = "WALK"
    PANIC = "PANIC"
    GUARD = "GUARD"
    TALK = "TALK"
    SLEEP = "SLEEP"

class AdvancedNPC:
    def __init__(self, name, role, pos, base_sheet, clothing_sheet=None):
        self.name, self.role, self.pos = name, role, list(pos)
        self.base_sheet, self.clothing_sheet = base_sheet, clothing_sheet
        self.dir, self.frame, self.state = random.randint(0, 3), 0, NPCBehavior.IDLE
        self.target, self.timer = None, random.randint(100, 300)
        self.speed = 1.0
        self.health = 100
        self.is_active = True
        self.chatter, self.chatter_timer = None, 0
        self.path_points = []
        self._init_role_speed()

    def _init_role_speed(self):
        speeds = {"Guard": 1.2, "Child": 1.5, "Elder": 0.6, "Worker": 0.9}
        self.speed = speeds.get(self.role, 1.0)

    def update(self, player_pos, world_state):
        if not self.is_active: return
        
        self.timer -= 1
        alarm = world_state.get("alarm_active", False)

        # State Transitions
        if alarm and self.state != NPCBehavior.PANIC:
            self.state = NPCBehavior.PANIC
            self.target = [2500, 3800] if self.role != "Guard" else [2500, 200]
            self.timer = 1000
        
        if self.timer <= 0 and not alarm:
            if self.role == "Guard":
                self.state = NPCBehavior.GUARD
                self.target = [self.pos[0] + random.randint(-200, 200), self.pos[1] + random.randint(-200, 200)]
            else:
                self.state = random.choice([NPCBehavior.WALK, NPCBehavior.IDLE])
                if self.state == NPCBehavior.WALK:
                    self.target = [random.randint(500, MAP_SIZE[0]-500), random.randint(500, MAP_SIZE[1]-500)]
            self.timer = random.randint(200, 600)

        # Movement Execution
        if self.target:
            dx, dy = self.target[0] - self.pos[0], self.target[1] - self.pos[1]
            dist = math.hypot(dx, dy)
            if dist > 5:
                mv_speed = self.speed * (2.0 if self.state == NPCBehavior.PANIC else 1.0)
                self.pos[0] += (dx/dist) * mv_speed
                self.pos[1] += (dy/dist) * mv_speed
                # Animation logic
                if abs(dx) > abs(dy): self.dir = 2 if dx > 0 else 3
                else: self.dir = 0 if dy > 0 else 1
                if pygame.time.get_ticks() % 100 < 20: self.frame = (self.frame + 1) % 6
            else:
                self.target = None
                if self.state != NPCBehavior.PANIC: self.state = NPCBehavior.IDLE

        # Interaction Chatter
        if self.chatter_timer > 0: self.chatter_timer -= 1
        else:
            if random.random() < 0.0002:
                self.chatter = self._get_random_line(alarm)
                self.chatter_timer = 180

    def _get_random_line(self, alarm):
        if alarm: return random.choice(["LARI KE BUNKER!", "DI MANA ANAKKU?", "TOLONG!", "AMBIL SENJATA!"])
        lines = {
            "Guard": ["Area aman.", "Tetap waspada.", "Lapor, tidak ada gerakan."],
            "Worker": ["Pekerjaan ini tak pernah usai.", "Butuh lebih banyak kayu.", "Generator berisik sekali."],
            "Child": ["Main yuk!", "Aku lapar...", "Lihat burung itu!"],
            "Elder": ["Dunia sudah banyak berubah.", "Dengarkan suara alam.", "Hati-hati di luar."]
        }
        return random.choice(lines.get(self.role, ["Halo."]))

    def draw(self, screen, camera, font):
        draw_pos = camera.apply(self.pos)
        # Shadow
        s_surf = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(s_surf, (0, 0, 0, 70), (0, 0, 40, 20))
        screen.blit(s_surf, (draw_pos[0]-20, draw_pos[1]-5))
        
        # Sprite
        row = self.dir + (4 if self.state in [NPCBehavior.WALK, NPCBehavior.PANIC] else 0)
        img = self.base_sheet.get_frame(row, self.frame)
        screen.blit(img, (draw_pos[0]-16, draw_pos[1]-24))
        if self.clothing_sheet:
            screen.blit(self.clothing_sheet.get_frame(row, self.frame), (draw_pos[0]-16, draw_pos[1]-24))
        
        # Speech Bubble
        if self.chatter_timer > 0:
            self._draw_bubble(screen, camera, draw_pos, font)

    def _draw_bubble(self, screen, camera, draw_pos, font):
        txt = font.render(self.chatter, True, (255, 255, 255))
        rect = txt.get_rect(center=(draw_pos[0], draw_pos[1]-60))
        bg_rect = rect.inflate(15, 10)
        pygame.draw.rect(screen, (20, 20, 20, 200), bg_rect, border_radius=5)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect, width=1, border_radius=5)
        screen.blit(txt, rect)

# =============================================================================
# ENVIRONMENT & MISSION CONTROL
# =============================================================================

class Mission3Logic:
    def __init__(self, journal, dialogue):
        self.journal, self.dialogue = journal, dialogue
        self.phase = "EXPLORATION"
        self.states = {
            "elder_met": False, 
            "gate_report": False, 
            "alarm_active": False,
            "defenses_ready": 0,
            "resources": {"Wood": 0, "Metal": 0, "Power": 100},
            "last_key": False
        }
        
        # Sub-systems
        self.ai = DialogueAI()
        self.text_input = TextInput(200, 400, 400)
        self.weather = WeatherSystem(800, 600)
        self.pop_manager = SanctuaryPopulation("FREE Mana Seed Character Base Demo 2.0")
        
        self.npcs = []
        self.particles = []
        self.interacting_npc = None
        self._setup_world()
        self.font_main = pygame.font.SysFont("monospace", 14, bold=True)
        self.font_tiny = pygame.font.SysFont("monospace", 10)

    def _setup_world(self):
        # Key NPCs
        self.npcs.append(self.pop_manager.generate_random_npc("Guard", "Kapten Jaka", (2500, 400)))
        self.npcs.append(self.pop_manager.generate_random_npc("Elder", "Penatua Aris", (1000, 1000)))
        self.npcs.append(self.pop_manager.generate_random_npc("Elite", "Ilmuwan Sara", (4000, 2000)))
        
        # Ambient Population
        for i in range(50):
            role = random.choice(["Citizen", "Worker", "Child"])
            pos = (random.randint(200, MAP_SIZE[0]-200), random.randint(200, MAP_SIZE[1]-200))
            self.npcs.append(self.pop_manager.generate_random_npc(role, f"Warga {i+1}", pos))

    def update(self, player, items, keys, effects=None, events=None):
        self.weather.update()
        
        # 1. Update NPCs
        world_state = {"alarm_active": self.states["alarm_active"]}
        for npc in self.npcs: npc.update(player.pos, world_state)
        
        # 2. Particles
        if random.random() < 0.1:
            self.particles.append(Particle(2500, 500, (255, 100, 0))) # Signal fire
        self.particles = [p for p in self.particles if p.update()]

        # 3. AI Interaction Logic
        if events and self.text_input.active:
            for event in events:
                msg = self.text_input.handle_event(event)
                if msg and self.interacting_npc:
                    self.ai.request_dialogue(self.interacting_npc.name, self.interacting_npc.role, msg)
                    self.dialogue.show(["...Menganalisis respon..."], is_thinking=True)
                    self.text_input.active = False
            return

        ai_res = self.ai.get_latest_response()
        if ai_res:
            self.dialogue.is_thinking = False
            self.dialogue.show([ai_res])
            self.interacting_npc = None

        # 4. Input & Progression
        enter = keys[pygame.K_RETURN]
        if not self.dialogue.active and not self.text_input.active:
            for npc in self.npcs:
                dist = math.hypot(player.pos[0] - npc.pos[0], player.pos[1] - npc.pos[1])
                if dist < 80 and enter and not self.states["last_key"]:
                    self.interacting_npc = npc
                    self.text_input.active = True
                    # PROGRESSION LOGIC
                    if npc.name == "Kapten Jaka":
                        if self.states["elder_met"] and not self.states["alarm_active"]:
                            self.states["alarm_active"] = True
                            # Move player to Watchtower position immediately
                            player.pos = [2500, 300]
                            if effects: effects.trigger_flash(100) # White transition flash
                            self.journal.add_entry("PERTAHANAN DIMULAI: Selamatkan Sanctuary!")
                            return "START_SHOOTING"
                    elif npc.name == "Penatua Aris":
                        self.states["elder_met"] = True
        
        self.states["last_key"] = enter

    def draw_ground(self, screen, camera):
        # Optimized Tiled Rendering
        vw, vh = screen.get_size()
        cx, cy = -camera.camera.x, -camera.camera.y
        view_rect = pygame.Rect(cx, cy, vw, vh)
        
        for r in range(0, MAP_SIZE[1], TILE_SIZE):
            for c in range(0, MAP_SIZE[0], TILE_SIZE):
                t_rect = pygame.Rect(c, r, TILE_SIZE, TILE_SIZE)
                if t_rect.colliderect(view_rect):
                    draw_pos = camera.apply((c, r))
                    col = GRASS_COLOR_1 if (r//TILE_SIZE + c//TILE_SIZE) % 2 == 0 else GRASS_COLOR_2
                    pygame.draw.rect(screen, col, (*draw_pos, TILE_SIZE, TILE_SIZE))
        
        # Road Network
        pygame.draw.rect(screen, PATH_COLOR, camera.apply(pygame.Rect(2400, 0, 200, MAP_SIZE[1])))
        pygame.draw.rect(screen, PATH_COLOR, camera.apply(pygame.Rect(0, 1900, MAP_SIZE[0], 200)))

    def draw_entities(self, screen, camera, player):
        # Depth Sorting for realistic layering
        all_ents = self.npcs + self.particles
        sorted_ents = sorted(all_ents, key=lambda e: e.pos[1])
        
        for ent in sorted_ents:
            if isinstance(ent, Particle): ent.draw(screen, camera)
            else:
                ent.draw(screen, camera, self.font_tiny)
                # Label
                d_pos = camera.apply(ent.pos)
                name_tag = self.font_main.render(ent.name, True, (255, 255, 100) if ent.role == "Guard" else (255, 255, 255))
                screen.blit(name_tag, (d_pos[0]-25, d_pos[1]-45))

        if self.text_input.active:
            self.text_input.draw(screen)
        
        self.weather.draw(screen)

    def get_status_text(self, player):
        if self.states["alarm_active"]: return "STATUS: PERTAHANAN KOTA AKTIF! TEMBAK SEMUA ZOMBIE!"
        if not self.states["elder_met"]: return "OBJEKTIF: Cari Penatua Aris (Ikuti garis kuning ke Barat Laut)"
        return "OBJEKTIF: Bicara ke Kapten Jaka di gerbang untuk mulai pertempuran!"

    def get_target_pos(self, player, items):
        if not self.states["elder_met"]: return (1000, 1000)
        return (2500, 400)

# =============================================================================
# SANCTUARY POPULATION HELPER
# =============================================================================

class SanctuaryPopulation:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.body_types = ["char_a_p1", "char_a_pONE1", "char_a_pONE2", "char_a_pONE3"]
        self.cache = {}
        self._load()

    def _load(self):
        for b in self.body_types:
            p = os.path.join(self.base_dir, b, f"{b}_0bas_humn_v00.png")
            if os.path.exists(p): self.cache[f"{b}_base"] = Spritesheet(p, 8, 8, scale=2.0)
            
            # Load outfits if available
            out_p = os.path.join(self.base_dir, b, "1out", f"{b}_1out_fstr_v01.png")
            if os.path.exists(out_p): self.cache[f"{b}_outfit"] = Spritesheet(out_p, 8, 8, scale=2.0)

    def generate_random_npc(self, role, name, pos):
        b = random.choice(self.body_types)
        base = self.cache.get(f"{b}_base", self.cache.get("char_a_p1_base"))
        outfit = self.cache.get(f"{b}_outfit")
        return AdvancedNPC(name, role, pos, base, outfit)
