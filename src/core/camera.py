import pygame

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity_pos):
        # Mengembalikan posisi yang sudah disesuaikan dengan kamera
        if isinstance(entity_pos, pygame.Rect):
            return entity_pos.move(self.camera.topleft)
        return (entity_pos[0] + self.camera.x, entity_pos[1] + self.camera.y)

    def update(self, target_pos):
        # Mengikuti target (player)
        x = -target_pos[0] + int(self.width / 2)
        y = -target_pos[1] + int(self.height / 2)

        # Batasan kamera agar tidak keluar map
        x = min(0, x) # kiri
        y = min(0, y) # atas
        x = max(-(self.map_width - self.width), x) # kanan
        y = max(-(self.map_height - self.height), y) # bawah
        
        self.camera = pygame.Rect(x, y, self.width, self.height)
