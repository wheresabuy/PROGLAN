# Penjelasan Kode: `engine.py`

Dokumen ini berisi penjelasan detail baris demi baris untuk file `/home/abuyyy/PemogramanLanjut/src/core/engine.py`. Penjelasan ini ditulis dalam bahasa Indonesia untuk membantu persiapan demo program.

---

## Deskripsi & Tujuan File
File `engine.py` berfungsi sebagai penggerak dasar (*core game engine*) permainan. Di dalamnya terdapat beberapa kelas utilitas penting:
1. **`Spritesheet`**: Memotong-motong lembaran gambar sprite besar (*spritesheet*) menjadi frame individual berskala untuk dianimasikan.
2. **`Camera`**: Mengatur efek pergeseran kamera 2D scroll mengikuti posisi target pemain agar tidak keluar dari area batas peta.
3. **`CurrencyManager`**: Menyimpan dan melacak saldo keuangan pemain, menangani transaksi penambahan koin perunggu (*Bronze*), serta konversi otomatis pecahan 100 Bronze = 1 Silver, dan 100 Silver = 1 Gold.
4. **`AudioManager`**: Mengontrol pemutaran musik latar (BGM) secara berulang dan efek suara tembakan/ledakan (SFX).
5. **`VisualEffects`**: Menggambar lapisan kegelapan malam dengan senter melingkar di sekeliling pemain, efek getaran layar (*screen shake*), dan efek kedipan putih kilatan cahaya tembakan.
6. **`MiniGame` & `MiniGameManager`**: Kelas abstraksi dan pengelola alur transisi daur hidup minigame, menyimpan/mengembalikan status eksplorasi, serta membagikan bonus uang perunggu berdasarkan performa bermain.

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel penjelasan baris demi baris dari kode sumber `engine.py`:

