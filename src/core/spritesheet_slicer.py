import pygame
import os

class SpriteSheetSlicer:
    """
    Utility untuk memotong sprite sheet secara otomatis dan menghapus background.
    """
    def __init__(self, filename, sprite_width, sprite_height, colorkey=None):
        """
        filename: path ke file sprite sheet (PNG)
        sprite_width, sprite_height: ukuran tiap icon (misal 32x32 atau 48x48)
        colorkey: warna background yang mau dihapus (misal (255, 0, 255) untuk pink)
                  Jika None, akan mengambil warna pixel di (0,0) sebagai background.
        """
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Gagal memuat sprite sheet: {filename}")
            self.sheet = None
            return

        self.sw = sprite_width
        self.sh = sprite_height
        self.colorkey = colorkey

    def get_sprite(self, col, row):
        """
        Mengambil satu sprite berdasarkan kolom dan baris (mulai dari 0).
        """
        if not self.sheet: return None
        
        rect = pygame.Rect(col * self.sw, row * self.sh, self.sw, self.sh)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)

        # Jika colorkey ditentukan, hapus background tersebut
        if self.colorkey is not None:
            image.set_colorkey(self.colorkey)
        
        return image

    def get_all_sprites(self, rows, cols):
        """
        Mengambil semua sprite dalam grid dan mengembalikannya sebagai list.
        """
        sprites = []
        for r in range(rows):
            for c in range(cols):
                sprites.append(self.get_sprite(c, r))
        return sprites

    def map_to_dict(self, item_names_grid):
        """
        Memetakan nama item ke sprite.
        item_names_grid: list of lists berisi nama item sesuai posisi di PNG.
        """
        mapping = {}
        for r, row_names in enumerate(item_names_grid):
            for c, name in enumerate(row_names):
                if name: # Jika nama tidak kosong
                    mapping[name] = self.get_sprite(c, r)
        return mapping
