import pygame
from src.missions.mission1 import Mission1Logic
from src.missions.mission2 import Mission2Logic, METRO_START_DIALOGUE
from src.missions.mission3 import Mission3Logic, PROLOGUE_M3

class MissionManager:
    def __init__(self, journal, dialogue, start_mission=1):
        self.journal = journal
        self.dialogue = dialogue
        self.current_mission_num = start_mission
        self.map_switched = False
        
        if start_mission == 1:
            self.current_mission_logic = Mission1Logic(journal, dialogue)
        elif start_mission == 3:
            self.current_mission_logic = Mission3Logic(journal, dialogue)
            self.dialogue.show(PROLOGUE_M3)
            self.journal.add_entry("MISI 3: The Sanctuary - Harapan Terakhir.")
        else:
            self.current_mission_logic = Mission1Logic(journal, dialogue)

    def update(self, player, items, keys, effects=None, events=None):
        # Cek transisi misi
        if self.current_mission_num == 1 and self.current_mission_logic.phase == "REPAIRED":
            if player.pos[0] > 2700 and player.pos[1] > 1300:
                self.next_mission(player)
        elif self.current_mission_num == 2 and self.current_mission_logic.phase == "COMPLETED":
            if player.pos[0] > 2200 and player.pos[1] > 1500:
                self.next_mission(player)

        # Pass events for AI input handling in Mission 3
        if hasattr(self.current_mission_logic, 'update'):
            import inspect
            sig = inspect.signature(self.current_mission_logic.update)
            if 'events' in sig.parameters:
                self.current_mission_logic.update(player, items, keys, effects, events)
            else:
                self.current_mission_logic.update(player, items, keys, effects)

    def next_mission(self, player):
        self.current_mission_num += 1
        self.map_switched = True
        if self.current_mission_num == 2:
            self.current_mission_logic = Mission2Logic(self.journal, self.dialogue)
            self.dialogue.show(METRO_START_DIALOGUE)
            player.pos = [100, 100] 
            self.journal.add_entry("MISI 2: Bayangan di Metro.")
        elif self.current_mission_num == 3:
            self.current_mission_logic = Mission3Logic(self.journal, self.dialogue)
            self.dialogue.show(PROLOGUE_M3)
            player.pos = [200, 200]
            self.journal.add_entry("MISI 3: The Sanctuary - Harapan Terakhir.")

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
