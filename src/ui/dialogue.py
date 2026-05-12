import pygame

class DialogueBox:
    def __init__(self, font_size=28):
        self.font = pygame.font.Font(None, font_size)
        self.active = False
        self.messages = []
        self.current_index = 0
        self.box_rect = pygame.Rect(50, 450, 700, 120)

    def show(self, messages):
        if isinstance(messages, str):
            self.messages = [messages]
        else:
            self.messages = messages
        self.current_index = 0
        self.active = True

    def next_message(self):
        self.current_index += 1
        if self.current_index >= len(self.messages):
            self.close()
            return False
        return True

    def close(self):
        self.active = False
        self.messages = []
        self.current_index = 0

    def draw(self, screen):
        if self.active and self.messages:
            # Shadow
            shadow_rect = self.box_rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            pygame.draw.rect(screen, (20, 20, 20), shadow_rect)
            
            # Main Box
            pygame.draw.rect(screen, (40, 40, 60), self.box_rect)
            pygame.draw.rect(screen, (180, 180, 200), self.box_rect, 3)
            
            # Render Text
            text = self.messages[self.current_index]
            text_surface = self.font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (self.box_rect.x + 20, self.box_rect.y + 25))
            
            # Hint to continue
            hint = self.font.render("[Press Enter]", True, (200, 200, 100))
            screen.blit(hint, (self.box_rect.right - 150, self.box_rect.bottom - 35))
