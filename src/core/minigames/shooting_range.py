import pygame, math, random, time
from typing import List, Dict, Tuple, Optional
from src.core.engine import MiniGame, Spritesheet

class PixelPalette:
    GOLD, CYAN_GLOW, FIRE_GLOW, BLOOD = (255, 215, 0), (0, 255, 255), (255, 50, 50), (180, 0, 0)

class Particle:
    def __init__(self, x, y, color, size_range=(2, 8)):
        self.pos, self.vel = [x, y], [random.uniform(-3, 3), random.uniform(-3, 3)]
        self.color, self.size, self.life = color, random.randint(*size_range), 1.0
    def update(self):
        self.pos[0] += self.vel[0]; self.pos[1] += self.vel[1]; self.life -= 0.02
        return self.life > 0
    def draw(self, screen, offset=(0,0)):
        pygame.draw.circle(screen, self.color, (int(self.pos[0] + offset[0]), int(self.pos[1] + offset[1])), int(self.size * self.life))

class WeaponType:
    UZI = {"name": "MICRO UZI (SMG)", "damage": 25, "ammo": 40, "recoil": 6, "delay": 3, "image_path": "assets/images/weapon_2.png", "scale": (450, 450)}
    SCAR = {"name": "SCAR-H (ASSAULT)", "damage": 45, "ammo": 30, "recoil": 14, "delay": 6, "image_path": "assets/images/weapon_1.png", "scale": (500, 500)}
    SHOTGUN = {"name": "SPAS-12 (SHOTGUN)", "damage": 120, "ammo": 8, "recoil": 32, "delay": 28, "image_path": "assets/images/weapon_3.png", "scale": (520, 520)}
    SNIPER = {"name": "AWM SNIPER", "damage": 250, "ammo": 5, "recoil": 48, "delay": 55, "image_path": "assets/images/weapon_4.png", "scale": (540, 540)}

class TacticalWeapon:
    def __init__(self, w_type, reload_max_time=60):
        self.type = w_type
        self.ammo_max = w_type["ammo"]
        self.ammo, self.is_reloading, self.reload_timer, self.shot_delay, self.reload_max_time = self.ammo_max, False, 0, 0, reload_max_time
    def update(self):
        if self.shot_delay > 0: self.shot_delay -= 1
        if self.is_reloading:
            self.reload_timer -= 1
            if self.reload_timer <= 0: self.ammo, self.is_reloading = self.ammo_max, False
    def can_shoot(self): return self.ammo > 0 and not self.is_reloading and self.shot_delay <= 0
    def shoot(self): self.ammo -= 1; self.shot_delay = self.type["delay"]
    def reload(self):
        if not self.is_reloading and self.ammo < self.ammo_max: self.is_reloading, self.reload_timer = True, self.reload_max_time

