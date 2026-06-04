import pygame
import math
import random
import time
from typing import List, Dict, Tuple, Optional
from src.core.minigame_manager import MiniGame

# =============================================================================
# CITY UNDER ATTACK: TACTICAL VISUAL OVERHAUL v4.0
# =============================================================================
# Featuring: Depth Shaded Skyscrapers, Blinking Roof Antennas, Detailed Window
# Glass, and Animated Breathing/Clawing Zombies with Tissue Details.
# =============================================================================

class PixelPalette:
    SKY_DEEP = (5, 5, 20)
    SKY_CHAOS = (30, 10, 50)
    CYAN_GLOW = (50, 220, 255)
    DEEP_NAVY = (15, 15, 45)
    NEON_ORANGE = (255, 150, 50)
    NEON_RED = (255, 50, 80)
    FIRE_GLOW = (255, 200, 50)
    GOLD = (255, 230, 100)
    BLOOD = (220, 30, 30)
    SMOKE = (60, 60, 75)
    SHELL = (180, 150, 20)
    EXPLOSION = [(255, 255, 200), (255, 200, 50), (255, 100, 0), (150, 50, 0)]

# =============================================================================
# VISUAL EFFECTS SYSTEM
# =============================================================================

class Particle:
    def __init__(self, x, y, color, size_range=(3, 7), vel_range=(-5, 5), gravity=0.15):
        self.pos = [x, y]
        self.vel = [random.uniform(*vel_range), random.uniform(-8, 2)]
        self.life = 1.0
        self.decay = random.uniform(0.01, 0.03)
        self.color = color
        self.size = random.randint(*size_range)
        self.gravity = gravity

    def update(self):
        self.pos[0] += self.vel[0]; self.pos[1] += self.vel[1]
        self.vel[1] += self.gravity; self.life -= self.decay
        return self.life > 0

    def draw(self, screen, offset=(0,0)):
        if self.life <= 0: return
        s = pygame.Surface((int(self.size), int(self.size)))
        s.set_alpha(int(self.life * 255)); s.fill(self.color)
        screen.blit(s, (self.pos[0] + offset[0], self.pos[1] + offset[1]))

class ExplosionParticle(Particle):
    def __init__(self, x, y):
        color = random.choice(PixelPalette.EXPLOSION)
        super().__init__(x, y, color, (5, 15), (-8, 8), gravity=0.05)
        self.vel[1] = random.uniform(-10, -3)

class ShellCasing:
    def __init__(self, x, y, side=1):
        self.pos = [x, y]
        self.vel = [random.uniform(5, 10) * side, random.uniform(-12, -7)]
        self.rot = 0
        self.rot_vel = random.randint(20, 40)
        self.gravity = 0.8

    def update(self):
        self.pos[0] += self.vel[0]; self.pos[1] += self.vel[1]
        self.vel[1] += self.gravity; self.rot += self.rot_vel
        return self.pos[1] < 650

    def draw(self, screen, offset=(0,0)):
        s = pygame.Surface((7, 3), pygame.SRCALPHA); s.fill(PixelPalette.SHELL)
        rotated = pygame.transform.rotate(s, self.rot)
        screen.blit(rotated, (self.pos[0] + offset[0], self.pos[1] + offset[1]))

# =============================================================================
# WEAPONRY SYSTEM
# =============================================================================

class WeaponType:
    PISTOL = {"name": "P-90 SILENCER", "ammo": 15, "reload": 60, "recoil": 10, "delay": 15, "damage": 100}
    RIFLE = {"name": "AR-15 TACTICAL", "ammo": 30, "reload": 100, "recoil": 20, "delay": 7, "damage": 150}
    SNIPER = {"name": "M82 BARRETT", "ammo": 5, "reload": 150, "recoil": 60, "delay": 50, "damage": 800}

