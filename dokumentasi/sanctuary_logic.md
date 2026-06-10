# Penjelasan Kode: `sanctuary_logic.py`

Dokumen ini berisi penjelasan detail baris demi baris untuk file `/home/abuyyy/PemogramanLanjut/src/core/sanctuary_logic.py`. Penjelasan ini ditulis dalam bahasa Indonesia untuk membantu persiapan demo program.

---

## Deskripsi & Tujuan File
File `sanctuary_logic.py` mengatur seluruh perilaku simulasi lingkungan, partikel visual, dialog cerita, dan interaksi pemain di area pangkalan aman ("The Sanctuary"):
1. **Partikel Lingkungan (`SanctuaryParticle`)**: Percikan api unggun, pendaran hijau stasiun medis, cipratan air kolam, dan debu pendaratan kotak suplai.
2. **Karakter Non-Pemain (`NPC`)**: Penatua Aris, Kapten Jaka, dan Warga Sipil yang ditempatkan secara teratur di koordinat peta.
3. **Mekanika Interaksi Lingkungan**:
   - Efek hangat/terbakar api unggun.
   - Pemulihan otomatis di area kasur medis.
   - Hambatan air dalam di kolam.
   - Penggunaan Loker Pakaian (Wardrobe) untuk modifikasi model sprite.
   - Penggunaan Stasiun Peningkatan (Upgrade Shop) untuk memperkuat statistik senjata.
   - Panggilan Kotak Suplai Udara (Supply Drop) di helipad dengan parasut udara dinamis dan hadiah koin.
4. **Logika Quest Pemicu Pertempuran**: Pemain harus berbicara dengan Penatua Aris sebelum dapat meyakinkan Kapten Jaka untuk mengaktifkan alarm pertahanan kota, memindahkan posisi ke menara, dan memicu peluncuran minigame.

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel analisis baris demi baris dari kode sumber `sanctuary_logic.py`:

| Baris | Kode Sumber | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import pygame` | Mengimpor pustaka Pygame untuk menangani grafik, bentuk geometris, font, dan input game. |
| **2** | `import math` | Mengimpor modul matematika untuk menghitung jarak Euclidean menggunakan `hypot` dan kalkulasi trigonometri. |
| **3** | `import random` | Mengimpor modul random untuk menghasilkan posisi partikel acak dan memilih dialog acak. |
| **4** | `class SanctuaryParticle:` | Deklarasi kelas `SanctuaryParticle` untuk membuat visual efek partikel kecil. |
| **5** | `    def __init__(self, x, y, color, vx=None, vy=None, size=None):` | Konstruktor partikel menerima koordinat awal, warna, kecepatan horizontal/vertikal opsional, dan ukuran opsional. |
| **6** | `        self.pos = [x, y]` | Menyimpan posisi partikel dalam list `[x, y]`. |
| **7** | `        self.vel = [vx if vx is not None else random.uniform(-1, 1), vy if vy is not None else random.uniform(-1.5, -0.5)]` | Menetapkan kecepatan gerak partikel (default horizontal acak -1 s.d 1, vertikal ke atas -1.5 s.d -0.5). |
| **8** | `        self.color = color` | Menyimpan warna partikel (RGB). |
| **9** | `        self.size = size if size is not None else random.randint(3, 6)` | Mengatur ukuran partikel awal (default acak 3 s.d 6 piksel). |
| **10** | `        self.life = 1.0` | Menetapkan sisa masa hidup partikel awal sebesar 100% (1.0). |
| **11** | `        self.decay = random.uniform(0.02, 0.04)` | Menetapkan tingkat pengurangan masa hidup per frame secara acak antara 0.02 s.d 0.04. |
| **12** | `    def update(self):` | Metode untuk memperbarui posisi dan masa hidup partikel di setiap frame. |
| **13** | `        self.pos[0] += self.vel[0]` | Menggeser posisi X partikel berdasarkan kecepatan horizontalnya. |
| **14** | `        self.pos[1] += self.vel[1]` | Menggeser posisi Y partikel berdasarkan kecepatan vertikalnya. |
| **15** | `        self.life -= self.decay` | Mengurangi sisa masa hidup partikel. |
| **16** | `        return self.life > 0` | Mengembalikan nilai `True` jika partikel masih hidup (`life > 0`), atau `False` jika sudah mati. |
| **17** | `    def draw(self, screen, camera):` | Menggambar lingkaran partikel ke layar. |
| **18** | `        draw_pos = camera.apply(self.pos)` | Menghitung koordinat layar partikel disesuaikan offset kamera scroll. |
| **19** | `        pygame.draw.circle(screen, self.color, (int(draw_pos[0]), int(draw_pos[1])), int(self.size * self.life))` | Merender lingkaran dengan ukuran yang mengecil seiring waktu (`size * life`). |
| **20** | `PROLOGUE_M3 = [` | Mendefinisikan list dialog prolog pembuka game. |
| **21** | `    "Cahaya matahari menyilaukan mataku...",` | Kalimat prolog baris 1. |
| **22** | `    "Setelah berhari-hari di dalam kegelapan Metro, akhirnya aku keluar.",` | Kalimat prolog baris 2. |
| **23** | `    "Tunggu... suara apa itu?",` | Kalimat prolog baris 3. |
| **24** | `    "Suara tawa? Suara orang berbicara?",` | Kalimat prolog baris 4. |
| **25** | `    "Selamat datang di 'The Sanctuary'. Benteng terakhir kemanusiaan."` | Kalimat prolog baris 5. |
| **26** | `]` | Menutup list dialog prolog. |
| **27** | `NPC_DIALOGUES = {` | Kamus dialog santai untuk NPC berdasarkan peran mereka. |
| **28** | `    "Guard": [` | Daftar dialog NPC Penjaga. |
| **29** | `        "Jaga langkahmu, kawan. Kami tidak ingin ada masalah di sini.",` | Opsi dialog penjaga 1. |
| **30** | `        "Senang melihat wajah baru yang bukan zombie."` | Opsi dialog penjaga 2. |
| **31** | `    ],` | Penutup dialog penjaga. |
| **32** | `    "Citizen": [` | Daftar dialog NPC Warga Sipil. |
| **33** | `        "Katanya ada kota lain di Utara, tapi siapa yang tahu?",` | Opsi warga 1. |
| **34** | `        "Anak-anak akhirnya bisa bermain tanpa rasa takut... setidaknya untuk sekarang."` | Opsi warga 2. |
| **35** | `    ],` | Penutup dialog warga. |
| **36** | `    "Elder": [` | Daftar dialog NPC Tetua. |
| **37** | `        "Selamat datang, pengembara. Kami sudah mendengar kabarmu lewat radio.",` | Opsi tetua 1. |
| **38** | `        "Dunia luar sudah hancur, tapi di sini... kita mencoba membangun kembali."` | Opsi tetua 2. |
| **39** | `    ]` | Penutup dialog tetua. |
| **40** | `}` | Penutup kamus `NPC_DIALOGUES`. |
| **41** | `class SanctuaryLogic:` | Deklarasi kelas utama logika lingkungan Sanctuary. |
| **42** | `    def __init__(self, dialogue):` | Inisialisasi logika Sanctuary dengan menyertakan objek dialog box. |
| **43** | `        self.dialogue = dialogue` | Menyimpan referensi objek dialog box. |
| **44** | `        self.alarm_active = False` | Status keaktifan alarm pertempuran (awal False). |
| **45** | `        self.elder_met = False` | Status apakah pemain sudah menemui Penatua Aris (awal False). |
| **46** | `        self.npcs = []` | List kosong untuk menampung instansiasi NPC. |
| **47** | `        self._setup_npcs()` | Memanggil metode internal untuk membuat NPC di peta. |
| **48** | `        self.font = pygame.font.SysFont("monospace", 14, bold=True)` | Inisialisasi font petunjuk interaksi monospace 14px tebal. |
| **49** | `        try:` | Blok try-except untuk memuat aset gambar peta Sanctuary. |
| **50** | `            self.map_img = pygame.image.load("assets/images/sanctuary_map.png").convert()` | Memuat gambar map latar belakang Sanctuary. |
| **51** | `            self.map_img = pygame.transform.scale(self.map_img, (2560, 1440))` | Menskalakan ukuran gambar peta menjadi 2560x1440 piksel. |
| **52** | `        except Exception as e:` | Menangkap kegagalan memuat gambar. |
| **53** | `            print(f"Error loading sanctuary map image: {e}")` | Mencetak pesan error ke konsol terminal. |
| **54** | `            self.map_img = None` | Menetapkan map_img ke None (mengaktifkan mode fallback warna rumput). |
| **55** | `        self.particles = []` | Inisialisasi list penampung partikel aktif di area Sanctuary. |
| **56** | `        self.floating_texts = []` | Inisialisasi list penampung teks melayang. |
| **57** | `        self.crate = None` | Status peti suplai helipad (awal None). |
| **58** | `        self.crate_cooldown = 0` | Waktu tunggu pemanggilan peti suplai berikutnya. |
| **59** | `    def _setup_npcs(self):` | Metode internal membuat dan memposisikan NPC di peta. |
| **60** | `        from src.entities.entities import NPC` | Mengimpor kelas `NPC` dari modul entitas terpadu. |
| **61** | `        self.npcs = [` | Mulai daftar inisialisasi objek NPC. |
| **62** | `            NPC(` | Instansiasi NPC Penatua Aris. |
| **63** | `                name="Penatua Aris",` | Nama NPC. |
| **64** | `                x=1280, y=600,` | Posisi di tengah pangkalan dekat api unggun. |
| **65** | `                role="Elder",` | Peran NPC. |
| **66** | `                base_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v09.png",` | File sprite tubuh dasar. |
| **67** | `                outfit_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v05.png",` | File sprite baju. |
| **68** | `                hair_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_bob1_v02.png"` | File sprite rambut. |
| **69** | `            ),` | Penutup NPC pertama. |
| **70** | `            NPC(` | Instansiasi NPC Kapten Jaka. |
| **71** | `                name="Kapten Jaka",` | Nama NPC. |
| **72** | `                x=1800, y=650,` | Posisi di jalan gerbang timur. |
| **73** | `                role="Guard",` | Peran NPC. |
| **74** | `                base_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v00.png",` | File sprite tubuh dasar. |
| **75** | `                outfit_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v01.png",` | File sprite baju penjaga. |
| **76** | `                hair_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_dap1_v08.png"` | File sprite rambut. |
| **77** | `            ),` | Penutup NPC kedua. |
| **78** | `            NPC(` | Instansiasi NPC Warga Sipil. |
| **79** | `                name="Warga Sipil",` | Nama NPC. |
| **80** | `                x=400, y=1100,` | Posisi di area medis sebelah barat. |
| **81** | `                role="Citizen",` | Peran NPC. |
| **82** | `                base_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v02.png",` | File sprite tubuh dasar. |
| **83** | `                outfit_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_pfpn_v02.png",` | File sprite baju warga. |
| **84** | `                hair_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_bob1_v10.png"` | File sprite rambut. |
| **85** | `            )` | Penutup NPC ketiga. |
| **86** | `        ]` | Penutup list `self.npcs`. |
| **87** | `    def update(self, player, interact_pressed):` | Metode update logika lingkungan per frame di area Sanctuary. |
| **88** | `        for npc in self.npcs:` | Melakukan perulangan untuk memperbarui AI pergerakan acak NPC. |
| **89** | `            npc.update(map_size=(2560, 1440))` | Menggerakkan NPC dalam batas peta Sanctuary. |
| **90** | `        self.particles = [p for p in self.particles if p.update()]` | Memperbarui partikel aktif dan menghapus partikel yang masa hidupnya habis. |
| **91** | `        for ft in self.floating_texts:` | Melakukan perulangan untuk memperbarui posisi teks melayang. |
| **92** | `            ft['pos'][1] -= 0.6` | Menggeser teks melayang ke atas (Y berkurang 0.6px per frame). |
| **93** | `            ft['timer'] -= 1` | Mengurangi sisa durasi tampil teks melayang. |
| **94** | `        self.floating_texts = [ft for ft in self.floating_texts if ft['timer'] > 0]` | Menyaring teks melayang yang sisa durasinya masih di atas 0. |
| **95** | `        if self.crate_cooldown > 0:` | Jika cooldown peti suplai aktif. |
| **96** | `            self.crate_cooldown -= 1` | Kurangi cooldown peti suplai sebanyak 1 per frame. |
| **97** | `        px, py = player.pos[0], player.pos[1]` | Menyalin posisi koordinat pemain saat ini ke variabel lokal. |
| **98** | `        player.speed_multiplier = 0.40` | Membatasi kecepatan berjalan pemain di Sanctuary secara default ke 40% agar santai. |
| **99** | `        campfire_dist = math.hypot(px - 1220, py - 560)` | Menghitung jarak pemain ke pusat api unggun di koordinat (1220, 560). |
| **100** | `        if campfire_dist < 120:` | Jika pemain berada di sekitar jangkauan api unggun (< 120px). |
| **101** | `            if campfire_dist < 30:` | Jika pemain terlalu dekat/menginjak api unggun (< 30px). |
| **102** | `                player.health = max(0.0, player.health - 0.7)` | Mengurangi darah pemain sebesar 0.7 per frame (terbakar). |
| **103** | `                player.injured = True` | Mengeset status cedera terluka menjadi `True`. |
| **104** | `                if random.random() < 0.15:` | Peluang 15% memunculkan indikator teks melayang terbakar. |
| **105** | `                    self.floating_texts.append({'text': "BURNING! -HP", 'pos': [px + random.randint(-15, 15), py - 20], 'timer': 20, 'color': (255, 50, 50)})` | Menambahkan teks melayang merah "BURNING! -HP". |
| **106** | `                if random.random() < 0.4:` | Peluang 40% mengeluarkan partikel api merah oranye di kaki pemain. |
| **107** | `                    self.particles.append(SanctuaryParticle(px + random.uniform(-10, 10), py + 10, (255, random.randint(50, 150), 0)))` | Menambahkan partikel api menyala. |
| **108** | `            else:` | Jika berada di zona hangat aman (jarak 30px s.d 120px). |
| **109** | `                if player.adrenaline_timer <= 0:` | Jika efek adrenalin belum aktif. |
| **110** | `                    self.floating_texts.append({'text': "WARMED BY CAMPFIRE (Speed Boost!)", 'pos': [px, py - 30], 'timer': 45, 'color': (255, 150, 0)})` | Menampilkan teks melayang oranye penanda status peningkatan kecepatan. |
| **111** | `                player.adrenaline_timer = 120` | Memberikan efek status adrenalin selama 120 frame (~2 detik). |
| **112** | `                if random.random() < 0.1:` | Peluang 10% memunculkan pendaran partikel percikan api kecil. |
| **113** | `                    self.particles.append(SanctuaryParticle(px + random.uniform(-10, 10), py + 10, (255, 180, 50), vy=random.uniform(-1.0, -0.3)))` | Menambahkan partikel percikan api ringan. |
| **114** | `        if 100 < px < 550 and 900 < py < 1350:` | Memeriksa apakah pemain berada di zona kasur medis sebelah barat daya. |
| **115** | `            if player.health < 100:` | Jika darah pemain kurang dari 100%. |
| **116** | `                player.health = min(100.0, player.health + 0.3)` | Memulihkan darah pemain sebesar 0.3 per frame. |
| **117** | `                player.injured = False` | Menghapus status cedera terluka pemain. |
| **118** | `                if random.random() < 0.08:` | Peluang 8% menampilkan indikator teks melayang pemulihan. |
| **119** | `                    self.floating_texts.append({'text': "+HEAL", 'pos': [px + random.randint(-15, 15), py - 20], 'timer': 25, 'color': (100, 255, 100)})` | Menambahkan teks melayang hijau "+HEAL". |
| **120** | `            if random.random() < 0.15:` | Peluang 15% memunculkan partikel pendaran hijau stasiun medis. |
| **121** | `                self.particles.append(SanctuaryParticle(px + random.uniform(-15, 15), py + 15, (50, 255, 50), size=random.randint(3, 5)))` | Menambahkan partikel hijau pemulihan. |
| **122** | `        if 1950 < px < 2400 and 900 < py < 1300:` | Memeriksa apakah pemain berjalan masuk ke kolam air sebelah tenggara. |
| **123** | `            player.speed_multiplier = 0.20` | Memotong kecepatan gerak pemain menjadi hanya 20% karena hambatan air. |
| **124** | `            is_moving = player.state in ['walk', 'run']` | Cek apakah pemain sedang dalam keadaan bergerak. |
| **125** | `            if is_moving and random.random() < 0.35:` | Jika bergerak di air, peluang 35% memicu cipratan air. |
| **126** | `                self.particles.append(SanctuaryParticle(px + random.uniform(-15, 15), py + 15, (100, 180, 255), vx=random.uniform(-1.2, 1.2), vy=random.uniform(-0.4, 0.4)))` | Menambahkan partikel percikan air berwarna biru muda. |
| **127** | `        helipad_dist = math.hypot(px - 430, py - 410)` | Menghitung jarak pemain ke pusat landasan helipad di koordinat (430, 410). |
| **128** | `        signal_to_return = None` | Inisialisasi variabel kembalian sinyal dengan `None`. |
| **129** | `        if helipad_dist < 60:` | Jika pemain berdiri di dekat helipad (< 60px). |
| **130** | `            if interact_pressed:` | Jika tombol interaksi ditekan. |
| **131** | `                if not self.crate and self.crate_cooldown <= 0:` | Jika tidak ada peti suplai aktif dan cooldown sudah selesai. |
| **132** | `                    self.crate = {'pos': [430, 410], 'z_height': 500, 'landed': False, 'opened': False}` | Menjatuhkan peti suplai baru di helipad pada ketinggian awal 500px di udara. |
| **133** | `                    self.floating_texts.append({'text': "SUPPLY DROP CALLED!", 'pos': [px, py - 30], 'timer': 60, 'color': (0, 255, 255)})` | Menampilkan teks melayang cyan pemicu peti suplai. |
| **134** | `                elif self.crate and self.crate['landed'] and not self.crate['opened']:` | Jika peti sudah mendarat di tanah dan belum dibuka pemain. |
| **135** | `                    self.crate['opened'] = True` | Mengubah status peti menjadi telah dibuka. |
| **136** | `                    self.floating_texts.append({'text': "+$150 BRONZE CURRENCY", 'pos': [px, py - 30], 'timer': 60, 'color': (255, 215, 0)})` | Menampilkan hadiah uang di layar. |
| **137** | `                    self.crate_cooldown = 1800` | Memasang cooldown pemanggilan peti selama 1800 frame (~30 detik). |
| **138** | `                    signal_to_return = "AWARD_150_BRONZE"` | Mengembalikan sinyal pemberian hadiah koin perunggu ke engine utama. |
| **139** | `        if self.crate:` | Jika objek peti suplai ada. |
| **140** | `            if not self.crate['landed']:` | Jika peti masih melayang di udara (belum mendarat). |
| **141** | `                self.crate['z_height'] -= 10` | Mengurangi ketinggian peti sebesar 10px per frame (turun vertikal). |
| **142** | `                if self.crate['z_height'] <= 0:` | Jika menyentuh tanah (ketinggian <= 0). |
| **143** | `                    self.crate['z_height'] = 0` | Mengunci ketinggian di 0. |
| **144** | `                    self.crate['landed'] = True` | Mengeset status mendarat menjadi `True`. |
| **145** | `                    for _ in range(20):` | Melakukan looping 20 kali untuk memicu efek pendaratan. |
| **146** | `                        self.particles.append(SanctuaryParticle(430, 410, (160, 160, 160), vx=random.uniform(-2.5, 2.5), vy=random.uniform(-1.5, 1.5)))` | Mengeluarkan partikel abu-abu debu tanah mengepul di sekitar peti. |
| **147** | `        if interact_pressed:` | Jika pemain menekan tombol interaksi di dekat NPC. |
| **148** | `            for npc in self.npcs:` | Melakukan iterasi di daftar NPC. |
| **149** | `                dist = math.hypot(player.pos[0] - npc.pos[0], player.pos[1] - npc.pos[1])` | Menghitung jarak pemain ke NPC. |
| **150** | `                if dist < 100:` | Jika pemain berada di dalam radius interaksi dekat NPC (< 100px). |
| **151** | `                    if npc.name == "Penatua Aris":` | Jika berbicara dengan Penatua Aris. |
| **152** | `                        self.elder_met = True` | Menyetel status pertemuan Penatua menjadi `True`. |
| **153** | `                        self.dialogue.show(["PENATUA ARIS: Selamat datang. Kota ini dalam bahaya.", "Bicara pada Kapten Jaka di gerbang jalan itu!"])` | Membuka kotak dialog cerita dan memberi instruksi menemui Kapten Jaka. |
| **154** | `                    elif npc.name == "Kapten Jaka":` | Jika berbicara dengan Kapten Jaka. |
| **155** | `                        if self.elder_met:` | Jika pemain sudah bertemu dengan Penatua Aris sebelumnya. |
| **156** | `                            self.alarm_active = True` | Aktifkan alarm kota pertahanan. |
| **157** | `                            player.pos = [2500, 300]` | Teleportasi posisi pemain ke dekat pagar pertahanan (2500, 300). |
| **158** | `                            self.dialogue.show(["KAPTEN JAKA: Zombie datang! Cepat ke menara!", "KITA HARUS BERTAHAN!"])` | Membuka dialog darurat ancaman zombie. |
| **159** | `                            return "START_SHOOTING"` | Mengembalikan sinyal `"START_SHOOTING"` ke loop utama untuk memulai minigame. |
| **160** | `                        else:` | Jika belum berbicara dengan Penatua Aris. |
| **161** | `                            self.dialogue.show(["KAPTEN JAKA: Cari Penatua Aris dulu! Dia di sebelah barat."])` | Memberi arahan untuk menemui Penatua Aris terlebih dahulu. |
| **162** | `                    else:` | Jika berbicara dengan NPC acak lainnya (Warga Sipil). |
| **163** | `                        role = npc.role` | Mengambil peran NPC. |
| **164** | `                        msg = random.choice(NPC_DIALOGUES.get(role, ["Halo!"]))` | Mengambil dialog santai acak dari database dialog NPC. |
| **165** | `                        self.dialogue.show([f"{npc.name}: {msg}"])` | Membuka dialog box menampilkan teks ucapan warga. |
| **166** | `                    return None` | Membatalkan interaksi ganda pada frame yang sama. |
| **167** | `        w_dist = math.hypot(px - 145, py - 875)` | Menghitung jarak pemain ke loker pakaian (Wardrobe) di koordinat (145, 875). |
| **168** | `        if w_dist < 60:` | Jika berada dekat loker wardrobe (< 60px). |
| **169** | `            if interact_pressed:` | Jika menekan tombol interaksi. |
| **170** | `                signal_to_return = "OPEN_WARDROBE"` | Mengeset sinyal kembalian ke `"OPEN_WARDROBE"` untuk membuka menu kostum. |
| **171** | `        upg_dist = math.hypot(px - 1500, py - 850)` | Menghitung jarak pemain ke komputer stasiun upgrade di koordinat (1500, 850). |
| **172** | `        if upg_dist < 60:` | Jika berada dekat komputer stasiun upgrade (< 60px). |
| **173** | `            if interact_pressed:` | Jika menekan tombol interaksi. |
| **174** | `                signal_to_return = "OPEN_UPGRADE_SHOP"` | Mengeset sinyal kembalian ke `"OPEN_UPGRADE_SHOP"` untuk membuka menu upgrade senjata. |
| **175** | `        return signal_to_return` | Mengembalikan sinyal interaksi aktif yang terdeteksi ke loop game utama. |
| **176** | `    def draw_ground(self, screen, camera):` | Menggambar grafis tanah/peta dasar Sanctuary. |
| **177** | `        if self.map_img:` | Jika gambar peta Sanctuary berhasil dimuat. |
| **178** | `            screen.blit(self.map_img, (camera.camera.x, camera.camera.y))` | Menggambar background peta dengan penyesuaian posisi kamera gulir. |
| **179** | `        else:` | Jika gambar peta gagal dimuat. |
| **180** | `            screen.fill((30, 100, 30))` | Fallback: Warnai latar belakang hijau rumput pekat. |
| **181** | `            pygame.draw.rect(screen, (100, 80, 50), camera.apply(pygame.Rect(950, 0, 300, 4000)))` | Fallback: Menggambar jalan tanah cokelat vertikal di peta. |
| **182** | `    def draw_entities(self, screen, camera, player=None):` | Menggambar objek/entitas berlapis di atas tanah Sanctuary. |
| **183** | `        for p in self.particles:` | Melakukan iterasi di list partikel aktif. |
| **184** | `            p.draw(screen, camera)` | Merender gambar lingkaran partikel ke layar. |
| **185** | `        if self.crate and not self.crate['opened']:` | Jika peti suplai aktif di peta dan belum dibuka. |
| **186** | `            cx, cy = self.crate['pos']` | Mengambil koordinat X dan Y peti suplai di peta. |
| **187** | `            screen_pos = camera.apply((cx, cy))` | Mengonversi koordinat peti di peta menjadi koordinat layar. |
| **188** | `            if not self.crate['landed']:` | Jika peti sedang melayang jatuh. |
| **189** | `                shadow_r = int(15 * (1.0 - self.crate['z_height'] / 500.0))` | Menghitung radius bayangan elips di tanah (membesar seiring turunnya peti). |
| **190** | `                shadow_surf = pygame.Surface((shadow_r * 2, shadow_r), pygame.SRCALPHA)` | Membuat permukaan transparan untuk bayangan. |
| **191** | `                pygame.draw.ellipse(shadow_surf, (0, 0, 0, 100), (0, 0, shadow_r * 2, shadow_r))` | Menggambar bayangan elips hitam transparan di tanah. |
| **192** | `                screen.blit(shadow_surf, (screen_pos[0] - shadow_r, screen_pos[1] - shadow_r // 2))` | Menempelkan bayangan tepat di bawah peti. |
| **193** | `                crate_y = screen_pos[1] - self.crate['z_height']` | Menghitung posisi Y rendering peti di layar (dikurangi tinggi jatuh). |
| **194** | `                pygame.draw.rect(screen, (120, 60, 10), (screen_pos[0] - 16, crate_y - 16, 32, 32), border_radius=4)` | Menggambar tepi luar peti cokelat tua. |
| **195** | `                pygame.draw.rect(screen, (180, 130, 40), (screen_pos[0] - 12, crate_y - 12, 24, 24), border_radius=2)` | Menggambar isi dalam peti cokelat muda. |
| **196** | `                pygame.draw.line(screen, (220, 220, 220), (screen_pos[0] - 16, crate_y - 16), (screen_pos[0] - 25, crate_y - 45), 2)` | Menggambar tali parasut sebelah kiri. |
| **197** | `                pygame.draw.line(screen, (220, 220, 220), (screen_pos[0] + 16, crate_y - 16), (screen_pos[0] + 25, crate_y - 45), 2)` | Menggambar tali parasut sebelah kanan. |
| **198** | `                pygame.draw.arc(screen, (240, 240, 240), (screen_pos[0] - 30, crate_y - 65, 60, 40), 0, math.pi, 3)` | Menggambar kubah parasut putih di atas peti. |
| **199** | `            else:` | Jika peti sudah mendarat di tanah. |
| **200** | `                pygame.draw.rect(screen, (120, 60, 10), (screen_pos[0] - 16, screen_pos[1] - 16, 32, 32), border_radius=4)` | Menggambar tepi luar peti di atas tanah. |
| **201** | `                pygame.draw.rect(screen, (180, 130, 40), (screen_pos[0] - 12, screen_pos[1] - 12, 24, 24), border_radius=2)` | Menggambar isi dalam peti di tanah. |
| **202** | `                if player:` | Memeriksa objek pemain. |
| **203** | `                    p_dist = math.hypot(player.pos[0] - cx, player.pos[1] - cy)` | Menghitung jarak pemain ke peti di tanah. |
| **204** | `                    if p_dist < 60:` | Jika pemain berada sangat dekat dengan peti (< 60px). |
| **205** | `                        hint = self.font.render("PRESS ENTER TO CLAIM SUPPLY", True, (0, 255, 255))` | Membuat permukaan teks petunjuk cyan. |
| **206** | `                        screen.blit(hint, (screen_pos[0] - hint.get_width() // 2, screen_pos[1] - 35))` | Menempelkan petunjuk tepat di atas peti suplai. |
| **207** | `        if player and not self.crate and self.crate_cooldown <= 0:` | Jika helipad kosong dan siap menerima panggilan drop. |
| **208** | `            h_dist = math.hypot(player.pos[0] - 430, player.pos[1] - 410)` | Menghitung jarak pemain ke landasan helipad. |
| **209** | `            if h_dist < 60:` | Jika berada sangat dekat helipad (< 60px). |
| **210** | `                h_pos = camera.apply((430, 410))` | Menghitung posisi koordinat layar helipad. |
| **211** | `                hint = self.font.render("PRESS ENTER TO CALL SUPPLY DROP", True, (0, 255, 255))` | Membuat teks petunjuk cyan. |
| **212** | `                screen.blit(hint, (h_pos[0] - hint.get_width() // 2, h_pos[1] - 25))` | Menempelkan petunjuk di atas helipad. |
| **213** | `        if player:` | Memeriksa objek pemain. |
| **214** | `            w_dist = math.hypot(player.pos[0] - 145, player.pos[1] - 875)` | Menghitung jarak pemain ke loker wardrobe. |
| **215** | `            if w_dist < 60:` | Jika berada dekat loker wardrobe (< 60px). |
| **216** | `                w_pos = camera.apply((145, 875))` | Menghitung posisi koordinat layar loker pakaian. |
| **217** | `                hint = self.font.render("PRESS ENTER TO USE WARDROBE", True, (0, 255, 255))` | Membuat teks petunjuk pemakaian loker pakaian. |
| **218** | `                screen.blit(hint, (w_pos[0] - hint.get_width() // 2, w_pos[1] - 25))` | Menempelkan petunjuk di atas loker pakaian. |
| **219** | `        upg_pos = camera.apply((1500, 850))` | Menghitung posisi koordinat layar komputer stasiun upgrade (1500, 850). |
| **220** | `        pygame.draw.rect(screen, (50, 60, 70), (upg_pos[0] - 20, upg_pos[1] - 30, 40, 60), border_radius=5)` | Menggambar badan luar konsol stasiun berwarna abu-abu biru dengan sudut membulat. |
| **221** | `        pygame.draw.rect(screen, (0, 255, 255), (upg_pos[0] - 20, upg_pos[1] - 30, 40, 60), 2, border_radius=5)` | Menggambar garis tepi konsol berwarna cyan neon terang. |
| **222** | `        pygame.draw.rect(screen, (10, 20, 30), (upg_pos[0] - 14, upg_pos[1] - 22, 28, 20))` | Menggambar layar gelap monitor komputer konsol. |
| **223** | `        pygame.draw.rect(screen, (0, 200, 200), (upg_pos[0] - 14, upg_pos[1] - 22, 28, 20), 1)` | Menggambar garis tepi layar monitor komputer berwarna cyan redup. |
| **224** | `        pulse = (pygame.time.get_ticks() // 400) % 2` | Membuat nilai modulo 2 berdasarkan waktu sistem untuk efek denyut lampu indikator. |
| **225** | `        screen_color = (0, 255, 120) if pulse else (0, 150, 80)` | Memilih warna hijau berkedip (hijau terang jika pulse=1, hijau gelap jika pulse=0). |
| **226** | `        pygame.draw.circle(screen, screen_color, (upg_pos[0] - 5, upg_pos[1] - 12), 2)` | Menggambar lampu indikator kiri yang berkedip hijau di layar monitor. |
| **227** | `        pygame.draw.circle(screen, (255, 50, 50), (upg_pos[0] + 5, upg_pos[1] - 12), 2)` | Menggambar lampu indikator kanan berwarna merah statis. |
| **228** | `        pygame.draw.rect(screen, (30, 35, 40), (upg_pos[0] - 22, upg_pos[1] - 2, 44, 8), border_radius=2)` | Menggambar keyboard fisik konsol di bagian bawah layar stasiun upgrade. |
| **229** | `        if player:` | Memeriksa objek pemain. |
| **230** | `            upg_dist = math.hypot(player.pos[0] - 1500, player.pos[1] - 850)` | Menghitung jarak pemain ke komputer stasiun upgrade. |
| **231** | `            if upg_dist < 60:` | Jika pemain berdiri dekat komputer stasiun upgrade (< 60px). |
| **232** | `                hint = self.font.render("PRESS ENTER TO UPGRADE WEAPONS", True, (0, 255, 255))` | Membuat teks petunjuk pemakaian toko peningkatan senjata. |
| **233** | `                screen.blit(hint, (upg_pos[0] - hint.get_width() // 2, upg_pos[1] - 55))` | Menempelkan petunjuk di atas stasiun upgrade. |
| **234** | `        for npc in self.npcs:` | Melakukan iterasi untuk menggambar setiap NPC di Sanctuary. |
| **235** | `            npc.draw(screen, camera)` | Menggambar sprite NPC disesuaikan posisi kamera. |
| **236** | `            d_pos = camera.apply(npc.pos)` | Menghitung koordinat kepala NPC di layar. |
| **237** | `            name_tag = self.font.render(npc.name, True, (255, 255, 255))` | Merender nama NPC berwarna putih. |
| **238** | `            screen.blit(name_tag, (d_pos[0] + 16 - name_tag.get_width() // 2, d_pos[1] - 15))` | Menampilkan label nama di atas kepala NPC dengan penyeimbang sumbu X. |
| **239** | `        for ft in self.floating_texts:` | Melakukan iterasi untuk menggambar setiap teks melayang aktif. |
| **240** | `            shadow_surf = self.font.render(ft['text'], True, (0, 0, 0))` | Merender teks bayangan berwarna hitam (RGB 0,0,0) sebagai outline. |
| **241** | `            text_surf = self.font.render(ft['text'], True, ft['color'])` | Merender teks utama berwarna sesuai kriteria partikel. |
| **242** | `            sp = camera.apply(ft['pos'])` | Menghitung koordinat layar teks melayang. |
| **243** | `            screen.blit(shadow_surf, (sp[0] + 1, sp[1] + 1))` | Menggambar teks bayangan hitam dengan pergeseran 1px (Y+1, X+1). |
| **244** | `            screen.blit(text_surf, sp)` | Menggambar teks utama di atas bayangannya pada posisi koordinat aslinya. |
| **245** | `    def get_status_text(self):` | Metode mengambil status objektif cerita Sanctuary aktif saat ini. |
| **246** | `        if self.alarm_active: return "STATUS: PERTAHANAN AKTIF!"` | Mengembalikan status alarm pertahanan kota aktif jika terpicu. |
| **247** | `        if not self.elder_met: return "OBJEKTIF: Cari dan bicara ke Penatua Aris (Warna Oranye)"` | Mengembalikan petunjuk mencari Penatua jika belum pernah bertemu. |
| **248** | `        return "OBJEKTIF: Bicara ke Kapten Jaka di jalan (Warna Biru)"` | Mengembalikan petunjuk bertemu Kapten Jaka jika prasyarat terpenuhi. |
| **249** | *(Baris Kosong)* | Akhir dari berkas kode sumber. |
