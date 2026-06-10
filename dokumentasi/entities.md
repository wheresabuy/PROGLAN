# Penjelasan Kode: `entities.py`

Dokumen ini berisi penjelasan detail baris demi baris untuk file `/home/abuyyy/PemogramanLanjut/src/entities/entities.py`. Penjelasan ini ditulis dalam bahasa Indonesia untuk membantu persiapan demo program.

---

## Deskripsi & Tujuan File
File `entities.py` mendefinisikan kelas-kelas entitas permainan (game entities) yang mendiami dunia Sanctuary maupun area pertempuran:
1. **`Player`**: Karakter utama pemain yang dapat bergerak dengan kontrol keyboard/kemampuan input proxy gestur, memiliki status nyawa, peningkatan kecepatan dari adrenalin, dan menangani render sprite animasi berskala.
2. **`NPC`**: Karakter non-pemain ramah di Sanctuary yang dapat berpatroli secara acak (wandering) di sekitar titik awal spawn, dibatasi jarak maksimum tertentu, dan memiliki animasi sprite pakaian/rambut terpisah.
3. **`ZombieNPC`**: Karakter musuh (zombie) yang mengejar pemain ketika pemain sedang berlari (`state == 'run'`) atau terpancing oleh item taktis Umpan (`Decoy`). Zombie dapat menerima damage terbakar dari Molotov dan memiliki timer stun.
4. **`Loot`**: Barang jarahan/drop item di tanah (seperti senjata/suplai) yang memiliki animasi melayang naik-turun secara smooth menggunakan fungsi sinus waktu, serta mendeteksi interaksi dengan pemain.
5. **`TacticalItem`**: Objek taktis yang dilempar oleh pemain (seperti Molotov, Decoy, atau Taser) yang bergerak meluncur menuju koordinat target lemparan sebelum aktif memberikan efek area (aoe/stunning) selama durasi tertentu.

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel penjelasan baris demi baris dari kode sumber `entities.py`:

| Baris | Kode Sumber | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import pygame, math, random` | Mengimpor pustaka Pygame untuk rendering grafis, math untuk kalkulasi jarak/trigonometri, dan random untuk nilai acak. |
| **2** | `from src.core.engine import Spritesheet` | Mengimpor kelas utilitas `Spritesheet` untuk memotong dan menskalakan animasi gambar karakter. |
| **3** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **4** | `class Player:` | Deklarasi kelas `Player` untuk mempresentasikan karakter utama pemain. |
| **5** | `    def __init__(self, x, y):` | Konstruktor kelas `Player` dengan parameter posisi awal `(x, y)`. |
| **6** | `        self.pos, self.direction, self.state, self.current_col = [x, y], 'down', 'stand', 0` | Menginisialisasi posisi, arah awal ('down'), kondisi awal ('stand'), dan kolom frame animasi awal ke 0. |
| **7** | `        self.sheet = Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v00.png", 8, 8, scale=2.0)` | Memuat spritesheet tubuh dasar manusia untuk pemain dengan skala pembesaran 2.0x. |
| **8** | `        self.clothing_sheet = Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v01.png", 8, 8, scale=2.0)` | Memuat spritesheet pakaian default untuk pemain (baju petualang). |
| **9** | `        self.clothing_active, self.hair_sheet, self.hat_sheet = True, Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_dap1_v08.png", 8, 8, scale=2.0), None` | Mengaktifkan pakaian default, memuat model rambut pemain, dan mengeset topi default ke `None`. |
| **10** | `        self.frame_timer, self.anim_speed, self.health, self.injured, self.speed_multiplier, self.adrenaline_timer = 0, 8, 100, True, 0.4, 0` | Mengeset variabel timer animasi, kecepatan pergantian frame (8 tick), darah awal (100), status terluka awal, pengali kecepatan awal (40% di Sanctuary), dan durasi status adrenalin (0). |
| **11** | `    def update(self, keys, collision_mask=None, map_size=None):` | Metode untuk memperbarui logika posisi dan animasi pemain berdasarkan tombol keyboard yang ditekan. |
| **12** | `        ad_bonus = 2.0 if self.adrenaline_timer > 0 else 1.0` | Menghitung bonus kecepatan 2.0x lipat jika status adrenalin sedang aktif (> 0). |
| **13** | `        if self.adrenaline_timer > 0: self.adrenaline_timer -= 1` | Jika timer adrenalin aktif, kurangi nilainya sebanyak 1 frame. |
| **14** | `        speed = float((5.0 if keys[pygame.K_LSHIFT] else 3.0) * ad_bonus * self.speed_multiplier)` | Menghitung kecepatan gerak: 5.0 jika berlari (K_LSHIFT) atau 3.0 jika berjalan biasa, dikalikan dengan bonus adrenalin dan speed multiplier. |
| **15** | `        moving = False` | Menetapkan status pergerakan awal pemain adalah tidak bergerak (`moving = False`). |
| **16** | `        if keys[pygame.K_RIGHT]: self.pos[0] += speed; self.direction = 'right'; moving = True` | Jika tombol kanan ditekan: tambah koordinat X, ubah arah ke 'right', dan set `moving = True`. |
| **17** | `        if keys[pygame.K_LEFT]:  self.pos[0] -= speed; self.direction = 'left'; moving = True` | Jika tombol kiri ditekan: kurangi koordinat X, ubah arah ke 'left', dan set `moving = True`. |
| **18** | `        if keys[pygame.K_UP]:    self.pos[1] -= speed; self.direction = 'up'; moving = True` | Jika tombol atas ditekan: kurangi koordinat Y, ubah arah ke 'up', dan set `moving = True`. |
| **19** | `        if keys[pygame.K_DOWN]:  self.pos[1] += speed; self.direction = 'down'; moving = True` | Jika tombol bawah ditekan: tambah koordinat Y, ubah arah ke 'down', dan set `moving = True`. |
| **20** | `        if map_size:` | Jika parameter ukuran peta dikirimkan (batas tepi peta). |
| **21** | `            self.pos[0] = max(0, min(self.pos[0], map_size[0] - 32))` | Membatasi koordinat X agar pemain tidak keluar dari tepi kiri (0) dan tepi kanan peta (lebar peta - 32px). |
| **22** | `            self.pos[1] = max(0, min(self.pos[1], map_size[1] - 32))` | Membatasi koordinat Y agar pemain tidak keluar dari tepi atas (0) dan tepi bawah peta (tinggi peta - 32px). |
| **23** | `        self.state = 'run' if (keys[pygame.K_LSHIFT] and moving) else 'walk' if moving else 'stand'` | Menentukan kondisi gerakan pemain: 'run' jika menekan Shift & bergerak, 'walk' jika hanya bergerak, dan 'stand' jika diam. |
| **24** | `        self.frame_timer += 1` | Meningkatkan nilai timer frame animasi untuk pergantian langkah. |
| **25** | `        if self.frame_timer >= self.anim_speed:` | Jika timer mencapai batas kecepatan animasi yang ditentukan. |
| **26** | `            self.frame_timer = 0` | Mengatur ulang timer frame animasi kembali ke 0. |
| **27** | `            self.current_col = 0 if self.state == 'stand' else (self.current_col + 1) % 6 if self.state == 'walk' else 6 + (self.current_col + 1) % 2` | Memilih kolom frame sprite: 0 jika diam, indeks 0 s.d 5 bergantian jika berjalan, dan indeks 6 s.d 7 bergantian jika berlari. |
| **28** | `    def draw(self, screen, camera=None):` | Metode untuk merender gambar sprite pemain ke layar. |
| **29** | `        row = {'down': 0, 'up': 1, 'right': 2, 'left': 3}[self.direction] + (0 if self.state == 'stand' else 4)` | Menentukan baris pada spritesheet: baris 0-3 untuk diam (sesuai arah), atau ditambah offset 4 (baris 4-7) untuk berjalan/berlari. |
| **30** | `        dp = camera.apply(self.pos) if camera else self.pos` | Menghitung posisi rendering di layar disesuaikan dengan posisi kamera scroll. |
| **31** | `        screen.blit(self.sheet.get_frame(row, self.current_col), dp)` | Menggambar sprite tubuh dasar pemain di posisi render. |
| **32** | `        if self.clothing_active and self.clothing_sheet: screen.blit(self.clothing_sheet.get_frame(row, self.current_col), dp)` | Menggambar layer sprite pakaian di atas tubuh dasar jika berstatus aktif. |
| **33** | `        if self.hair_sheet: screen.blit(self.hair_sheet.get_frame(row, self.current_col), dp)` | Menggambar layer sprite rambut pemain di atas tubuh dasar. |
| **34** | `        if self.hat_sheet: screen.blit(self.hat_sheet.get_frame(row, self.current_col), dp)` | Menggambar layer sprite topi/aksesoris kepala jika ada. |
| **35** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **36** | `class NPC:` | Deklarasi kelas `NPC` untuk karakter non-pemain yang ramah di dunia Sanctuary. |
| **37** | `    def __init__(self, name, x, y, role, base_path, outfit_path=None, hair_path=None):` | Konstruktor kelas `NPC` menerima nama, koordinat awal, peran, dan path asset spritesheet tubuh, pakaian, dan rambut. |
| **38** | `        self.name, self.pos, self.role = name, [x, y], role` | Menyimpan nama, list koordinat posisi `[x, y]`, dan peran (role) dari NPC. |
| **39** | `        self.sheet = Spritesheet(base_path, 8, 8, scale=2.0)` | Memuat spritesheet tubuh dasar NPC dengan skala 2.0x. |
| **40** | `        self.outfit_sheet = Spritesheet(outfit_path, 8, 8, scale=2.0) if outfit_path else None` | Memuat spritesheet baju NPC jika ada. |
| **41** | `        self.hair_sheet = Spritesheet(hair_path, 8, 8, scale=2.0) if hair_path else None` | Memuat spritesheet rambut NPC jika ada. |
| **42** | `        self.direction, self.state, self.current_col, self.frame_timer, self.anim_speed = 'down', 'stand', 0, 0, 8` | Mengatur arah awal ('down'), kondisi awal ('stand'), indeks kolom animasi (0), timer frame (0), dan kecepatan animasi (8). |
| **43** | `        self.wander_timer, self.target_dir, self.speed, self.spawn_pos, self.max_wander_dist = random.randint(30, 90), [0, 0], 1.0, [x, y], 100` | Menginisialisasi waktu tunggu patroli acak, arah tujuan patroli, kecepatan gerak (1.0), posisi asal spawn, dan jarak radius patroli maksimal (100px). |
| **44** | `    def update(self, map_size=None):` | Metode untuk memperbarui AI pergerakan acak NPC. |
| **45** | `        self.wander_timer -= 1` | Mengurangi timer tunggu patroli acak NPC sebanyak 1 per frame. |
| **46** | `        if self.wander_timer <= 0:` | Jika timer habis, saatnya mengambil keputusan patroli baru. |
| **47** | `            self.wander_timer = random.randint(60, 180)` | Mengatur ulang timer tunggu acak berikutnya antara 60 hingga 180 frame. |
| **48** | `            if random.random() < 0.5:` | Peluang 50% untuk memutuskan diam saja di tempat. |
| **49** | `                self.state, self.target_dir = 'stand', [0, 0]` | Mengeset kondisi diam dan arah tujuan ke `[0, 0]`. |
| **50** | `            else:` | Peluang 50% lainnya untuk memutuskan bergerak berjalan patroli. |
| **51** | `                angle = random.uniform(0, 2 * math.pi)` | Menghasilkan sudut pergerakan acak dalam radian (0 hingga 2*pi). |
| **52** | `                self.target_dir = [math.cos(angle), math.sin(angle)]` | Menghitung vektor arah X dan Y berdasarkan sudut menggunakan fungsi kosinus dan sinus. |
| **53** | `                self.state = 'walk'` | Mengubah kondisi NPC menjadi sedang berjalan (`'walk'`). |
| **54** | `                dx, dy = self.target_dir` | Menyalin nilai arah pergerakan X dan Y. |
| **55** | `                self.direction = ('right' if dx > 0 else 'left') if abs(dx) > abs(dy) else ('down' if dy > 0 else 'up')` | Menentukan arah hadap NPC ('right', 'left', 'up', 'down') berdasarkan vektor arah pergerakan terbesar. |
| **56** | `        if self.state == 'walk':` | Jika kondisi NPC saat ini adalah sedang berjalan. |
| **57** | `            nx, ny = self.pos[0] + self.target_dir[0]*self.speed, self.pos[1] + self.target_dir[1]*self.speed` | Menghitung koordinat posisi target baru `nx` dan `ny` berdasarkan arah dan kecepatan. |
| **58** | `            if math.hypot(nx - self.spawn_pos[0], ny - self.spawn_pos[1]) < self.max_wander_dist:` | Memeriksa jarak dari posisi baru ke posisi spawn awal. Jika masih di dalam batas radius (100px). |
| **59** | `                self.pos = [nx, ny]` | Memperbarui posisi NPC ke koordinat baru tersebut. |
| **60** | `            else:` | Jika posisi baru berada di luar batas radius patroli. |
| **61** | `                self.state, self.target_dir, self.wander_timer = 'stand', [0, 0], 15` | Membatalkan gerakan, diam di tempat, dan set timer keputusan baru ke 15 frame lagi. |
| **62** | `        if map_size:` | Jika dibatasi oleh ukuran peta. |
| **63** | `            self.pos[0] = max(0, min(self.pos[0], map_size[0] - 32))` | Membatasi posisi X di dalam area peta agar NPC tidak berjalan ke luar peta. |
| **64** | `            self.pos[1] = max(0, min(self.pos[1], map_size[1] - 32))` | Membatasi posisi Y di dalam area peta. |
| **65** | `        self.frame_timer += 1` | Menambah timer frame animasi NPC. |
| **66** | `        if self.frame_timer >= self.anim_speed:` | Jika timer mencapai batas interval animasi. |
| **67** | `            self.frame_timer = 0` | Mereset timer frame animasi NPC ke 0. |
| **68** | `            self.current_col = 0 if self.state == 'stand' else (self.current_col + 1) % 6` | Mengeset frame: 0 jika diam, atau bergantian kolom 0 s.d 5 jika berjalan. |
| **69** | `    def draw(self, screen, camera=None):` | Metode untuk menggambar grafis sprite NPC ke layar. |
| **70** | `        row = {'down': 0, 'up': 1, 'right': 2, 'left': 3}[self.direction] + (0 if self.state == 'stand' else 4)` | Memilih baris di spritesheet berdasarkan arah dan status (diam vs berjalan). |
| **71** | `        dp = camera.apply(self.pos) if camera else self.pos` | Menghitung posisi gambar NPC disesuaikan pergerakan kamera. |
| **72** | `        screen.blit(self.sheet.get_frame(row, self.current_col), dp)` | Menggambar layer sprite tubuh dasar NPC. |
| **73** | `        if self.outfit_sheet: screen.blit(self.outfit_sheet.get_frame(row, self.current_col), dp)` | Menggambar layer pakaian NPC jika ada. |
| **74** | `        if self.hair_sheet: screen.blit(self.hair_sheet.get_frame(row, self.current_col), dp)` | Menggambar layer rambut NPC jika ada. |
| **75** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **76** | `class ZombieNPC:` | Deklarasi kelas `ZombieNPC` untuk musuh zombie di peta pertempuran. |
| **77** | `    def __init__(self, x, y):` | Konstruktor kelas `ZombieNPC` menerima posisi awal `(x, y)`. |
| **78** | `        self.pos, self.sheet = [x, y], Spritesheet("assets/enemies/zombie_new.png", 8, 8, scale=2.0)` | Menyimpan posisi dan memuat spritesheet aset zombie baru berskala 2.0x. |
| **79** | `        self.direction, self.state, self.current_col, self.frame_timer, self.anim_speed, self.speed, self.stun_timer, self.health = 'down', 'stand', 0, 0, 10, 2.5, 0, 100` | Inisialisasi arah awal ('down'), kondisi ('stand'), indeks kolom frame, timer animasi, kecepatan animasi (10 tick), kecepatan jalan zombie (2.5), durasi stun (0), dan nyawa zombie (100). |
| **80** | `    def update(self, player_pos, player_state, tactical_items=[]):` | Metode untuk memperbarui perilaku kecerdasan buatan (AI) zombie mengejar pemain/item taktis. |
| **81** | `        if self.stun_timer > 0:` | Memeriksa apakah zombie sedang ter-stun (misalnya terkena serangan Taser/Molotov). |
| **82** | `            self.stun_timer -= 1; self.state = 'stand'; return` | Jika ter-stun: kurangi durasi stun, set kondisi diam (`'stand'`), dan batalkan pergerakan frame ini. |
| **83** | `        t_pos, agg = player_pos, (player_state == 'run')` | Menetapkan target kejar default ke pemain, dan status agresif aktif (`agg = True`) jika pemain berlari (`'run'`). |
| **84** | `        for item in tactical_items:` | Iterasi untuk mendeteksi keberadaan item taktis yang dilempar di peta. |
| **85** | `            if item.item_type == "Decoy" and item.active and item.reached_target and math.hypot(item.pos[0] - self.pos[0], item.pos[1] - self.pos[1]) < 400:` | Jika ada item Umpan (`Decoy`) yang aktif, sudah mendarat di target, dan jaraknya dekat (< 400px). |
| **86** | `                t_pos, agg = item.pos, True; break` | Alihkan target kejaran zombie ke posisi Umpan tersebut, dan set status agresif ke `True`. Hentikan perulangan. |
| **87** | `        for item in tactical_items:` | Iterasi kedua untuk mendeteksi interaksi serangan Molotov. |
| **88** | `            if item.item_type == "Molotov" and item.reached_target and item.active and math.hypot(item.pos[0] - self.pos[0], item.pos[1] - self.pos[1]) < 50:` | Jika zombie berdiri di dalam radius api Molotov (< 50px) yang sedang aktif di tanah. |
| **89** | `                self.health -= 2; self.stun_timer = 20` | Kurangi darah zombie sebanyak 2 per frame, dan beri efek stun selama 20 frame. |
| **90** | `        if agg and self.health > 0:` | Jika zombie dalam kondisi agresif (mengejar target) dan masih hidup. |
| **91** | `            dx, dy = t_pos[0] - self.pos[0], t_pos[1] - self.pos[1]` | Menghitung jarak horizontal (dx) dan vertikal (dy) ke posisi target. |
| **92** | `            dist = math.hypot(dx, dy)` | Menghitung jarak lurus ke target. |
| **93** | `            if dist > 10:` | Jika jarak ke target masih lebih dari 10px. |
| **94** | `                self.pos[0] += (dx / dist) * self.speed` | Gerakkan zombie mendekati koordinat X target sesuai rasio jarak dan kecepatannya. |
| **95** | `                self.pos[1] += (dy / dist) * self.speed` | Gerakkan zombie mendekati koordinat Y target. |
| **96** | `                self.state = 'walk'` | Ubah status kondisi zombie menjadi berjalan (`'walk'`). |
| **97** | `                self.direction = ('right' if dx > 0 else 'left') if abs(dx) > abs(dy) else ('down' if dy > 0 else 'up')` | Menentukan arah hadap zombie berdasarkan arah pergerakan dominan. |
| **98** | `            else: self.state = 'stand'` | Jika sangat dekat (< 10px), ubah status menjadi diam di tempat. |
| **99** | `        else: self.state = 'stand'` | Jika tidak agresif (pemain berjalan pelan/tidak ada decoy), zombie diam di tempat. |
| **100** | `        self.frame_timer += 1` | Tambah timer animasi zombie. |
| **101** | `        if self.frame_timer >= self.anim_speed:` | Jika timer mencapai interval pergantian frame animasi. |
| **102** | `            self.frame_timer = 0` | Mereset timer frame ke 0. |
| **103** | `            self.current_col = 0 if self.state == 'stand' else (self.current_col + 1) % 6` | Mengganti kolom frame: 0 jika diam, atau 0 s.d 5 secara bergiliran jika berjalan. |
| **104** | `    def draw(self, screen, camera=None):` | Metode untuk menggambar zombie di layar. |
| **105** | `        row = {'down': 0, 'up': 1, 'right': 2, 'left': 3}[self.direction] + (0 if self.state == 'stand' else 4)` | Memilih baris spritesheet berdasarkan arah hadap dan status. |
| **106** | `        dp = camera.apply(self.pos) if camera else self.pos` | Menyesuaikan posisi gambar zombie dengan posisi kamera. |
| **107** | `        screen.blit(self.sheet.get_frame(row, self.current_col), dp)` | Menggambar sprite zombie ke layar. |
| **108** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **109** | `class Loot:` | Deklarasi kelas `Loot` untuk item jarahan di lantai. |
| **110** | `    def __init__(self, name, x, y, item_type, image=None, prompt=None):` | Konstruktor menerima nama item, koordinat `(x, y)`, jenis item, gambar opsional, dan petunjuk teks interaksi opsional. |
| **111** | `        self.name, self.pos, self.item_type = name, (x, y), item_type` | Menyimpan nama, koordinat posisi, dan jenis item loot. |
| **112** | `        self.prompt, self.collected, self.hover_offset = prompt or f"Tekan [ENTER] untuk ambil {name}", False, 0` | Menetapkan teks petunjuk interaksi default, status belum diambil (`collected = False`), dan offset melayang awal (0). |
| **113** | `        if image:` | Jika gambar item dikirimkan sebagai argumen. |
| **114** | `            if isinstance(image, str):` | Memeriksa apakah parameter gambar bertipe string (path file gambar). |
| **115** | `                try:` | Membuka blok penanganan kesalahan saat memuat gambar eksternal. |
| **116** | `                    self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (64, 64))` | Memuat gambar dari path, menjaga transparansi, dan menskalakannya menjadi ukuran 64x64px. |
| **117** | `                except:` | Jika pemuatan gambar dari path gagal/error. |
| **118** | `                    self.image = pygame.Surface((40, 40)); self.image.fill((255, 0, 0))` | Opsi darurat: buat permukaan merah berukuran 40x40px sebagai pengganti. |
| **119** | `            else: self.image = pygame.transform.scale(image, (64, 64))` | Jika parameter merupakan objek Surface Pygame, langsung skala menjadi 64x64px. |
| **120** | `        else:` | Jika tidak ada parameter gambar yang dikirimkan. |
| **121** | `            self.image = pygame.Surface((40, 40)); self.image.fill((255, 215, 0))` | Buat permukaan berwarna emas (255, 215, 0) berukuran 40x40px. |
| **122** | `        self.rect = self.image.get_rect(topleft=(x, y))` | Mengambil pembatas persegi panjang (`Rect`) dari gambar item diposisikan di topleft `(x, y)`. |
| **123** | `    def check_interaction(self, player_pos):` | Metode memeriksa apakah pemain berada dekat dengan item loot tersebut. |
| **124** | `        return math.hypot(self.pos[0] - player_pos[0], self.pos[1] - player_pos[1]) < 100` | Mengembalikan nilai `True` jika jarak pemain ke posisi item kurang dari 100px. |
| **125** | `    def get_interaction_prompt(self): return self.prompt` | Mengambil teks pesan instruksi pengambilan item. |
| **126** | `    def draw(self, screen, player_pos, camera=None):` | Metode untuk menggambar item loot ke layar dengan animasi melayang. |
| **127** | `        if not self.collected:` | Menggambar item hanya jika statusnya belum diambil oleh pemain. |
| **128** | `            self.hover_offset = math.sin(pygame.time.get_ticks() * 0.005) * 10` | Animasi melayang: gunakan fungsi gelombang sinus waktu aktif sistem untuk menghasilkan gerakan naik-turun berkisar +/- 10px. |
| **129** | `            dp = camera.apply(self.pos) if camera else self.pos` | Menghitung koordinat rendering disesuaikan dengan posisi gulir kamera. |
| **130** | `            screen.blit(self.image, (dp[0], dp[1] + self.hover_offset))` | Menggambar gambar item loot di layar dengan tambahan offset melayang naik-turun pada sumbu Y. |
| **131** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **132** | `class TacticalItem:` | Deklarasi kelas `TacticalItem` untuk item taktis yang dapat dilempar (Molotov, Decoy, Taser). |
| **133** | `    def __init__(self, x, y, item_type, target_pos=None):` | Konstruktor menerima posisi lempar awal `(x, y)`, jenis item, dan posisi target koordinat pendaratan. |
| **134** | `        self.pos, self.item_type, self.timer, self.active, self.target_pos, self.speed = [x, y], item_type, 0, True, target_pos, 8` | Inisialisasi posisi awal, jenis item, timer aktif (0), status aktif (`True`), posisi target lemparan, dan kecepatan luncur peluru item (8px per frame). |
| **135** | `        self.reached_target = False if target_pos else True` | Mengeset status pendaratan: `False` jika ada koordinat target lempar (harus meluncur dulu), atau `True` jika tidak ada. |
| **136** | `    def update(self):` | Metode untuk memperbarui fisika peluncuran dan durasi aktif item taktis. |
| **137** | `        if not self.reached_target and self.target_pos:` | Jika item belum mendarat di target dan memiliki tujuan target lempar. |
| **138** | `            dx, dy = self.target_pos[0] - self.pos[0], self.target_pos[1] - self.pos[1]` | Menghitung jarak horizontal dan vertikal ke posisi target lempar. |
| **139** | `            dist = math.hypot(dx, dy)` | Menghitung jarak total tersisa. |
| **140** | `            if dist < self.speed:` | Jika sisa jarak lebih kecil dari kecepatan luncur (8px). |
| **141** | `                self.pos, self.reached_target = list(self.target_pos), True` | Item langsung tiba di posisi target tujuan dan status `reached_target` diset `True`. |
| **142** | `            else:` | Jika sisa jarak masih lebih besar dari kecepatan. |
| **143** | `                self.pos[0] += (dx / dist) * self.speed` | Menggeser posisi X mendekati target sesuai rasio kecepatan. |
| **144** | `                self.pos[1] += (dy / dist) * self.speed` | Menggeser posisi Y mendekati target. |
| **145** | `        self.timer += 1` | Menambahkan nilai timer aktif item taktis sebanyak 1 per frame. |
| **146** | `        dur = {"Molotov": 180, "Decoy": 600, "Taser": 10}.get(self.item_type, 100)` | Menentukan durasi aktif: Molotov aktif 180 frame (~3 detik), Decoy aktif 600 frame (~10 detik), Taser aktif 10 frame. |
| **147** | `        if self.timer > dur: self.active = False` | Jika timer aktif melebihi batas durasi item, set status keaktifan item menjadi `False` (item hancur/mati). |
| **148** | `    def draw(self, screen, camera):` | Metode untuk merender efek visual item taktis ke layar. |
| **149** | `        dp = camera.apply(self.pos)` | Menghitung koordinat rendering di layar sesuai dengan pergeseran kamera scroll. |
| **150** | `        if self.item_type == "Molotov" and self.reached_target:` | Efek visual Molotov: jika bertipe Molotov dan sudah mendarat di tanah. |
| **151** | `            pygame.draw.circle(screen, (255, 100, 0) if self.timer % 10 < 5 else (255, 200, 0), dp, 50)` | Menggambar area api lingkaran di tanah berjejaring 50px yang bergantian warna oranye (255, 100, 0) dan kuning (255, 200, 0) setiap 5 frame untuk efek kedipan api. |
| **152** | `        elif self.item_type == "Decoy":` | Efek visual Umpan (Decoy). |
| **153** | `            c = (0, 0, 255) if self.timer % 20 < 10 else (100, 100, 255)` | Menggunakan warna biru berkedip setiap 10 frame (biru pekat vs biru terang). |
| **154** | `            pygame.draw.circle(screen, c, dp, 10)` | Menggambar lingkaran kecil umpan berjejari 10px di tengah. |
| **155** | `            pygame.draw.circle(screen, c, dp, (self.timer % 40) * 2, 1)` | Menggambar lingkaran radar pemancar suara yang mengembang keluar secara dinamis (efek gelombang suara penarik zombie). |
| **156** | `        elif self.item_type == "Taser":` | Efek visual Taser. |
| **157** | `            pygame.draw.line(screen, (255, 255, 255), dp, (dp[0]+10, dp[1]-10), 2)` | Menggambar garis petir kecil berwarna putih (255, 255, 255) setebal 2px dari titik taser ke arah atas-kanan. |
| **158** | *(Baris Kosong)* | Akhir dari berkas kode sumber. |