class TacticalWeapon:
    def __init__(self, w_type=WeaponType.RIFLE):
        self.type = w_type
        self.ammo_max = w_type["ammo"]
        self.ammo = self.ammo_max
        self.is_reloading = False
        self.reload_timer = 0
        self.recoil_v = 0
        self.shot_delay = 0

    def update(self):
        if self.shot_delay > 0: self.shot_delay -= 1
        if self.recoil_v > 0: self.recoil_v *= 0.85
        if self.is_reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.ammo = self.ammo_max
                self.is_reloading = False

    def can_shoot(self):
        return self.ammo > 0 and not self.is_reloading and self.shot_delay <= 0

    def shoot(self):
        self.ammo -= 1
        self.recoil_v = self.type["recoil"]
        self.shot_delay = self.type["delay"]

    def reload(self):
        if not self.is_reloading and self.ammo < self.ammo_max:
            self.is_reloading = True
            self.reload_timer = self.type["reload"]

# =============================================================================
# ENEMY & WORLD SYSTEM
# =============================================================================

class ZombieType:
    NORMAL = {"hp": 100, "color": (50, 110, 50), "speed": 1, "scale": 1.8}
    FAST = {"hp": 60, "color": (180, 40, 40), "speed": 2.2, "scale": 1.4}
    TANK = {"hp": 1200, "color": (30, 60, 30), "speed": 0.4, "scale": 4.0} # GIGA ZOMBIE (Reduced scale to prevent overlapping)