| Baris | Kode Sumber | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import pygame, random, math, os` | Mengimpor Pygame untuk grafik/audio, random untuk acak, math untuk trigonometri, dan os untuk path file. |
| **2** | `from typing import Optional` | Mengimpor tipe `Optional` untuk anotasi tipe data statis. |
| **3** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **4** | `class Spritesheet:` | Deklarasi kelas `Spritesheet` untuk memotong dan mengelola kumpulan frame animasi gambar. |
| **5** | `    def __init__(self, filename, cols, rows, scale=1.5):` | Konstruktor menerima path file gambar, jumlah kolom, jumlah baris, dan faktor skala pembesaran. |
| **6** | `        self.sheet = pygame.image.load(filename).convert_alpha()` | Memuat gambar spritesheet dari path dan mengonversi format warna alpha transparansi piksel. |
| **7** | `        self.cols, self.rows, self.scale = cols, rows, scale` | Menyimpan jumlah kolom, jumlah baris, dan skala pembesaran di atribut objek. |
| **8** | `        self.fw, self.fh = self.sheet.get_width() // cols, self.sheet.get_height() // rows` | Menghitung lebar (`fw`) dan tinggi (`fh`) masing-masing frame gambar (lebar total / kolom, tinggi total / baris). |
| **9** | `        self.frames = [[pygame.transform.scale(self.sheet.subsurface((c*self.fw, r*self.fh, self.fw, self.fh)), (int(self.fw*scale), int(self.fh*scale))) for c in range(cols)] for r in range(rows)]` | Memotong frame individual menggunakan `subsurface` di setiap koordinat baris/kolom, lalu menskalakan ukurannya secara dinamis menggunakan list comprehension bersarang. |
| **10** | `    def get_frame(self, row, col): return self.frames[row][col]` | Metode pembantu untuk mengambil gambar frame tertentu pada baris dan kolom yang diminta. |
| **11** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **12** | `class Camera:` | Deklarasi kelas `Camera` untuk mengendalikan pandangan scroll 2D. |
| **13** | `    def __init__(self, w, h, mw, mh):` | Konstruktor menerima lebar layar (`w`), tinggi layar (`h`), lebar peta maksimal (`mw`), dan tinggi peta maksimal (`mh`). |
| **14** | `        self.camera = pygame.Rect(0, 0, w, h)` | Membuat objek Rect Pygame sebagai pembatas pandangan kamera awal di (0,0). |
| **15** | `        self.w, self.h, self.mw, self.mh = w, h, mw, mh` | Menyimpan resolusi layar dan ukuran maksimal peta. |
| **16** | `    def apply(self, pos):` | Menghitung posisi objek di layar berdasarkan posisi aslinya di peta dikurangi pergeseran kamera. |
| **17** | `        return pos.move(self.camera.topleft) if isinstance(pos, pygame.Rect) else (pos[0] + self.camera.x, pos[1] + self.camera.y)` | Jika bertipe Rect, geser topleft-nya. Jika berupa koordinat list/tuple, tambahkan offset X/Y kamera. |
| **18** | `    def update(self, t):` | Metode untuk memperbarui koordinat kamera agar berpusat mengikuti target posisi `t` (pemain). |
| **19** | `        x = max(-(self.mw - self.w), min(0, -t[0] + self.w // 2))` | Menghitung posisi horizontal X kamera agar berada di tengah target, dibatasi agar tidak melampaui batas tepi peta. |
| **20** | `        y = max(-(self.mh - self.h), min(0, -t[1] + self.h // 2))` | Menghitung posisi vertikal Y kamera agar berada di tengah target, dibatasi batas tepi peta. |
| **21** | `        self.camera = pygame.Rect(x, y, self.w, self.h)` | Menyimpan koordinat kamera baru ke dalam objek Rect `self.camera`. |
| **22** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **23** | `class CurrencyManager:` | Deklarasi kelas `CurrencyManager` untuk mengelola uang koin pemain. |
| **24** | `    def __init__(self): self.bronze = self.silver = self.gold = 0` | Konstruktor menetapkan saldo awal bronze, silver, dan gold ke 0. |
| **25** | `    def add_bronze(self, amt): self.bronze += amt; self._convert()` | Menambahkan sejumlah uang perunggu (bronze) lalu memicu fungsi konversi nilai mata uang. |
| **26** | `    def get_total_bronze(self): return self.bronze + (self.silver * 100) + (self.gold * 10000)` | Mengalkulasi total seluruh uang jika semua koin dilebur ke satuan perunggu (1 Silver = 100 Bronze, 1 Gold = 10.000 Bronze). |
| **27** | `    def deduct_bronze(self, amt):` | Mengurangi saldo perunggu pemain jika total seluruh uang mencukupi. |
| **28** | `        tot = self.get_total_bronze()` | Mendapatkan total kekayaan pemain dalam satuan perunggu. |
| **29** | `        if tot < amt: return False` | Jika total uang kurang dari jumlah yang ditarik, batalkan transaksi dan kembalikan `False`. |
| **30** | `        self.gold, r = divmod(tot - amt, 10000)` | Menghitung sisa koin emas baru dengan membagi total sisa uang dengan 10.000 (fungsi divmod mengembalikan hasil bagi dan sisa). |
| **31** | `        self.silver, self.bronze = divmod(r, 100)` | Menghitung sisa koin perak dan perunggu dari sisa kembalian pembagian sebelumnya dibagi 100. |
| **32** | `        return True` | Mengembalikan `True` tanda pengurangan sukses dilakukan. |
| **33** | `    def _convert(self):` | Metode internal mengonversi pecahan perunggu ke perak dan perak ke emas. |
| **34** | `        if self.bronze >= 100: self.silver += self.bronze // 100; self.bronze %= 100` | Jika koin perunggu >= 100, konversi kelipatannya ke perak dan simpan sisanya. |
| **35** | `        if self.silver >= 100: self.gold += self.silver // 100; self.silver %= 100` | Jika koin perak >= 100, konversi kelipatannya ke emas dan simpan sisanya. |
| **36** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **37** | `class AudioManager:` | Deklarasi kelas `AudioManager` untuk memproses musik dan efek suara. |
| **38** | `    def __init__(self):` | Konstruktor pembuat manajer audio. |
| **39** | `        pygame.mixer.init()` | Menginisialisasi modul audio mixer milik Pygame. |
| **40** | `        self.bgm_volume, self.sfx_volume, self.current_bgm = 0.5, 0.7, None` | Mengeset volume musik latar default (50%), volume efek suara (70%), dan lagu latar aktif saat ini ke `None`. |
| **41** | `    def play_bgm(self, f, loops=-1):` | Memutar file musik latar (BGM) secara looping terus menerus. |
| **42** | `        try:` | Blok penanganan kesalahan pemuatan audio. |
| **43** | `            if self.current_bgm == f: return` | Jika lagu latar yang diminta sedang diputar saat ini, jangan putar ulang agar tidak lag. |
| **44** | `            pygame.mixer.music.load(f)` | Memuat file audio musik latar dari path `f`. |
| **45** | `            pygame.mixer.music.set_volume(self.bgm_volume)` | Mengatur volume suara pemutaran musik latar. |
| **46** | `            pygame.mixer.music.play(loops)` | Memutar musik latar secara berulang sesuai parameter `loops` (default -1 berarti tiada henti). |
| **47** | `            self.current_bgm = f` | Menyimpan nama path file lagu latar aktif saat ini. |
| **48** | `        except: pass` | Abaikan kesalahan jika file musik rusak atau tidak ditemukan. |
| **49** | `    def stop_bgm(self): pygame.mixer.music.stop(); self.current_bgm = None` | Menghentikan pemutaran musik latar dan mereset current_bgm ke `None`. |
| **50** | `    def play_sfx(self, f):` | Memutar efek suara (SFX) singkat secara instan. |
| **51** | `        try:` | Blok penanganan kesalahan pemuatan audio SFX. |
| **52** | `            s = pygame.mixer.Sound(f)` | Memuat file efek suara dari path `f` ke objek Sound. |
| **53** | `            s.set_volume(self.sfx_volume)` | Mengatur tingkat volume pemutaran efek suara. |
| **54** | `            s.play()` | Memainkan suara efek sekali jalan. |
| **55** | `        except: pass` | Abaikan kesalahan jika file suara tidak ditemukan. |
| **56** | `    def set_volumes(self, bv, sv):` | Mengubah volume musik latar dan efek suara secara dinamis. |
| **57** | `        self.bgm_volume, self.sfx_volume = bv, sv` | Menyimpan setelan volume BGM dan SFX baru ke atribut objek. |
| **58** | `        pygame.mixer.music.set_volume(bv)` | Menerapkan volume baru ke lagu latar yang sedang berputar di sistem. |
| **59** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **60** | `class VisualEffects:` | Deklarasi kelas `VisualEffects` untuk menggambar efek getaran, gelap malam, dan kedipan tembakan. |
| **61** | `    def __init__(self, w, h):` | Konstruktor menerima lebar (`w`) dan tinggi (`h`) layar game. |
| **62** | `        self.w, self.h = w, h` | Menyimpan dimensi layar game. |
| **63** | `        self.darkness_surf = pygame.Surface((w, h), pygame.SRCALPHA)` | Membuat bidang permukaan gambar kegelapan malam seukuran layar berkemampuan transparansi alpha (`SRCALPHA`). |
| **64** | `        self.flash_surf = pygame.Surface((w, h))` | Membuat bidang permukaan gambar kedipan putih kilatan seukuran layar. |
| **65** | `        self.flash_surf.fill((255,255,255))` | Mewarnai permukaan kilatan dengan warna putih polos (RGB 255,255,255). |
| **66** | `        self.flash_timer = self.flash_duration = self.shake_amount = 0` | Menginisialisasi timer kilatan, durasi kilatan, dan tingkat getaran layar awal ke 0. |
| **67** | `    def draw_darkness(self, screen, p_pos, camera, light_on, bat, injured):` | Metode untuk menggambar kegelapan malam dengan pendaran lingkaran senter di tubuh pemain. |
| **68** | `        c = (25 + int(abs(math.sin(pygame.time.get_ticks() * 0.003)) * 40), 15, 15) if injured else (15, 15, 25)` | Memilih warna kegelapan: berdenyut kemerahan jika pemain cedera (`injured = True`), atau biru kehitaman jika sehat. |
| **69** | `        self.darkness_surf.fill((*c, 255))` | Mewarnai seluruh bidang kegelapan dengan warna terpilih secara pekat (alpha 255). |
| **70** | `        if light_on and bat > 0:` | Jika senter dinyalakan oleh pemain dan daya baterai masih tersisa (> 0). |
| **71** | `            sp = camera.apply(p_pos)` | Menghitung koordinat posisi pemain di layar menggunakan kamera. |
| **72** | `            cx, cy = int(sp[0] + 32), int(sp[1] + 32)` | Menghitung koordinat titik tengah senter (posisi X/Y pemain + offset 32px setengah ukuran sprite). |
| **73** | `            for r in range(200, 0, -8):` | Looping menggambar gradasi lingkaran luar ke dalam dari jejari 200px mengecil kelipatan 8px. |
| **74** | `                pygame.draw.circle(self.darkness_surf, (0,0,0, max(0, min(255, int(255 * (1.0 - (r / 200)))))), (cx, cy), r)` | Menggambar lingkaran transparan parsial di atas permukaan kegelapan. Semakin dekat ke pusat lingkaran, nilai alpha semakin mendekati 0 (transparan), membentuk efek pendaran senter. |
| **75** | `        screen.blit(self.darkness_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)` | Menempelkan bidang kegelapan ke layar menggunakan operasi masking pengurangan piksel (`BLEND_RGBA_SUB`). |
| **76** | `    def trigger_flash(self, dur=120): self.flash_timer, self.flash_duration, self.shake_amount = dur, max(1, dur), 15` | Memicu getaran layar (15px) dan kedipan putih layar dengan durasi `dur` frame. |
| **77** | `    def draw_flash(self, screen):` | Menggambar efek getaran layar dan kilatan putih pudar secara gradual. |
| **78** | `        off = [random.randint(-self.shake_amount, self.shake_amount), random.randint(-self.shake_amount, self.shake_amount)] if self.shake_amount > 0 else [0, 0]` | Menghitung offset koordinat layar acak horizontal/vertikal jika getaran layar aktif (> 0). |
| **79** | `        if self.shake_amount > 0: self.shake_amount -= 1` | Meredam kekuatan getaran layar dengan menguranginya 1 per frame. |
| **80** | `        if self.flash_timer > 0:` | Jika timer kilatan kedipan putih sedang berjalan. |
| **81** | `            self.flash_surf.set_alpha(max(0, min(255, int((self.flash_timer / self.flash_duration) * 255))))` | Mengatur tingkat transparansi alpha kilatan putih agar memudar seiring berkurangnya timer. |
| **82** | `            screen.blit(self.flash_surf, off)` | Menggambar kilatan putih di layar dengan tambahan offset koordinat getaran. |
| **83** | `            self.flash_timer -= 1` | Mengurangi timer kedipan putih sebanyak 1 per frame. |
| **84** | `        return tuple(off)` | Mengembalikan koordinat offset getaran layar untuk disesuaikan pada rendering peta Sanctuary. |
| **85** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **86** | `class MiniGame:` | Deklarasi kelas induk dasar `MiniGame` yang diabstraksi untuk membuat minigame baru. |
| **87** | `    def __init__(self, scr, clk, mgr):` | Konstruktor menerima objek screen utama, objek clock Pygame, dan objek minigame manager. |
| **88** | `        self.screen, self.clock, self.manager, self.running, self.score = scr, clk, mgr, True, 0` | Menyimpan referensi screen, clock, manager, status keaktifan game (`True`), dan skor awal (0). |
| **89** | `        self.font = pygame.font.SysFont("Arial", 24, bold=True)` | Inisialisasi font default Arial 24px tebal untuk kebutuhan minigame. |
| **90** | `    def handle_event(self, e): pass` | Metode placeholder untuk menangani kejadian/event input di minigame (diimplementasikan di kelas turunan). |
| **91** | `    def update(self, dt): pass` | Metode placeholder logika pembaruan frame minigame. |
| **92** | `    def draw(self): pass` | Metode placeholder menggambar grafis minigame. |
| **93** | `    def exit_game(self, res=None): self.running = False; self.manager.return_to_main(res)` | Metode untuk menghentikan minigame dan mengembalikan hasil laporan skor ke manager utama. |
| **94** | *(Baris Kosong)* | Pemisah visual antarkelas. |
| **95** | `class MiniGameManager:` | Deklarasi kelas `MiniGameManager` sebagai jembatan daur hidup pemanggilan minigame. |
| **96** | `    def __init__(self, eng):` | Konstruktor menerima objek proxy engine utama game (`eng`). |
| **97** | `        self.main_engine, self.active_game, self.saved_main_state = eng, None, None` | Menyimpan referensi engine utama, objek minigame aktif (`None`), dan backup status dunia utama (`None`). |
| **98** | `    def start_minigame(self, cls): self.active_game = cls(self.main_engine.screen, self.main_engine.clock, self)` | Memulai minigame baru dengan menginstansiasi kelas minigame yang diminta (`cls`). |
| **99** | `    def return_to_main(self, res):` | Keluar dari minigame dan mengembalikan kontrol ke dunia Sanctuary utama. |
| **100** | `        self.active_game, self.last_result = None, res` | Menghapus instansi minigame aktif dan menyimpan laporan hasil akhirnya. |
| **101** | `        if res: ...` | Memberikan bonus uang koin perunggu ke saldo pemain dan mengakumulasikan skor minigame ke total `point_kill` pada engine proxy. |
| **102** | `    def update(self, dt):` | Memperbarui logika minigame aktif di setiap frame. |
| **103** | `        if self.active_game: self.active_game.update(dt)` | Jika sedang bermain minigame, panggil metode `.update()` minigame tersebut. |
| **104** | `    def draw(self):` | Menggambar visual minigame aktif ke layar. |
| **105** | `        if self.active_game: self.active_game.draw()` | Jika sedang bermain minigame, panggil metode `.draw()` minigame tersebut. |
| **106** | `    @property` | Mendeklarasikan properti getter untuk mengecek status permainan. |
| **107** | `    def in_minigame(self): return self.active_game is not None` | Mengembalikan status `True` jika pemain sedang berada di dalam minigame. |
| **108** | *(Baris Kosong)* | Akhir dari berkas kode sumber. |
