import pygame, random, math, os, time
from typing import Optional

class Spritesheet:
    def __init__(self, filename, cols, rows, scale=1.5):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.cols, self.rows, self.scale = cols, rows, scale
        self.fw, self.fh = self.sheet.get_width() // cols, self.sheet.get_height() // rows
        self.frames = [[pygame.transform.scale(self.sheet.subsurface((c*self.fw, r*self.fh, self.fw, self.fh)), (int(self.fw*scale), int(self.fh*scale))) for c in range(cols)] for r in range(rows)]
    def get_frame(self, row, col): return self.frames[row][col]

class Camera:
    def __init__(self, w, h, mw, mh):
        self.camera = pygame.Rect(0, 0, w, h)
        self.w, self.h, self.mw, self.mh = w, h, mw, mh
    def apply(self, pos):
        return pos.move(self.camera.topleft) if isinstance(pos, pygame.Rect) else (pos[0] + self.camera.x, pos[1] + self.camera.y)
    def update(self, t):
        x = max(-(self.mw - self.w), min(0, -t[0] + self.w // 2))
        y = max(-(self.mh - self.h), min(0, -t[1] + self.h // 2))
        self.camera = pygame.Rect(x, y, self.w, self.h)

class CurrencyManager:
    def __init__(self): self.bronze = self.silver = self.gold = 0
    def add_bronze(self, amt): self.bronze += amt; self._convert()
    def get_total_bronze(self): return self.bronze + (self.silver * 100) + (self.gold * 10000)
    def deduct_bronze(self, amt):
        tot = self.get_total_bronze()
        if tot < amt: return False
        self.gold, r = divmod(tot - amt, 10000)
        self.silver, self.bronze = divmod(r, 100)
        return True
    def _convert(self):
        if self.bronze >= 100: self.silver += self.bronze // 100; self.bronze %= 100
        if self.silver >= 100: self.gold += self.silver // 100; self.silver %= 100

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.bgm_volume, self.sfx_volume, self.current_bgm = 0.5, 0.7, None
    def play_bgm(self, f, loops=-1):
        try:
            if self.current_bgm == f: return
            pygame.mixer.music.load(f)
            pygame.mixer.music.set_volume(self.bgm_volume)
            pygame.mixer.music.play(loops)
            self.current_bgm = f
        except: pass
    def stop_bgm(self): pygame.mixer.music.stop(); self.current_bgm = None
    def play_sfx(self, f):
        try:
            s = pygame.mixer.Sound(f)
            s.set_volume(self.sfx_volume)
            s.play()
        except: pass
    def set_volumes(self, bv, sv):
        self.bgm_volume, self.sfx_volume = bv, sv
        pygame.mixer.music.set_volume(bv)

class VisualEffects:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.darkness_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        self.flash_surf = pygame.Surface((w, h))
        self.flash_surf.fill((255,255,255))
        self.flash_timer = self.flash_duration = self.shake_amount = 0
    def draw_darkness(self, screen, p_pos, camera, light_on, bat, injured):
        # Waktu Indonesia (UTC+7) dipercepat 5x
        game_secs = ((time.time() + 7*3600) * 5) % 86400
        hour = game_secs / 3600.0
        
        # Intensitas Kegelapan (0.0 Siang - 1.0 Malam)
        # Peak gelap jam 00:00, Terang jam 12:00
        dark_mult = (math.cos((hour - 12) * math.pi / 12) + 1) / 2
        
        # Warna overlay untuk dikurangi (BLEND_RGBA_SUB)
        # Malam: mendekati (180, 180, 220) | Siang: mendekati (0, 0, 0)
        base_r = int(180 * dark_mult)
        base_g = int(180 * dark_mult)
        base_b = int(220 * dark_mult)

        if injured:
            pulse = int(abs(math.sin(pygame.time.get_ticks() * 0.003)) * 40)
            base_r = min(255, base_r + pulse)
            
        c = (base_r, base_g, base_b)
        self.darkness_surf.fill((*c, 255))
        
        if light_on and bat > 0:
            sp = camera.apply(p_pos)
            cx, cy = int(sp[0] + 32), int(sp[1] + 32)
            # Lubang Senter: Jadikan hitam (0,0,0) agar tidak mengurangi warna screen
            for r in range(250, 0, -10):
                alpha = int(255 * (1.0 - (r / 250)))
                pygame.draw.circle(self.darkness_surf, (0, 0, 0, alpha), (cx, cy), r)
        
        screen.blit(self.darkness_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    def trigger_flash(self, dur=120): self.flash_timer, self.flash_duration, self.shake_amount = dur, max(1, dur), 15
    def draw_flash(self, screen):
        off = [random.randint(-self.shake_amount, self.shake_amount), random.randint(-self.shake_amount, self.shake_amount)] if self.shake_amount > 0 else [0, 0]
        if self.shake_amount > 0: self.shake_amount -= 1
        if self.flash_timer > 0:
            self.flash_surf.set_alpha(max(0, min(255, int((self.flash_timer / self.flash_duration) * 255))))
            screen.blit(self.flash_surf, off)
            self.flash_timer -= 1
        return tuple(off)

class MiniGame:
    def __init__(self, scr, clk, mgr):
        self.screen, self.clock, self.manager, self.running, self.score = scr, clk, mgr, True, 0
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
    def handle_event(self, e): pass
    def update(self, dt): pass
    def draw(self): pass
    def exit_game(self, res=None): self.running = False; self.manager.return_to_main(res)

class MiniGameManager:
    def __init__(self, eng):
        self.main_engine, self.active_game, self.saved_main_state = eng, None, None
    def start_minigame(self, cls): self.active_game = cls(self.main_engine.screen, self.main_engine.clock, self)
    def return_to_main(self, res):
        self.active_game, self.last_result = None, res
        if res:
            score = res.get('score', 0)
            self.main_engine.currency.add_bronze(res.get('bronze_earned', score // 10))
            if hasattr(self.main_engine, 'point_kill'):
                self.main_engine.point_kill += score
    def update(self, dt):
        if self.active_game: self.active_game.update(dt)
    def draw(self):
        if self.active_game: self.active_game.draw()
    @property
    def in_minigame(self): return self.active_game is not None
