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
from src.core.crafting_system import CraftingSystem
from src.ui.item_codex import ItemCodex
from src.core.smart_slicer import SmartSlicer
from src.entities.tactical_item import TacticalItem
from comvis.gestures import GestureThread

class KeyProxy:
    def __init__(self, keys_pressed):
        self.keys_pressed = keys_pressed
        self.overrides = {}
    
    def __getitem__(self, key):
        return self.overrides.get(key, self.keys_pressed[key])

def load_mission_assets(mission_num, icon_map):
    # Default icon jika tidak ketemu
    def get_icon(name):
        return icon_map.get(name, pygame.Surface((32, 32)))

    if mission_num == 1:
        bg = pygame.image.load("assets/images/background.png").convert()
        items = [
            Loot("Kotak P3K", 250, 300, "medkit", get_icon("Pembalut Lukaku")),
            Loot("Baju Survival", 300, 500, "clothing", get_icon("Kain Bekas")),
            Loot("Foto Kusam", 150, 150, "photo"),
            Loot("Kunci Gerbang", 500, 1400, "key", get_icon("Lempeng Besi")),
            Loot("Jerigen Bensin", 2200, 1400, "fuel", get_icon("Jerigen Bensin")),
            Loot("Antena Radio", 1500, 400, "antenna", get_icon("Antena Radio")),
            Loot("Baterai Militer", 2500, 500, "safe", get_icon("Baterai Militer")),
            Loot("Chip Frekuensi", 2700, 100, "chip", get_icon("Chip Frekuensi")),
            Loot("Catatan Militer", 1000, 1000, "note", get_icon("Kain Bekas")),
            Loot("Generator", 2350, 500, "decoration", get_icon("Lempeng Besi")),
            Loot("Mayat Ilmuwan", 2700, 150, "decoration", get_icon("Kain Bekas")),
            
            # --- ITEM BARU UNTUK CRAFTING ---
            Loot("Kabel", 400, 600, "material", get_icon("Kabel")),
            Loot("Botol Kosong", 600, 200, "material", get_icon("Botol Kosong")),
            Loot("Kain Bekas", 800, 1100, "material", get_icon("Kain Bekas")),
            Loot("Tanaman Obat", 1200, 300, "material", get_icon("Tanaman Obat")),
            Loot("Lempeng Besi", 2000, 1200, "material", get_icon("Lempeng Besi")),
            Loot("Sepatu Tua", 100, 1400, "material", get_icon("Kain Bekas")),
            Loot("Mata Air", 1800, 100, "decoration", get_icon("Mata Air")),
            Loot("Pembalut Lukaku", 2400, 800, "material", get_icon("Pembalut Lukaku"))
        ]
        map_size = (2816, 1536)
    elif mission_num == 2:
        bg = pygame.image.load("assets/images/background_mission2.png").convert()
        items = [
            Loot("Kartu Akses Kapten", 1100, 1000, "card", get_icon("Chip Frekuensi")),
            Loot("Cairan Pelarut", 200, 200, "solvent", get_icon("Cairan Pelarut")),
            Loot("Baterai Cadangan", 2000, 1500, "battery", get_icon("Baterai Cadangan")),
            Loot("Mayat Kapten", 1100, 1050, "decoration", get_icon("Kain Bekas"))
        ]
        map_size = (2400, 1792)
    elif mission_num == 3:
        # Menggunakan background mission 1 sebagai placeholder atau bisa diganti asset baru
        bg = pygame.image.load("assets/images/background.png").convert() 
        items = [] # Misi 3 lebih fokus ke NPC daripada loot liar
        map_size = (4000, 3000) # Map sangat besar!
    return bg, items, map_size

