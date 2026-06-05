# Dokumentasi dan Penjelasan Baris Demi Baris: `sanctuary_logic.py`

## Deskripsi & Tujuan File
File `sanctuary_logic.py` bertanggung jawab untuk mengatur seluruh logika dan interaksi lingkungan di dalam zona aman ("The Sanctuary") pada game. Di zona ini, pemain tidak langsung bertempur, melainkan dapat memulihkan diri, memanggil bantuan suplai, mengganti pakaian di loker, serta berinteraksi dengan karakter non-pemain (NPC) untuk memajukan alur cerita game ke tahap pertempuran aktif.

---

## Daftar Import
File ini mengimpor tiga modul dasar berikut:
1. **`pygame`**: Pustaka utama yang digunakan untuk penanganan grafis 2D, rendering gambar peta, penggambaran bentuk (seperti lingkaran dan persegi panjang), pemrosesan teks/font, serta pemetaan koordinat game.
2. **`math`**: Digunakan untuk fungsi matematika dasar, khususnya `math.hypot()` untuk menghitung jarak antara pemain dengan objek-objek interaktif (seperti api unggun, helipad, loker, dan NPC) berdasarkan rumus jarak Euclidean.
3. **`random`**: Digunakan untuk menghasilkan variasi acak nilai numerik, seperti kecepatan gerak partikel, laju memudarnya partikel, posisi acak teks melayang, serta pemilihan pesan dialog acak dari daftar dialog NPC.

---

## Penjelasan Baris Demi Baris

Berikut adalah rincian penjelasan untuk setiap baris kode yang ada di dalam `sanctuary_logic.py`:

### 1. Definisi Kelas `SanctuaryParticle` (Baris 1 - 23)
Bagian ini mendefinisikan partikel visual kecil yang digunakan untuk mempercantik efek lingkungan (seperti percikan api unggun, pendaran hijau di kasur medis, cipratan air di kolam, dan debu pendaratan peti suplai).

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| 1 | `import pygame` | Mengimpor pustaka Pygame untuk rendering grafis, teks, dan penanganan input. |
| 2 | `import math` | Mengimpor modul `math` untuk perhitungan matematika seperti fungsi `hypot` untuk jarak. |
| 3 | `import random` | Mengimpor modul `random` untuk menghasilkan angka acak untuk partikel dan dialog. |
| 4 | | Baris kosong sebagai pemisah. |
| 5 | `class SanctuaryParticle:` | Mendefinisikan kelas `SanctuaryParticle` untuk efek partikel visual (misalnya percikan api, efek penyembuhan, percikan air). |
| 6 | `    def __init__(self, x, y, color, vx=None, vy=None, size=None):` | Konstruktor kelas partikel yang menerima koordinat awal `(x, y)`, warna `color`, kecepatan horizontal `vx`, kecepatan vertikal `vy`, dan ukuran `size`. |
| 7 | `        self.pos = [x, y]` | Menyimpan posisi partikel dalam bentuk list koordinat `[x, y]`. |
| 8 | `        self.vel = [vx if vx is not None else random.uniform(-1, 1), vy if vy is not None else random.uniform(-1.5, -0.5)]` | Menetapkan kecepatan partikel. Jika tidak diberikan, kecepatan horizontal berkisar acak antara -1 dan 1, dan kecepatan vertikal berkisar antara -1.5 dan -0.5 (bergerak ke atas). |
| 9 | `        self.color = color` | Menyimpan warna partikel (format RGB). |
| 10 | `        self.size = size if size is not None else random.randint(3, 6)` | Menetapkan ukuran partikel. Defaultnya adalah bilangan bulat acak antara 3 dan 6 piksel. |
| 11 | `        self.life = 1.0` | Menetapkan sisa masa hidup partikel awal sebesar 100% (skala 0.0 hingga 1.0). |
| 12 | `        self.decay = random.uniform(0.02, 0.04)` | Menetapkan tingkat pengurangan (decay) masa hidup per frame secara acak antara 0.02 dan 0.04. |
| 13 | | Baris kosong sebagai pemisah. |
| 14 | `    def update(self):` | Metode untuk memperbarui posisi dan sisa hidup partikel di setiap frame. |
| 15 | `        self.pos[0] += self.vel[0]` | Memperbarui posisi X berdasarkan kecepatan horizontal. |
| 16 | `        self.pos[1] += self.vel[1]` | Memperbarui posisi Y berdasarkan kecepatan vertikal. |
| 17 | `        self.life -= self.decay` | Mengurangi masa hidup partikel berdasarkan nilai decay. |
| 18 | `        return self.life > 0` | Mengembalikan nilai `True` jika partikel masih hidup (`life > 0`), atau `False` jika partikel harus dihapus. |
| 19 | | Baris kosong sebagai pemisah. |
| 20 | `    def draw(self, screen, camera):` | Metode untuk menggambar partikel ke layar game. |
| 21 | `        draw_pos = camera.apply(self.pos)` | Menyesuaikan posisi partikel berdasarkan posisi kamera game agar bergeser saat layar bergerak. |
| 22 | `        pygame.draw.circle(screen, self.color, (int(draw_pos[0]), int(draw_pos[1])), int(self.size * self.life))` | Menggambar lingkaran kecil di layar dengan warna tertentu dan ukuran yang mengecil seiring berjalannya waktu (`size * life`). |
| 23 | | Baris kosong sebagai pemisah. |

---

