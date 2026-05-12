import pygame

class Spritesheet:
    def __init__(self, filename, cols, rows, scale=1.5):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.cols = cols
        self.rows = rows
        self.scale = scale
        self.fw = self.sheet.get_width() // cols
        self.fh = self.sheet.get_height() // rows
        self.frames = [[None for _ in range(cols)] for _ in range(rows)]
        self._slice()

    def _slice(self):
        for r in range(self.rows):
            for c in range(self.cols):
                frame = self.sheet.subsurface((c * self.fw, r * self.fh, self.fw, self.fh))
                self.frames[r][c] = pygame.transform.scale(frame, (int(self.fw * self.scale), int(self.fh * self.scale)))

    def get_frame(self, row, col):
        return self.frames[row][col]
