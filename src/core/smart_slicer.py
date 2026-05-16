import pygame

class SmartSlicer:
    """
    Slicer pintar yang mencari 'pulau' pixel (kumpulan pixel yang menyambung)
    untuk dipotong secara otomatis meskipun posisinya tidak beraturan.
    """
    def __init__(self, filename, colorkey=None):
        try:
            self.image = pygame.image.load(filename).convert_alpha()
            # Jika tidak ada transparansi sama sekali, gunakan colorkey
            if colorkey:
                self.image.set_colorkey(colorkey)
            else:
                # Cek jika pixel (0,0) adalah warna solid (bukan transparan)
                # Kita asumsikan itu adalah background jika alpha-nya 255
                bg_color = self.image.get_at((0, 0))
                if bg_color[3] == 255:
                    self.image.set_colorkey(bg_color)
                    # Convert ke surface baru yang punya alpha beneran setelah set_colorkey
                    new_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                    new_surf.blit(self.image, (0,0))
                    self.image = new_surf
        except:
            print(f"Gagal memuat {filename}")
            self.image = None

    def extract_all_items(self, padding=2):
        """
        Mencari semua objek di gambar berdasarkan transparansi.
        Mengembalikan list of Surfaces.
        """
        if not self.image: return []
        
        width, height = self.image.get_size()
        visited = set()
        items = []

        for y in range(height):
            for x in range(width):
                # Jika pixel tidak transparan dan belum dikunjungi
                if self.image.get_at((x, y))[3] > 0 and (x, y) not in visited:
                    # Cari batas objek (bounding box) menggunakan Flood Fill sederhana
                    rect = self._find_bounding_box(x, y, visited)
                    
                    # Tambahkan sedikit padding agar tidak terpotong pas di pinggir
                    rect.inflate_ip(padding, padding)
                    rect.clamp_ip(self.image.get_rect())
                    
                    # Potong gambarnya
                    item_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
                    item_surf.blit(self.image, (0, 0), rect)
                    items.append(item_surf)
        
        return items

    def _find_bounding_box(self, start_x, start_y, visited):
        """Flood fill untuk mencari area objek"""
        width, height = self.image.get_size()
        stack = [(start_x, start_y)]
        min_x, min_y = start_x, start_y
        max_x, max_y = start_x, start_y
        
        while stack:
            x, y = stack.pop()
            if (x, y) in visited: continue
            visited.add((x, y))
            
            # Update bounds
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)
            
            # Cek tetangga (4 arah)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if self.image.get_at((nx, ny))[3] > 0 and (nx, ny) not in visited:
                        stack.append((nx, ny))
        
        return pygame.Rect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
