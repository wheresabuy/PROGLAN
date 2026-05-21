import pygame
import math
import random
from .story import ECHO_M2, QUEST_M2_HINTS, STEALTH_WARNING
from src.entities.zombie import ZombieNPC

class Mission2Logic:
    def __init__(self, journal, dialogue):
        self.journal = journal
        self.dialogue = dialogue
        self.phase = "CHECK_BIO_LOCK"
        self.zombie = ZombieNPC(1500, 1500)
        self.states = {
            "bio_lock_inspected": False,
            "has_access_card": False,
            "generator_b_on": False,
            "has_solvent": False,
            "echoes": [False for _ in range(len(ECHO_M2))],
            "stealth_detected": False
        }
        # Titik-titik sarang alien (Pemain harus pelan di sini)
        self.alien_nests = [(800, 400), (1800, 1200), (500, 1500)]

    def update(self, player, items, keys, effects=None):
        self.zombie.update(player.pos, player.state)
        # 1. Mekanik Stealth (Sangat Kompleks)
        # Jika player LARI (Shift) di dekat sarang, mereka terdeteksi
        for nx, ny in self.alien_nests:
            dist = math.sqrt((player.pos[0]-nx)**2 + (player.pos[1]-ny)**2)
            if dist < 250: # Jarak pendengaran alien
                if player.state == 'run' and not self.states["stealth_detected"]:
                    self.states["stealth_detected"] = True
                    if effects: effects.trigger_flash(30) # Red flash?
                    self.dialogue.show(STEALTH_WARNING)
                    # Hukuman: Reset posisi ke awal koridor
                    player.pos = [player.pos[0] - 100, player.pos[1] - 100]
                    self.states["stealth_detected"] = False
                    return

        # 2. Echo Memories
        for i, (ex, ey, msg) in enumerate(ECHO_M2):
            dist = math.sqrt((player.pos[0]-ex)**2 + (player.pos[1]-ey)**2)
            if dist < 120 and not self.states["echoes"][i]:
                self.states["echoes"][i] = True
                if effects: effects.trigger_flash(80)
                self.dialogue.show(["*Gema Metro*", msg])
                self.journal.add_entry(f"Metro: {msg}")

        # 3. Rantai Teka-teki (Sequential Puzzle)
        # Tahap 1: Periksa Pintu Exit
        if 2200 < player.pos[0] < 2400 and 1500 < player.pos[1] < 1700 and not self.states["bio_lock_inspected"]:
            self.states["bio_lock_inspected"] = True
            self.phase = "FIND_CARD"
            self.dialogue.show([
                "Pintu ini tertutup lendir hijau yang berdenyut.",
                "Sangat keras... senterku bahkan tidak bisa menembusnya.",
                "Aku butuh Kartu Akses untuk masuk ke Lab Medis di ujung Barat,",
                "lalu mencari Cairan Pelarut (Solvent) di sana."
            ])
            self.journal.add_entry("Misi 2: Cari Kartu Akses dari mayat Kapten.")

        # Tahap 2: Generator Check
        if 100 < player.pos[0] < 300 and 100 < player.pos[1] < 300 and not self.states["generator_b_on"]:
            if keys[pygame.K_RETURN]: # Diubah dari K_f ke K_RETURN
                self.states["generator_b_on"] = True
                self.dialogue.show(["Generator Sektor B menyala!", "Pintu Lab Medis sekarang memiliki daya."])

        # Tahap 4: Final Escape
        if self.states["has_solvent"] and 2200 < player.pos[0] < 2400 and 1500 < player.pos[1] < 1700:
            if keys[pygame.K_RETURN]: # Diubah dari K_f ke K_RETURN
                self.phase = "COMPLETED"
                self.dialogue.show([
                    "Menuangkan cairan pelarut ke lendir bio...",
                    "Lendir itu berteriak! Suaranya memekakkan telinga!",
                    "Pintu terbuka! Aku harus lari sebelum mereka mengepungku!"
                ])

    def draw_entities(self, screen, camera, player):
        self.zombie.draw(screen, camera)

        # Font pixel sederhana
        font = pygame.font.SysFont("monospace", 16, bold=True)

        # Peringatan Visual Zombie
        if math.hypot(self.zombie.pos[0] - player.pos[0], self.zombie.pos[1] - player.pos[1]) < 200:
             surf = pygame.Surface((800, 600))
             surf.set_alpha(50)
             surf.fill((200, 0, 0))
             screen.blit(surf, (0, 0))

        # Render Prompts... (dan seterusnya)
        # Generator
        if not self.states["generator_b_on"]:
            if math.hypot(200 - player.pos[0], 200 - player.pos[1]) < 150:
                screen.blit(font.render("Tekan ENTER: Nyalakan Generator", True, (255, 255, 0)), camera.apply((150, 150)))
        
        # Pintu Bio-Lock
        if self.states["has_solvent"] and not self.phase == "COMPLETED":
             if math.hypot(2300 - player.pos[0], 1600 - player.pos[1]) < 150:
                screen.blit(font.render("Tekan ENTER: Gunakan Solvent", True, (255, 255, 0)), camera.apply((2250, 1550)))

    def get_status_text(self, player):
        if not self.states["bio_lock_inspected"]: return QUEST_M2_HINTS["bio_lock"]
        if not self.states["has_access_card"]: return QUEST_M2_HINTS["keycard"]
        if not self.states["generator_b_on"]: return QUEST_M2_HINTS["power_puzzle"]
        if not self.states["has_solvent"]: return QUEST_M2_HINTS["find_solvent"]
        return QUEST_M2_HINTS["escape"]

    def get_target_pos(self, player, items):
        # Kompleks: Tidak ada garis bantuan di Misi 2
        return None