if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Project 23 - Survival")
    clock = pygame.time.Clock()

    # Ekstraksi Icon Sekali di Awal (Optimasi + Fuzzy Background Removal)
    sheet = pygame.image.load("assets/images/items_all.png").convert_alpha()
    bg_color = sheet.get_at((0, 0)) # Ambil warna acuan background
    
    sw, sh = sheet.get_width() // 4, sheet.get_height() // 4
    icons = []
    
    threshold = 30 # Toleransi warna background (AI noise)
    
    for r in range(4):
        for c in range(4):
            rect = pygame.Rect(c*sw, r*sh, sw, sh)
            icon_surf = sheet.subsurface(rect).copy()
            
            # Fuzzy background removal (Hapus noise background)
            pixel_array = pygame.PixelArray(icon_surf)
            for x in range(icon_surf.get_width()):
                for y in range(icon_surf.get_height()):
                    curr_color = icon_surf.unmap_rgb(pixel_array[x, y])
                    # Hitung jarak warna (Euclidean distance sederhana)
                    dist = sum([abs(curr_color[i] - bg_color[i]) for i in range(3)])
                    if dist < threshold:
                        pixel_array[x, y] = (0, 0, 0, 0) # Jadikan transparan total
            del pixel_array # Penting untuk unlock surface
            icons.append(icon_surf)
    
    item_names = [
        "Kain Bekas", "Baterai Cadangan", "Cairan Pelarut", "Antena Radio",
        "Botol Kosong", "Lempeng Besi", "Jerigen Bensin", "Hacking Tool",
        "Kabel", "Mata Air", "Signal Booster", "Baterai Militer",
        "Tanaman Obat", "Pembalut Lukaku", "Baterai Militer 2", "Chip Frekuensi"
    ]
    icon_map = {name: icons[i] for i, name in enumerate(item_names) if i < len(icons)}

    # Inisialisasi Gesture Control (Thread)
    gesture_thread = GestureThread(0)
    gesture_thread.start()

    # Inisialisasi Crafting & Codex
    crafting_system = CraftingSystem()
    item_codex = ItemCodex()

    player = Player(400, 400) # Mulai di posisi default misi 1
    dialogue = DialogueBox()
    journal = JournalManager()
    inventory = Inventory()
    inventory.crafting_system = crafting_system
    
    currency = CurrencyManager()
    hud = HUD(currency)
    
    # Mulai dari MISI 1
    mission = MissionManager(journal, dialogue, start_mission=1)
    effects = VisualEffects(WIDTH, HEIGHT)

    bg_img, items, map_size = load_mission_assets(1, icon_map)
    camera = Camera(WIDTH, HEIGHT, map_size[0], map_size[1])

    # List untuk menampung item taktis yang aktif di map
    active_tacticals = []
    # List zombie
    from src.entities.zombie import ZombieNPC
    zombies = [ZombieNPC(1000, 500), ZombieNPC(1500, 800), ZombieNPC(2000, 300)]

    flashlight_on = False
    battery_level = 100.0 # Baterai mulai penuh
    font_pixel = pygame.font.SysFont("monospace", 14) 
    dialogue.show(PROLOG_DIALOGUE)

    while True:
        if mission.map_switched:
            mission.map_switched = False
            bg_img, items, map_size = load_mission_assets(mission.current_mission_num, icon_map)
            camera = Camera(WIDTH, HEIGHT, map_size[0], map_size[1])
            effects.trigger_flash(200)

        events = pygame.event.get()
        current_g = gesture_thread.current_gesture # Baca gestur SEKALI per frame

        for event in events:
            if event.type == pygame.QUIT:
                gesture_thread.stop()
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if item_codex.active:
                    if event.key == pygame.K_UP: item_codex.scroll(-1)
                    if event.key == pygame.K_DOWN: item_codex.scroll(1)
                    if event.key == pygame.K_l: item_codex.toggle()
                    continue

                if inventory.active:
                    if event.key == pygame.K_UP: inventory.move_cursor(0, -1)
                    if event.key == pygame.K_DOWN: inventory.move_cursor(0, 1)
                    if event.key == pygame.K_LEFT: inventory.move_cursor(-1, 0)
                    if event.key == pygame.K_RIGHT: inventory.move_cursor(1, 0)
                    if event.key == pygame.K_RETURN: inventory.select_item()
                    if event.key == pygame.K_c:
                        msg = inventory.attempt_craft()
                        if msg: dialogue.show([msg])
                    if event.key == pygame.K_u:
                        used_item = inventory.attempt_use()
                        if used_item:
                            inventory.toggle()
                            if used_item == "Bom Molotov":
                                target = [player.pos[0] + 150, player.pos[1]]
                                active_tacticals.append(TacticalItem(player.pos[0], player.pos[1], "Molotov", target))
                            elif used_item == "Umpan Elektronik":
                                active_tacticals.append(TacticalItem(player.pos[0], player.pos[1], "Decoy"))
                            elif used_item == "Taser Rakitan":
                                active_tacticals.append(TacticalItem(player.pos[0], player.pos[1], "Taser"))
                            elif used_item == "Medkit Medis":
                                player.health = 100; player.injured = False; player.speed_multiplier = 1.0
                                dialogue.show(["Menggunakan Medkit. Luka sembuh total!"])
                            elif used_item in ["Baterai Militer", "Baterai Cadangan"]:
                                battery_level = min(100.0, battery_level + 50.0)
                                dialogue.show(["Baterai senter terisi kembali!"])
                
                if event.key == pygame.K_j: journal.toggle()
                if event.key == pygame.K_i: inventory.toggle()
                if event.key == pygame.K_l: item_codex.toggle()
                if event.key == pygame.K_f:
                    if battery_level > 0: flashlight_on = not flashlight_on
                    else: dialogue.show(["Baterai habis! Cari baterai cadangan."])
                if dialogue.active and event.key == pygame.K_RETURN: dialogue.next_message()

        keys = KeyProxy(pygame.key.get_pressed())
        # Optimasi: Gunakan gestur untuk mensimulasikan KEYDOWN event agar tidak berulang (debounce)
        # Namun untuk movement, tetap gunakan state keys.overrides
        if not inventory.active:
            if current_g == "ATAS": keys.overrides[pygame.K_UP] = True
            elif current_g == "BAWAH": keys.overrides[pygame.K_DOWN] = True
            elif current_g == "KIRI": keys.overrides[pygame.K_LEFT] = True
            elif current_g == "KANAN": keys.overrides[pygame.K_RIGHT] = True
            elif current_g in ["AMBIL", "ENTER"]: keys.overrides[pygame.K_RETURN] = True
        
        # Penanganan Baterai Habis
        if battery_level <= 0:
            battery_level = 0
            flashlight_on = False

        # --- UPDATE LOGIC RESTORATION ---
        can_update = not any([journal.active, inventory.active, dialogue.active, item_codex.active])
        if hasattr(mission.current_mission_logic, 'text_input') and mission.current_mission_logic.text_input.active:
            can_update = True 

        if can_update:
            player.update(keys, map_size=map_size) # Hardened with map_size
            mission.update(player, items, keys, effects, events)
            for t in active_tacticals[:]:
                t.update()
                if not t.active: active_tacticals.remove(t)
            for z in zombies:
                z.update(player.pos, player.state, active_tacticals)
        # --- END RESTORATION ---

        camera.update(player.pos) # FIX: Kamera harus update tiap frame!

        if not dialogue.active:
            for item in items:
                if item.check_interaction(player.pos) and not item.collected and keys[pygame.K_RETURN]:
                    if item.item_type in ["antenna", "chip", "fuel", "material", "card", "key", "note", "battery", "solvent"]:
                        item.collected = True
                        inventory.add_item(item.name, item.image)
                        if item.item_type == "antenna": mission.states["radio_parts"]["Antena"] = True
                        if item.item_type == "chip": mission.states["radio_parts"]["Chip"] = True
                        if item.item_type == "card": mission.states["has_access_card"] = True
                        if item.item_type == "key": mission.states["has_gate_key"] = True
                        if item.item_type == "solvent": mission.states["has_solvent"] = True
                        dialogue.show([f"Mengambil {item.name}."])
                    elif item.item_type == "clothing":
                        item.collected = True; player.clothing_active = True; dialogue.show(["Mendapatkan Baju Survival."])
                    elif item.item_type == "adrenalin":
                        item.collected = True; player.adrenaline_timer = 300; dialogue.show(["Menggunakan Adrenalin!"])
                    elif item.item_type == "medkit":
                        item.collected = True; player.injured = False; player.speed_multiplier = 1.0
                        effects.trigger_flash(60); dialogue.show(["Luka mulai membaik."])
                    elif item.item_type == "photo":
                        item.collected = True; mission.states["has_photo"] = True; dialogue.show(["Foto keluargaku..."])
                    elif item.item_type == "safe" and mission.states.get("generator_on", False):
                        item.collected = True; mission.states["radio_parts"]["Baterai"] = True; battery_level = 100; dialogue.show(["Mendapatkan baterai."])

        if hasattr(mission.current_mission_logic, 'draw_ground'):
            mission.current_mission_logic.draw_ground(screen, camera)
        else:
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
        
        for t in active_tacticals: t.draw(screen, camera)
        for z in zombies: z.draw(screen, camera)
        player.draw(screen, camera)
        
        if mission.current_mission_num in [2, 3]:
            mission.draw_entities(screen, camera, player)

        if not journal.active and not inventory.active:
            effects.draw_darkness(screen, player.pos, camera, flashlight_on, battery_level, player.injured)
            effects.draw_flash(screen)

        dialogue.draw(screen); journal.draw(screen); inventory.draw(screen); item_codex.draw(screen)
        status_text = mission.get_status_text(player)
        pygame.draw.rect(screen, (0,0,0,150), (10, HEIGHT-35, 450, 25))
        screen.blit(font_pixel.render(status_text, True, (255, 255, 0)), (15, HEIGHT-30))
        
        if battery_level >= 0:
            bar_color = (50, 200, 50) if battery_level > 20 else (200, 50, 50)
            pygame.draw.rect(screen, (50, 50, 50), (10, 10, 100, 10))
            pygame.draw.rect(screen, bar_color, (10, 10, int(battery_level), 10))
            screen.blit(font_pixel.render(f"FLASHLIGHT: {int(battery_level)}%", True, (255, 255, 255)), (10, 25))

        hud.draw(screen, player, battery_level)
        pygame.display.flip()
        clock.tick(60)
