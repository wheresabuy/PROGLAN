import pygame
import sys
from src.entities.player import Player
from src.entities.loot import Loot
from src.ui.dialogue import DialogueBox
from src.ui.journal import JournalManager
from src.ui.inventory import Inventory
from src.ui.hud import HUD
from src.core.currency import CurrencyManager
from src.core.camera import Camera
from src.core.mission_manager import MissionManager
from src.core.visual_effects import VisualEffects
from src.missions.mission1 import PROLOG_DIALOGUE
from comvis.gestures import GestureThread

class KeyProxy:
    def __init__(self, keys_pressed):
        self.keys_pressed = keys_pressed
        self.overrides = {}
    
    def __getitem__(self, key):
        return self.overrides.get(key, self.keys_pressed[key])

def load_mission_assets(mission_num):
    if mission_num == 1:
        bg = pygame.image.load("assets/images/background.png").convert()
        items = [
            Loot("Kotak P3K", 250, 300, "medkit", "assets/images/p3k.png"),
            Loot("Baju Survival", 300, 500, "clothing", "assets/images/chip.png"),
            Loot("Foto Kusam", 150, 150, "photo"),
            Loot("Kunci Gerbang", 500, 1400, "key", "assets/images/kuncigerbang.png"),
            Loot("Jerigen Bensin", 2200, 1400, "fuel", "assets/images/jerigenbensin.png"),
            Loot("Antena Radio", 1500, 400, "antenna", "assets/images/antena.png"),
            Loot("Baterai Militer", 2500, 500, "safe", "assets/images/brankas.png"),
            Loot("Chip Frekuensi", 2700, 100, "chip", "assets/images/chip.png"),
            Loot("Catatan Militer", 1000, 1000, "note", "assets/images/surat-removebg-preview.png"),
            Loot("Generator", 2350, 500, "decoration", "assets/images/generator.png"),
            Loot("Mayat Ilmuwan", 2700, 150, "decoration", "assets/images/mayat.png")
        ]
        map_size = (2816, 1536)
    else: # Misi 2
        bg = pygame.image.load("assets/images/background_mission2.png").convert()
        items = [
            Loot("Kartu Akses Kapten", 1100, 1000, "card", "assets/images/kuncigerbang.png"),
            Loot("Cairan Pelarut", 200, 200, "solvent", "assets/images/p3k.png"),
            Loot("Baterai Cadangan", 2000, 1500, "battery", "assets/images/jerigenbensin.png"),
            Loot("Mayat Kapten", 1100, 1050, "decoration", "assets/images/mayat.png")
        ]
        map_size = (2400, 1792)
    return bg, items, map_size

