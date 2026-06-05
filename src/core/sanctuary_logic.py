import pygame
import math
import random

class SanctuaryParticle:
    def __init__(self, x, y, color, vx=None, vy=None, size=None):
        self.pos = [x, y]
        self.vel = [vx if vx is not None else random.uniform(-1, 1), vy if vy is not None else random.uniform(-1.5, -0.5)]
        self.color = color
        self.size = size if size is not None else random.randint(3, 6)
        self.life = 1.0
        self.decay = random.uniform(0.02, 0.04)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.life -= self.decay
        return self.life > 0

    def draw(self, screen, camera):
        draw_pos = camera.apply(self.pos)
        pygame.draw.circle(screen, self.color, (int(draw_pos[0]), int(draw_pos[1])), int(self.size * self.life))

# Dialogue constants embedded for simplicity
PROLOGUE_M3 = [
    "Cahaya matahari menyilaukan mataku...",
    "Setelah berhari-hari di dalam kegelapan Metro, akhirnya aku keluar.",
    "Tunggu... suara apa itu?",
    "Suara tawa? Suara orang berbicara?",
    "Selamat datang di 'The Sanctuary'. Benteng terakhir kemanusiaan."
]

NPC_DIALOGUES = {
    "Guard": [
        "Jaga langkahmu, kawan. Kami tidak ingin ada masalah di sini.",
        "Senang melihat wajah baru yang bukan zombie."
    ],
    "Citizen": [
        "Katanya ada kota lain di Utara, tapi siapa yang tahu?",
        "Anak-anak akhirnya bisa bermain tanpa rasa takut... setidaknya untuk sekarang."
    ],
    "Elder": [
        "Selamat datang, pengembara. Kami sudah mendengar kabarmu lewat radio.",
        "Dunia luar sudah hancur, tapi di sini... kita mencoba membangun kembali."
    ]
}