### 2. Konstanta Dialog (Baris 24 - 46)
Bagian ini menyimpan teks percakapan narasi pembuka game dan dialog interaktif para NPC.

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| 24 | `# Dialogue constants embedded for simplicity` | Komentar yang menjelaskan bahwa konstanta dialog diletakkan di sini untuk kesederhanaan struktur kode. |
| 25 | `PROLOGUE_M3 = [` | Mendefinisikan list `PROLOGUE_M3` yang berisi teks prolog saat pemain pertama kali keluar dari area Metro. |
| 26 | `    "Cahaya matahari menyilaukan mataku...",` | Teks prolog indeks ke-0. |
| 27 | `    "Setelah berhari-hari di dalam kegelapan Metro, akhirnya aku keluar.",` | Teks prolog indeks ke-1. |
| 28 | `    "Tunggu... suara apa itu?",` | Teks prolog indeks ke-2. |
| 29 | `    "Suara tawa? Suara orang berbicara?",` | Teks prolog indeks ke-3. |
| 30 | `    "Selamat datang di 'The Sanctuary'. Benteng terakhir kemanusiaan."` | Teks prolog indeks ke-4. |
| 31 | `]` | Menutup list `PROLOGUE_M3`. |
| 32 | | Baris kosong sebagai pemisah. |
| 33 | `NPC_DIALOGUES = {` | Mendefinisikan kamus (dictionary) `NPC_DIALOGUES` yang mengelompokkan pesan dialog acak berdasarkan peran NPC. |
| 34 | `    "Guard": [` | Membuka daftar dialog untuk NPC penjaga (Guard). |
| 35 | `        "Jaga langkahmu, kawan. Kami tidak ingin ada masalah di sini.",` | Pilihan dialog penjaga ke-1. |
| 36 | `        "Senang melihat wajah baru yang bukan zombie."` | Pilihan dialog penjaga ke-2. |
| 37 | `    ],` | Menutup daftar dialog penjaga. |
| 38 | `    "Citizen": [` | Membuka daftar dialog untuk NPC warga sipil (Citizen). |
| 39 | `        "Katanya ada kota lain di Utara, tapi siapa yang tahu?",` | Pilihan dialog warga ke-1. |
| 40 | `        "Anak-anak akhirnya bisa bermain tanpa rasa takut... setidaknya untuk sekarang."` | Pilihan dialog warga ke-2. |
| 41 | `    ],` | Menutup daftar dialog warga. |
| 42 | `    "Elder": [` | Membuka daftar dialog untuk NPC tetua (Elder). |
| 43 | `        "Selamat datang, pengembara. Kami sudah mendengar kabarmu lewat radio.",` | Pilihan dialog tetua ke-1. |
| 44 | `        "Dunia luar sudah hancur, tapi di sini... kita mencoba membangun kembali."` | Pilihan dialog tetua ke-2. |
| 45 | `    ]` | Menutup daftar dialog tetua. |
| 46 | `}` | Menutup dictionary `NPC_DIALOGUES`. |
| 47 | | Baris kosong sebagai pemisah. |

---

### 3. Inisialisasi Kelas `SanctuaryLogic` (Baris 48 - 99)
Bagian ini mengatur konstruktor kelas logika dan memicu pemuatan NPC di titik-titik koordinat tertentu di peta.

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| 48 | `class SanctuaryLogic:` | Mendefinisikan kelas utama `SanctuaryLogic` yang mengontrol semua mekanisme interaksi di area Sanctuary. |
| 49 | `    def __init__(self, dialogue):` | Inisialisasi objek logika Sanctuary dengan menyertakan sistem dialog (`dialogue`). |
| 50 | `        self.dialogue = dialogue` | Menyimpan referensi ke objek dialog untuk menampilkan teks dialog di layar. |
| 51 | `        self.alarm_active = False` | Menetapkan status alarm tanda bahaya awal bernilai `False` (belum aktif). |
| 52 | `        self.elder_met = False` | Menetapkan status apakah pemain sudah bertemu Penatua Aris awal bernilai `False`. |
| 53 | `        self.npcs = []` | Inisialisasi list kosong untuk menampung objek NPC. |
| 54 | `        self._setup_npcs()` | Memanggil metode internal `_setup_npcs` untuk membuat dan memposisikan NPC di map. |
| 55 | `        self.font = pygame.font.SysFont("monospace", 14, bold=True)` | Menginisialisasi objek font monospaced berukuran 14 tebal untuk teks interaksi dan nama tag. |
| 56 | | Baris kosong sebagai pemisah. |
| 57 | `        # Load map background` | Komentar penanda bagian memuat gambar latar belakang map. |
| 58 | `        try:` | Membuka blok `try` untuk penanganan kesalahan saat memuat file eksternal gambar map. |
| 59 | `            self.map_img = pygame.image.load("assets/images/sanctuary_map.png").convert()` | Memuat gambar map dari aset lokal dan mengonversinya untuk performa rendering yang lebih cepat. |
| 60 | `            self.map_img = pygame.transform.scale(self.map_img, (2560, 1440))` | Mengubah ukuran gambar map agar sesuai dengan dimensi peta Sanctuary (2560x1440 piksel). |
| 61 | `        except Exception as e:` | Menangkap kesalahan jika file gambar tidak ditemukan atau rusak. |
| 62 | `            print(f"Error loading sanctuary map image: {e}")` | Menampilkan pesan kesalahan di konsol jika terjadi kegagalan pemuatan gambar. |
| 63 | `            self.map_img = None` | Menetapkan `self.map_img` ke `None` sebagai fallback jika gagal memuat gambar. |
| 64 | | Baris kosong sebagai pemisah. |
| 65 | `        self.particles = []` | Inisialisasi list kosong untuk menampung partikel aktif. |
| 66 | `        self.floating_texts = []` | Inisialisasi list kosong untuk teks melayang (misalnya "+HEAL", "BURNING!"). |
| 67 | `        self.crate = None` | Inisialisasi status kotak suplai udara (supply drop) bernilai `None` (belum dipanggil). |
| 68 | `        self.crate_cooldown = 0` | Menetapkan cooldown awal pemanggilan supply drop ke 0. |
| 69 | | Baris kosong sebagai pemisah. |
| 70 | `    def _setup_npcs(self):` | Metode internal untuk mengimpor kelas NPC dan menyusun daftar karakter NPC beserta aset grafisnya. |
| 71 | `        from src.entities.npc import NPC` | Mengimpor kelas `NPC` dari modul entitas secara lokal untuk menghindari circular import. |
| 72 | | Baris kosong sebagai pemisah. |
| 73 | `        # Position NPCs inside the rooftop base layout (2560, 1440)` | Komentar mengenai koordinat posisi NPC di dalam batas peta. |
| 74 | `        self.npcs = [` | Mulai membuat list objek NPC. |
| 75 | `            NPC(` | Instansiasi NPC pertama. |
| 76 | `                name="Penatua Aris", ` | Nama NPC adalah Penatua Aris. |
| 77 | `                x=1280, y=600, ` | Menaruh posisi Penatua Aris di tengah-tengah peta. |
| 78 | `                role="Elder",` | Perannya adalah Elder (Tetua). |
| 79 | `                base_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v09.png",` | Path gambar dasar karakter. |
| 80 | `                outfit_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v05.png",` | Path gambar pakaian karakter. |
| 81 | `                hair_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_bob1_v02.png"` | Path gambar gaya rambut karakter. |
| 82 | `            ),` | Penutup objek NPC pertama. |
| 83 | `            NPC(` | Instansiasi NPC kedua. |
| 84 | `                name="Kapten Jaka", ` | Nama NPC adalah Kapten Jaka. |
| 85 | `                x=1800, y=650, ` | Menaruh posisinya di sebelah timur gerbang jalan. |
| 86 | `                role="Guard",` | Perannya adalah Guard (Penjaga). |
| 87 | `                base_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v00.png",` | Path gambar dasar karakter. |
| 88 | `                outfit_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v01.png",` | Path gambar pakaian. |
| 89 | `                hair_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_dap1_v08.png"` | Path gambar rambut. |
| 90 | `            ),` | Penutup objek NPC kedua. |
| 91 | `            NPC(` | Instansiasi NPC ketiga. |
| 92 | `                name="Warga Sipil", ` | Nama NPC adalah Warga Sipil. |
| 93 | `                x=400, y=1100, ` | Menaruh posisinya di bagian barat dekat area medis. |
| 94 | `                role="Citizen",` | Perannya adalah Citizen (Warga Sipil). |
| 95 | `                base_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v02.png",` | Path gambar dasar karakter. |
| 96 | `                outfit_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_pfpn_v02.png",` | Path gambar pakaian warga. |
| 97 | `                hair_path="FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_bob1_v10.png"` | Path gambar rambut warga. |
| 98 | `            )` | Penutup objek NPC ketiga. |
| 99 | `        ]` | Menutup list `self.npcs`. |

