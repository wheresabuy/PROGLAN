import pygame
import os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.bgm_volume = 0.5
        self.sfx_volume = 0.7
        self.current_bgm = None

    def play_bgm(self, filename, loops=-1):
        """Memutar musik latar. loops=-1 berarti looping selamanya."""
        try:
            if self.current_bgm == filename:
                return
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(self.bgm_volume)
            pygame.mixer.music.play(loops)
            self.current_bgm = filename
        except Exception as e:
            print(f"Error playing BGM {filename}: {e}")

    def stop_bgm(self):
        pygame.mixer.music.stop()
        self.current_bgm = None

    def play_sfx(self, filename):
        """Memutar efek suara sekali (misal: ambil item, flashbang)."""
        try:
            sound = pygame.mixer.Sound(filename)
            sound.set_volume(self.sfx_volume)
            sound.play()
        except Exception as e:
            print(f"Error playing SFX {filename}: {e}")

    def set_volumes(self, bgm_vol, sfx_vol):
        self.bgm_volume = bgm_vol
        self.sfx_volume = sfx_vol
        pygame.mixer.music.set_volume(bgm_vol)
