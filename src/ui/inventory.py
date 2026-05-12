import pygame

class Inventory:
    def __init__(self):
        self.active = False
        self.grid_cols, self.grid_rows = 8, 4
        self.slot_size = 50
        self.items = {} 
        self.box_rect = pygame.Rect(100, 100, 500, 300)
        self.font = pygame.font.Font(None, 24)

    def add_item(self, item_name, image):
        if item_name in self.items:
            self.items[item_name]["count"] += 1
        else:
            thumb = pygame.transform.scale(image, (40, 40))
            self.items[item_name] = {"image": thumb, "count": 1}

    def toggle(self):
        self.active = not self.active

    def draw(self, screen):
        if not self.active: return
        
        # Background UI
        pygame.draw.rect(screen, (205, 170, 125), self.box_rect)
        pygame.draw.rect(screen, (139, 69, 19), self.box_rect, 5) 

        # Gambar Grid
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                slot_x = self.box_rect.x + 20 + c * (self.slot_size + 5)
                slot_y = self.box_rect.y + 20 + r * (self.slot_size + 5)
                pygame.draw.rect(screen, (160, 130, 90), (slot_x, slot_y, self.slot_size, self.slot_size))
                pygame.draw.rect(screen, (100, 70, 40), (slot_x, slot_y, self.slot_size, self.slot_size), 2)
        
        # Gambar Item
        idx = 0
        for name, data in self.items.items():
            r, c = divmod(idx, self.grid_cols)
            slot_x = self.box_rect.x + 20 + c * (self.slot_size + 5) + 5
            slot_y = self.box_rect.y + 20 + r * (self.slot_size + 5) + 5
            screen.blit(data["image"], (slot_x, slot_y))
            count_text = self.font.render(str(data["count"]), True, (255, 255, 255))
            screen.blit(count_text, (slot_x + 30, slot_y + 30))
            idx += 1