---

### 4. Metode `update` - Bagian Logika Lingkungan (Baris 101 - 161)
Bagian ini mengatur logika interaksi pemain terhadap objek lingkungan sekitar seperti api unggun, kasur medis, dan kolam air.

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| 101 | `    def update(self, player, interact_pressed):` | Metode `update` utama yang berjalan setiap frame untuk memproses semua interaksi pemain dengan dunia Sanctuary. |
| 102 | `        # Update NPC movements and animations` | Komentar penanda pembaruan keadaan NPC. |
| 103 | `        for npc in self.npcs:` | Melakukan iterasi pada setiap NPC di dalam list `npcs`. |
| 104 | `            npc.update(map_size=(2560, 1440))` | Memperbarui pergerakan dan animasi NPC agar tetap berada di dalam batas peta (2560, 1440). |
| 105 | | Baris kosong sebagai pemisah. |
| 106 | `        # Update particles & floating texts` | Komentar penanda pembaruan partikel dan teks melayang. |
| 107 | `        self.particles = [p for p in self.particles if p.update()]` | Memperbarui setiap partikel dan menyaring partikel yang sisa hidupnya (`life`) sudah habis (`False`). |
| 108 | `        for ft in self.floating_texts:` | Melakukan iterasi pada setiap teks melayang yang aktif. |
| 109 | `            ft['pos'][1] -= 0.6` | Menggeser posisi vertikal teks melayang ke atas sebesar 0.6 piksel per frame (efek mengapung). |
| 110 | `            ft['timer'] -= 1` | Mengurangi timer durasi tampilnya teks melayang sebesar 1 frame. |
| 111 | `        self.floating_texts = [ft for ft in self.floating_texts if ft['timer'] > 0]` | Menyaring dan menyisakan teks melayang yang durasi timernya masih di atas 0. |
| 112 | | Baris kosong sebagai pemisah. |
| 113 | `        # Decrement cooldown` | Komentar pengurangan cooldown. |
| 114 | `        if self.crate_cooldown > 0:` | Mengecek apakah cooldown kotak suplai masih aktif (> 0). |
| 115 | `            self.crate_cooldown -= 1` | Mengurangi nilai cooldown kotak suplai sebanyak 1 frame. |
| 116 | | Baris kosong sebagai pemisah. |
| 117 | `        px, py = player.pos[0], player.pos[1]` | Menyalin posisi X dan Y pemain ke variabel lokal `px` dan `py` agar kode lebih pendek. |
| 118 | | Baris kosong sebagai pemisah. |
| 119 | `        # Default speed multiplier` | Komentar penetapan pengali kecepatan normal di area Sanctuary. |
| 120 | `        player.speed_multiplier = 0.40` | Membatasi kecepatan gerak pemain di Sanctuary menjadi 40% dari kecepatan aslinya (membuat pergerakan terkesan santai). |
| 121 | | Baris kosong sebagai pemisah. |
| 122 | `        # --- 1. CAMPFIRE INTERACTION (Warming vs Burning) ---` | Komentar interaksi dengan api unggun (hangat vs terbakar). |
| 123 | `        campfire_dist = math.hypot(px - 1220, py - 560)` | Menghitung jarak lurus (jarak Euclidean) antara pemain dan pusat api unggun di koordinat (1220, 560). |
| 124 | `        if campfire_dist < 120:` | Mengecek jika pemain berada dalam jangkauan pengaruh api unggun (< 120 piksel). |
| 125 | `            if campfire_dist < 30:` | Jika pemain berdiri tepat di atas api unggun (< 30 piksel). |
| 126 | `                # Walked directly into the fire! Take damage` | Komentar: pemain terbakar karena masuk ke api unggun langsung. |
| 127 | `                player.health = max(0.0, player.health - 0.7)` | Mengurangi kesehatan (`health`) pemain sebesar 0.7 per frame, dibatasi paling rendah 0.0. |
| 128 | `                player.injured = True` | Mengeset status terluka pemain menjadi `True`. |
| 129 | `                if random.random() < 0.15:` | Peluang 15% setiap frame untuk menampilkan teks melayang peringatan terbakar. |
| 130 | `                    self.floating_texts.append({'text': "BURNING! -HP", 'pos': [px + random.randint(-15, 15), py - 20], 'timer': 20, 'color': (255, 50, 50)})` | Menambahkan teks melayang berwarna merah bertuliskan "BURNING! -HP" di dekat pemain. |
| 131 | `                # Spawn fire particles on player` | Komentar: memunculkan partikel api pada tubuh pemain. |
| 132 | `                if random.random() < 0.4:` | Peluang 40% setiap frame untuk memunculkan partikel api. |
| 133 | `                    self.particles.append(SanctuaryParticle(px + random.uniform(-10, 10), py + 10, (255, random.randint(50, 150), 0)))` | Menambahkan partikel berwarna oranye/merah menyala di sekitar posisi pemain. |
| 134 | `            else:` | Jika pemain berada di jarak hangat (antara 30 hingga 120 piksel dari api unggun). |
| 135 | `                # Warmed next to the fire! Stamina boost` | Komentar: efek menghangatkan diri untuk meningkatkan stamina/kecepatan. |
| 136 | `                if player.adrenaline_timer <= 0:` | Jika efek boost adrenalin pemain belum aktif. |
| 137 | `                    self.floating_texts.append({'text': "WARMED BY CAMPFIRE (Speed Boost!)", 'pos': [px, py - 30], 'timer': 45, 'color': (255, 150, 0)})` | Menambahkan teks melayang berwarna oranye bertuliskan pesan peningkatan kecepatan. |
| 138 | `                player.adrenaline_timer = 120` | Memberikan durasi status adrenalin (boost kecepatan) selama 120 frame. |
| 139 | `                # Spawn gentle orange sparks` | Komentar: memunculkan percikan bunga api lembut. |
| 140 | `                if random.random() < 0.1:` | Peluang 10% setiap frame untuk memunculkan partikel percikan api. |
| 141 | `                    self.particles.append(SanctuaryParticle(px + random.uniform(-10, 10), py + 10, (255, 180, 50), vy=random.uniform(-1.0, -0.3)))` | Menambahkan partikel percikan api ringan berwarna kuning/oranye yang terbang ke atas. |
| 142 | | Baris kosong sebagai pemisah. |
| 143 | `        # --- 2. MEDICAL AREA INTERACTION (Healing Beds) ---` | Komentar interaksi dengan area medis (kasur perawatan). |
| 144 | `        if 100 < px < 550 and 900 < py < 1350:` | Memeriksa apakah pemain berada di dalam wilayah persegi area medis (X antara 100-550, Y antara 900-1350). |
| 145 | `            if player.health < 100:` | Jika kesehatan pemain di bawah batas maksimum (100). |
| 146 | `                player.health = min(100.0, player.health + 0.3)` | Memulihkan kesehatan pemain sebesar 0.3 per frame, dibatasi maksimum 100.0. |
| 147 | `                player.injured = False` | Menghilangkan status cedera (`injured = False`) setelah dirawat. |
| 148 | `                if random.random() < 0.08:` | Peluang 8% untuk memunculkan indikator teks melayang pemulihan. |
| 149 | `                    self.floating_texts.append({'text': "+HEAL", 'pos': [px + random.randint(-15, 15), py - 20], 'timer': 25, 'color': (100, 255, 100)})` | Menambahkan teks melayang berwarna hijau "+HEAL". |
| 150 | `            # Spawn green healing particles` | Komentar: memunculkan partikel penyembuhan hijau. |
| 151 | `            if random.random() < 0.15:` | Peluang 15% setiap frame untuk memunculkan partikel penyembuhan. |
| 152 | `                self.particles.append(SanctuaryParticle(px + random.uniform(-15, 15), py + 15, (50, 255, 50), size=random.randint(3, 5)))` | Menambahkan partikel kecil berwarna hijau di posisi pemain. |
| 153 | | Baris kosong sebagai pemisah. |
| 154 | `        # --- 3. POND INTERACTION (Deep Water slowdown & splash) ---` | Komentar interaksi dengan kolam air (memperlambat gerakan & cipratan air). |
| 155 | `        if 1950 < px < 2400 and 900 < py < 1300:` | Memeriksa apakah pemain berada di dalam area kolam air (X antara 1950-2400, Y antara 900-1300). |
| 156 | `            player.speed_multiplier = 0.20 # Slowed down by water` | Memperlambat pergerakan pemain menjadi hanya 20% karena berjalan di air dalam. |
| 157 | `            # Spawn water splashes if player is moving` | Komentar: memunculkan cipratan air saat pemain bergerak di air. |
| 158 | `            is_moving = player.state in ['walk', 'run']` | Mengecek apakah status pergerakan pemain adalah sedang berjalan (`walk`) atau berlari (`run`). |
| 159 | `            if is_moving and random.random() < 0.35:` | Jika pemain sedang bergerak, peluang 35% untuk memunculkan percikan air. |
| 160 | `                self.particles.append(SanctuaryParticle(px + random.uniform(-15, 15), py + 15, (100, 180, 255), vx=random.uniform(-1.2, 1.2), vy=random.uniform(-0.4, 0.4)))` | Menambahkan partikel berwarna biru muda dengan kecepatan sebaran menyamping yang merepresentasikan cipratan air. |
| 161 | | Baris kosong sebagai pemisah. |

