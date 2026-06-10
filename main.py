import pygame
import sys
from src.entities.entities import Player
from src.ui.dialogue import DialogueBox
from src.ui.hud import HUD
from src.core.engine import CurrencyManager, Camera, VisualEffects, MiniGameManager
from src.core.sanctuary_logic import SanctuaryLogic
from comvis.gestures import GestureThread
class InputProxy:
    def __init__(self, keys_pressed):
        self.keys = keys_pressed
        self.overrides = {}
    def __getitem__(self, key):
        return self.overrides.get(key, self.keys[key])
def main():
    pygame.init()
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("City Under Attack - Sanctuary Defense")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)
    weapon_upgrades = {"damage_level": 0, "ammo_level": 0, "reload_level": 0, "firerate_level": 0}
    selected_weapon = "SHOTGUN"
    player = Player(500, 450)
    camera = Camera(WIDTH, HEIGHT, 2560, 1440)
    dialogue = DialogueBox()
    currency = CurrencyManager()
    hud = HUD(currency)
    effects = VisualEffects(WIDTH, HEIGHT)
    game_logic = SanctuaryLogic(dialogue)
    dialogue.box_rect = pygame.Rect(100, 500, 1080, 150)
    gesture_thread = GestureThread(0)
    gesture_thread.start()
    class EngineProxy:
        def __init__(self, s, c, cur, upg, gt, sw):
            self.screen = s
            self.clock = c
            self.currency = cur
            self.weapon_upgrades = upg
            self.gesture_thread = gt
            self.selected_weapon = sw
            self.point_kill = 0
    engine_proxy = EngineProxy(screen, clock, currency, weapon_upgrades, gesture_thread, "SHOTGUN")
    minigame_manager = MiniGameManager(engine_proxy)
    smoothed_hx = WIDTH // 2
    smoothed_hy = HEIGHT // 2
    SKIN_OPTIONS = [
        f"FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v{str(i).zfill(2)}.png"
        for i in range(11)
    ]
    SKIN_NAMES = [f"Human Skin {i+1}" for i in range(11)]
    OUTFIT_OPTIONS = [
        None,
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_undi_v01.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_boxr_v01.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v01.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v02.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v03.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v04.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v05.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_pfpn_v01.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_pfpn_v02.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_pfpn_v03.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_pfpn_v04.png",
        "FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_pfpn_v05.png",
    ]
    OUTFIT_NAMES = [
        "Bare / Tanpa Baju",
        "Underwear (Undies)",
        "Boxer Shorts",
        "Forester Uniform (Blue)",
        "Forester Uniform (Brown)",
        "Forester Uniform (Green)",
        "Forester Uniform (Beige)",
        "Forester Uniform (Red)",
        "Peasant Pants (Blue)",
        "Peasant Pants (Green)",
        "Peasant Pants (Brown)",
        "Peasant Pants (Purple)",
        "Peasant Pants (Black)",
    ]
    HAIR_OPTIONS = [None]
    HAIR_NAMES = ["Bald / Gundul"]
    for i in range(14):
        HAIR_OPTIONS.append(f"FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_bob1_v{str(i).zfill(2)}.png")
        HAIR_NAMES.append(f"Bob Cut Hair v{str(i).zfill(2)}")
    for i in range(14):
        HAIR_OPTIONS.append(f"FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_dap1_v{str(i).zfill(2)}.png")
        HAIR_NAMES.append(f"Dapper Hair v{str(i).zfill(2)}")
    HAT_OPTIONS = [None]
    HAT_NAMES = ["No Hat / Tanpa Topi"]
    for i in range(1, 6):
        HAT_OPTIONS.append(f"FREE Mana Seed Character Base Demo 2.0/char_a_p1/5hat/char_a_p1_5hat_pfht_v{str(i).zfill(2)}.png")
        HAT_NAMES.append(f"Farmer Straw Hat v{str(i).zfill(2)}")
    for i in range(1, 6):
        HAT_OPTIONS.append(f"FREE Mana Seed Character Base Demo 2.0/char_a_p1/5hat/char_a_p1_5hat_pnty_v{str(i).zfill(2)}.png")
        HAT_NAMES.append(f"Pointy Wizard Hat v{str(i).zfill(2)}")
    wardrobe_active = False
    wardrobe_category = 0
    wardrobe_indices = [0, 3, 23, 0]
    upgrade_shop_active = False
    upgrade_shop_category = 0
    UPGRADE_COSTS = [100, 250, 500]
    # weapon_upgrades defined early
    def update_player_wardrobe():
        from src.core.engine import Spritesheet
        player.sheet = Spritesheet(SKIN_OPTIONS[wardrobe_indices[0]], 8, 8, scale=2.0)
        outfit_path = OUTFIT_OPTIONS[wardrobe_indices[1]]
        if outfit_path:
            player.clothing_sheet = Spritesheet(outfit_path, 8, 8, scale=2.0)
            player.clothing_active = True
        else:
            player.clothing_sheet = None
            player.clothing_active = False
        hair_path = HAIR_OPTIONS[wardrobe_indices[2]]
        if hair_path:
            player.hair_sheet = Spritesheet(hair_path, 8, 8, scale=2.0)
        else:
            player.hair_sheet = None
        hat_path = HAT_OPTIONS[wardrobe_indices[3]]
        if hat_path:
            player.hat_sheet = Spritesheet(hat_path, 8, 8, scale=2.0)
        else:
            player.hat_sheet = None
    update_player_wardrobe()
    while True:
        dt = clock.tick(60) / 16.67
        events = pygame.event.get()
        gesture_thread.in_minigame = minigame_manager.in_minigame
        current_g = gesture_thread.current_gesture
        h_pos = gesture_thread.hand_pos
        if wardrobe_active:
            for event in events:
                if event.type == pygame.QUIT:
                    gesture_thread.stop()
                    gesture_thread.join(timeout=1.0)
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        wardrobe_category = (wardrobe_category - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        wardrobe_category = (wardrobe_category + 1) % 4
                    elif event.key == pygame.K_LEFT:
                        if wardrobe_category == 0:
                            wardrobe_indices[0] = (wardrobe_indices[0] - 1) % len(SKIN_OPTIONS)
                        elif wardrobe_category == 1:
                            wardrobe_indices[1] = (wardrobe_indices[1] - 1) % len(OUTFIT_OPTIONS)
                        elif wardrobe_category == 2:
                            wardrobe_indices[2] = (wardrobe_indices[2] - 1) % len(HAIR_OPTIONS)
                        elif wardrobe_category == 3:
                            wardrobe_indices[3] = (wardrobe_indices[3] - 1) % len(HAT_OPTIONS)
                        update_player_wardrobe()
                    elif event.key == pygame.K_RIGHT:
                        if wardrobe_category == 0:
                            wardrobe_indices[0] = (wardrobe_indices[0] + 1) % len(SKIN_OPTIONS)
                        elif wardrobe_category == 1:
                            wardrobe_indices[1] = (wardrobe_indices[1] + 1) % len(OUTFIT_OPTIONS)
                        elif wardrobe_category == 2:
                            wardrobe_indices[2] = (wardrobe_indices[2] + 1) % len(HAIR_OPTIONS)
                        elif wardrobe_category == 3:
                            wardrobe_indices[3] = (wardrobe_indices[3] + 1) % len(HAT_OPTIONS)
                        update_player_wardrobe()
                    elif event.key == pygame.K_RETURN:
                        wardrobe_active = False
            game_logic.draw_ground(screen, camera)
            game_logic.draw_entities(screen, camera, player)
            player.draw(screen, camera)
            effects.draw_flash(screen)
            dialogue.draw(screen)
            hud.draw(screen, player, 100)
            overlay_w, overlay_h = 720, 440
            ox = (WIDTH - overlay_w) // 2
            oy = (HEIGHT - overlay_h) // 2
            s = pygame.Surface((overlay_w, overlay_h), pygame.SRCALPHA)
            pygame.draw.rect(s, (10, 15, 20, 240), (0, 0, overlay_w, overlay_h), border_radius=15)
            pygame.draw.rect(s, (0, 255, 255, 180), (0, 0, overlay_w, overlay_h), 2, border_radius=15)
            screen.blit(s, (ox, oy))
            font_title = pygame.font.SysFont("Arial", 22, bold=True)
            font_body = pygame.font.SysFont("Arial", 15, bold=True)
            font_option = pygame.font.SysFont("Arial", 14)
            font_hint = pygame.font.SysFont("Arial", 13)
            title_surf = font_title.render("KUSTOMISASI PENGEMBARA (WARDROBE)", True, (0, 255, 255))
            screen.blit(title_surf, (ox + 30, oy + 20))
            pygame.draw.line(screen, (0, 100, 100), (ox + 30, oy + 50), (ox + overlay_w - 30, oy + 50), 2)
            pygame.draw.rect(screen, (20, 30, 40, 255), (ox + 30, oy + 65, 180, 290), border_radius=10)
            pygame.draw.rect(screen, (0, 150, 150, 100), (ox + 30, oy + 65, 180, 290), 1, border_radius=10)
            preview_lbl = font_hint.render("PREVIEW", True, (0, 200, 200))
            screen.blit(preview_lbl, (ox + 30 + (180 - preview_lbl.get_width()) // 2, oy + 75))
            pygame.draw.ellipse(screen, (0, 255, 255, 70), (ox + 60, oy + 265, 120, 25))
            preview_timer = getattr(player, 'preview_timer', 0) + 1
            player.preview_timer = preview_timer
            preview_col = (preview_timer // 8) % 6
            preview_row = 4
            preview_surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            preview_surf.blit(player.sheet.get_frame(preview_row, preview_col), (0, 0))
            if player.clothing_active and player.clothing_sheet:
                preview_surf.blit(player.clothing_sheet.get_frame(preview_row, preview_col), (0, 0))
            if player.hair_sheet:
                preview_surf.blit(player.hair_sheet.get_frame(preview_row, preview_col), (0, 0))
            if player.hat_sheet:
                preview_surf.blit(player.hat_sheet.get_frame(preview_row, preview_col), (0, 0))
            scaled_preview = pygame.transform.scale(preview_surf, (160, 160))
            screen.blit(scaled_preview, (ox + 40, oy + 105))
            categories = [
                ("1. KULIT / SKIN", SKIN_NAMES[wardrobe_indices[0]]),
                ("2. SET BAJU & CELANA", OUTFIT_NAMES[wardrobe_indices[1]]),
                ("3. GAYA RAMBUT / HAIR", HAIR_NAMES[wardrobe_indices[2]]),
                ("4. TOPI / HAT", HAT_NAMES[wardrobe_indices[3]])
            ]
            for idx, (cat_name, opt_name) in enumerate(categories):
                row_y = oy + 65 + (idx * 72)
                row_h = 60
                is_selected = (wardrobe_category == idx)
                if is_selected:
                    row_s = pygame.Surface((460, row_h), pygame.SRCALPHA)
                    pygame.draw.rect(row_s, (0, 255, 255, 45), (0, 0, 460, row_h), border_radius=8)
                    pygame.draw.rect(row_s, (0, 255, 255, 180), (0, 0, 460, row_h), 2, border_radius=8)
                    screen.blit(row_s, (ox + 230, row_y))
                    cat_color = (0, 255, 255)
                    opt_color = (255, 255, 255)
                else:
                    row_s = pygame.Surface((460, row_h), pygame.SRCALPHA)
                    pygame.draw.rect(row_s, (30, 40, 50, 120), (0, 0, 460, row_h), border_radius=8)
                    pygame.draw.rect(row_s, (100, 100, 100, 50), (0, 0, 460, row_h), 1, border_radius=8)
                    screen.blit(row_s, (ox + 230, row_y))
                    cat_color = (150, 170, 180)
                    opt_color = (160, 160, 160)
                lbl_surf = font_body.render(cat_name, True, cat_color)
                screen.blit(lbl_surf, (ox + 245, row_y + 8))
                if is_selected:
                    opt_text = f"◀  {opt_name}  ▶"
                else:
                    opt_text = f"   {opt_name}   "
                opt_surf = font_option.render(opt_text, True, opt_color)
                screen.blit(opt_surf, (ox + 245, row_y + 32))
            pygame.draw.line(screen, (0, 100, 100), (ox + 30, oy + 370), (ox + overlay_w - 30, oy + 370), 1)
            help_text = "▲/▼ Pilih Kategori   |   ◀/▶ Ganti Pilihan   |   ENTER Simpan & Keluar"
            help_surf = font_hint.render(help_text, True, (0, 255, 120))
            screen.blit(help_surf, (ox + (overlay_w - help_surf.get_width()) // 2, oy + 382))
            pygame.display.flip()
            continue
        if upgrade_shop_active:
            for event in events:
                if event.type == pygame.QUIT:
                    gesture_thread.stop()
                    gesture_thread.join(timeout=1.0)
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        upgrade_shop_category = (upgrade_shop_category - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        upgrade_shop_category = (upgrade_shop_category + 1) % 4
                    elif event.key == pygame.K_RETURN:
                        cat_key = ["damage_level", "ammo_level", "reload_level", "firerate_level"][upgrade_shop_category]
                        current_lvl = weapon_upgrades[cat_key]
                        if current_lvl < 3:
                            cost = UPGRADE_COSTS[current_lvl]
                            if currency.deduct_bronze(cost):
                                weapon_upgrades[cat_key] += 1
                                effects.flash_timer = 4
                    elif event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_q]:
                        upgrade_shop_active = False
            game_logic.draw_ground(screen, camera)
            game_logic.draw_entities(screen, camera, player)
            player.draw(screen, camera)
            effects.draw_flash(screen)
            dialogue.draw(screen)
            hud.draw(screen, player, 100)
            overlay_w, overlay_h = 750, 450
            ox = (WIDTH - overlay_w) // 2
            oy = (HEIGHT - overlay_h) // 2
            s = pygame.Surface((overlay_w, overlay_h), pygame.SRCALPHA)
            pygame.draw.rect(s, (15, 10, 25, 240), (0, 0, overlay_w, overlay_h), border_radius=15)
            pygame.draw.rect(s, (255, 50, 100, 180), (0, 0, overlay_w, overlay_h), 2, border_radius=15)
            screen.blit(s, (ox, oy))
            font_title = pygame.font.SysFont("Arial", 22, bold=True)
            font_body = pygame.font.SysFont("Arial", 16, bold=True)
            font_option = pygame.font.SysFont("Arial", 14)
            font_hint = pygame.font.SysFont("Arial", 13)
            title_surf = font_title.render("STASIUN UPGRADE SENJATA (WEAPON UPGRADES)", True, (255, 50, 100))
            screen.blit(title_surf, (ox + 30, oy + 20))
            pygame.draw.line(screen, (120, 30, 50), (ox + 30, oy + 55), (ox + overlay_w - 30, oy + 55), 2)
            total_money = currency.get_total_bronze()
            money_txt = f"TOTAL UANG: {total_money} Bronze ({currency.gold}G, {currency.silver}S, {currency.bronze}B)"
            money_surf = font_body.render(money_txt, True, (255, 215, 0))
            screen.blit(money_surf, (ox + overlay_w - 30 - money_surf.get_width(), oy + 23))
            pygame.draw.rect(screen, (30, 20, 40), (ox + 30, oy + 70, 200, 290), border_radius=10)
            pygame.draw.rect(screen, (255, 50, 100, 80), (ox + 30, oy + 70, 200, 290), 1, border_radius=10)
            wpn_lbl = font_body.render("STATUS SENJATA", True, (255, 255, 255))
            screen.blit(wpn_lbl, (ox + 30 + (200 - wpn_lbl.get_width()) // 2, oy + 85))
            gun_ox, gun_oy = ox + 130, oy + 220
            pygame.draw.rect(screen, (100, 100, 110), (gun_ox - 60, gun_oy - 15, 100, 25), border_radius=3)
            pygame.draw.rect(screen, (255, 50, 100), (gun_ox - 60, gun_oy - 15, 100, 2))
            pygame.draw.rect(screen, (60, 60, 65), (gun_ox + 10, gun_oy + 10, 25, 55), border_radius=5)
            pygame.draw.rect(screen, (40, 40, 45), (gun_ox - 20, gun_oy - 25, 30, 10))
            pygame.draw.circle(screen, (255, 0, 0), (gun_ox + 10, gun_oy - 20), 2)
            stat_y = oy + 280
            stats_text = [
                f"Dmg: {40 + weapon_upgrades['damage_level']*15}",
                f"Mag: {30 + weapon_upgrades['ammo_level']*10} Peluru",
                f"Reload: {(60 - weapon_upgrades['reload_level']*15)/60:.2f}s",
                f"Rate: {60 / max(2, 5 - weapon_upgrades['firerate_level']):.1f} r/s"
            ]
            for i, st in enumerate(stats_text):
                st_surf = font_option.render(st, True, (200, 200, 220))
                screen.blit(st_surf, (ox + 50, stat_y + i * 20))
            categories_info = [
                ("DAMAGE (Daya Hancur)", "damage_level", lambda lvl: f"{40 + lvl*15} -> {40 + (lvl+1)*15 if lvl < 3 else 'MAX'}", "+15 Damage"),
                ("MAGAZINE (Kapasitas)", "ammo_level", lambda lvl: f"{30 + lvl*10} -> {30 + (lvl+1)*10 if lvl < 3 else 'MAX'}", "+10 Peluru"),
                ("RELOAD SPEED (Isi Peluru)", "reload_level", lambda lvl: f"{(60 - lvl*15)/60:.2f}s -> {(60 - (lvl+1)*15)/60 if lvl < 3 else 0:.2f}s", "Isi Ulang Lebih Cepat"),
                ("FIRE RATE (Kecepatan Tembak)", "firerate_level", lambda lvl: f"{60 / max(2, 5 - lvl):.1f}/s -> {60 / max(2, 5 - (lvl+1)) if lvl < 3 else 0:.1f}/s", "Tembak Lebih Cepat")
            ]
            for idx, (cat_name, cat_key, val_func, bonus_desc) in enumerate(categories_info):
                row_y = oy + 70 + (idx * 70)
                row_h = 60
                lvl = weapon_upgrades[cat_key]
                is_selected = (upgrade_shop_category == idx)
                row_s = pygame.Surface((460, row_h), pygame.SRCALPHA)
                if is_selected:
                    pygame.draw.rect(row_s, (255, 50, 100, 45), (0, 0, 460, row_h), border_radius=8)
                    pygame.draw.rect(row_s, (255, 50, 100, 180), (0, 0, 460, row_h), 2, border_radius=8)
                    cat_color = (255, 80, 130)
                    txt_color = (255, 255, 255)
                else:
                    pygame.draw.rect(row_s, (40, 30, 50, 120), (0, 0, 460, row_h), border_radius=8)
                    pygame.draw.rect(row_s, (150, 100, 120, 50), (0, 0, 460, row_h), 1, border_radius=8)
                    cat_color = (200, 170, 180)
                    txt_color = (180, 180, 180)
                screen.blit(row_s, (ox + 260, row_y))
                title_txt = f"{cat_name}  [Lv {lvl}/3]"
                lbl_surf = font_body.render(title_txt, True, cat_color)
                screen.blit(lbl_surf, (ox + 275, row_y + 8))
                if lvl < 3:
                    cost = UPGRADE_COSTS[lvl]
                    has_enough = (total_money >= cost)
                    cost_color = (100, 255, 100) if has_enough else (255, 100, 100)
                    desc_txt = f"{val_func(lvl)} ({bonus_desc})"
                    desc_surf = font_option.render(desc_txt, True, txt_color)
                    screen.blit(desc_surf, (ox + 275, row_y + 32))
                    cost_txt = f"BIAYA: {cost} Bronze"
                    cost_surf = font_body.render(cost_txt, True, cost_color)
                    screen.blit(cost_surf, (ox + 690 - cost_surf.get_width(), row_y + 18))
                else:
                    desc_txt = f"SELESAI UPGRADE (MAX)"
                    desc_surf = font_body.render(desc_txt, True, (0, 255, 120))
                    screen.blit(desc_surf, (ox + 275, row_y + 32))
            pygame.draw.line(screen, (120, 30, 50), (ox + 30, oy + 380), (ox + overlay_w - 30, oy + 380), 1)
            help_text = "▲/▼ Pilih Upgrade   |   ENTER Beli Peningkatan   |   ESC/BACKSPACE/Q Keluar"
            help_surf = font_hint.render(help_text, True, (0, 255, 120))
            screen.blit(help_surf, (ox + (overlay_w - help_surf.get_width()) // 2, oy + 395))
            pygame.display.flip()
            continue
        interact_pressed = False
        if minigame_manager.in_minigame:
            for event in events:
                if event.type == pygame.QUIT:
                    gesture_thread.stop()
                    gesture_thread.join(timeout=1.0)
                    pygame.quit(); sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    smoothed_hx, smoothed_hy = event.pos
                minigame_manager.active_game.handle_event(event)
            if current_g != "None":
                target_hx = int(h_pos[0] * WIDTH)
                target_hy = int(h_pos[1] * HEIGHT)
                lerp_factor = 0.40
                smoothed_hx = smoothed_hx + (target_hx - smoothed_hx) * lerp_factor
                smoothed_hy = smoothed_hy + (target_hy - smoothed_hy) * lerp_factor
                fake_move = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (int(smoothed_hx), int(smoothed_hy))})
                minigame_manager.active_game.handle_event(fake_move)
            if gesture_thread.recoil_active:
                minigame_manager.active_game.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1}))
            minigame_manager.update(dt)
            minigame_manager.draw()
            cam_surf = gesture_thread.frame
            if cam_surf:
                screen.blit(cam_surf, (WIDTH - 180, 90))
                pygame.draw.rect(screen, (0, 255, 255), (WIDTH - 180, 90, 160, 120), 2)
                screen.blit(font.render(f"GESTURE: {current_g}", True, (0, 255, 255)), (WIDTH - 180, 215))
            pygame.display.flip()
            continue
        for event in events:
            if event.type == pygame.QUIT:
                gesture_thread.stop()
                gesture_thread.join(timeout=1.0)
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if dialogue.active:
                    if event.key == pygame.K_RETURN:
                        dialogue.next_message()
                else:
                    if event.key == pygame.K_RETURN:
                        interact_pressed = True
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        names = {pygame.K_1: "UZI", pygame.K_2: "SCAR", pygame.K_3: "SHOTGUN", pygame.K_4: "SNIPER"}
                        req_weapon = names[event.key]
                        unlocked = True
                        msg = ""
                        if req_weapon == "UZI" and engine_proxy.point_kill < 10000:
                            unlocked = False
                            msg = f"UZI TERKUNCI! Butuh {10000 - engine_proxy.point_kill} poin"
                        elif req_weapon == "SCAR" and engine_proxy.point_kill < 20000:
                            unlocked = False
                            msg = f"SCAR TERKUNCI! Butuh {20000 - engine_proxy.point_kill} poin"
                        
                        if unlocked:
                            selected_weapon = req_weapon
                            engine_proxy.selected_weapon = selected_weapon
                            game_logic.floating_texts.append({'text': f"SIAP: {selected_weapon}", 'pos': [player.pos[0], player.pos[1] - 40], 'timer': 45, 'color': (0, 255, 255)})
                        else:
                            game_logic.floating_texts.append({'text': msg, 'pos': [player.pos[0], player.pos[1] - 40], 'timer': 60, 'color': (255, 50, 50)})
        keys = InputProxy(pygame.key.get_pressed())
        if current_g == "ATAS": keys.overrides[pygame.K_UP] = True
        elif current_g == "BAWAH": keys.overrides[pygame.K_DOWN] = True
        elif current_g == "KIRI": keys.overrides[pygame.K_LEFT] = True
        elif current_g == "KANAN": keys.overrides[pygame.K_RIGHT] = True
        elif current_g in ["PISTOL", "AMBIL", "ENTER"]: interact_pressed = True
        if not dialogue.active:
            player.update(keys, map_size=(2560, 1440))
            camera.update(player.pos)
            signal = game_logic.update(player, interact_pressed)
            if signal == "START_SHOOTING":
                from src.core.minigames.shooting_range import ShootingRangeUltimate
                minigame_manager.start_minigame(ShootingRangeUltimate)
            elif signal == "AWARD_150_BRONZE":
                currency.add_bronze(150)
            elif signal == "OPEN_WARDROBE":
                wardrobe_active = True
            elif signal == "OPEN_UPGRADE_SHOP":
                upgrade_shop_active = True
        game_logic.draw_ground(screen, camera)
        game_logic.draw_entities(screen, camera, player)
        player.draw(screen, camera)
        effects.draw_flash(screen)
        dialogue.draw(screen)
        hud.draw(screen, player, 100)
        status = game_logic.get_status_text()
        pygame.draw.rect(screen, (10, 10, 15, 200), (10, HEIGHT-85, 480, 75), border_radius=5)
        pygame.draw.rect(screen, (0, 255, 255, 100), (10, HEIGHT-85, 480, 75), 1, border_radius=5)
        screen.blit(font.render(status, True, (255, 255, 0)), (15, HEIGHT-80))
        screen.blit(font.render(f"POINT KILL: {engine_proxy.point_kill} | UZI (10k): {'BUKA' if engine_proxy.point_kill >= 10000 else 'KUNCI'} | SCAR (20k): {'BUKA' if engine_proxy.point_kill >= 20000 else 'KUNCI'}", True, (255, 215, 0)), (15, HEIGHT-58))
        screen.blit(font.render(f"SENJATA SIAP: {selected_weapon} (Tekan 1-4 untuk Ganti)", True, (0, 255, 255)), (15, HEIGHT-35))
        cam_surf = gesture_thread.frame
        if cam_surf:
            screen.blit(cam_surf, (WIDTH - 180, 20))
            pygame.draw.rect(screen, (0, 255, 255), (WIDTH - 180, 20, 160, 120), 2)
            screen.blit(font.render(f"GESTURE: {current_g}", True, (0, 255, 255)), (WIDTH - 180, 145))
        pygame.display.flip()
if __name__ == "__main__":
    main()
