import pygame

class HUD:
    def __init__(self, currency):
        self.currency = currency
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        text = f"Gold: {self.currency.gold} | Silver: {self.currency.silver} | Bronze: {self.currency.bronze}"
        hud_surface = self.font.render(text, True, (255, 255, 0))
        screen.blit(hud_surface, (20, 20))