---

### 5. Metode `update` - Bagian Helipad & Fisika Crate Suplai (Baris 162 - 188)
Bagian ini menangani pemanggilan peti suplai udara, penanganan penurunan ketinggian peti, efek debu saat mendarat, serta pembukaan peti.

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| 162 | `        # --- 4. HELIPAD SUPPLY DROP INTERACTION ---` | Komentar interaksi helipad dan kiriman suplai. |
| 163 | `        helipad_dist = math.hypot(px - 430, py - 410)` | Menghitung jarak pemain ke pusat helipad di koordinat (430, 410). |
| 164 | `        signal_to_return = None` | Inisialisasi variabel kembalian sinyal dengan `None`. |
| 165 | `        if helipad_dist < 60:` | Jika pemain berdiri sangat dekat dengan pusat helipad (< 60 piksel). |
| 166 | `            if interact_pressed:` | Jika pemain menekan tombol interaksi (Enter). |
| 167 | `                if not self.crate and self.crate_cooldown <= 0:` | Jika saat ini belum ada peti suplai yang dijatuhkan dan cooldown sudah habis. |
| 168 | `                    # Spawn falling crate` | Komentar: memunculkan peti yang sedang jatuh. |
| 169 | `                    self.crate = {'pos': [430, 410], 'z_height': 500, 'landed': False, 'opened': False}` | Membuat kamus properti peti yang ditempatkan di (430, 410) pada ketinggian awal 500 piksel di udara, belum mendarat (`landed=False`), dan belum dibuka (`opened=False`). |
| 170 | `                    self.floating_texts.append({'text': "SUPPLY DROP CALLED!", 'pos': [px, py - 30], 'timer': 60, 'color': (0, 255, 255)})` | Menambahkan teks melayang cyan "SUPPLY DROP CALLED!" sebagai konfirmasi panggilan. |
| 171 | `                elif self.crate and self.crate['landed'] and not self.crate['opened']:` | Jika peti sudah ada, sudah mendarat, tetapi belum dibuka oleh pemain. |
| 172 | `                    # Open crate and award Bronze` | Komentar: membuka peti dan memberikan hadiah mata uang Bronze. |
| 173 | `                    self.crate['opened'] = True` | Mengubah status peti menjadi telah dibuka (`opened = True`). |
| 174 | `                    self.floating_texts.append({'text': "+$150 BRONZE CURRENCY", 'pos': [px, py - 30], 'timer': 60, 'color': (255, 215, 0)})` | Menambahkan teks melayang berwarna emas "+$150 BRONZE CURRENCY". |
| 175 | `                    self.crate_cooldown = 1800 # 30 seconds cooldown` | Menetapkan durasi cooldown peti selama 1800 frame (~30 detik pada game 60 FPS). |
| 176 | `                    signal_to_return = "AWARD_150_BRONZE"` | Mengatur sinyal pengembalian agar game engine memberikan uang $150 Bronze kepada pemain. |
| 177 | | Baris kosong sebagai pemisah. |
| 178 | `        # Update Supply Crate physics` | Komentar pembaruan fisika jatuhnya peti suplai. |
| 179 | `        if self.crate:` | Jika objek peti suplai ada (aktif). |
| 180 | `            if not self.crate['landed']:` | Jika peti belum menyentuh tanah. |
| 181 | `                self.crate['z_height'] -= 10` | Mengurangi ketinggian `z_height` sebesar 10 piksel per frame (peti turun secara vertikal). |
| 182 | `                if self.crate['z_height'] <= 0:` | Jika ketinggian peti sudah mencapai 0 atau kurang (menyentuh tanah). |
| 183 | `                    self.crate['z_height'] = 0` | Mengunci ketinggian di angka 0. |
| 184 | `                    self.crate['landed'] = True` | Mengubah status peti menjadi telah mendarat (`landed = True`). |
| 185 | `                    # Spawn dust landing particles` | Komentar: memunculkan partikel debu saat mendarat. |
| 186 | `                    for _ in range(20):` | Melakukan perulangan 20 kali untuk menghasilkan 20 partikel debu seketika. |
| 187 | `                        self.particles.append(SanctuaryParticle(430, 410, (160, 160, 160), vx=random.uniform(-2.5, 2.5), vy=random.uniform(-1.5, 1.5)))` | Menambahkan partikel abu-abu yang terlempar ke segala arah dari lokasi pendaratan peti. |
| 188 | | Baris kosong sebagai pemisah. |

