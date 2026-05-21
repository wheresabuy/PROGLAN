import pygame

class TextInput:
    """A simple text input handler for Pygame."""
    def __init__(self, x, y, width, font_size=20):
        self.rect = pygame.Rect(x, y, width, 40)
        self.font = pygame.font.SysFont("Arial", font_size)
        self.text = ""
        self.active = False
        self.color_active = (100, 200, 255)
        self.color_inactive = (50, 50, 70)
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if not self.active: return None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                result = self.text
                self.text = ""
                self.active = False
                return result
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.active = False
            else:
                if len(self.text) < 40: # Limit length
                    self.text += event.unicode
        return None

    def draw(self, screen):
        if not self.active: return
        
        # Shadow
        pygame.draw.rect(screen, (10, 10, 10), (self.rect.x+2, self.rect.y+2, self.rect.width, self.rect.height), border_radius=5)
        # Main Box
        pygame.draw.rect(screen, self.color_inactive, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.color_active, self.rect, width=2, border_radius=5)
        
        # Render Text
        txt_surf = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(txt_surf, (self.rect.x + 10, self.rect.y + 10))
        
        # Cursor
        self.cursor_timer += 1
        if self.cursor_timer % 30 < 15:
            cx = self.rect.x + 10 + txt_surf.get_width()
            pygame.draw.line(screen, (255, 255, 255), (cx, self.rect.y + 8), (cx, self.rect.y + 32), 2)
            
        # Hint
        hint = self.font.render("Ketik pesanmu dan tekan ENTER", True, (150, 150, 150))
        screen.blit(hint, (self.rect.x, self.rect.y - 25))