---

## Hubungan dan Alur Penggunaan Entitas

Setiap entitas bekerja sama di bawah naungan game loop utama:
* **Pergerakan Pemain**: Pemain diperbarui menggunakan metode `.update()` di game loop Sanctuary atau pertahanan. Pakaian, rambut, dan aksesoris digambar terpisah agar dapat diubah secara dinamis.
* **Perilaku AI Zombie**: Ketika diaktifkan di kota pertahanan, `ZombieNPC` memantau list `tactical_items`. Jika pemain melempar `Decoy`, zombie beralih arah mengejar koordinat umpan alih-alih mengejar pemain. Jika zombie berjalan di atas api `Molotov`, nyawanya terpangkas cepat dan mengalami status stun.
* **Fisika Lemparan Barang**: Ketika pemain menekan klik kanan untuk melempar item taktis (misal Molotov), game memicu pembuatan objek `TacticalItem` baru. Objek tersebut berpindah sumbu X/Y frame demi frame sampai tiba di target klik kursor (`reached_target = True`), lalu memicu efek visual dan damage.
* **Sistem Looting**: Ketika zombie musuh dikalahkan, ia dapat meninggalkan item `Loot` di tanah. Pemain yang mendekati item tersebut (< 100px) akan melihat teks petunjuk `get_interaction_prompt()`. Jika menekan tombol Enter, item loot diambil, memicu fungsi internal pemain, dan status item diset `.collected = True` untuk dihapus dari layar.