---

### 6. Metode `update` - Bagian Dialog NPC & Loker (Baris 189 - 217)
Bagian ini mendeteksi interaksi tombol enter dengan NPC di dekat pemain, serta pengaktifan gerbang pertahanan menembak dan pintu loker pakaian.

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| 189 | `        # Interaksi sederhana dengan NPC` | Komentar bagian interaksi dengan karakter non-pemain (NPC). |
| 190 | `        if interact_pressed:` | Memeriksa apakah tombol interaksi ditekan pada frame ini. |
| 191 | `            for npc in self.npcs:` | Melakukan iterasi ke setiap NPC yang ada. |
| 192 | `                dist = math.hypot(player.pos[0] - npc.pos[0], player.pos[1] - npc.pos[1])` | Menghitung jarak antara posisi pemain dan posisi NPC. |
| 193 | `                if dist < 100: # Jangkauan interaksi diperluas ke 100px` | Jika jarak pemain dengan NPC berada di dalam radius interaksi (< 100 piksel). |
| 194 | `                    if npc.name == "Penatua Aris":` | Jika NPC yang diajak bicara adalah "Penatua Aris". |
| 195 | `                        self.elder_met = True` | Menandai bahwa pemain sudah bertemu Penatua Aris (`elder_met = True`). |
| 196 | `                        self.dialogue.show(["PENATUA ARIS: Selamat datang. Kota ini dalam bahaya.", "Bicara pada Kapten Jaka di gerbang jalan itu!"])` | Memanggil antarmuka dialog untuk menampilkan pesan selamat datang dan petunjuk lanjut. |
| 197 | `                    elif npc.name == "Kapten Jaka":` | Jika NPC yang diajak bicara adalah "Kapten Jaka". |
| 198 | `                        if self.elder_met:` | Memeriksa apakah pemain sudah memenuhi syarat bertemu Penatua Aris terlebih dahulu. |
| 199 | `                            self.alarm_active = True` | Mengaktifkan status alarm bahaya (`alarm_active = True`). |
| 200 | `                            player.pos = [2500, 300]` | Memindahkan/teleportasi posisi pemain ke dekat menara pertahanan di koordinat (2500, 300). |
| 201 | `                            self.dialogue.show(["KAPTEN JAKA: Zombie datang! Cepat ke menara!", "KITA HARUS BERTAHAN!"])` | Menampilkan dialog darurat Kapten Jaka yang menyuruh bersiap perang. |
| 202 | `                            return "START_SHOOTING"` | Mengembalikan sinyal `"START_SHOOTING"` ke game loop utama untuk memulai fase pertempuran/menembak. |
| 203 | `                        else:` | Jika pemain belum berbicara dengan Penatua Aris sebelumnya. |
| 204 | `                            self.dialogue.show(["KAPTEN JAKA: Cari Penatua Aris dulu! Dia di sebelah barat."])` | Menampilkan dialog Kapten Jaka yang menolak bicara sebelum pemain menemui Penatua. |
| 205 | `                    else:` | Jika NPC yang diajak bicara adalah NPC lain (misalnya Warga Sipil). |
| 206 | `                        role = npc.role` | Mengambil peran NPC tersebut. |
| 207 | `                        msg = random.choice(NPC_DIALOGUES.get(role, ["Halo!"]))` | Mengambil pesan dialog acak dari dictionary `NPC_DIALOGUES` sesuai peran NPC, atau default "Halo!". |
| 208 | `                        self.dialogue.show([f"{npc.name}: {msg}"])` | Menampilkan nama NPC beserta pesan dialog acak tersebut. |
| 209 | `                    return None` | Menghentikan fungsi dan mengembalikan `None` (mencegah interaksi ganda dengan NPC lain dalam frame yang sama). |
| 210 | | Baris kosong sebagai pemisah. |
| 211 | `        # --- 5. WARDROBE LOCKER INTERACTION ---` | Komentar interaksi loker pakaian. |
| 212 | `        w_dist = math.hypot(px - 145, py - 875)` | Menghitung jarak pemain ke loker pakaian yang berada di koordinat (145, 875). |
| 213 | `        if w_dist < 60:` | Jika pemain berada sangat dekat dengan loker pakaian (< 60 piksel). |
| 214 | `            if interact_pressed:` | Jika tombol interaksi ditekan. |
| 215 | `                signal_to_return = "OPEN_WARDROBE"` | Mengatur sinyal pengembalian menjadi `"OPEN_WARDROBE"` untuk membuka menu penggantian pakaian pemain. |
| 216 | | Baris kosong sebagai pemisah. |
| 217 | `        return signal_to_return` | Mengembalikan sinyal interaksi (seperti `"OPEN_WARDROBE"`, `"AWARD_150_BRONZE"`, atau `None`) untuk direspons oleh sistem game utama. |
| 218 | | Baris kosong sebagai pemisah. |

