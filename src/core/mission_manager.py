import pygame
from src.missions.mission1 import Mission1Logic
from src.missions.mission2 import Mission2Logic, METRO_START_DIALOGUE

class MissionManager:
    def __init__(self, journal, dialogue):
        self.journal = journal
        self.dialogue = dialogue
        self.current_mission_num = 1
        self.current_mission_logic = Mission1Logic(journal, dialogue)
        self.map_switched = False

    def update(self, player, items, keys, effects=None):
        # Cek transisi misi
        if self.current_mission_num == 1 and self.current_mission_logic.phase == "REPAIRED":
            # Jika player sampai di ujung timur map misi 1 (Pintu Metro)
            if player.pos[0] > 2700 and player.pos[1] > 1300:
                self.next_mission(player)

        self.current_mission_logic.update(player, items, keys, effects)

    def next_mission(self, player):
        self.current_mission_num += 1
        self.map_switched = True
        if self.current_mission_num == 2:
            self.current_mission_logic = Mission2Logic(self.journal, self.dialogue)
            self.dialogue.show(METRO_START_DIALOGUE)
            # Reset posisi player untuk map baru
            player.pos = [100, 100] 
            self.journal.add_entry("MISI 2: Bayangan di Metro.")

    def get_status_text(self, player):
        return self.current_mission_logic.get_status_text(player)

    def get_target_pos(self, player, items):
        return self.current_mission_logic.get_target_pos(player, items)

    def draw_entities(self, screen, camera, player):
        if hasattr(self.current_mission_logic, 'draw_entities'):
            self.current_mission_logic.draw_entities(screen, camera, player)

    @property
    def states(self):
        return self.current_mission_logic.states