if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Project 23 - Survival")
    clock = pygame.time.Clock()

    # Inisialisasi Gesture Control (Thread)
    camera_path = 'http://10.193.124.171:8080/video'
    gesture_thread = GestureThread(camera_path)
    gesture_thread.start()

    player = Player(200, 200)
    dialogue = DialogueBox()
    journal = JournalManager()
    inventory = Inventory()
    currency = CurrencyManager()
    hud = HUD(currency)
    
    mission = MissionManager(journal, dialogue)
    effects = VisualEffects(WIDTH, HEIGHT)

    bg_img, items, map_size = load_mission_assets(1)
    camera = Camera(WIDTH, HEIGHT, map_size[0], map_size[1])

    flashlight_on = False
    battery_level = 0.0
    font_pixel = pygame.font.SysFont("monospace", 16, bold=True)
    dialogue.show(PROLOG_DIALOGUE)

    while True:
        if mission.map_switched:
            mission.map_switched = False
            bg_img, items, map_size = load_mission_assets(mission.current_mission_num)
            camera = Camera(WIDTH, HEIGHT, map_size[0], map_size[1])
            effects.trigger_flash(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gesture_thread.stop()
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j: journal.toggle()
                if event.key == pygame.K_i: inventory.toggle()
                if event.key == pygame.K_f and battery_level > 0: flashlight_on = not flashlight_on
                if dialogue.active and event.key == pygame.K_RETURN: dialogue.next_message()

        # Gabungkan input Keyboard & Gestur menggunakan Proxy
        keys = KeyProxy(pygame.key.get_pressed())
        
        # Mapping gestur ke key virtual
        current_g = gesture_thread.current_gesture
        if current_g in ["ATAS", "ATAS1"]:
            keys.overrides[pygame.K_UP] = True
        elif current_g == "BAWAH":
            keys.overrides[pygame.K_DOWN] = True
        elif current_g == "KIRI":
            keys.overrides[pygame.K_LEFT] = True
        elif current_g == "KANAN":
            keys.overrides[pygame.K_RIGHT] = True
        elif current_g == "AMBIL_BARANG":
            keys.overrides[pygame.K_RETURN] = True

        if not any([journal.active, inventory.active, dialogue.active]):
            player.update(keys)
            mission.update(player, items, keys, effects)
        
        camera.update(player.pos)
        if flashlight_on: battery_level -= 0.01

        if not dialogue.active:
            for item in items:
                if item.check_interaction(player.pos) and not item.collected and keys[pygame.K_RETURN]:
                    if item.item_type == "clothing":
                        item.collected = True; player.clothing_active = True; dialogue.show(["Mendapatkan Baju Survival. Karakter mengenakannya secara otomatis."])
                    elif item.item_type == "adrenalin":
                        item.collected = True; player.adrenaline_timer = 300; dialogue.show(["Menggunakan Adrenalin! Kecepatan meningkat!"])
                    elif item.item_type == "medkit":
                        item.collected = True; player.injured = False; player.speed_multiplier = 1.0
                        effects.trigger_flash(60); dialogue.show(["Luka mulai membaik."])
                    elif item.item_type == "photo":
                        item.collected = True; mission.states["has_photo"] = True; dialogue.show(["Foto keluargaku..."])
                    elif item.item_type == "key":
                        item.collected = True; mission.states["has_gate_key"] = True; dialogue.show(["Kunci Gerbang Kota."])
                    elif item.item_type == "card":
                        item.collected = True; mission.states["has_access_card"] = True; dialogue.show(["Mendapatkan Kartu Akses Kapten."])
                    elif item.item_type == "solvent":
                        if mission.states.get("generator_b_on", False):
                            item.collected = True; mission.states["has_solvent"] = True
                            dialogue.show(["Mendapatkan Cairan Pelarut (Solvent)."])
                        else:
                            dialogue.show(["Pintu Lab terkunci. Butuh daya dari Generator Sektor B (Utara)."])
                    elif item.item_type == "safe" and mission.states.get("generator_on", False):
                        item.collected = True; mission.states["radio_parts"]["Baterai"] = True; battery_level = 100; dialogue.show(["Mendapatkan baterai."])
                    elif item.item_type in ["antenna", "chip", "fuel"]:
                        item.collected = True; inventory.add_item(item.name, item.image)
                        if item.item_type == "antenna": mission.states["radio_parts"]["Antena"] = True
                        if item.item_type == "chip": mission.states["radio_parts"]["Chip"] = True
                        dialogue.show([f"Mengambil {item.name}."])

        screen.blit(bg_img, camera.apply((0, 0)))
        target_pos = mission.get_target_pos(player, items)
        if target_pos:
            start_p = camera.apply((player.pos[0]+32, player.pos[1]+32))
            end_p = camera.apply(target_pos)
            pygame.draw.line(screen, (255, 255, 0), start_p, end_p, 1)
            pygame.draw.circle(screen, (255, 255, 0), end_p, 5, 1)

        for item in items:
            if not item.collected:
                item.draw(screen, player.pos, camera)
                if item.check_interaction(player.pos):
                    prompt_text = item.get_interaction_prompt()
                    text_surf = font_pixel.render(prompt_text, True, (255, 255, 0))
                    draw_pos = camera.apply(item.pos)
                    screen.blit(text_surf, (draw_pos[0] - 20, draw_pos[1] - 30))
        player.draw(screen, camera)
        if mission.current_mission_num == 2:
            mission.draw_entities(screen, camera, player)

        if not journal.active and not inventory.active:
            effects.draw_darkness(screen, player.pos, camera, flashlight_on, battery_level, player.injured)
            effects.draw_flash(screen)

        dialogue.draw(screen); journal.draw(screen); inventory.draw(screen)
        status_text = mission.get_status_text(player)
        pygame.draw.rect(screen, (0,0,0,150), (10, HEIGHT-35, 450, 25))
        screen.blit(font_pixel.render(status_text, True, (255, 255, 0)), (15, HEIGHT-30))
        
        if battery_level >= 0:
            bar_color = (50, 200, 50) if battery_level > 20 else (200, 50, 50)
            pygame.draw.rect(screen, (50, 50, 50), (10, 10, 100, 10))
            pygame.draw.rect(screen, bar_color, (10, 10, int(battery_level), 10))
            screen.blit(font_pixel.render(f"FLASHLIGHT: {int(battery_level)}%", True, (255, 255, 255)), (10, 25))

        hud.draw(screen)
        pygame.display.flip()
        clock.tick(60)