class MidnightSkyscraper:
    def __init__(self, x, w, h, depth):
        self.x, self.w, self.h, self.depth = x, w, h, depth
        self.win_grid = []
        self.has_antenna = random.random() > 0.5
        self.antenna_h = random.randint(30, 60)
        self._init_windows()

    def _init_windows(self):
        r_gap, c_gap = 40, 45
        for y in range(45, self.h - 60, r_gap):
            for x in range(25, self.w - 30, c_gap):
                is_lit = random.random() > 0.85
                lit_color = random.choice([(255, 230, 150), (200, 220, 255), (255, 180, 100)]) if is_lit else None
                # Add random offset to window positions to make layout look organic/randomized
                rx = x + random.randint(-4, 4)
                ry = y + random.randint(-4, 4)
                self.win_grid.append({'pos': (rx, ry), 'zombie': None, 'lit_color': lit_color})

    def draw(self, screen, off_x, shake=(0,0)):
        px, ty = int(self.x - off_x * self.depth) + shake[0], int(600 - self.h) + shake[1]
        
        # Base building silhouette color (varies by depth for realistic atmospheric perspective)
        # Closer buildings are darker; further buildings blend into the foggy purple sky
        fog_factor = min(1.0, max(0.0, (self.depth - 0.1) / 0.8))
        bg_sky = PixelPalette.SKY_CHAOS
        building_base_color = (
            int(PixelPalette.DEEP_NAVY[0] + (bg_sky[0] - PixelPalette.DEEP_NAVY[0]) * fog_factor * 0.4),
            int(PixelPalette.DEEP_NAVY[1] + (bg_sky[1] - PixelPalette.DEEP_NAVY[1]) * fog_factor * 0.4),
            int(PixelPalette.DEEP_NAVY[2] + (bg_sky[2] - PixelPalette.DEEP_NAVY[2]) * fog_factor * 0.4)
        )
        
        pygame.draw.rect(screen, building_base_color, (px, ty, self.w, self.h))
        
        # Draw vertical structural column textures
        col_color = (max(0, building_base_color[0] - 8), max(0, building_base_color[1] - 8), max(0, building_base_color[2] - 12))
        for cx in range(px + 8, px + self.w - 8, 22):
            pygame.draw.rect(screen, col_color, (cx, ty, 4, self.h))
            
        # Draw horizontal floor beams
        for cy in range(ty + 25, ty + self.h - 40, 18):
            pygame.draw.rect(screen, col_color, (px, cy, self.w, 1))

        # Static Cracks for post-apocalyptic atmosphere
        random.seed(self.x)
        if random.random() > 0.3:
            crack_x = px + random.randint(15, self.w - 20)
            crack_y = ty + random.randint(40, self.h - 80)
            pygame.draw.line(screen, (5, 5, 10), (crack_x, crack_y), (crack_x + 8, crack_y + 16), 1)
            pygame.draw.line(screen, (5, 5, 10), (crack_x + 8, crack_y + 16), (crack_x + 4, crack_y + 26), 1)

        # Draw Antenna with blinking light on top of some buildings
        if self.has_antenna:
            ax = px + self.w // 2
            ay = ty - self.antenna_h
            pygame.draw.line(screen, col_color, (ax, ty), (ax, ay), 2)
            # Blinking red warning beacon
            if pygame.time.get_ticks() % 1000 < 500:
                pygame.draw.circle(screen, (255, 40, 40), (ax, ay), 4)

        # Windows
        for win in self.win_grid:
            wx, wy = px + win['pos'][0], ty + win['pos'][1]
            
            # Window dimensions
            ww, wh = 8, 12
            
            if win['zombie']:
                # Draw dark window frame background first
                pygame.draw.rect(screen, (10, 10, 15), (wx - ww//2, wy - wh, ww, wh))
                pygame.draw.rect(screen, (35, 35, 45), (wx - ww//2, wy - wh, ww, wh), 1)
                
                # Retrieve zombie details
                z = win['zombie']
                s = z["scale"]
                rw, rh = int(12 * s), int(15 * s)
                
                # Creepy animated swaying and bobbing to make them look alive
                tick = pygame.time.get_ticks()
                sway_x = math.sin(tick * 0.006 + wx) * 1.5 * s
                bob_y = math.cos(tick * 0.008 + wy) * 0.8 * s
                
                # Creepy glow effect surrounding the zombie
                glow_surf = pygame.Surface((rw + 12, rh + 12), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (220, 30, 30, 45), (6, 6, rw, rh), border_radius=max(1, int(3*s)))
                screen.blit(glow_surf, (wx + sway_x - rw//2 - 6, wy + bob_y - rh - 6))
                
                # Zombie Body (Shirt/Tattered Clothes)
                shirt_color = (60, 40, 45) if z["color"][0] > 100 else (35, 45, 35)
                pygame.draw.rect(screen, shirt_color, (wx + sway_x - rw//2, wy + bob_y - rh//2, rw, rh//2), border_radius=max(1, int(2*s)))
                
                # Zombie Skin (Head & Body structure)
                head_r = max(2, int(4 * s))
                head_y = wy + bob_y - rh + head_r
                pygame.draw.circle(screen, z["color"], (wx + sway_x, head_y), head_r)
                
                # Brain exposure (Pink/red spot on one side of head)
                pygame.draw.circle(screen, (220, 90, 120), (wx + sway_x - int(1.5*s), head_y - int(1.5*s)), max(1, int(1.5*s)))
                
                # Glowing Eyes (flashing occasionally)
                eye_c = (255, 0, 0) if random.random() > 0.05 else (255, 255, 100)
                eye_y = head_y - max(1, int(1 * s))
                eye_w = max(1, int(1.2 * s))
                pygame.draw.circle(screen, eye_c, (wx + sway_x - max(1, int(1.5*s)), eye_y), eye_w)
                pygame.draw.circle(screen, eye_c, (wx + sway_x + max(1, int(1.5*s)), eye_y), eye_w)
                
                # Creepy open mouth (screaming face)
                mouth_y = head_y + max(1, int(1.5 * s))
                pygame.draw.rect(screen, (5, 5, 5), (wx + sway_x - max(1, int(1*s)), mouth_y, max(1, int(2*s)), max(1, int(1.5*s))))
                
                # Little teeth inside screaming mouth
                pygame.draw.rect(screen, (255, 255, 255), (wx + sway_x - max(1, int(0.5*s)), mouth_y, max(1, int(1*s)), max(1, int(0.5*s))))
                
                # Tattered arms reaching out of windows (clawing animation)
                wave_l = math.sin(tick * 0.01 + wx) * 2.0 * s
                wave_r = math.cos(tick * 0.01 + wx) * 2.0 * s
                pygame.draw.line(screen, z["color"], (wx + sway_x - rw//3, wy + bob_y - rh//2), (wx + sway_x - rw//2 - max(1, int(2*s)), wy + bob_y - rh//2 - max(1, int(4*s)) + wave_l), max(1, int(1.5*s)))
                pygame.draw.line(screen, z["color"], (wx + sway_x + rw//3, wy + bob_y - rh//2), (wx + sway_x + rw//2 + max(1, int(2*s)), wy + bob_y - rh//2 - max(1, int(4*s)) + wave_r), max(1, int(1.5*s)))
            else:
                # If window is lit, draw warm glow, otherwise draw dark window glass
                if win['lit_color']:
                    pygame.draw.rect(screen, win['lit_color'], (wx - ww//2, wy - wh, ww, wh), border_radius=1)
                    pygame.draw.rect(screen, (40, 45, 60), (wx - ww//2, wy - wh, ww, wh), 1)
                    pygame.draw.line(screen, (30, 30, 40), (wx, wy - wh), (wx, wy), 1)
                else:
                    pygame.draw.rect(screen, (12, 16, 25), (wx - ww//2, wy - wh, ww, wh), border_radius=1)
                    pygame.draw.rect(screen, (25, 30, 45), (wx - ww//2, wy - wh, ww, wh), 1)

# =============================================================================
# MAIN MINIGAME CLASS
# =============================================================================

class ShootingRangeUltimate(MiniGame):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        self.weapons = [TacticalWeapon(WeaponType.PISTOL), TacticalWeapon(WeaponType.RIFLE), TacticalWeapon(WeaponType.SNIPER)]
        self.w_idx = 1
        self.weapon = self.weapons[self.w_idx]
        
        self.skyscrapers = []
        self._init_world()
        self.crosshair = [400, 300]
        self.score, self.base_hp, self.timer = 0, 100, 900.0 # Timer increased to 15 minutes
        self.particles, self.shells = [], []
        self.screen_shake = 0
        self.muzzle_flash = 0
        self.spawn_rate = 40
        self.spawn_counter = 0

        # Load shoot sound
        self.shoot_sound = None
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except Exception as e:
                print("Failed to initialize pygame.mixer:", e)
        if pygame.mixer.get_init():
            try:
                self.shoot_sound = pygame.mixer.Sound('/home/abuyyy/suarapistol.mp3')
            except Exception as e:
                print("Failed to load shoot sound:", e)

    def _init_world(self):
        for i in range(15):
            d = 0.1 + (i * 0.05)
            self.skyscrapers.append(MidnightSkyscraper(i*220 - 500, random.randint(120, 220), random.randint(350, 850), d))

    def update(self, dt):
        self.timer -= (1/60.0) * dt
        # Win condition: score >= 5000. No more exit on city integrity <= 0.
        if self.timer <= 0 or self.score >= 5000:
            self.exit_game({'score': self.score})

        self.weapon.update()
        self.screen_shake = max(0, self.screen_shake - 3)
        self.muzzle_flash = max(0, self.muzzle_flash - 1)
        
        # Spawning
        self.spawn_counter += 1
        if self.spawn_counter >= self.spawn_rate:
            self._spawn_zombie()
            self.spawn_counter = 0
            self.spawn_rate = max(12, self.spawn_rate - 0.2)

        # Base Defense Logic (City integrity loss is disabled per request)
        for b in self.skyscrapers:
            for w in b.win_grid:
                if w['zombie']:
                    w['timer'] -= 1
                    if w['timer'] <= 0:
                        w['zombie'] = None
                        # City integrity no longer decreases
                        self.screen_shake = 20

        self.particles = [p for p in self.particles if p.update()]
        self.shells = [s for s in self.shells if s.update()]

    def _spawn_zombie(self):
        # Calculate current scroll offset based on crosshair x
        ox = (self.crosshair[0] - 400) * 0.4
        
        # Gather all empty windows on VISIBLE skyscrapers to prevent off-screen spawning
        empty_spots = []
        for b in self.skyscrapers:
            px = int(b.x - ox * b.depth)
            # Check if building is horizontally visible on the screen (with margins)
            if px + b.w >= -50 and px <= 850:
                for w in b.win_grid:
                    if not w['zombie']:
                        empty_spots.append((b, w))
                        
        if empty_spots:
            b, w = random.choice(empty_spots)
            z_type = random.choices([ZombieType.NORMAL, ZombieType.FAST, ZombieType.TANK], weights=[50, 35, 15])[0]
            w['zombie'] = z_type.copy()
            w['timer'] = int(240 / z_type["speed"])
            w['is_giga'] = z_type["scale"] > 2.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION: self.crosshair = list(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: self._handle_shoot()
            elif event.button == 4: self._switch_weapon(-1)
            elif event.button == 5: self._switch_weapon(1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: self.weapon.reload()
            if event.key in [pygame.K_q, pygame.K_TAB]: self._switch_weapon(1)

    def _handle_shoot(self):
        if self.weapon.can_shoot():
            self.weapon.shoot()
            if self.shoot_sound:
                self.shoot_sound.play()
            self.screen_shake = self.weapon.type["recoil"] // 2
            self.muzzle_flash = 6
            # Fire at muzzle
            for _ in range(15): self.particles.append(ExplosionParticle(400, 580))
            self.shells.append(ShellCasing(420, 580))
            self._check_hit()
        elif self.weapon.ammo <= 0: self.weapon.reload()

    def _switch_weapon(self, delta):
        self.w_idx = (self.w_idx + delta) % len(self.weapons)
        self.weapon = self.weapons[self.w_idx]

    def _check_hit(self):
        ox = (self.crosshair[0] - 400) * 0.4
        hit = False
        for b in sorted(self.skyscrapers, key=lambda x: x.depth, reverse=True):
            px, ty = int(b.x - ox * b.depth), int(600 - b.h)
            for w in b.win_grid:
                if w['zombie']:
                    wx, wy = px + w['pos'][0], ty + w['pos'][1]
                    s = w['zombie']['scale']
                    area_x = 22 * s
                    area_y_up = 25 * s
                    area_y_down = 10 * s
                    
                    # Direct check on zombie's actual hitbox boundaries
                    if (wx - area_x <= self.crosshair[0] <= wx + area_x) and \
                       (wy - area_y_up <= self.crosshair[1] <= wy + area_y_down):
                        w['zombie']["hp"] -= self.weapon.type["damage"]
                        if w['zombie']["hp"] <= 0:
                            w['zombie'] = None
                            self.score += 1000 if s > 2 else 500
                            self._create_explosion(self.crosshair[0], self.crosshair[1], s)
                        hit = True
                        break
            if hit:
                break

    def _create_explosion(self, x, y, scale=1.0):
        count = int(40 * scale)
        for _ in range(count): self.particles.append(ExplosionParticle(x, y))
        for _ in range(count//2): self.particles.append(Particle(x, y, PixelPalette.BLOOD, (5, 12)))

    def draw(self):
        shk = (random.randint(-self.screen_shake, self.screen_shake), random.randint(-self.screen_shake, self.screen_shake))
        ox = (self.crosshair[0] - 400) * 0.4
        
        # Background
        for y in range(0, 600, 8):
            c = [PixelPalette.SKY_DEEP[i] + (PixelPalette.SKY_CHAOS[i]-PixelPalette.SKY_DEEP[i])*(y/600) for i in range(3)]
            pygame.draw.rect(self.screen, c, (0, y, 800, 8))

        for b in sorted(self.skyscrapers, key=lambda x: x.depth): b.draw(self.screen, ox, shk)
        for p in self.particles: p.draw(self.screen, shk)
        for s in self.shells: s.draw(self.screen, shk)

        # WATCHTOWER RAILING (Character Location)
        self._draw_watchtower(shk)

        # MUZZLE FLASH
        if self.muzzle_flash > 0:
            f_s = pygame.Surface((800, 600), pygame.SRCALPHA)
            pygame.draw.circle(f_s, (255, 180, 50, 180), (400, 600), 250 + random.randint(0, 80))
            self.screen.blit(f_s, (0, 0), special_flags=pygame.BLEND_ADD)
            pygame.draw.line(self.screen, (255, 255, 150), (400, 600), self.crosshair, self.muzzle_flash * 3)

        self._draw_weapon_silhouette(shk)
        self._draw_hud()
        self._draw_crosshair()

    def _draw_watchtower(self, shk):
        # Concrete balcony floor and railing
        color = (20, 20, 30)
        pygame.draw.rect(self.screen, color, (0, 520 + shk[1], 800, 80)) # Floor
        pygame.draw.rect(self.screen, (40, 40, 50), (0, 520 + shk[1], 800, 10)) # Top Edge
        # Pillars
        for x in [100, 300, 500, 700]:
            pygame.draw.rect(self.screen, (30, 30, 40), (x, 480 + shk[1], 40, 40))

    def _draw_weapon_silhouette(self, shk):
        cx, cy = self.crosshair
        # Weapon sways slightly toward crosshair
        sway_x = (cx - 400) * 0.08
        sway_y = (cy - 300) * 0.05
        
        # Draw Weapon (Tactical Silhouette)
        w_color = (10, 10, 15)
        # Barrel/Body
        pygame.draw.rect(self.screen, w_color, (370 + sway_x + shk[0], 480 + sway_y + shk[1], 60, 150), border_radius=5)
        # Scope
        pygame.draw.rect(self.screen, (15, 15, 20), (385 + sway_x + shk[0], 460 + sway_y + shk[1], 30, 30), border_radius=3)
        # Tactical light glow on weapon (very subtle)
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.circle(self.screen, (50, 150, 255, 50), (375 + int(sway_x), 500 + int(sway_y)), 5)

    def _draw_hud(self):
        pygame.draw.rect(self.screen, (5, 5, 15), (0, 0, 800, 120))
        pygame.draw.line(self.screen, (255, 0, 0), (0, 120), (800, 120), 4)
        
        f = pygame.font.SysFont("monospace", 22, bold=True)
        self.screen.blit(f.render(f"GUN: {self.weapon.type['name']}", True, PixelPalette.FIRE_GLOW), (20, 15))
        
        # Display formatted remaining time (MM:SS)
        minutes = max(0, int(self.timer) // 60)
        seconds = max(0, int(self.timer) % 60)
        time_str = f"TIME: {minutes:02d}:{seconds:02d}"
        self.screen.blit(f.render(time_str, True, PixelPalette.GOLD), (320, 15))
        
        # Display target score of 5000 (We use self.score as score variable from MiniGame base class)
        self.screen.blit(f.render(f"INTEL: {self.score:04d}/05000", True, PixelPalette.CYAN_GLOW), (510, 15))
        
        # Ammo Reserve Bar (Clean layout, moved up as City Integrity is removed)
        aw = int((self.weapon.ammo / self.weapon.ammo_max) * 250)
        pygame.draw.rect(self.screen, (0, 40, 60), (20, 65, 250, 20))
        pygame.draw.rect(self.screen, PixelPalette.CYAN_GLOW, (20, 65, aw, 20))
        self.screen.blit(f.render("AMMO RESERVE", True, (200, 200, 200)), (280, 60))

    def _draw_crosshair(self):
        cx, cy = self.crosshair
        pygame.draw.circle(self.screen, (255, 255, 255), (int(cx), int(cy)), 30, 2)
        pygame.draw.line(self.screen, (255, 0, 0), (cx-40, cy), (cx+40, cy), 2)
        pygame.draw.line(self.screen, (255, 0, 0), (cx, cy-40), (cx, cy+40), 2)

class SystemLore: DATA = {f"NODE_{i}": f"SIGNAL_{random.randint(1,100)}" for i in range(2500)}