---

### 7. Metode Gambar Dasar & Entitas Peta (Baris 219 - 296)
Bagian ini mengatur visualisasi peta latar belakang dan rendering entitas secara berlapis agar mengikuti arah kamera.

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| 219 | `    def draw_ground(self, screen, camera):` | Metode untuk menggambar elemen latar belakang peta Sanctuary. |
| 220 | `        if self.map_img:` | Memeriksa apakah gambar peta berhasil dimuat. |
| 221 | `            # Draw the background map using camera offset` | Komentar: menggambar peta latar menggunakan koordinat kamera. |
| 222 | `            screen.blit(self.map_img, (camera.camera.x, camera.camera.y))` | Menggambar (blit) gambar peta berukuran besar ke layar sesuai dengan koordinat kamera agar mengikuti pergerakan pemain. |
| 223 | `        else:` | Jika gambar peta gagal dimuat. |
| 224 | `            # Draw fallback background or simple grid` | Komentar: menggambar latar belakang alternatif. |
| 225 | `            screen.fill((30, 100, 30))` | Mewarnai seluruh layar dengan warna hijau rumput `(30, 100, 30)` sebagai pengganti gambar peta yang hilang. |
| 226 | `            # Simple road (Sesuai dengan posisi Kapten Jaka)` | Komentar: menggambar jalan sederhana. |
| 227 | `            pygame.draw.rect(screen, (100, 80, 50), camera.apply(pygame.Rect(950, 0, 300, 4000)))` | Menggambar persegi panjang jalan berwarna cokelat tanah yang disesuaikan posisinya dengan pergerakan kamera. |
| 228 | | Baris kosong sebagai pemisah. |
| 229 | `    def draw_entities(self, screen, camera, player=None):` | Metode untuk menggambar entitas di atas tanah, seperti partikel, peti suplai, petunjuk interaksi, NPC, dan teks melayang. |
| 230 | `        # Draw particles` | Komentar menggambar partikel. |
| 231 | `        for p in self.particles:` | Melakukan iterasi ke seluruh partikel aktif. |
| 232 | `            p.draw(screen, camera)` | Menggambar partikel tersebut ke layar melalui metode bawaan partikel. |
| 233 | | Baris kosong sebagai pemisah. |
| 234 | `        # Draw Supply Crate` | Komentar menggambar peti suplai. |
| 235 | `        if self.crate and not self.crate['opened']:` | Jika peti suplai ada dan belum dibuka oleh pemain. |
| 236 | `            cx, cy = self.crate['pos']` | Mendapatkan koordinat X dan Y peti suplai di peta. |
| 237 | `            screen_pos = camera.apply((cx, cy))` | Mengonversi koordinat peta peti suplai menjadi koordinat layar menggunakan objek kamera. |
| 238 | | Baris kosong sebagai pemisah. |
| 239 | `            if not self.crate['landed']:` | Jika peti sedang melayang jatuh (belum mendarat). |
| 240 | `                # Draw shadow on ground` | Komentar menggambar bayangan di tanah. |
| 241 | `                shadow_r = int(15 * (1.0 - self.crate['z_height'] / 500.0))` | Menghitung radius bayangan secara dinamis. Semakin dekat peti dengan tanah (`z_height` mendekati 0), bayangannya akan semakin besar (radius maksimal 15). |
| 242 | `                shadow_surf = pygame.Surface((shadow_r * 2, shadow_r), pygame.SRCALPHA)` | Membuat bidang permukaan transparan (`SRCALPHA`) untuk menggambar bayangan elips. |
| 243 | `                pygame.draw.ellipse(shadow_surf, (0, 0, 0, 100), (0, 0, shadow_r * 2, shadow_r))` | Menggambar bentuk elips hitam transparan (alpha = 100) sebagai bayangan peti di tanah. |
| 244 | `                screen.blit(shadow_surf, (screen_pos[0] - shadow_r, screen_pos[1] - shadow_r // 2))` | Menempelkan permukaan bayangan tepat di bawah posisi jatuh peti. |
| 245 | `                # Draw falling crate` | Komentar menggambar peti yang melayang jatuh. |
| 246 | `                crate_y = screen_pos[1] - self.crate['z_height']` | Menghitung posisi Y rendering peti di layar dengan mengurangi koordinat tanah dengan tinggi jatuh `z_height`. |
| 247 | `                pygame.draw.rect(screen, (120, 60, 10), (screen_pos[0] - 16, crate_y - 16, 32, 32), border_radius=4)` | Menggambar badan luar peti berukuran 32x32 berwarna cokelat tua dengan sudut membulat. |
| 248 | `                pygame.draw.rect(screen, (180, 130, 40), (screen_pos[0] - 12, crate_y - 12, 24, 24), border_radius=2)` | Menggambar badan dalam peti berukuran 24x24 berwarna cokelat terang sebagai variasi tekstur peti. |
| 249 | `                # Parachute strings & dome` | Komentar menggambar tali dan parasut peti. |
| 250 | `                pygame.draw.line(screen, (220, 220, 220), (screen_pos[0] - 16, crate_y - 16), (screen_pos[0] - 25, crate_y - 45), 2)` | Menggambar tali parasut sebelah kiri yang menghubungkan peti dengan kubah parasut. |
| 251 | `                pygame.draw.line(screen, (220, 220, 220), (screen_pos[0] + 16, crate_y - 16), (screen_pos[0] + 25, crate_y - 45), 2)` | Menggambar tali parasut sebelah kanan. |
| 252 | `                pygame.draw.arc(screen, (240, 240, 240), (screen_pos[0] - 30, crate_y - 65, 60, 40), 0, math.pi, 3)` | Menggambar lengkungan berbentuk kubah parasut berwarna putih abu-abu di atas peti. |
| 253 | `            else:` | Jika peti sudah mendarat di tanah. |
| 254 | `                # Crate landed on ground` | Komentar peti mendarat di tanah. |
| 255 | `                pygame.draw.rect(screen, (120, 60, 10), (screen_pos[0] - 16, screen_pos[1] - 16, 32, 32), border_radius=4)` | Menggambar badan luar peti di tanah pada koordinat dasarnya. |
| 256 | `                pygame.draw.rect(screen, (180, 130, 40), (screen_pos[0] - 12, screen_pos[1] - 12, 24, 24), border_radius=2)` | Menggambar badan dalam peti di tanah. |
| 257 | | Baris kosong sebagai pemisah. |
| 258 | `                # Draw interact hint` | Komentar menggambar petunjuk tombol interaksi. |
| 259 | `                if player:` | Memeriksa apakah objek pemain ada. |
| 260 | `                    p_dist = math.hypot(player.pos[0] - cx, player.pos[1] - cy)` | Menghitung jarak pemain ke peti yang mendarat. |
| 261 | `                    if p_dist < 60:` | Jika pemain berada dekat dengan peti (< 60 piksel). |
| 262 | `                        hint = self.font.render("PRESS ENTER TO CLAIM SUPPLY", True, (0, 255, 255))` | Membuat permukaan teks petunjuk "PRESS ENTER TO CLAIM SUPPLY" berwarna cyan. |
| 263 | `                        screen.blit(hint, (screen_pos[0] - hint.get_width() // 2, screen_pos[1] - 35))` | Menampilkan teks petunjuk tersebut tepat di atas peti (jarak 35 piksel ke atas). |
| 264 | | Baris kosong sebagai pemisah. |
| 265 | `        # Draw Helipad prompt if player is close` | Komentar menggambar petunjuk helipad. |
| 266 | `        if player and not self.crate and self.crate_cooldown <= 0:` | Jika pemain ada, belum ada peti aktif, dan cooldown bernilai 0 atau kurang. |
| 267 | `            h_dist = math.hypot(player.pos[0] - 430, player.pos[1] - 410)` | Menghitung jarak pemain ke helipad. |
| 268 | `            if h_dist < 60:` | Jika pemain berdiri di dekat helipad (< 60 piksel). |
| 269 | `                h_pos = camera.apply((430, 410))` | Mengonversi koordinat helipad ke posisi layar game. |
| 270 | `                hint = self.font.render("PRESS ENTER TO CALL SUPPLY DROP", True, (0, 255, 255))` | Membuat teks instruksi "PRESS ENTER TO CALL SUPPLY DROP" berwarna cyan. |
| 271 | `                screen.blit(hint, (h_pos[0] - hint.get_width() // 2, h_pos[1] - 25))` | Menggambar teks petunjuk tepat di atas helipad. |
| 272 | | Baris kosong sebagai pemisah. |
| 273 | `        # Draw Wardrobe Locker prompt if player is close` | Komentar menggambar petunjuk loker pakaian. |
| 274 | `        if player:` | Memeriksa keberadaan pemain. |
| 275 | `            w_dist = math.hypot(player.pos[0] - 145, player.pos[1] - 875)` | Menghitung jarak pemain ke loker pakaian (145, 875). |
| 276 | `            if w_dist < 60:` | Jika pemain berdiri di dekat loker pakaian (< 60 piksel). |
| 277 | `                w_pos = camera.apply((145, 875))` | Mengonversi koordinat loker ke posisi layar. |
| 278 | `                hint = self.font.render("PRESS ENTER TO USE WARDROBE", True, (0, 255, 255))` | Membuat teks instruksi "PRESS ENTER TO USE WARDROBE" berwarna cyan. |
| 279 | `                screen.blit(hint, (w_pos[0] - hint.get_width() // 2, w_pos[1] - 25))` | Menggambar teks petunjuk tepat di atas loker pakaian. |
| 280 | | Baris kosong sebagai pemisah. |
| 281 | `        # Draw NPCs` | Komentar bagian menggambar NPC. |
| 282 | `        for npc in self.npcs:` | Melakukan iterasi pada semua NPC yang terdaftar. |
| 283 | `            npc.draw(screen, camera)` | Memanggil metode bawaan NPC untuk menggambar dirinya berdasarkan posisinya terhadap kamera. |
| 284 | | Baris kosong sebagai pemisah. |
| 285 | `            # Draw name tag above their head` | Komentar menggambar label nama di atas kepala NPC. |
| 286 | `            d_pos = camera.apply(npc.pos)` | Mengonversi koordinat NPC ke posisi layar. |
| 287 | `            name_tag = self.font.render(npc.name, True, (255, 255, 255))` | Membuat teks nama NPC berwarna putih. |
| 288 | `            screen.blit(name_tag, (d_pos[0] + 16 - name_tag.get_width() // 2, d_pos[1] - 15))` | Menempelkan label nama di atas kepala karakter NPC (posisi disesuaikan dengan lebar teks dan offset). |
| 289 | | Baris kosong sebagai pemisah. |
| 290 | `        # Draw floating texts` | Komentar menggambar teks melayang. |
| 291 | `        for ft in self.floating_texts:` | Melakukan iterasi ke setiap teks melayang aktif. |
| 292 | `            shadow_surf = self.font.render(ft['text'], True, (0, 0, 0))` | Membuat teks bayangan berwarna hitam untuk efek outline agar teks lebih terbaca. |
| 293 | `            text_surf = self.font.render(ft['text'], True, ft['color'])` | Membuat teks utama dengan warna yang ditentukan di kamus properti teks melayang tersebut. |
| 294 | `            sp = camera.apply(ft['pos'])` | Mengonversi koordinat teks melayang ke layar berdasarkan pergerakan kamera. |
| 295 | `            screen.blit(shadow_surf, (sp[0] + 1, sp[1] + 1))` | Menggambar teks bayangan dengan pergeseran 1 piksel ke kanan dan ke bawah. |
| 296 | `            screen.blit(text_surf, sp)` | Menggambar teks utama di atas bayangannya pada posisi aslinya. |
| 297 | | Baris kosong sebagai pemisah. |

