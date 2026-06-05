import pygame
import math
import random
import time
from typing import List, Dict, Tuple, Optional
from src.core.minigame_manager import MiniGame
from src.core.spritesheet import Spritesheet

# =============================================================================
# CONSTANTS & ASSETS
# =============================================================================

class PixelPalette:
    GOLD = (255, 215, 0)
    CYAN_GLOW = (0, 255, 255)
    FIRE_GLOW = (255, 50, 50)
    BLOOD = (180, 0, 0)

# Placeholder classes to ensure compatibility with existing logic
class Particle:
    def __init__(self, x, y, color, size_range=(2, 8)):
        self.pos = [x, y]
        self.vel = [random.uniform(-3, 3), random.uniform(-3, 3)]
        self.color = color
        self.size = random.randint(*size_range)
        self.life = 1.0

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.life -= 0.02
        return self.life > 0

    def draw(self, screen, offset=(0,0)):
        pygame.draw.circle(screen, self.color, (int(self.pos[0] + offset[0]), int(self.pos[1] + offset[1])), int(self.size * self.life))

class WeaponType:
    RIFLE = {"name": "M4-A1 TACTICAL", "damage": 40, "ammo": 30, "recoil": 15, "delay": 5}

class TacticalWeapon:
    def __init__(self, w_type):
        self.type = w_type
        self.ammo_max = w_type["ammo"]
        self.ammo = self.ammo_max
        self.is_reloading = False
        self.reload_timer = 0
        self.shot_delay = 0

    def update(self):
        if self.shot_delay > 0: self.shot_delay -= 1
        if self.is_reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0:
                self.ammo = self.ammo_max
                self.is_reloading = False
    
    def can_shoot(self):
        return self.ammo > 0 and not self.is_reloading and self.shot_delay <= 0

    def shoot(self):
        self.ammo -= 1
        self.shot_delay = self.type["delay"]

    def reload(self):
        if not self.is_reloading and self.ammo < self.ammo_max:
            self.is_reloading = True
            self.reload_timer = 60

# =============================================================================
# MAIN MINIGAME CLASS
# =============================================================================