class SanctuaryLogic:
    def __init__(self, dialogue):
        self.dialogue = dialogue
        self.alarm_active = False
        self.elder_met = False
        self.npcs = []
        self._setup_npcs()
        self.font = pygame.font.SysFont("monospace", 14, bold=True)

        # Load map background
        try:
            self.map_img = pygame.image.load("assets/images/sanctuary_map.png").convert()
            self.map_img = pygame.transform.scale(self.map_img, (2560, 1440))
        except Exception as e:
            print(f"Error loading sanctuary map image: {e}")
            self.map_img = None

        self.particles = []
        self.floating_texts = []
        self.crate = None
        self.crate_cooldown = 0

    def _setup_npcs(self):
        from src.entities.npc import NPC
        
        # Position NPCs inside the rooftop base layout (2560, 1440)
        self.npcs = [
            NPC(
                name="Penatua Aris", 
                x=1280, y=600, 
                role="Elder",
                base_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v09.png",
                outfit_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v05.png",
                hair_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_bob1_v02.png"
            ),
            NPC(
                name="Kapten Jaka", 
                x=1800, y=650, 
                role="Guard",
                base_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v00.png",
                outfit_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v01.png",
                hair_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_dap1_v08.png"
            ),
            NPC(
                name="Warga Sipil", 
                x=400, y=1100, 
                role="Citizen",
                base_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v02.png",
                outfit_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_pfpn_v02.png",
                hair_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_bob1_v10.png"
            )
        ]

    def update(self, player, interact_pressed):
        # Update NPC movements and animations
        for npc in self.npcs:
            npc.update(map_size=(2560, 1440))

        # Update particles & floating texts
        self.particles = [p for p in self.particles if p.update()]
        for ft in self.floating_texts:
            ft['pos'][1] -= 0.6
            ft['timer'] -= 1
        self.floating_texts = [ft for ft in self.floating_texts if ft['timer'] > 0]
        
        # Decrement cooldown
        if self.crate_cooldown > 0:
            self.crate_cooldown -= 1

        px, py = player.pos[0], player.pos[1]
        
        # Default speed multiplier
        player.speed_multiplier = 0.40

        # --- 1. CAMPFIRE INTERACTION (Warming vs Burning) ---
        campfire_dist = math.hypot(px - 1220, py - 560)
        if campfire_dist < 120:
            if campfire_dist < 30:
                # Walked directly into the fire! Take damage
                player.health = max(0.0, player.health - 0.7)
                player.injured = True
                if random.random() < 0.15:
                    self.floating_texts.append({'text': "BURNING! -HP", 'pos': [px + random.randint(-15, 15), py - 20], 'timer': 20, 'color': (255, 50, 50)})
                # Spawn fire particles on player
                if random.random() < 0.4:
                    self.particles.append(SanctuaryParticle(px + random.uniform(-10, 10), py + 10, (255, random.randint(50, 150), 0)))
            else:
                # Warmed next to the fire! Stamina boost
                if player.adrenaline_timer <= 0:
                    self.floating_texts.append({'text': "WARMED BY CAMPFIRE (Speed Boost!)", 'pos': [px, py - 30], 'timer': 45, 'color': (255, 150, 0)})
                player.adrenaline_timer = 120
                # Spawn gentle orange sparks
                if random.random() < 0.1:
                    self.particles.append(SanctuaryParticle(px + random.uniform(-10, 10), py + 10, (255, 180, 50), vy=random.uniform(-1.0, -0.3)))

        # --- 2. MEDICAL AREA INTERACTION (Healing Beds) ---
        if 100 < px < 550 and 900 < py < 1350:
            if player.health < 100:
                player.health = min(100.0, player.health + 0.3)
                player.injured = False
                if random.random() < 0.08:
                    self.floating_texts.append({'text': "+HEAL", 'pos': [px + random.randint(-15, 15), py - 20], 'timer': 25, 'color': (100, 255, 100)})
            # Spawn green healing particles
            if random.random() < 0.15:
                self.particles.append(SanctuaryParticle(px + random.uniform(-15, 15), py + 15, (50, 255, 50), size=random.randint(3, 5)))

        # --- 3. POND INTERACTION (Deep Water slowdown & splash) ---
        if 1950 < px < 2400 and 900 < py < 1300:
            player.speed_multiplier = 0.20 # Slowed down by water
            # Spawn water splashes if player is moving
            is_moving = player.state in ['walk', 'run']
            if is_moving and random.random() < 0.35:
                self.particles.append(SanctuaryParticle(px + random.uniform(-15, 15), py + 15, (100, 180, 255), vx=random.uniform(-1.2, 1.2), vy=random.uniform(-0.4, 0.4)))

        # --- 4. HELIPAD SUPPLY DROP INTERACTION ---
        helipad_dist = math.hypot(px - 430, py - 410)
        signal_to_return = None
        if helipad_dist < 60:
            if interact_pressed:
                if not self.crate and self.crate_cooldown <= 0:
                    # Spawn falling crate
                    self.crate = {'pos': [430, 410], 'z_height': 500, 'landed': False, 'opened': False}
                    self.floating_texts.append({'text': "SUPPLY DROP CALLED!", 'pos': [px, py - 30], 'timer': 60, 'color': (0, 255, 255)})
                elif self.crate and self.crate['landed'] and not self.crate['opened']:
                    # Open crate and award Bronze
                    self.crate['opened'] = True
                    self.floating_texts.append({'text': "+$150 BRONZE CURRENCY", 'pos': [px, py - 30], 'timer': 60, 'color': (255, 215, 0)})
                    self.crate_cooldown = 1800 # 30 seconds cooldown
                    signal_to_return = "AWARD_150_BRONZE"

        # Update Supply Crate physics
        if self.crate:
            if not self.crate['landed']:
                self.crate['z_height'] -= 10
                if self.crate['z_height'] <= 0:
                    self.crate['z_height'] = 0
                    self.crate['landed'] = True
                    # Spawn dust landing particles
                    for _ in range(20):
                        self.particles.append(SanctuaryParticle(430, 410, (160, 160, 160), vx=random.uniform(-2.5, 2.5), vy=random.uniform(-1.5, 1.5)))

        # Interaksi sederhana dengan NPC
        if interact_pressed:
            for npc in self.npcs:
                dist = math.hypot(player.pos[0] - npc.pos[0], player.pos[1] - npc.pos[1])
                if dist < 100: # Jangkauan interaksi diperluas ke 100px
                    if npc.name == "Penatua Aris":
                        self.elder_met = True
                        self.dialogue.show(["PENATUA ARIS: Selamat datang. Kota ini dalam bahaya.", "Bicara pada Kapten Jaka di gerbang jalan itu!"])
                    elif npc.name == "Kapten Jaka":
                        if self.elder_met:
                            self.alarm_active = True
                            player.pos = [2500, 300]
                            self.dialogue.show(["KAPTEN JAKA: Zombie datang! Cepat ke menara!", "KITA HARUS BERTAHAN!"])
                            return "START_SHOOTING"
                        else:
                            self.dialogue.show(["KAPTEN JAKA: Cari Penatua Aris dulu! Dia di sebelah barat."])
                    else:
                        role = npc.role
                        msg = random.choice(NPC_DIALOGUES.get(role, ["Halo!"]))
                        self.dialogue.show([f"{npc.name}: {msg}"])
                    return None
                    
        # --- 5. WARDROBE LOCKER INTERACTION ---
        w_dist = math.hypot(px - 145, py - 875)
        if w_dist < 60:
            if interact_pressed:
                signal_to_return = "OPEN_WARDROBE"

        return signal_to_return

    def draw_ground(self, screen, camera):
        if self.map_img:
            # Draw the background map using camera offset
            screen.blit(self.map_img, (camera.camera.x, camera.camera.y))
        else:
            # Draw fallback background or simple grid
            screen.fill((30, 100, 30)) # Grass green
            # Simple road (Sesuai dengan posisi Kapten Jaka)
            pygame.draw.rect(screen, (100, 80, 50), camera.apply(pygame.Rect(950, 0, 300, 4000)))

    def draw_entities(self, screen, camera, player=None):
        # Draw particles
        for p in self.particles:
            p.draw(screen, camera)

        # Draw Supply Crate
        if self.crate and not self.crate['opened']:
            cx, cy = self.crate['pos']
            screen_pos = camera.apply((cx, cy))
            
            if not self.crate['landed']:
                # Draw shadow on ground
                shadow_r = int(15 * (1.0 - self.crate['z_height'] / 500.0))
                shadow_surf = pygame.Surface((shadow_r * 2, shadow_r), pygame.SRCALPHA)
                pygame.draw.ellipse(shadow_surf, (0, 0, 0, 100), (0, 0, shadow_r * 2, shadow_r))
                screen.blit(shadow_surf, (screen_pos[0] - shadow_r, screen_pos[1] - shadow_r // 2))
                # Draw falling crate
                crate_y = screen_pos[1] - self.crate['z_height']
                pygame.draw.rect(screen, (120, 60, 10), (screen_pos[0] - 16, crate_y - 16, 32, 32), border_radius=4)
                pygame.draw.rect(screen, (180, 130, 40), (screen_pos[0] - 12, crate_y - 12, 24, 24), border_radius=2)
                # Parachute strings & dome
                pygame.draw.line(screen, (220, 220, 220), (screen_pos[0] - 16, crate_y - 16), (screen_pos[0] - 25, crate_y - 45), 2)
                pygame.draw.line(screen, (220, 220, 220), (screen_pos[0] + 16, crate_y - 16), (screen_pos[0] + 25, crate_y - 45), 2)
                pygame.draw.arc(screen, (240, 240, 240), (screen_pos[0] - 30, crate_y - 65, 60, 40), 0, math.pi, 3)
            else:
                # Crate landed on ground
                pygame.draw.rect(screen, (120, 60, 10), (screen_pos[0] - 16, screen_pos[1] - 16, 32, 32), border_radius=4)
                pygame.draw.rect(screen, (180, 130, 40), (screen_pos[0] - 12, screen_pos[1] - 12, 24, 24), border_radius=2)
                
                # Draw interact hint
                if player:
                    p_dist = math.hypot(player.pos[0] - cx, player.pos[1] - cy)
                    if p_dist < 60:
                        hint = self.font.render("PRESS ENTER TO CLAIM SUPPLY", True, (0, 255, 255))
                        screen.blit(hint, (screen_pos[0] - hint.get_width() // 2, screen_pos[1] - 35))

        # Draw Helipad prompt if player is close
        if player and not self.crate and self.crate_cooldown <= 0:
            h_dist = math.hypot(player.pos[0] - 430, player.pos[1] - 410)
            if h_dist < 60:
                h_pos = camera.apply((430, 410))
                hint = self.font.render("PRESS ENTER TO CALL SUPPLY DROP", True, (0, 255, 255))
                screen.blit(hint, (h_pos[0] - hint.get_width() // 2, h_pos[1] - 25))

        # Draw Wardrobe Locker prompt if player is close
        if player:
            w_dist = math.hypot(player.pos[0] - 145, player.pos[1] - 875)
            if w_dist < 60:
                w_pos = camera.apply((145, 875))
                hint = self.font.render("PRESS ENTER TO USE WARDROBE", True, (0, 255, 255))
                screen.blit(hint, (w_pos[0] - hint.get_width() // 2, w_pos[1] - 25))

        # Draw NPCs
        for npc in self.npcs:
            npc.draw(screen, camera)
            
            # Draw name tag above their head
            d_pos = camera.apply(npc.pos)
            name_tag = self.font.render(npc.name, True, (255, 255, 255))
            screen.blit(name_tag, (d_pos[0] + 16 - name_tag.get_width() // 2, d_pos[1] - 15))

        # Draw floating texts
        for ft in self.floating_texts:
            shadow_surf = self.font.render(ft['text'], True, (0, 0, 0))
            text_surf = self.font.render(ft['text'], True, ft['color'])
            sp = camera.apply(ft['pos'])
            screen.blit(shadow_surf, (sp[0] + 1, sp[1] + 1))
            screen.blit(text_surf, sp)

    def get_status_text(self):
        if self.alarm_active: return "STATUS: PERTAHANAN AKTIF!"
        if not self.elder_met: return "OBJEKTIF: Cari dan bicara ke Penatua Aris (Warna Oranye)"
        return "OBJEKTIF: Bicara ke Kapten Jaka di jalan (Warna Biru)"