---

### 8. Metode `get_status_text` (Baris 298 - 302)
Bagian ini mengembalikan teks objektif petunjuk jalan aktif pada HUD game.

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| 298 | `    def get_status_text(self):` | Metode untuk mengambil teks objektif misi atau status permainan saat ini di area Sanctuary untuk ditampilkan pada HUD/antarmuka game. |
| 299 | `        if self.alarm_active: return "STATUS: PERTAHANAN AKTIF!"` | Jika status alarm aktif, mengembalikan teks status pertahanan aktif. |
| 300 | `        if not self.elder_met: return "OBJEKTIF: Cari dan bicara ke Penatua Aris (Warna Oranye)"` | Jika pemain belum bertemu Penatua Aris, mengembalikan petunjuk objektif untuk mencari Penatua Aris. |
| 301 | `        return "OBJEKTIF: Bicara ke Kapten Jaka di jalan (Warna Biru)"` | Jika sudah bertemu Penatua Aris tetapi alarm belum aktif, mengembalikan petunjuk untuk menemui Kapten Jaka. |
| 302 | | Akhir file kode sumber. |

---

## Alur Kerja Utama

Berikut adalah alur logika utama dari file ini saat dipanggil oleh game engine:

1. **Inisialisasi (`__init__`)**:
   - Memanggil `_setup_npcs()` untuk meletakkan tiga karakter NPC di posisi koordinat yang telah ditentukan pada peta (peta berukuran 2560x1440).
   - Memuat file gambar latar belakang peta (`sanctuary_map.png`). Jika gagal, sistem akan menggunakan warna rumput hijau polos dan menggambar jalan cokelat tanah sebagai opsi darurat (*fallback*).
   
