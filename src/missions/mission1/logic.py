import pygame
import math
from .story import ECHO_MEMORIES, QUEST_STORY_HINTS, FINAL_TRANSMISSION

class Mission1Logic:
    def __init__(self, journal, dialogue):
        self.journal = journal
        self.dialogue = dialogue
        self.phase = "AWAKENING"
        self.states = {
            "memories_found": 0,
            "generator_on": False,
            "has_photo": False,
            "has_gate_key": False,
            "gate_opened": False,
            "radio_parts": {"Antena": False, "Baterai": False, "Chip": False},
            "echoes": [False for _ in range(len(ECHO_MEMORIES))]
        }

    def update(self, player, items, keys, effects=None):
        # 1. Handle Echo Memories
        for i, (ex, ey, msg) in enumerate(ECHO_MEMORIES):
            dist = math.sqrt((player.pos[0]-ex)**2 + (player.pos[1]-ey)**2)
            if dist < 100 and not self.states["echoes"][i]:
                self.states["echoes"][i] = True
                if effects: effects.trigger_flash(150) # Flashbang durasi panjang
                self.dialogue.show(["*Gema Masa Lalu*", msg])
                self.journal.add_entry(f"Info: {msg}")

        # 2. Logic Gerbang Terkunci
        if 1800 < player.pos[0] < 1900 and 700 < player.pos[1] < 900 and not self.states["gate_opened"]:
            if self.states["has_gate_key"]:
                if keys[pygame.K_e]:
                    self.states["gate_opened"] = True
                    self.dialogue.show(["Membuka gerbang pusat kota...", "Akses ke area timur terbuka."])
            else:
                player.pos[0] -= 5
                self.dialogue.show(["Gerbang ini terkunci rantai.", "Aku butuh kunci gerbang. Sepertinya terjatuh di sekitar area rongsokan di Barat."])

        # 3. Logic Generator
        if 2300 < player.pos[0] < 2400 and 450 < player.pos[1] < 550 and not self.states["generator_on"]:
            has_fuel = any(i.name == "Jerigen Bensin" and i.collected for i in items)
            if has_fuel and keys[pygame.K_e]:
                self.states["generator_on"] = True
                self.dialogue.show(["Listrik menyala! Brankas sekarang aktif."])

        # 4. Check Radio Assembly
        if all(self.states["radio_parts"].values()) and self.phase == "AWAKENING":
            self.phase = "REPAIRED"
            self.dialogue.show(FINAL_TRANSMISSION)

    def get_status_text(self, player):
        if player.injured: return QUEST_STORY_HINTS["injured"]
        if not self.states["has_photo"]: return QUEST_STORY_HINTS["photo"]
        if not self.states["has_gate_key"]: return QUEST_STORY_HINTS["key"]
        if not self.states["gate_opened"]: return QUEST_STORY_HINTS["gate"]
        if not all(self.states["radio_parts"].values()):
            parts = [k for k, v in self.states["radio_parts"].items() if not v]
            return f"QUEST: Rakit Radio (Cari: {', '.join(parts)})"
        return QUEST_STORY_HINTS["exit"]

    def get_target_pos(self, player, items):
        # Menentukan koordinat target berdasarkan progres
        if player.injured: return (250, 300) # Kotak P3K
        if not self.states["has_photo"]: return (150, 150) # Foto
        if not self.states["has_gate_key"]: return (500, 1400) # Kunci
        if not self.states["gate_opened"]: return (1850, 800) # Gerbang
        
        # Cari komponen radio yang belum diambil
        if not self.states["radio_parts"]["Antena"]: return (1500, 400)
        if not self.states["generator_on"]: return (2350, 500) # Ke Generator dulu
        if not self.states["radio_parts"]["Baterai"]: return (2500, 500) # Brankas
        if not self.states["radio_parts"]["Chip"]: return (2700, 100)
        
        return (2700, 1400) # Metro

