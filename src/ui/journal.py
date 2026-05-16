import pygame

class JournalManager:
    def __init__(self):
        self.entries = []
        self.active = False
        self.font = pygame.font.SysFont("monospace", 16)

    def add_entry(self, text):
        if text not in self.entries:
            self.entries.append(text)

    def toggle(self):
        self.active = not self.active

    def draw(self, screen):
        if self.active:
            # Draw journal background
            pygame.draw.rect(screen, (40, 40, 40), (100, 50, 600, 500))
            pygame.draw.rect(screen, (255, 255, 255), (100, 50, 600, 500), 2)
            
            # Draw entries
            y = 80
            for entry in self.entries:
                lines = self._wrap_text(entry, 60)
                for line in lines:
                    text_surface = self.font.render(line, True, (200, 200, 200))
                    screen.blit(text_surface, (120, y))
                    y += 30
                y += 20

    def _wrap_text(self, text, max_chars):
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            if len(' '.join(current_line + [word])) <= max_chars:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        return lines
