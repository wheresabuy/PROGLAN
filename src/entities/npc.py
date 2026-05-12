import pygame

class NPC:
    def __init__(self, name, x, y, dialog):
        self.name = name
        self.pos = (x, y)
        self.dialog = dialog
        self.rect = pygame.Rect(x, y, 50, 50) # Hitbox

    def check_interaction(self, player_pos):
        # Hitung jarak kasar
        dx = self.pos[0] - player_pos[0]
        dy = self.pos[1] - player_pos[1]
        return (dx**2 + dy**2)**0.5 < 100

    def draw(self, screen):
        # Untuk sekarang gambar kotak sederhana sebagai NPC
        pygame.draw.rect(screen, (0, 255, 0), self.rect)
