# Penjelasan Kode: `shooting_range.py`

Dokumen ini berisi penjelasan detail baris demi baris untuk file `/home/abuyyy/PemogramanLanjut/src/core/minigames/shooting_range.py`. Penjelasan ini ditulis dalam bahasa Indonesia untuk membantu persiapan demo program.

---

## Deskripsi & Tujuan File
File `shooting_range.py` mendefinisikan seluruh logika dari minigame **"City Under Attack"** (latihan menembak untuk mempertahankan kota):
1. **Konfigurasi Senjata (`WeaponType` & `TacticalWeapon`)**: Mengatur statistik dasar 4 senjata (Micro Uzi, SCAR-H, Spas-12 Shotgun, AWM Sniper) beserta sistem amunisi, penanganan delay tembakan, dan durasi isi ulang (*reload*).
2. **Sistem Deteksi Tembakan & Recoil**: Mengurangi amunisi, memutar SFX tembakan (`suarapistol.mp3`), memicu getaran layar (*screen shake*), dan mendeteksi tabrakan koordinat kursor (*crosshair*) dengan zombie (termasuk deteksi *headshot* / tembakan di kepala untuk melipatgandakan damage).
3. **Mekanisme Target Zombie**: Zombie akan spawn secara berkala dengan arah dan baris animasi yang acak, bergerak mendekati layar bawah, dan memiliki bar nyawa di atas kepala. Setiap kelipatan 15 eliminasi, Boss Zombie ("Crimson Abomination") raksasa akan lahir dengan kapasitas nyawa tebal dan memberikan hadiah bonus melimpah.
4. **Bantuan Bidik Otomatis (`Aim Assist`) & Bidikan Kunci**: Memeriksa target terdekat dengan retikel kursor, lalu mendorong kursor secara magnetis mendekat sebesar 55% ke arah kepala zombie jika berada di dalam radius sensitivitas (90px) untuk mempermudah bidikan pemain webcam.

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel penjelasan baris demi baris dari kode sumber `shooting_range.py`:

| Baris | Kode Sumber | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import pygame, math, random, time` | Mengimpor Pygame untuk grafik/audio, math untuk perhitungan jarak, random untuk acak, dan time untuk jeda waktu. |
| **2** | `from typing import List, Dict, Tuple, Optional` | Mengimpor helper tipe data untuk petunjuk tipe statis (typing). |
| **3** | `from src.core.engine import MiniGame, Spritesheet` | Mengimpor kelas induk `MiniGame` dan pembaca visual `Spritesheet` dari engine utama. |
| **4** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **5** | `class PixelPalette:` | Deklarasi kelas `PixelPalette` untuk menyimpan warna-warna tema UI game. |
| **6** | `    GOLD, CYAN_GLOW, FIRE_GLOW, BLOOD = (255, 215, 0), (0, 255, 255), (255, 50, 50), (180, 0, 0)` | Konstanta warna koin emas, cyan berpendar, merah api, dan merah darah zombie. |
| **7** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **8** | `class Particle:` | Deklarasi kelas `Particle` untuk partikel cipratan darah ketika zombie tertembak. |
| **9** | `    def __init__(self, x, y, color, size_range=(2, 8)):` | Konstruktor menerima koordinat awal partikel, warna, dan rentang ukuran opsional. |
| **10** | `        self.pos, self.shadow = [x, y], [random.uniform(-3, 3), random.uniform(-3, 3)]` | Menyimpan posisi dan kecepatan sebaran horizontal/vertikal acak (antara -3 s.d 3). |
| **11** | `        self.color, self.size, self.life = color, random.randint(*size_range), 1.0` | Menyimpan warna, memilih ukuran acak, dan menetapkan masa hidup awal partikel ke 100% (1.0). |
| **12** | `    def update(self):` | Metode memperbarui pergerakan dan sisa masa hidup partikel di setiap frame. |
| **13** | `        self.pos[0] += self.vel[0]; self.pos[1] += self.vel[1]; self.life -= 0.02` | Menggeser koordinat X/Y partikel sesuai kecepatannya, lalu mengurangi masa hidup sebesar 0.02 per frame. |
| **14** | `        return self.life > 0` | Mengembalikan status `True` jika partikel masih hidup (`life > 0`), atau `False` jika sudah mati. |
| **15** | `    def draw(self, screen, offset=(0,0)):` | Menggambar lingkaran partikel ke layar. |
| **16** | `        pygame.draw.circle(screen, self.color, (int(self.pos[0] + offset[0]), int(self.pos[1] + offset[1])), int(self.size * self.life))` | Menggambar partikel bulat disesuaikan dengan goyangan getar layar (`offset`). |
| **17** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **18** | `class WeaponType:` | Deklarasi kelas statistik senjata permainan. |
| **19** | `    UZI = {"name": "MICRO UZI (SMG)", ...}` | Kamus data Micro Uzi: damage 25, peluru 40, recoil ringan 6px, delay tembak sangat cepat 3 frame (beruntun). |
| **20** | `    SCAR = {"name": "SCAR-H (ASSAULT)", ...}` | Kamus data SCAR-H: damage 45, peluru 30, recoil sedang 14px, delay tembak 6 frame. |
| **21** | `    SHOTGUN = {"name": "SPAS-12 (SHOTGUN)", ...}` | Kamus data Spas-12: damage besar 120, peluru 8, recoil kuat 32px, delay tembak lambat 28 frame. |
| **22** | `    SNIPER = {"name": "AWM SNIPER", ...}` | Kamus data AWM Sniper: damage sangat besar 250, peluru 5, recoil sangat kuat 48px, delay tembak sangat lambat 55 frame. |
| **23** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **24** | `class TacticalWeapon:` | Deklarasi kelas `TacticalWeapon` untuk memproses logika individual senjata aktif. |
| **25** | `    def __init__(self, w_type, reload_max_time=60):` | Konstruktor menerima kamus tipe senjata (`w_type`) dan batas waktu reload default 60 frame. |
| **26** | `        self.type = w_type` | Menyimpan kamus tipe data senjata. |
| **27** | `        self.ammo_max = w_type["ammo"]` | Menyimpan kapasitas amunisi maksimal senjata. |
| **28** | `        self.ammo, self.is_reloading, self.reload_timer, self.shot_delay, self.reload_max_time = self.ammo_max, False, 0, 0, reload_max_time` | Mengeset peluru awal, status reload (`False`), timer reload (0), jeda tembak (0), dan batas maksimal waktu reload. |
| **29** | `    def update(self):` | Memperbarui sisa jeda tembak dan durasi reload senjata per frame. |
| **30** | `        if self.shot_delay > 0: self.shot_delay -= 1` | Jika jeda tembak aktif, kurangi nilainya sebanyak 1 tick. |
| **31-33** | `        if self.is_reloading: ...` | Jika sedang reload: kurangi timer reload. Jika timer habis, isi peluru penuh kembali dan set status reload ke `False`. |
| **34** | `    def can_shoot(self): return self.ammo > 0 and not self.is_reloading and self.shot_delay <= 0` | Mengembalikan status `True` jika peluru masih ada, tidak sedang reload, dan jeda tembak bernilai 0. |
| **35** | `    def shoot(self): self.ammo -= 1; self.shot_delay = self.type["delay"]` | Mengurangi amunisi sebanyak 1 dan memasang jeda delay tembak sesuai jenis senjata. |
| **36-37** | `    def reload(self): ...` | Memulai proses pengisian peluru baru jika sedang tidak reload dan peluru di magazine belum penuh. |
| **38** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **39** | `class ShootingRangeUltimate(MiniGame):` | Deklarasi kelas utama minigame "City Under Attack". |
| **40-41** | `    def __init__(self, screen, clock, manager): super().__init__(...)` | Konstruktor minigame memanggil inisialisasi kelas induk `MiniGame`. |
| **42** | `        self.width, self.height = 1280, 720` | Resolusi layar minigame: 1280x720 piksel. |
| **43** | `        self.crosshair, self.score, self.timer, self.kills, self.headshots, self.bronze_earned, self.boss_spawned_count = [640, 360], 0, 90.0, 0, 0, 0, 0` | Inisialisasi kursor tengah, skor 0, sisa waktu awal 90 detik, eliminasi, headshot, perolehan Bronze, dan hitungan boss spawn. |
| **44-47** | `        try: self.bg_img = ... except: ...` | Memuat gambar latar belakang kota hancur `city_bg.png` seukuran layar (fallback warna abu-abu biru gelap jika gagal). |
| **48-52** | `        self.weapon_images = {} ...` | Loop otomatis untuk memuat 4 gambar visual model senjata FPS berskala (Micro Uzi, SCAR-H, Spas-12, AWM Sniper). |
| **53-55** | `        try: self.zombie_sheet = ...` | Memuat spritesheet visual zombie musuh berskala pembesaran 2.5x. |
| **56** | `        upgrades = getattr(self.manager.main_engine, "weapon_upgrades", ...)` | Mengambil setelan data upgrade level senjata dari dunia Sanctuary utama. |
| **57-63** | `        self.weapons = {} ...` | Menginstansiasi 4 senjata pemain dengan penyesuaian bonus upgrade (Lv upgrade menambah Damage +25%, kapasitas Ammo +25%, mempercepat reload, dan mempercepat firerate). |
| **64** | `        self.current_weapon_name = getattr(self.manager.main_engine, "selected_weapon", "SCAR")` | **Sistem Senjata Terkunci**: Mengunci senjata minigame agar sesuai dengan senjata pilihan terakhir di Sanctuary. |
| **65** | `        self.targets, self.particles, self.floating_texts, self.flash_timer, self.shake_v = [], [], [], 0, 0` | Inisialisasi list zombie aktif, partikel, teks melayang, timer kilatan tembakan, dan kekuatan getar layar aktif. |
| **66** | `        self.font_header, self.font_tactical = pygame.font.SysFont("monospace", 36, bold=True), pygame.font.SysFont("monospace", 18, bold=True)` | Inisialisasi font teks utama 36px tebal dan font UI taktis 18px tebal. |
| **67-70** | `        try: self.shoot_sfx = ...` | Memuat file audio efek suara tembakan senjata (`suarapistol.mp3`) dengan volume 60%. |
| **71** | *(Baris Kosong)* | Pemisah visual. |
| **72-73** | `    @property def weapon(self): return self.weapons[self.current_weapon_name]` | Properti getter mengambil objek senjata aktif pemain saat ini. |
| **74** | *(Baris Kosong)* | Pemisah visual. |
| **75** | `    def _trigger_shot(self):` | Metode internal menembakkan satu peluru dan memproses pencocokan tembakan. |
| **76** | `        self.weapon.shoot(); self.flash_timer, self.shake_v = 5, self.weapon.type["recoil"]` | Kurangi peluru, picu kedipan flash putih 5 frame, pasang getaran recoil layar. |
| **77** | `        if self.shoot_sfx: self.shoot_sfx.play()` | Putar efek suara tembakan. |
| **78** | `        hit = False` | Status penanda apakah tembakan mengenai zombie (awal False). |
| **79-80** | `        for t in self.targets: hx, hy, hr = ...` | Mengambil koordinat kepala zombie (titik tengah sumbu X, sumbu Y ber-offset ke atas, dan radius kepala 40% dari ukuran tubuh). |
| **81-82** | `            dist_head = math.hypot(...) ; dist_body = ...` | Menghitung jarak bidikan crosshair ke kepala zombie dan jarak ke badan zombie. |
| **83** | `            if dist_head < hr or dist_body < t['size']:` | Jika kursor masuk ke radius kepala atau radius badan zombie. |
| **84** | `                is_hs = dist_head < hr` | Status boolean `is_hs` bernilai `True` jika mengenai kepala. |
| **85** | `                dmg = self.weapon.type["damage"] * (2 if is_hs else 1)` | Damage tembakan dilipatgandakan menjadi 2x lipat jika Headshot. |
| **86** | `                self.floating_texts.append(...)` | Menambahkan teks melayang kerusakan berwarna kuning emas jika "CRITICAL! Headshot" atau abu-abu jika tembakan biasa. |
| **87** | `                for _ in range(15 if is_hs else 8): self.particles.append(...)` | Memunculkan partikel sebaran darah zombie di titik benturan peluru (lebih banyak jika headshot). |
| **88** | `                t['hp'] -= dmg` | Mengurangi nyawa zombie. |
| **89** | `                if t['hp'] <= 0:` | Jika nyawa zombie habis (zombie tereliminasi). |
| **90** | `                    self.kills += 1; is_boss = t.get('is_boss', False)` | Tambah total eliminasi, cek status apakah target merupakan Boss Zombie. |
| **91** | `                    mult = 1.0 if self.kills < 10 else 1.5 if self.kills < 25 else 2.0 if self.kills < 50 else 3.0 if self.kills < 80 else 5.0` | Menghitung pengali skor beruntun (*Score Multiplier*) berdasarkan jumlah eliminasi. |
| **92-96** | `                    if is_boss: ...` | Logika kematian Boss Zombie: +1000 Poin, +200 Bronze, bonus tambahan waktu +20 detik, picu shake layar kuat (40px), dan pemicu sebaran partikel masif. |
| **97-103** | `                    else: ...` | Logika kematian zombie biasa: tambah headshot tracker jika sesuai, skor +150 (HS) / +100 (Body), klaim uang dikalikan multiplier, bonus waktu +4.0s (HS) / +2.5s (Body). |
| **104** | `                    t['active'] = False` | Menonaktifkan status zombie agar terhapus dari daftar aktif. |
| **105** | `                hit = True; break` | Mengubah status hit ke `True` dan hentikan perulangan target (satu peluru menembus satu zombie terdepan). |
| **106-107** | `        if not hit: for _ in range(3): self.particles.append(...)` | Jika peluru meleset mengenai latar belakang tembok, buat 3 partikel percikan abu-abu. |
| **108** | *(Baris Kosong)* | Pemisah visual. |
| **109** | `    def handle_event(self, event):` | Metode memproses kejadian input mouse fisik dan keyboard. |
| **110** | `        if event.type == pygame.MOUSEMOTION: self.crosshair = list(event.pos)` | Mengikuti posisi mouse jika pemain menggerakkan mouse fisik. |
| **111-112** | `        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.weapon.can_shoot(): self._trigger_shot()` | Tembak 1 peluru saat klik kiri mouse ditekan dan senjata siap. |
| **113-114** | `        if event.type == pygame.KEYDOWN: if event.key == pygame.K_r: self.weapon.reload()` | Lakukan pengisian peluru manual jika tombol `R` ditekan. |
| **115** | *(Baris Kosong)* | Pemisah visual. |
| **116** | `    def update(self, dt):` | Metode update logika minigame per frame. |
| **117** | `        self.timer -= dt / 60.0` | Mengurangi sisa waktu bermain minigame. |
| **118** | `        if self.timer <= 0: self.exit_game({'score': self.score, 'bronze_earned': self.bronze_earned})` | Jika waktu habis, matikan minigame dan laporkan skor ke Sanctuary. |
| **119** | `        for w in self.weapons.values(): w.update()` | Memperbarui status cooldown internal di seluruh daftar senjata. |
| **120-127** | `        # Gesture-based reloading ...` | **Reload Gestur**: Membaca thread gestur tangan. Jika tangan mengepal (`FIST`) atau gestur (`RELOAD`) terdeteksi dan magazine belum penuh, picu reload otomatis. |
| **128-133** | `        is_auto = self.current_weapon_name in ["UZI", "SCAR"] ...` | **Tembak Otomatis (Uzi/Scar)**: Jika tombol mouse ditekan terus menerus ATAU gestur tangan berbentuk pistol (`PISTOL`) diacungkan, tembak secara otomatis secepat mungkin sesuai jeda senjata. |
| **134-135** | `        if self.flash_timer > 0: self.flash_timer -= 1` | Mengurangi timer kedipan efek tembak. |
| **136** | `        if self.shake_v > 0: self.shake_v *= 0.85` | Meredam getaran layar secara bertahap (dikalikan 0.85 per frame). |
| **137-141** | `        next_boss = 15 * (self.boss_spawned_count + 1) ...` | **AI Melahirkan Boss**: Lahirkan Boss Zombie Crimson Abomination setiap kelipatan 15 eliminasi. Pasang nyawa tebal (600 HP) dan beri getaran layar kuat. |
| **142-146** | `        max_targets = 8 + min(7, self.kills // 5) ...` | **AI Melahirkan Zombie**: Melahirkan zombie baru di koordinat acak jika jumlah di layar kurang dari kapasitas maksimum target (kapasitas bertambah sulit seiring eliminasi). |
| **147-156** | `        speed_mult = 1.0 + (self.kills / 25.0) ...` | **AI Gerakan Zombie**: Menggerakkan koordinat zombie (zombie bergerak turun ke bawah jika sumbu animasi bernilai 4, bergerak ke kanan jika sumbu 6, dan bergerak ke kiri jika sumbu 7). Kecepatan zombie bertambah seiring eliminasi. |
| **157** | `        self.targets = [t for t in self.targets if t['active'] and t['timer'] > 0 and t['pos'][1] < 670]` | Menyaring dan menyisakan zombie yang masih aktif, durasinya belum habis, dan belum melintasi batas pertahanan bawah (670px). |
| **158** | `        self.particles = [p for p in self.particles if p.update()]` | Memperbarui status partikel cipratan darah di layar. |
| **159-160** | `        for ft in self.floating_texts: ft['pos'][1] -= 0.8; ft['timer'] -= 1 ...` | Menggeser teks melayang ke atas dan menyaring teks yang durasinya habis. |
| **161-169** | `        closest_t = None; min_d = 90.0 ...` | **Sistem Bantuan Bidik (Aim Assist)**: Memindai seluruh zombie terdekat. Jika koordinat kepala zombie berada di dalam radius sensitivitas bidikan (< 90px), tarik/geser kursor crosshair secara magnetis mendekat sebesar 55% agar mempermudah pemakaian tangan webcam. |
| **170** | `    def _draw_pistol_fps(self, screen, offset):` | Metode menggambar model visual senjata FPS di kanan bawah layar game. |
| **171-173** | `        cx, cy = self.crosshair ...` | Menghitung koordinat posisi gambar senjata agar ikut bergerak sedikit bergoyang mengikuti retikel bidikan kursor pemain. |
| **174-177** | `        img = self.weapon_images.get(self.current_weapon_name) ...` | Menggambar visual model senjata terpilih disesuaikan recoil getaran layar. |
| **178-180** | `        else: ...` | Fallback: gambar persegi panjang abu-abu sederhana sebagai model pistol darurat jika file aset gambar gagal dimuat. |
| **181** | *(Baris Kosong)* | Pemisah visual. |
| **182** | `    def draw(self):` | Metode utama merender seluruh elemen visual minigame ke layar. |
| **183-184** | `        offset = (...) ; self.screen.blit(self.bg_img, offset)` | Menghitung pergeseran acak getaran layar (recoil/shake) lalu merender gambar latar belakang kota. |
| **185-197** | `        for t in self.targets: ...` | Loop menggambar zombie di layar. Jika spritesheet berhasil dimuat: blit frame sprite zombie (lebih besar 2.2x jika tipe Boss), gambar elips bayangan merah di tanah, dan gambar bar nyawa di atas kepala zombie. |
| **198-199** | `            else: ...` | Fallback: gambar lingkaran hijau-merah sederhana sebagai visual zombie darurat jika spritesheet tidak ditemukan. |
| **200** | `        for p in self.particles: p.draw(self.screen, offset)` | Menggambar seluruh partikel cipratan darah. |
| **201-203** | `        for ft in self.floating_texts: ...` | Menggambar teks melayang kerusakan (dengan outline bayangan hitam agar terbaca). |
| **204-210** | `        if self.flash_timer > 0: ...` | Menggambar kedipan flash layar putih kekuningan saat menembak, dan lingkaran oranye kilatan api moncong senjata (*muzzle flash*). |
| **211** | `        self._draw_pistol_fps(self.screen, offset)` | Memanggil fungsi penggambaran model visual senjata FPS. |
| **212-214** | `        pygame.draw.rect(...) ; pygame.draw.line(...)` | Menggambar panel kepala atas berwarna gelap dan garis pembatas neon merah setebal 3px. |
| **215-216** | `        self.screen.blit(self.font_header.render("CITY UNDER ATTACK", ...))` | Menampilkan judul minigame dan total eliminasi serta pengali skor di panel atas. |
| **217-218** | `        self.screen.blit(...)` | Menampilkan total skor dan perolehan Bronze di panel atas sebelah kanan. |
| **219-220** | `        self.screen.blit(...)` | Menampilkan nama senjata aktif dan sisa peluru/magazine di panel atas sebelah kiri bawah. |
| **221-224** | `        pygame.draw.rect(self.screen, (10, 10, 15, 200), (950, 600, 310, 80) ...` | Menggambar panel visual info senjata terkunci di pojok kanan bawah. Menampilkan teks penegasan bahwa senjata aktif saat ini sedang terkunci untuk kestabilan gameplay. |
| **225-226** | `        mins, secs = int(self.timer)//60, int(self.timer)%60 ...` | Menampilkan jam pewaktu hitung mundur sisa waktu bermain minigame di bagian tengah atas. |
| **227-234** | `        boss = next(...)` | Menggambar boss bar besar berwarna merah neon di bagian tengah atas jika Crimson Abomination (Boss Zombie) sedang aktif. |
| **235-240** | `        locked = None ...` | Mengecek apakah target di dekat kursor terkunci (radius < 12px) untuk mengubah retikel menjadi merah tanda sasaran pas. |
| **241-243** | `        pygame.draw.circle(...)` | Menggambar retikel kursor crosshair bidikan bulat berpendar hijau (atau merah jika target terkunci). |
| **244** | `        if locked: pygame.draw.rect(...)` | Menggambar kotak target penanda merah 44x44px di tubuh zombie jika bidikan terkunci telak. |
| **245** | *(Baris Kosong)* | Akhir dari berkas kode sumber. |

---

## Mekanika Kunci Senjata & Stabilitas Gestur
* **Masalah Awal**: Tangan goyang webcam sering memicu pergantian senjata yang tidak disengaja (misalpeace sign tanpa sengaja terbaca saat menembak), sehingga minigame lag dan peluru macet.
* **Solusi Terkunci**: Pemilihan senjata hanya bisa dilakukan di dunia Sanctuary utama menggunakan tombol keyboard `1`-`4`. Ketika masuk ke mode minigame, senjata aktif dikunci secara permanen (`self.current_weapon_name = selected_weapon`). Pilihan gestur webcam hanya dibatasi untuk membidik (`AIM`), menembak (`PISTOL`), dan mengisi peluru (`FIST`) sehingga performa minigame sangat mulus dan stabil.
