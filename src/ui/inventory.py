import pygame

class Inventory:
    def __init__(self):
        self.active = False
        self.grid_cols, self.grid_rows = 8, 4
        self.slot_size = 50
        self.items = {} # Format: {"Item Name": {"image": Surface, "count": N}}
        self.item_list = [] # Untuk navigasi berdasarkan index: ["Item A", "Item B"]
        self.box_rect = pygame.Rect(100, 100, 500, 400) # Dipertinggi untuk area info
        self.font = pygame.font.SysFont("monospace", 14)
        self.cursor_idx = 0
        self.selected_indices = []
        self.crafting_system = None # Akan di-set dari main.py

    def add_item(self, item_name, image):
        if item_name in self.items:
            self.items[item_name]["count"] += 1
        else:
            thumb = pygame.transform.scale(image, (40, 40))
            self.items[item_name] = {"image": thumb, "count": 1, "original_image": image}
            self.item_list.append(item_name)

    def remove_item(self, item_name):
        if item_name in self.items:
            self.items[item_name]["count"] -= 1
            if self.items[item_name]["count"] <= 0:
                del self.items[item_name]
                if item_name in self.item_list:
                    self.item_list.remove(item_name)
            
            # Reset cursor jika out of bounds
            if not self.item_list:
                self.cursor_idx = 0
            else:
                self.cursor_idx = min(self.cursor_idx, len(self.item_list) - 1)

    def toggle(self):
        self.active = not self.active
        self.selected_indices = [] # Reset seleksi saat buka/tutup

    def move_cursor(self, dx, dy):
        if not self.active: return
        # Navigasi grid
        col = self.cursor_idx % self.grid_cols
        row = self.cursor_idx // self.grid_cols
        
        new_col = (col + dx) % self.grid_cols
        new_row = (row + dy) % self.grid_rows
        
        self.cursor_idx = new_row * self.grid_cols + new_col
        # Clamp to item list length if needed to prevent ghost selection
        if self.item_list:
             self.cursor_idx = min(self.cursor_idx, len(self.item_list) - 1)

    def select_item(self):
        if not self.active: return
        if self.item_list and self.cursor_idx < len(self.item_list):
            if self.cursor_idx in self.selected_indices:
                self.selected_indices.remove(self.cursor_idx)
            else:
                self.selected_indices.append(self.cursor_idx)

    def attempt_craft(self):
        if not self.active or len(self.selected_indices) < 2: return None
        
        # Ensure all selected indices are still valid
        self.selected_indices = [idx for idx in self.selected_indices if idx < len(self.item_list)]
        if len(self.selected_indices) < 2: return "Pilih minimal 2 item."

        selected_names = [self.item_list[idx] for idx in self.selected_indices]
        result_name, description = self.crafting_system.check_recipe(selected_names)
        
        if result_name:
            for name in selected_names:
                self.remove_item(name)
            
            # Cari icon untuk item baru (Gunakan SmartSlicer mapping jika ada)
            self.add_item(result_name, pygame.Surface((40,40))) 
            self.selected_indices = []
            return f"Berhasil merakit: {result_name}!"
        else:
            self.selected_indices = []
            return "Kombinasi gagal. Tidak ada yang terjadi."

    def attempt_use(self):
        """Menggunakan item yang sedang disorot kursor"""
        if not self.active or not self.item_list or self.cursor_idx >= len(self.item_list): 
            return None
        
        item_name = self.item_list[self.cursor_idx]
        usable_items = [
            "Bom Molotov", "Umpan Elektronik", "Taser Rakitan", 
            "Medkit Medis", "Energy Drink", "Stimulan Adrenalin",
            "Baterai Militer", "Baterai Cadangan"
        ]
        
        if item_name in usable_items:
            self.remove_item(item_name)
            return item_name
        return None

    def draw(self, screen):
        if not self.active: return
        
        # Background UI
        pygame.draw.rect(screen, (40, 40, 45, 200), self.box_rect)
        pygame.draw.rect(screen, (200, 200, 220), self.box_rect, 3) 

        # Gambar Grid & Cursor
        for i in range(self.grid_rows * self.grid_cols):
            r, c = divmod(i, self.grid_cols)
            slot_x = self.box_rect.x + 20 + c * (self.slot_size + 5)
            slot_y = self.box_rect.y + 20 + r * (self.slot_size + 5)
            
            color = (60, 60, 70)
            if i == self.cursor_idx:
                color = (100, 100, 150) # Highlight Cursor
            if i in self.selected_indices:
                color = (50, 150, 50) # Highlight Selected
                
            pygame.draw.rect(screen, color, (slot_x, slot_y, self.slot_size, self.slot_size))
            pygame.draw.rect(screen, (100, 100, 100), (slot_x, slot_y, self.slot_size, self.slot_size), 2)
        
        # Gambar Item
        for idx, name in enumerate(self.item_list):
            r, c = divmod(idx, self.grid_cols)
            slot_x = self.box_rect.x + 20 + c * (self.slot_size + 5) + 5
            slot_y = self.box_rect.y + 20 + r * (self.slot_size + 5) + 5
            data = self.items[name]
            screen.blit(data["image"], (slot_x, slot_y))
            
            if data["count"] > 1:
                count_text = self.font.render(str(data["count"]), True, (255, 255, 255))
                screen.blit(count_text, (slot_x + 30, slot_y + 30))

        # Panel Info & Hints
        info_rect = pygame.Rect(self.box_rect.x + 10, self.box_rect.y + 250, 480, 140)
        pygame.draw.rect(screen, (30, 30, 35), info_rect)
        
        # Hints
        hints = self.crafting_system.get_hints(self.item_list)
        y_offset = 5
        title_hint = self.font.render("PETUNJUK CRAFTING:", True, (255, 255, 0))
        screen.blit(title_hint, (info_rect.x + 10, info_rect.y + y_offset))
        
        y_offset += 25
        for hint in hints[:3]: # Tampilkan max 3 hint
            hint_surf = self.font.render(f"- {hint}", True, (200, 200, 200))
            screen.blit(hint_surf, (info_rect.x + 10, info_rect.y + y_offset))
            y_offset += 20

        # Instruksi
        instr = self.font.render("[ARAH] Geser [ENTER] Pilih/Batal [C] Rakit", True, (0, 255, 255))
        screen.blit(instr, (self.box_rect.x + 20, self.box_rect.bottom - 25))
