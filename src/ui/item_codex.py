import pygame

class ItemCodex:
    def __init__(self):
        self.active = False
        self.font_small = pygame.font.SysFont("monospace", 14)
        self.font_medium = pygame.font.SysFont("monospace", 16)
        self.font_header = pygame.font.SysFont("monospace", 18)
        
        self.scroll_y = 0
        self.max_display = 12
        self.box_rect = pygame.Rect(50, 50, 700, 500)
        
        self.rarity_colors = {
            "Common": (200, 200, 200),
            "Uncommon": (50, 205, 50),
            "Rare": (30, 144, 255),
            "Epic": (148, 0, 211),
            "Legendary": (255, 140, 0)
        }

        # Data semua item (Metadata)
        self.all_items = [
            # RAW MATERIALS
            {"name": "Kain Bekas", "rarity": "Common", "desc": "Tersebar di area pemukiman. Bahan dasar hampir semua item."},
            {"name": "Botol Kosong", "rarity": "Common", "desc": "Sering ditemukan di tempat sampah. Untuk wadah kimia/bom."},
            {"name": "Kabel", "rarity": "Common", "desc": "Area teknis/listrik. Untuk item bertema setrum/elektronik."},
            {"name": "Tanaman Obat", "rarity": "Common", "desc": "Area taman/hutan. Bahan dasar medis."},
            {"name": "Baterai Cadangan", "rarity": "Common", "desc": "Laci atau perangkat lama. Sumber daya gadget."},
            {"name": "Lempeng Besi", "rarity": "Uncommon", "desc": "Area konstruksi. Untuk pertahanan dan senjata tajam."},
            {"name": "Mata Air", "rarity": "Uncommon", "desc": "Area tertentu di map. Sumber air bersih."},
            {"name": "Pembalut Lukaku", "rarity": "Uncommon", "desc": "Kotak P3K lama. Bahan medis menengah."},
            {"name": "Cairan Pelarut", "rarity": "Rare", "desc": "Laboratorium atau bengkel. Bahan kimia korosif."},
            {"name": "Jerigen Bensin", "rarity": "Rare", "desc": "Stasiun bensin. Bahan bakar dan peledak."},
            {"name": "Antena Radio", "rarity": "Epic", "desc": "Puncak gedung. Komponen komunikasi canggih."},
            {"name": "Baterai Militer", "rarity": "Epic", "desc": "Peti militer. Daya sangat besar untuk gadget high-end."},
            {"name": "Chip Frekuensi", "rarity": "Legendary", "desc": "Ruang kontrol. Otak gadget pintar."},
            
            # CRAFTED ITEMS
            {"name": "Umpan Elektronik", "rarity": "Epic", "desc": "Menarik perhatian zombie ke satu titik tertentu."},
            {"name": "Taser Rakitan", "rarity": "Uncommon", "desc": "Menyetrum 1 zombie hingga kaku sejenak."},
            {"name": "Bom Molotov", "rarity": "Rare", "desc": "Ledakan api area, sangat efektif membakar gerombolan."},
            {"name": "Antiseptik Kuat", "rarity": "Rare", "desc": "Menyembuhkan infeksi dan luka berat karakter."},
            {"name": "Armor Diperkuat", "rarity": "Rare", "desc": "Baju pelindung yang mengurangi damage serangan zombie."},
            {"name": "Machete Karatan", "rarity": "Uncommon", "desc": "Senjata jarak dekat darurat untuk memukul mundur zombie."},
            {"name": "Obor Darurat", "rarity": "Common", "desc": "Cahaya tanpa baterai, tapi bisa mati jika kena angin."},
            {"name": "Shock Armor", "rarity": "Epic", "desc": "Zombie yang menggigitmu akan tersetrum secara otomatis."},
            {"name": "Acid Blade", "rarity": "Epic", "desc": "Pedang yang dilapisi asam, memberikan damage racun."},
            {"name": "Shock Decoy", "rarity": "Legendary", "desc": "Umpan yang menyetrum massal saat disentuh zombie."},
            {"name": "Ghillie Suit", "rarity": "Epic", "desc": "Sangat sulit dideteksi zombie selama tidak bergerak."},
            {"name": "Medkit Medis", "rarity": "Epic", "desc": "Memulihkan kesehatan secara penuh secara instan."},
            {"name": "Hacking Tool", "rarity": "Legendary", "desc": "Bisa digunakan untuk membuka pintu elektronik."},
            {"name": "Shock Trap", "rarity": "Rare", "desc": "Jebakan lantai listrik yang dipasang di tanah."},
            {"name": "Signal Booster", "rarity": "Epic", "desc": "Meningkatkan jangkauan radio pemanggil bantuan."},
            {"name": "Bom Serpihan", "rarity": "Epic", "desc": "Ledakan kuat yang menyebarkan serpihan besi tajam."},
            {"name": "Energy Drink", "rarity": "Rare", "desc": "Memulihkan stamina dan menambah kecepatan gerak."},
            {"name": "Teh Herbal", "rarity": "Common", "desc": "Meningkatkan stamina maksimal untuk sementara waktu."},
            {"name": "Stimulan Adrenalin", "rarity": "Rare", "desc": "Berlari tanpa lelah selama durasi singkat."}
        ]

    def toggle(self):
        self.active = not self.active

    def scroll(self, direction):
        if not self.active: return
        self.scroll_y += direction
        # Batasi scroll
        max_scroll = max(0, len(self.all_items) - self.max_display)
        self.scroll_y = max(0, min(self.scroll_y, max_scroll))

    def draw(self, screen):
        if not self.active: return
        
        # Background Overlay
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((20, 20, 25, 230))
        screen.blit(overlay, (0, 0))
        
        # Main Box
        pygame.draw.rect(screen, (35, 45, 55), self.box_rect)
        pygame.draw.rect(screen, (80, 150, 200), self.box_rect, 3)
        
        # Header Table
        header_y = self.box_rect.y + 10
        col_widths = [50, 160, 100, 360]
        col_x = [self.box_rect.x + 10, self.box_rect.x + 60, self.box_rect.x + 220, self.box_rect.x + 320]
        
        headers = ["ICON", "ITEM", "RARITY", "KETERANGAN & PENGGUNAAN"]
        for i, text in enumerate(headers):
            h_surf = self.font_header.render(text, True, (100, 200, 255))
            screen.blit(h_surf, (col_x[i], header_y))
        
        pygame.draw.line(screen, (80, 150, 200), (self.box_rect.x + 5, header_y + 30), (self.box_rect.right - 5, header_y + 30), 2)

        # Draw List Items
        start_idx = self.scroll_y
        end_idx = min(start_idx + self.max_display, len(self.all_items))
        
        current_y = header_y + 40
        row_height = 35
        
        for i in range(start_idx, end_idx):
            item = self.all_items[i]
            
            # Row Background (Zebra striping)
            if i % 2 == 0:
                pygame.draw.rect(screen, (45, 55, 65), (self.box_rect.x + 5, current_y - 5, self.box_rect.width - 10, row_height))
            
            # Icon Placeholder
            pygame.draw.rect(screen, (60, 70, 80), (col_x[0], current_y, 30, 30))
            
            # Name
            name_surf = self.font_medium.render(item["name"], True, (255, 255, 255))
            screen.blit(name_surf, (col_x[1], current_y + 5))
            
            # Rarity
            rarity_color = self.rarity_colors.get(item["rarity"], (255, 255, 255))
            rarity_surf = self.font_medium.render(item["rarity"], True, rarity_color)
            screen.blit(rarity_surf, (col_x[2], current_y + 5))
            
            # Description (Auto-wrap simple)
            desc_text = item["desc"]
            if len(desc_text) > 45: desc_text = desc_text[:42] + "..."
            desc_surf = self.font_small.render(desc_text, True, (200, 200, 200))
            screen.blit(desc_surf, (col_x[3], current_y + 8))
            
            current_y += row_height
            # Horizontal lines for rows
            pygame.draw.line(screen, (60, 80, 100), (self.box_rect.x + 5, current_y - 5), (self.box_rect.right - 5, current_y - 5), 1)

        # Scrollbar Indicator
        bar_height = self.box_rect.height - 80
        if len(self.all_items) > self.max_display:
            scroll_bar_y = self.box_rect.y + 40 + (self.scroll_y / (len(self.all_items) - self.max_display)) * (bar_height - 30)
            pygame.draw.rect(screen, (100, 200, 255), (self.box_rect.right - 15, scroll_bar_y, 8, 30))

        # Instructions
        instr = self.font_small.render("[ARAH ATAS/BAWAH] Scroll [L] Tutup Daftar", True, (255, 255, 0))
        screen.blit(instr, (self.box_rect.x + 10, self.box_rect.bottom - 20))