class ShootingRangeUltimate(MiniGame):
    def __init__(self, screen, clock, manager):
        super().__init__(screen, clock, manager)
        self.width, self.height = 1280, 720
        self.crosshair, self.score, self.timer, self.kills, self.headshots, self.bronze_earned, self.boss_spawned_count = [640, 360], 0, 90.0, 0, 0, 0, 0
        try:
            self.bg_img = pygame.transform.scale(pygame.image.load("assets/city_bg.png").convert(), (1280, 720))
        except:
            self.bg_img = pygame.Surface((1280, 720)); self.bg_img.fill((10, 10, 30))
        self.weapon_images = {}
        for w_name, w_type in [("UZI", WeaponType.UZI), ("SCAR", WeaponType.SCAR), ("SHOTGUN", WeaponType.SHOTGUN), ("SNIPER", WeaponType.SNIPER)]:
            try:
                self.weapon_images[w_name] = pygame.transform.scale(pygame.image.load(w_type["image_path"]).convert_alpha(), w_type["scale"])
            except: self.weapon_images[w_name] = None
        try:
            self.zombie_sheet = Spritesheet("assets/enemies/zombie_new.png", 8, 8, scale=2.5)
        except: self.zombie_sheet = None
        upgrades = getattr(self.manager.main_engine, "weapon_upgrades", {"damage_level": 0, "ammo_level": 0, "reload_level": 0, "firerate_level": 0})
        self.weapons = {}
        for w_key, w_type in [("UZI", WeaponType.UZI), ("SCAR", WeaponType.SCAR), ("SHOTGUN", WeaponType.SHOTGUN), ("SNIPER", WeaponType.SNIPER)]:
            w_copy = w_type.copy()
            w_copy["damage"] = int(w_copy["damage"] * (1.0 + upgrades["damage_level"] * 0.25))
            w_copy["ammo"] = int(w_copy["ammo"] * (1.0 + upgrades["ammo_level"] * 0.25))
            w_copy["delay"] = max(1, int(w_copy["delay"] * (1.0 - upgrades["firerate_level"] * 0.15)))
            self.weapons[w_key] = TacticalWeapon(w_copy, max(15, 60 - upgrades["reload_level"] * 15))
        self.current_weapon_name = getattr(self.manager.main_engine, "selected_weapon", "SCAR")
        self.targets, self.particles, self.floating_texts, self.flash_timer, self.shake_v = [], [], [], 0, 0
        self.font_header, self.font_tactical = pygame.font.SysFont("monospace", 36, bold=True), pygame.font.SysFont("monospace", 18, bold=True)
        try:
            self.shoot_sfx = pygame.mixer.Sound("assets/suarapistol.mp3")
            self.shoot_sfx.set_volume(0.6)
        except: self.shoot_sfx = None

    @property
    def weapon(self): return self.weapons[self.current_weapon_name]

    def _trigger_shot(self):
        self.weapon.shoot(); self.flash_timer, self.shake_v = 5, self.weapon.type["recoil"]
        if self.shoot_sfx: self.shoot_sfx.play()
        hit = False
        for t in self.targets:
            hx, hy, hr = t['pos'][0], t['pos'][1] - int(t['size'] * 0.5), int(t['size'] * 0.4)
            dist_head = math.hypot(self.crosshair[0] - hx, self.crosshair[1] - hy)
            dist_body = math.hypot(self.crosshair[0] - t['pos'][0], self.crosshair[1] - t['pos'][1])
            if dist_head < hr or dist_body < t['size']:
                is_hs = dist_head < hr
                dmg = self.weapon.type["damage"] * (2 if is_hs else 1)
                self.floating_texts.append({'text': f"CRITICAL! -{dmg}" if is_hs else f"-{dmg}", 'pos': [self.crosshair[0], self.crosshair[1] - 15], 'timer': 25 if is_hs else 20, 'color': (255, 215, 0) if is_hs else (220, 220, 220)})
                for _ in range(15 if is_hs else 8): self.particles.append(Particle(hx if is_hs else t['pos'][0], hy if is_hs else t['pos'][1], (255, 50, 50) if is_hs else PixelPalette.BLOOD, (3, 6) if is_hs else (2, 5)))
                t['hp'] -= dmg
                if t['hp'] <= 0:
                    self.kills += 1; is_boss = t.get('is_boss', False)
                    mult = 1.0 if self.kills < 10 else 1.5 if self.kills < 25 else 2.0 if self.kills < 50 else 3.0 if self.kills < 80 else 5.0
                    if is_boss:
                        self.score += 1000; self.bronze_earned += 200; self.timer = min(180.0, self.timer + 20.0); self.shake_v = 40
                        self.floating_texts.append({'text': "BOSS DEFEATED! +1000 PTS (+200B)", 'pos': [t['pos'][0] - 120, t['pos'][1] - 40], 'timer': 75, 'color': (255, 0, 128)})
                        self.floating_texts.append({'text': "+20.0s BONUS TIME", 'pos': [t['pos'][0] - 50, t['pos'][1] - 70], 'timer': 60, 'color': (0, 255, 255)})
                        for _ in range(40): self.particles.append(Particle(t['pos'][0], t['pos'][1], (255, 50, 50), (4, 9)))
                    else:
                        self.headshots += 1 if is_hs else 0
                        self.score += 150 if is_hs else 100
                        payout = int((15 if is_hs else 10) * mult)
                        self.bronze_earned += payout; self.timer = min(180.0, self.timer + (4.0 if is_hs else 2.5))
                        self.floating_texts.append({'text': f"+{'150 HEADSHOT' if is_hs else '100'} KILL (+{payout}B)", 'pos': [t['pos'][0] - 50, t['pos'][1] - 40], 'timer': 45 if is_hs else 35, 'color': (255, 215, 0) if is_hs else (100, 255, 100)})
                        self.floating_texts.append({'text': f"+{4.0 if is_hs else 2.5:.1f}s TIME", 'pos': [t['pos'][0] + 10, t['pos'][1] - 65], 'timer': 30, 'color': (0, 255, 255)})
                    t['active'] = False
                hit = True; break
        if not hit:
            for _ in range(3): self.particles.append(Particle(self.crosshair[0], self.crosshair[1], (200, 200, 200), (2, 4)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION: self.crosshair = list(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.weapon.can_shoot():
            self._trigger_shot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: self.weapon.reload()

    def update(self, dt):
        self.timer -= dt / 60.0
        if self.timer <= 0: self.exit_game({'score': self.score, 'bronze_earned': self.bronze_earned})
        for w in self.weapons.values(): w.update()
        
        # Gesture-based reloading
        gt = getattr(self.manager.main_engine, "gesture_thread", None)
        if gt:
            g = gt.current_gesture
            if g == "FIST" and not self.weapon.is_reloading and self.weapon.ammo < self.weapon.ammo_max:
                self.weapon.reload()

        is_auto = self.current_weapon_name in ["UZI", "SCAR"]
        if is_auto:
            mouse_hold = pygame.mouse.get_pressed()[0]
            gesture_hold = gt and gt.current_gesture == "PISTOL"
            if (mouse_hold or gesture_hold) and self.weapon.can_shoot():
                self._trigger_shot()
                
        if self.flash_timer > 0: self.flash_timer -= 1
        if self.shake_v > 0: self.shake_v *= 0.85
        next_boss = 15 * (self.boss_spawned_count + 1)
        if self.kills >= next_boss and not any(t.get('is_boss', False) for t in self.targets):
            self.targets.append({'pos': [random.randint(200, 1080), random.randint(250, 520)], 'size': 110, 'hp': 600, 'max_hp': 600, 'active': True, 'timer': 1200, 'anim_row': random.choice([0,2,3,4,6,7]), 'frame': random.randint(0,5), 'frame_timer': 0, 'is_boss': True})
            self.boss_spawned_count += 1; self.shake_v = 25
            self.floating_texts.append({'text': "WARNING: BOSS ZOMBIE HAS SPAWNED!", 'pos': [640 - 200, 260], 'timer': 90, 'color': (255, 0, 0)})
        max_targets = 8 + min(7, self.kills // 5)
        if len(self.targets) < max_targets and random.random() < min(0.15, 0.05 + (self.kills / 100.0)):
            ar = random.choice([0, 2, 3, 4, 6, 7])
            sx = 50 if ar == 6 else 1230 if ar == 7 else random.randint(100, 1180)
            self.targets.append({'pos': [sx, random.randint(200, 570)], 'size': random.randint(35, 55), 'hp': 100, 'max_hp': 100, 'active': True, 'timer': random.randint(240, 480), 'anim_row': ar, 'frame': random.randint(0,5), 'frame_timer': 0})
        speed_mult = 1.0 + (self.kills / 25.0)
        for t in self.targets:
            t['timer'] -= 1; t['frame_timer'] += 1
            if t['frame_timer'] >= 8: t['frame_timer'], t['frame'] = 0, (t['frame'] + 1) % 6
            factor = (0.5 if t.get('is_boss', False) else 1.0) * speed_mult
            if t['anim_row'] == 4: t['pos'][1] += 0.8 * factor
            elif t['anim_row'] == 6: t['pos'][0] += 1.2 * factor
            elif t['anim_row'] == 7: t['pos'][0] -= 1.2 * factor
            if t['anim_row'] == 6 and t['pos'][0] > 1230: t['anim_row'] = 7
            elif t['anim_row'] == 7 and t['pos'][0] < 50: t['anim_row'] = 6
        self.targets = [t for t in self.targets if t['active'] and t['timer'] > 0 and t['pos'][1] < 670]
        self.particles = [p for p in self.particles if p.update()]
        for ft in self.floating_texts: ft['pos'][1] -= 0.8; ft['timer'] -= 1
        self.floating_texts = [ft for ft in self.floating_texts if ft['timer'] > 0]
        closest_t = None; min_d = 90.0
        for t in self.targets:
            hx, hy = t['pos'][0], t['pos'][1] - int(t['size'] * 0.5)
            d = math.hypot(self.crosshair[0] - hx, self.crosshair[1] - hy)
            if d < min_d: min_d, closest_t = d, (hx, hy)
        if closest_t:
            self.crosshair[0] = int(self.crosshair[0] + (closest_t[0] - self.crosshair[0]) * 0.55)
            self.crosshair[1] = int(self.crosshair[1] + (closest_t[1] - self.crosshair[1]) * 0.55)

    def _draw_pistol_fps(self, screen, offset):
        cx, cy = self.crosshair
        base_x = 896 + (cx - 640) * 0.1 + offset[0]
        base_y = 576 + (cy - 360) * 0.05 + offset[1] - (self.shake_v * 2)
        img = self.weapon_images.get(self.current_weapon_name)
        if img:
            ox, oy = (-220, -220) if self.current_weapon_name == "UZI" else (-320, -280) if self.current_weapon_name == "SNIPER" else (-280, -250)
            screen.blit(img, (base_x + ox, base_y + oy))
        else:
            pygame.draw.rect(screen, (30, 30, 35), (base_x - 100, base_y - 20, 150, 40), border_radius=5)
            pygame.draw.circle(screen, (0, 0, 0), (base_x - 100, base_y), 6)

    def draw(self):
        offset = (random.uniform(-self.shake_v, self.shake_v), random.uniform(-self.shake_v, self.shake_v))
        self.screen.blit(self.bg_img, offset)
        for t in self.targets:
            tp = (int(t['pos'][0] + offset[0]), int(t['pos'][1] + offset[1]))
            if self.zombie_sheet:
                is_boss = t.get('is_boss', False)
                frame = self.zombie_sheet.get_frame(t['anim_row'], t['frame'])
                if is_boss: frame = pygame.transform.scale(frame, (int(frame.get_width() * 2.2), int(frame.get_height() * 2.2)))
                fw, fh = frame.get_width(), frame.get_height()
                pygame.draw.ellipse(self.screen, (255, 0, 128, 100) if is_boss else (255, 0, 0, 70), (tp[0] - t['size'], tp[1] + fh // 2 - 15, t['size'] * 2, 16), 2)
                self.screen.blit(frame, (tp[0] - fw // 2, tp[1] - fh // 2))
                bx, by, bw, bh = tp[0] - (100 if is_boss else 45) // 2, tp[1] - fh // 2 - 10, 100 if is_boss else 45, 8 if is_boss else 5
                pygame.draw.rect(self.screen, (100, 0, 0), (bx, by, bw, bh))
                pygame.draw.rect(self.screen, (255, 0, 128) if is_boss else (0, 255, 0), (bx, by, int(bw * (max(0, t['hp']) / t.get('max_hp', 100.0))), bh))
            else:
                pygame.draw.circle(self.screen, (50, 70, 50), tp, t['size'])
                pygame.draw.circle(self.screen, (150, 0, 0), tp, t['size']//2)
        for p in self.particles: p.draw(self.screen, offset)
        for ft in self.floating_texts:
            self.screen.blit(self.font_tactical.render(ft['text'], True, (0, 0, 0)), (ft['pos'][0] + 1, ft['pos'][1] + 1))
            self.screen.blit(self.font_tactical.render(ft['text'], True, ft['color']), ft['pos'])
        if self.flash_timer > 0:
            f = pygame.Surface((self.width, self.height), pygame.SRCALPHA); f.fill((255, 255, 200, 150))
            self.screen.blit(f, (0, 0), special_flags=pygame.BLEND_ADD)
            active_img = self.weapon_images.get(self.current_weapon_name)
            fx = int(self.width * 0.7 - 240 + offset[0]) if active_img else int(self.width * 0.7 - 180 + offset[0])
            fy = int(self.height * 0.8 - 195 + offset[1] - (self.shake_v * 2)) if active_img else int(self.height * 0.8 + 30 + offset[1])
            pygame.draw.circle(self.screen, (255, 200, 50), (fx, fy), 50 + random.randint(0, 30))
        self._draw_pistol_fps(self.screen, offset)
        pygame.draw.rect(self.screen, (10, 10, 15, 230), (0, 0, self.width, 80))
        pygame.draw.line(self.screen, (255, 50, 50), (0, 80), (self.width, 80), 3)
        mult = 1.0 if self.kills < 10 else 1.5 if self.kills < 25 else 2.0 if self.kills < 50 else 3.0 if self.kills < 80 else 5.0
        self.screen.blit(self.font_header.render("CITY UNDER ATTACK", True, (255, 50, 50)), (20, 10))
        self.screen.blit(self.font_tactical.render(f"KILLS: {self.kills} (HS: {self.headshots}) | MULTIPLIER: {mult:.1f}x", True, (0, 255, 255)), (25, 50))
        self.screen.blit(self.font_tactical.render(f"SCORE: {self.score:08d}", True, PixelPalette.GOLD), (self.width - 250, 15))
        self.screen.blit(self.font_tactical.render(f"MONEY: +{self.bronze_earned} BRONZE", True, (0, 255, 100)), (self.width - 250, 45))
        self.screen.blit(self.font_tactical.render(f"SENJATA: {self.weapon.type['name']}", True, (255, 255, 0)), (20, 90))
        self.screen.blit(self.font_tactical.render(f"AMMO: {self.weapon.ammo}/{self.weapon.ammo_max}", True, (255, 255, 255)), (20, 115))
        pygame.draw.rect(self.screen, (10, 10, 15, 200), (950, 600, 310, 80), border_radius=8)
        pygame.draw.rect(self.screen, (0, 255, 255, 100), (950, 600, 310, 80), 1, border_radius=8)
        self.screen.blit(self.font_tactical.render("SENJATA AKTIF (KUNCI):", True, (255, 255, 0)), (960, 615))
        self.screen.blit(self.font_tactical.render(self.weapon.type["name"], True, (0, 255, 255)), (960, 645))
        mins, secs = int(self.timer)//60, int(self.timer)%60
        self.screen.blit(self.font_tactical.render(f"TIME LEFT: {mins:02d}:{secs:02d}", True, (255, 50, 50) if self.timer <= 20 else (255, 255, 255)), (self.width // 2 - 80, 30))
        boss = next((t for t in self.targets if t.get('is_boss', False)), None)
        if boss:
            pygame.draw.rect(self.screen, (20, 20, 20, 200), (385, 90, 510, 30), border_radius=5)
            pygame.draw.rect(self.screen, (80, 0, 0), (390, 95, 500, 20), border_radius=3)
            pygame.draw.rect(self.screen, (255, 0, 50), (390, 95, int(500 * max(0, boss['hp']) / boss.get('max_hp', 600)), 20), border_radius=3)
            pygame.draw.rect(self.screen, (255, 215, 0), (390, 95, 500, 20), 2, border_radius=3)
            lbl = self.font_tactical.render("CRIMSON ABOMINATION (BOSS)", True, (255, 255, 255))
            self.screen.blit(lbl, (390 + (500 - lbl.get_width()) // 2, 73))
        locked = None; min_d = 12.0
        for t in self.targets:
            hx, hy = t['pos'][0], t['pos'][1] - int(t['size'] * 0.5)
            d = math.hypot(self.crosshair[0] - hx, self.crosshair[1] - hy)
            if d < min_d: min_d, locked = d, (hx, hy)
        ch_c = (255, 50, 50) if locked else (0, 255, 0)
        pygame.draw.circle(self.screen, ch_c, self.crosshair, 25, 2)
        pygame.draw.line(self.screen, ch_c, (self.crosshair[0]-35, self.crosshair[1]), (self.crosshair[0]+35, self.crosshair[1]), 2)
        pygame.draw.line(self.screen, ch_c, (self.crosshair[0], self.crosshair[1]-35), (self.crosshair[0], self.crosshair[1]+35), 2)
        if locked: pygame.draw.rect(self.screen, (255, 50, 50), (int(locked[0] + offset[0]) - 22, int(locked[1] + offset[1]) - 22, 44, 44), 2)
