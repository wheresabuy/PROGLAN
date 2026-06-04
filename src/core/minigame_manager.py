import pygame
import sys
from typing import Dict, Optional

class MiniGame:
    """Base class untuk semua sub-game. Memiliki loop sendiri namun tetap dalam satu engine."""
    def __init__(self, screen, clock, manager):
        self.screen = screen
        self.clock = clock
        self.manager = manager
        self.running = True
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 24, bold=True)

    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self): pass
    
    def exit_game(self, result_data=None):
        self.running = False
        self.manager.return_to_main(result_data)

class MiniGameManager:
    """
    Orkestrator yang mengelola transisi antara game utama dan sub-game.
    Memungkinkan 'Sub-Game' berjalan tanpa mengganggu state game utama.
    """
    def __init__(self, main_engine):
        self.main_engine = main_engine
        self.active_game: Optional[MiniGame] = None
        self.saved_main_state = None

    def start_minigame(self, game_class: type):
        print(f"Switching to Mini-Game: {game_class.__name__}")
        self.active_game = game_class(self.main_engine.screen, self.main_engine.clock, self)
        
    def return_to_main(self, result_data):
        print("Returning to Main Game Story...")
        self.active_game = None
        self.last_result = result_data
        # Handle results (e.g., reward player based on score)
        if result_data:
            self.main_engine.currency.add_bronze(result_data.get('score', 0) // 10)

    def update(self, dt):
        if self.active_game:
            self.active_game.update(dt)

    def draw(self):
        if self.active_game:
            self.active_game.draw()
            
    @property
    def in_minigame(self):
        return self.active_game is not None