class ShootingRangeUltimate(MiniGame):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        self.width, self.height = 1280, 720
        self.crosshair = [self.width // 2, self.height // 2]
        self.score = 0
        self.timer = 90.0  # High-intensity initial timer
        self.kills = 0
        self.headshots = 0
        self.bronze_earned = 0
        
        # Load custom background
        try:
            self.bg_img = pygame.image.load("assets/city_bg.png").convert()
            self.bg_img = pygame.transform.scale(self.bg_img, (self.width, self.height))
        except:
            self.bg_img = pygame.Surface((self.width, self.height))
            self.bg_img.fill((10, 10, 30))

        # Load weapon image
        try:
            self.weapon_img = pygame.image.load("assets/images/fps_pistol_tactical.png").convert_alpha()
            self.weapon_img = pygame.transform.scale(self.weapon_img, (500, 500))
        except Exception as e:
            print(f"Error loading weapon image: {e}")
            self.weapon_img = None

        # Load zombie sheet
        try:
            self.zombie_sheet = Spritesheet("assets/enemies/zombie_new.png", 8, 8, scale=2.5)
        except Exception as e:
            print(f"Error loading zombie sheet: {e}")
            self.zombie_sheet = None

        self.weapon = TacticalWeapon(WeaponType.RIFLE)
        self.targets = []
        self.particles = []
        self.floating_texts = []
        self.flash_timer = 0
        self.shake_v = 0

        self.font_header = pygame.font.SysFont("monospace", 36, bold=True)
        self.font_tactical = pygame.font.SysFont("monospace", 18, bold=True)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.crosshair = list(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.weapon.can_shoot():
                self.weapon.shoot()
                self.flash_timer = 5
                self.shake_v = self.weapon.type["recoil"]
                
                # Check for hits
                hit = False
                for t in self.targets:
                    # Calculate head position relative to target center
                    head_x = t['pos'][0]
                    head_y = t['pos'][1] - int(t['size'] * 0.5)
                    head_radius = int(t['size'] * 0.4)
                    
                    dist_head = math.hypot(self.crosshair[0] - head_x, self.crosshair[1] - head_y)
                    dist_body = math.hypot(self.crosshair[0] - t['pos'][0], self.crosshair[1] - t['pos'][1])
                    
                    if dist_head < head_radius or dist_body < t['size']:
                        is_headshot = dist_head < head_radius
                        damage = self.weapon.type["damage"]
                        if is_headshot:
                            damage *= 2
                            self.floating_texts.append({'text': f"CRITICAL! -{damage}", 'pos': [self.crosshair[0], self.crosshair[1] - 15], 'timer': 25, 'color': (255, 215, 0)})
                            for _ in range(15):
                                self.particles.append(Particle(head_x, head_y, (255, 50, 50), size_range=(3, 6)))
                        else:
                            self.floating_texts.append({'text': f"-{damage}", 'pos': [self.crosshair[0], self.crosshair[1] - 15], 'timer': 20, 'color': (220, 220, 220)})
                            for _ in range(8):
                                self.particles.append(Particle(t['pos'][0], t['pos'][1], PixelPalette.BLOOD, size_range=(2, 5)))
                        
                        t['hp'] -= damage
                        if t['hp'] <= 0:
                            self.kills += 1
                            
                            # Multiplier scales up with more kills
                            if self.kills < 10:
                                multiplier = 1.0
                            elif self.kills < 25:
                                multiplier = 1.5
                            elif self.kills < 50:
                                multiplier = 2.0
                            elif self.kills < 80:
                                multiplier = 3.0
                            else:
                                multiplier = 5.0
                                
                            if is_headshot:
                                self.headshots += 1
                                self.score += 150
                                base_bronze = 15
                                timer_add = 4.0
                                payout = int(base_bronze * multiplier)
                                self.bronze_earned += payout
                                self.timer = min(180.0, self.timer + timer_add)
                                
                                txt = f"+150 HEADSHOT KILL (+{payout}B)"
                                self.floating_texts.append({'text': txt, 'pos': [t['pos'][0] - 60, t['pos'][1] - 40], 'timer': 45, 'color': (255, 215, 0)})
                                self.floating_texts.append({'text': f"+{timer_add:.1f}s TIME", 'pos': [t['pos'][0] + 10, t['pos'][1] - 65], 'timer': 30, 'color': (0, 255, 255)})
                            else:
                                self.score += 100
                                base_bronze = 10
                                timer_add = 2.5
                                payout = int(base_bronze * multiplier)
                                self.bronze_earned += payout
                                self.timer = min(180.0, self.timer + timer_add)
                                
                                txt = f"+100 KILL (+{payout}B)"
                                self.floating_texts.append({'text': txt, 'pos': [t['pos'][0] - 40, t['pos'][1] - 40], 'timer': 35, 'color': (100, 255, 100)})
                                self.floating_texts.append({'text': f"+{timer_add:.1f}s TIME", 'pos': [t['pos'][0] + 10, t['pos'][1] - 65], 'timer': 30, 'color': (0, 255, 255)})
                            
                            t['active'] = False
                        hit = True
                        break
                
                if not hit:
                    for _ in range(3):
                        self.particles.append(Particle(self.crosshair[0], self.crosshair[1], (200, 200, 200), size_range=(2, 4)))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: self.weapon.reload()

    def update(self, dt):
        self.timer -= dt / 60.0
        if self.timer <= 0:
            self.exit_game({'score': self.score, 'bronze_earned': self.bronze_earned})
        
        self.weapon.update()
        if self.flash_timer > 0: self.flash_timer -= 1
        if self.shake_v > 0: self.shake_v *= 0.85
        
        # Dynamic Spawning limits & rates based on kills
        max_targets = 8 + min(7, self.kills // 5)
        spawn_chance = min(0.15, 0.05 + (self.kills / 100.0))
        
        if len(self.targets) < max_targets and random.random() < spawn_chance:
            anim_row = random.choice([0, 2, 3, 4, 6, 7])
            start_x = random.randint(100, self.width - 100)
            start_y = random.randint(200, self.height - 150)
            if anim_row == 6:
                start_x = 50
            elif anim_row == 7:
                start_x = self.width - 50
                
            self.targets.append({
                'pos': [start_x, start_y],
                'size': random.randint(35, 55),
                'hp': 100,
                'active': True,
                'timer': random.randint(240, 480),
                'anim_row': anim_row,
                'frame': random.randint(0, 5),
                'frame_timer': 0
            })
            
        # Update targets
        # Movement speed scales up as player kills more zombies
        speed_mult = 1.0 + (self.kills / 25.0)
        
        for t in self.targets:
            t['timer'] -= 1
            t['frame_timer'] += 1
            if t['frame_timer'] >= 8:
                t['frame_timer'] = 0
                t['frame'] = (t['frame'] + 1) % 6
            
            # Movement for walking zombies
            if t['anim_row'] == 4:
                t['pos'][1] += 0.8 * speed_mult
            elif t['anim_row'] == 6:
                t['pos'][0] += 1.2 * speed_mult
            elif t['anim_row'] == 7:
                t['pos'][0] -= 1.2 * speed_mult
                
            if t['anim_row'] == 6 and t['pos'][0] > self.width - 50:
                t['anim_row'] = 7
            elif t['anim_row'] == 7 and t['pos'][0] < 50:
                t['anim_row'] = 6
                
        self.targets = [t for t in self.targets if t['active'] and t['timer'] > 0 and t['pos'][1] < self.height - 50]
        self.particles = [p for p in self.particles if p.update()]
        
        # Update floating texts
        for ft in self.floating_texts:
            ft['pos'][1] -= 0.8
            ft['timer'] -= 1
        self.floating_texts = [ft for ft in self.floating_texts if ft['timer'] > 0]

        # Aim-Assist / Auto-Lock (snaps to the closest zombie's head)
        closest_target = None
        min_dist = 90.0  # lock-on threshold in pixels
        for t in self.targets:
            head_x = t['pos'][0]
            head_y = t['pos'][1] - int(t['size'] * 0.5)
            dist = math.hypot(self.crosshair[0] - head_x, self.crosshair[1] - head_y)
            if dist < min_dist:
                min_dist = dist
                closest_target = (head_x, head_y)
                
        if closest_target:
            # Smooth snap to head (0.55 interpolation)
            self.crosshair[0] = int(self.crosshair[0] + (closest_target[0] - self.crosshair[0]) * 0.55)
            self.crosshair[1] = int(self.crosshair[1] + (closest_target[1] - self.crosshair[1]) * 0.55)

    def _draw_pistol_fps(self, screen, offset):
        # Weapon Sway & Recoil Calculation
        cx, cy = self.crosshair
        # Sways towards crosshair (lagging behind slightly)
        sway_x = (cx - self.width//2) * 0.1
        sway_y = (cy - self.height//2) * 0.05
        
        # Position base for the hand/gun (bottom right quadrant)
        base_x = self.width * 0.7 + sway_x + offset[0]
        base_y = self.height * 0.8 + sway_y + offset[1] - (self.shake_v * 2) # Recoil jump
        
        if self.weapon_img:
            # Draw the loaded weapon image (with glow details)
            screen.blit(self.weapon_img, (base_x - 320, base_y - 280))
        else:
            # --- DRAW HAND ---
            skin_color = (220, 150, 120)
            # Main palm/wrist
            pygame.draw.ellipse(screen, skin_color, (base_x - 40, base_y + 40, 120, 200))
            # Thumb
            pygame.draw.ellipse(screen, skin_color, (base_x - 60, base_y + 60, 60, 40))
            
            # --- DRAW GUN BODY ---
            gun_dark = (30, 30, 35)
            gun_light = (50, 50, 60)
            
            # Main slide (the top part)
            pygame.draw.rect(screen, gun_dark, (base_x - 180, base_y, 220, 60), border_radius=5)
            pygame.draw.rect(screen, gun_light, (base_x - 180, base_y, 220, 5), border_radius=2) # Top highlight
            
            # Grip/Handle (under the hand)
            pygame.draw.rect(screen, (20, 20, 25), (base_x - 30, base_y + 50, 70, 150), border_radius=8)
            
            # Details on slide
            for i in range(5):
                pygame.draw.line(screen, (10, 10, 10), (base_x - 20 + i*10, base_y + 10), (base_x - 20 + i*10, base_y + 50), 2)
                
            # --- RED DOT SIGHT (Reflex Sight) ---
            sight_x = base_x - 100
            sight_y = base_y - 45
            # Sight frame
            pygame.draw.rect(screen, (20, 20, 20), (sight_x, sight_y, 60, 45), border_radius=5)
            pygame.draw.rect(screen, (40, 40, 50), (sight_x + 5, sight_y + 5, 50, 30), border_radius=3)
            # The Red Dot
            pulse = (pygame.time.get_ticks() // 200) % 2
            dot_color = (255, 0, 0) if pulse else (200, 0, 0)
            pygame.draw.circle(screen, dot_color, (sight_x + 30, sight_y + 20), 4)
            
            # Muzzle hole
            pygame.draw.circle(screen, (0, 0, 0), (base_x - 180, base_y + 30), 8)

    def draw(self):
        # Screen Shake
        offset = (random.uniform(-self.shake_v, self.shake_v), random.uniform(-self.shake_v, self.shake_v))
        
        # Draw Background
        self.screen.blit(self.bg_img, offset)
        
        # Draw Targets (Zombies)
        for t in self.targets:
            tp = (int(t['pos'][0] + offset[0]), int(t['pos'][1] + offset[1]))
            
            if self.zombie_sheet:
                frame = self.zombie_sheet.get_frame(t['anim_row'], t['frame'])
                fw, fh = frame.get_width(), frame.get_height()
                
                # Draw target ring under their feet
                glow_surf = pygame.Surface((t['size'] * 2, 16), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surf, (255, 0, 0, 70), (0, 0, t['size'] * 2, 16), 2)
                self.screen.blit(glow_surf, (tp[0] - t['size'], tp[1] + fh // 2 - 15))
                
                # Draw zombie sprite centered
                self.screen.blit(frame, (tp[0] - fw // 2, tp[1] - fh // 2))
                
                # HP Bar above head
                hp_pct = max(0, t['hp']) / 100.0
                bar_w = 45
                bar_h = 5
                bx = tp[0] - bar_w // 2
                by = tp[1] - fh // 2 - 10
                pygame.draw.rect(self.screen, (100, 0, 0), (bx, by, bar_w, bar_h))
                pygame.draw.rect(self.screen, (0, 255, 0), (bx, by, int(bar_w * hp_pct), bar_h))
            else:
                # Body
                pygame.draw.circle(self.screen, (50, 70, 50), tp, t['size'])
                # Head/Core
                pygame.draw.circle(self.screen, (150, 0, 0), tp, t['size']//2)
            
        # VFX
        for p in self.particles: p.draw(self.screen, offset)
        
        # Draw Floating Texts
        for ft in self.floating_texts:
            shadow_surf = self.font_tactical.render(ft['text'], True, (0, 0, 0))
            text_surf = self.font_tactical.render(ft['text'], True, ft['color'])
            self.screen.blit(shadow_surf, (ft['pos'][0] + 1, ft['pos'][1] + 1))
            self.screen.blit(text_surf, ft['pos'])
        
        # Flash
        if self.flash_timer > 0:
            f = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            f.fill((255, 255, 200, 150))
            self.screen.blit(f, (0, 0), special_flags=pygame.BLEND_ADD)
            # Muzzle Flash point
            if self.weapon_img:
                flash_x = int(self.width * 0.7 - 240 + offset[0])
                flash_y = int(self.height * 0.8 - 195 + offset[1] - (self.shake_v * 2))
            else:
                flash_x = int(self.width * 0.7 - 180 + offset[0])
                flash_y = int(self.height * 0.8 + 30 + offset[1])
            pygame.draw.circle(self.screen, (255, 200, 50), (flash_x, flash_y), 50 + random.randint(0, 30))

        # --- DRAW FPS PISTOL ---
        self._draw_pistol_fps(self.screen, offset)
        
        # HUD Top
        pygame.draw.rect(self.screen, (10, 10, 15, 230), (0, 0, self.width, 80))
        pygame.draw.line(self.screen, (255, 50, 50), (0, 80), (self.width, 80), 3)
        
        # Calculate current multiplier for draw
        if self.kills < 10:
            multiplier = 1.0
        elif self.kills < 25:
            multiplier = 1.5
        elif self.kills < 50:
            multiplier = 2.0
        elif self.kills < 80:
            multiplier = 3.0
        else:
            multiplier = 5.0
            
        self.screen.blit(self.font_header.render("CITY UNDER ATTACK", True, (255, 50, 50)), (20, 10))
        
        # Left Stats
        stat_lbl = f"KILLS: {self.kills} (HS: {self.headshots}) | MULTIPLIER: {multiplier:.1f}x"
        self.screen.blit(self.font_tactical.render(stat_lbl, True, (0, 255, 255)), (25, 50))
        
        # Right Stats
        self.screen.blit(self.font_tactical.render(f"SCORE: {self.score:08d}", True, PixelPalette.GOLD), (self.width - 250, 15))
        self.screen.blit(self.font_tactical.render(f"MONEY: +{self.bronze_earned} BRONZE", True, (0, 255, 100)), (self.width - 250, 45))
        
        # Ammo overlay
        self.screen.blit(self.font_tactical.render(f"AMMO: {self.weapon.ammo}/{self.weapon.ammo_max}", True, (255, 255, 255)), (20, 90))
        
        # Timer
        mins, secs = int(self.timer)//60, int(self.timer)%60
        timer_color = (255, 50, 50) if self.timer <= 20 else (255, 255, 255)
        self.screen.blit(self.font_tactical.render(f"TIME LEFT: {mins:02d}:{secs:02d}", True, timer_color), (self.width // 2 - 80, 30))

        # Check if locked onto any target (distance to head < 12 pixels after auto-lock snap)
        is_locked = False
        locked_pos = None
        for t in self.targets:
            head_x = t['pos'][0]
            head_y = t['pos'][1] - int(t['size'] * 0.5)
            dist = math.hypot(self.crosshair[0] - head_x, self.crosshair[1] - head_y)
            if dist < 12.0:
                is_locked = True
                locked_pos = (head_x, head_y)
                break

        # Crosshair
        ch_color = (255, 50, 50) if is_locked else (0, 255, 0)
        pygame.draw.circle(self.screen, ch_color, self.crosshair, 25, 2)
        pygame.draw.line(self.screen, ch_color, (self.crosshair[0]-35, self.crosshair[1]), (self.crosshair[0]+35, self.crosshair[1]), 2)
        pygame.draw.line(self.screen, ch_color, (self.crosshair[0], self.crosshair[1]-35), (self.crosshair[0], self.crosshair[1]+35), 2)

        # Draw red lock square bracket around locked head
        if is_locked and locked_pos:
            tx, ty = int(locked_pos[0] + offset[0]), int(locked_pos[1] + offset[1])
            pygame.draw.rect(self.screen, (255, 50, 50), (tx - 22, ty - 22, 44, 44), 2)
