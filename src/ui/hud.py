import pygame
import time

class HUD:
    def __init__(self, currency):
        self.currency = currency
        self.font_main = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_sub = pygame.font.SysFont("Arial", 12)
        
        # Simpan nilai untuk animasi smooth
        self.display_gold = currency.gold
        self.display_silver = currency.silver
        self.display_bronze = currency.bronze
        
        # Warna Palette
        self.CLR_BG = (20, 20, 20, 180)  # Dark transparent
        self.CLR_ACCENT = (255, 215, 0)   # Gold
        self.CLR_WHITE = (240, 240, 240)
        self.CLR_HEALTH = (231, 76, 60)   # Red
        self.CLR_STAMINA = (46, 204, 113) # Green
        self.CLR_BATTERY = (52, 152, 219) # Blue

    def _draw_bar(self, screen, x, y, width, label, value, max_value, color):
        # Background Bar
        pygame.draw.rect(screen, (40, 40, 40), (x, y, width, 8), border_radius=4)
        # Fill Bar
        fill_w = int((value / max_value) * width)
        if fill_w > 0:
            pygame.draw.rect(screen, color, (x, y, fill_w, 8), border_radius=4)
        # Label
        lbl_surf = self.font_sub.render(label, True, (150, 150, 150))
        screen.blit(lbl_surf, (x, y - 15))

    def draw(self, screen, player=None, battery_level=100):
        # 1. Background Panel (Clean Rect)
        panel_rect = pygame.Rect(20, 20, 260, 100)
        bg_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, self.CLR_BG, bg_surf.get_rect(), border_radius=10)
        screen.blit(bg_surf, (panel_rect.x, panel_rect.y))

        # 2. Update Animasi Angka (Simple lerp)
        self.display_gold += (self.currency.gold - self.display_gold) * 0.1
        self.display_silver += (self.currency.silver - self.display_silver) * 0.1
        self.display_bronze += (self.currency.bronze - self.display_bronze) * 0.1

        # 3. Currency Display (Horizontal Row)
        currencies = [
            ("G", int(self.display_gold), (255, 215, 0)),
            ("S", int(self.display_silver), (192, 192, 192)),
            ("B", int(self.display_bronze), (205, 127, 50))
        ]
        
        start_x = 40
        for icon, val, color in currencies:
            # Icon Circle
            pygame.draw.circle(screen, color, (start_x, 45), 8)
            # Value
            val_surf = self.font_main.render(str(val), True, self.CLR_WHITE)
            screen.blit(val_surf, (start_x + 15, 35))
            start_x += 75

        # 4. Status Bars (Vertical Stack)
        hp = player.health if player else 100
        stamina = player.stamina if hasattr(player, 'stamina') else 100
        
        bar_x = 40
        self._draw_bar(screen, bar_x, 80, 200, "HEALTH", hp, 100, self.CLR_HEALTH)
        self._draw_bar(screen, bar_x, 105, 200, "BATTERY", battery_level, 100, self.CLR_BATTERY)