2. **Pembaruan Logika (`update`)**:
   - **Perubahan Kecepatan Pemain**: Membatasi laju jalan pemain secara default sebesar 40% agar suasana kota aman terasa tenang.
   - **Update Gerak NPC & Efek**: Memperbarui status animasi NPC, partikel aktif, laju pengurangan usia partikel (*decay*), dan pergerakan vertikal teks melayang ke atas.
   - **Api Unggun (Campfire)**: Pemain yang terlalu dekat (< 30px) akan kehilangan HP dan terbakar. Jika berada di jarak hangat (30px - 120px), pemain akan mendapatkan dorongan stamina (*speed boost*).
   - **Area Medis (Medical Area)**: Jika koordinat pemain berada dalam rentang kamar medis, HP-nya akan pulih secara bertahap dan memunculkan pendaran partikel hijau.
   - **Kolam Air (Pond)**: Pemain yang melewati kolam air kecepatannya dipangkas menjadi 20% dan memicu partikel cipratan air.
   - **Loker Pakaian (Wardrobe)**: Mendeteksi interaksi tombol enter di dekat loker dan mengirim sinyal `"OPEN_WARDROBE"`.
   - **Kotak Suplai Udara (Helipad Supply Drop)**: Jika dipanggil di helipad, peti akan dijatuhkan dari langit secara perlahan. Ketika menyentuh tanah, partikel debu menyebar. Pemain dapat membukanya untuk mendapatkan uang $150 Bronze (dikirim lewat sinyal `"AWARD_150_BRONZE"`).

3. **Mekanik Alur Cerita Utama (NPC Quest)**:
   - Pemain tidak bisa memulai pertempuran sebelum berbicara dengan **Penatua Aris** (untuk mengeset status `elder_met` menjadi `True`).
   - Setelah menemui Penatua Aris, pemain dapat berbicara dengan **Kapten Jaka** di gerbang timur. Hal ini memicu alarm bahaya (`alarm_active = True`), memindahkan posisi pemain ke menara pertahanan, dan mengembalikan sinyal `"START_SHOOTING"` untuk memicu transisi ke modus pertempuran aktif.

4. **Rendering Grafis (`draw_ground` dan `draw_entities`)**:
   - `draw_ground` menggambar latar belakang peta dengan kompensasi koordinat kamera game.
   - `draw_entities` menggambar seluruh objek berlapis di atas tanah mulai dari partikel, animasi terjun payung peti suplai beserta bayangannya di tanah, model NPC beserta tag nama di atas kepalanya, teks melayang (+HEAL, BURNING!), dan petunjuk instruksi interaktif ("PRESS ENTER TO...").
