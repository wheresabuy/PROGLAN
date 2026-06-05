# Penjelasan Source Code: `player.py`

## Deskripsi & Tujuan File
File `player.py` mendefinisikan kelas `Player` yang mewakili karakter utama yang dikendalikan oleh pemain di dalam game. Kelas ini bertanggung jawab untuk:
- Menyimpan status data pemain (posisi, arah hadap, kondisi kesehatan, efek status seperti adrenalin, dan animasi).
- Memuat aset gambar berupa beberapa lapisan (layer) sprite sheet (kulit dasar, pakaian, rambut, dan topi) menggunakan kelas `Spritesheet`.
- Memperbarui pergerakan dan status animasi karakter berdasarkan input keyboard (panah untuk bergerak, Shift kiri untuk berlari).
- Membatasi pergerakan pemain agar tidak melewati batas peta.
- Menggambar karakter lapis demi lapis ke layar dengan memperhitungkan posisi kamera (kamera viewport).

---

## Daftar Import
Berikut adalah daftar pustaka atau modul yang diimpor pada file ini:
* **`pygame`**: Pustaka utama yang digunakan untuk penanganan grafis game, penanganan input keyboard (misal mendeteksi tombol arah dan tombol Shift), serta utilitas game lainnya.
* **`src.core.spritesheet.Spritesheet`**: Kelas kustom yang digunakan untuk menginisialisasi, memotong, dan mengambil frame individual dari gambar sprite sheet bertingkat/berlapisan (layered spritesheet).

---

## Penjelasan Baris Demi Baris

| Baris | Kode | Penjelasan |
| :--- | :--- | :--- |
| **1** | `import pygame` | Mengimpor pustaka Pygame untuk menangani grafik, input, dan game loop. |
| **2** | `from src.core.spritesheet import Spritesheet` | Mengimpor kelas `Spritesheet` untuk memotong dan mengelola animasi karakter dari sprite sheet. |
| **3** | *[Baris Kosong]* | Digunakan sebagai pemisah visual antar baris kode. |
| **4** | `class Player:` | Mendefinisikan kelas bernama `Player` yang mempresentasikan karakter pemain dalam game. |
| **5** | `    def __init__(self, x, y):` | Metode inisialisasi (konstruktor) kelas `Player` yang menerima parameter posisi awal `x` dan `y`. |
| **6** | `        self.pos = [x, y]` | Menyimpan koordinat posisi pemain saat ini dalam list dua elemen `[x, y]` untuk kemudahan modifikasi. |
| **7** | `        # Base skin` | Komentar penjelas bahwa bagian di bawahnya menginisialisasi gambar dasar kulit karakter. |
| **8** | `        self.sheet = Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/char_a_p1_0bas_humn_v00.png", 8, 8, scale=2.0)` | Membuat objek `Spritesheet` untuk kulit dasar karakter dengan resolusi sprite 8x8 dan perbesaran skala 2.0 kali lipat. |
| **9** | *[Baris Kosong]* | Pemisah visual. |
| **10** | `        # Clothing / Outfit` | Komentar penjelas untuk bagian inisialisasi pakaian karakter. |
| **11** | `        self.clothing_sheet = Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/1out/char_a_p1_1out_fstr_v01.png", 8, 8, scale=2.0)` | Membuat objek `Spritesheet` untuk pakaian karakter dengan skala perbesaran 2.0. |
| **12** | `        self.clothing_active = True # Start with default clothes active` | Variabel penanda apakah pakaian karakter sedang aktif (ditampilkan) atau tidak. Bernilai `True` secara default. |
| **13** | *[Baris Kosong]* | Pemisah visual. |
| **14** | `        # Hair (Default: Dapper Hair Brown/v08)` | Komentar penjelas untuk bagian rambut default karakter. |
| **15** | `        self.hair_sheet = Spritesheet("FREE Mana Seed Character Base Demo 2.0/char_a_p1/4har/char_a_p1_4har_dap1_v08.png", 8, 8, scale=2.0)` | Membuat objek `Spritesheet` untuk rambut karakter (menggunakan gaya "Dapper Hair Brown") dengan skala perbesaran 2.0. |
| **16** | *[Baris Kosong]* | Pemisah visual. |
| **17** | `        # Hat (Default: None)` | Komentar penjelas untuk inisialisasi topi karakter. |
| **18** | `        self.hat_sheet = None` | Mengeset topi bawaan karakter menjadi kosong (`None`), artinya karakter tidak memakai topi di awal game. |
| **19** | *[Baris Kosong]* | Pemisah visual. |
| **20** | `        self.direction = 'down'` | Mengatur arah hadap awal pemain ke arah bawah ('down'). Arah hadap menentukan baris sprite mana yang akan digambar. |
| **21** | `        self.state = 'stand'` | Mengatur status/kondisi gerak awal pemain yaitu berdiri/diam ('stand'). |
| **22** | `        self.current_col = 0` | Mengatur indeks kolom frame animasi aktif awal ke kolom 0. |
| **23** | `        self.frame_timer = 0` | Variabel penghitung waktu (timer) untuk mengontrol kapan frame animasi beralih ke kolom berikutnya. |
| **24** | `        self.anim_speed = 8` | Menentukan durasi frame aktif sebelum beralih ke frame berikutnya (semakin kecil, semakin cepat animasi berganti). |
| **25** | `        self.health = 100` | Menyimpan jumlah nyawa/darah (health) awal pemain, yaitu 100 poin. |
| **26** | `        self.injured = True` | Status boolean yang menandakan apakah pemain dalam kondisi cedera/terluka. |
| **27** | `        self.speed_multiplier = 0.4` | Pengali kecepatan bawaan untuk memperlambat gerakan dasar agar lebih realistis. |
| **28** | `        self.adrenaline_timer = 0` | Menyimpan timer sisa efek peningkatan kecepatan (adrenalin). Dimulai dari 0 (tidak aktif). |
| **29** | *[Baris Kosong]* | Pemisah visual. |
| **30** | `    def update(self, keys, collision_mask=None, map_size=None):` | Mendefinisikan fungsi `update` untuk memproses input tombol, menghitung posisi baru pemain, dan mengelola state animasi setiap frame. |
| **31** | `        adrenaline_bonus = 2.0 if self.adrenaline_timer > 0 else 1.0` | Menghitung bonus kecepatan berdasarkan adrenalin. Jika timer adrenalin aktif (> 0), pemain bergerak 2 kali lebih cepat, jika tidak bonus bernilai 1.0. |
| **32** | `        if self.adrenaline_timer > 0: self.adrenaline_timer -= 1` | Jika timer adrenalin aktif, kurangi nilai timer tersebut sebanyak 1 frame (berfungsi sebagai hitung mundur). |
| **33** | *[Baris Kosong]* | Pemisah visual. |
| **34** | `        base_speed = (5.0 if keys[pygame.K_LSHIFT] else 3.0) * adrenaline_bonus` | Menghitung kecepatan dasar. Pemain mendapat kecepatan 5.0 jika menahan Shift Kiri (berlari), dan 3.0 jika berjalan biasa. Kecepatan ini lalu dikalikan dengan `adrenaline_bonus`. |
| **35** | `        speed = float(base_speed * self.speed_multiplier)` | Menghitung nilai akhir kecepatan dengan mengalikan `base_speed` dan `speed_multiplier` lalu dikonversi ke tipe bilangan riil (`float`). |
| **36** | `        moving = False` | Menandai variabel `moving` dengan nilai `False` di setiap frame untuk mendeteksi apakah tombol pergerakan ditekan. |
| **37** | *[Baris Kosong]* | Pemisah visual. |
| **38** | `        if keys[pygame.K_RIGHT]: self.pos[0] += speed; self.direction = 'right'; moving = True` | Jika tombol panah kanan ditekan: geser posisi X pemain ke kanan sebesar `speed`, set arah ke `'right'`, dan ubah status `moving` menjadi `True`. |
| **39** | `        if keys[pygame.K_LEFT]:  self.pos[0] -= speed; self.direction = 'left'; moving = True` | Jika tombol panah kiri ditekan: geser posisi X pemain ke kiri sebesar `speed`, set arah ke `'left'`, dan ubah status `moving` menjadi `True`. |
| **40** | `        if keys[pygame.K_UP]:    self.pos[1] -= speed; self.direction = 'up'; moving = True` | Jika tombol panah atas ditekan: geser posisi Y pemain ke atas sebesar `speed`, set arah ke `'up'`, dan ubah status `moving` menjadi `True`. |
| **41** | `        if keys[pygame.K_DOWN]:  self.pos[1] += speed; self.direction = 'down'; moving = True` | Jika tombol panah bawah ditekan: geser posisi Y pemain ke bawah sebesar `speed`, set arah ke `'down'`, dan ubah status `moving` menjadi `True`. |
| **42** | *[Baris Kosong]* | Pemisah visual. |
| **43** | `        # Clamp position to map size if provided` | Komentar penjelas untuk bagian pembatasan wilayah gerak pemain (bounding box). |
| **44** | `        if map_size:` | Memeriksa apakah parameter batas peta (`map_size`) diberikan. |
| **45** | `            self.pos[0] = max(0, min(self.pos[0], map_size[0] - 32))` | Membatasi koordinat X pemain agar tidak kurang dari 0 dan tidak melebihi lebar peta dikurangi 32 piksel (lebar sprite pemain). |
| **46** | `            self.pos[1] = max(0, min(self.pos[1], map_size[1] - 32))` | Membatasi koordinat Y pemain agar tidak kurang dari 0 dan tidak melebihi tinggi peta dikurangi 32 piksel (tinggi sprite pemain). |
| **47** | *[Baris Kosong]* | Pemisah visual. |
| **48** | `        if keys[pygame.K_LSHIFT] and moving: self.state = 'run'` | Mengubah status state pemain ke `'run'` jika tombol Shift kiri ditekan bersamaan dengan tombol arah bergerak. |
| **49** | `        elif moving: self.state = 'walk'` | Mengubah status state pemain ke `'walk'` jika pemain bergerak tanpa menekan tombol Shift kiri. |
| **50** | `        else: self.state = 'stand'` | Mengubah status state pemain ke `'stand'` jika pemain tidak menekan tombol arah gerak sama sekali (diam). |
| **51** | *[Baris Kosong]* | Pemisah visual. |
| **52** | `        self.frame_timer += 1` | Menambah durasi penghitung frame animasi pemain sebanyak 1 pada setiap siklus pembaruan. |
| **53** | `        if self.frame_timer >= self.anim_speed:` | Memeriksa apakah penghitung frame sudah melampaui batas kecepatan animasi yang ditentukan (`anim_speed`). |
| **54** | `            self.frame_timer = 0` | Mengatur ulang (reset) penghitung frame animasi ke 0 untuk memulai hitungan siklus baru. |
| **55** | `            if self.state == 'stand': self.current_col = 0` | Jika pemain sedang diam, kolom frame animasi dikunci pada indeks 0 (frame diam). |
| **56** | `            elif self.state == 'walk': self.current_col = (self.current_col + 1) % 6` | Jika berjalan, geser frame animasi ke kolom selanjutnya dengan rentang siklus 0 hingga 5 (total 6 frame berjalan). |
| **57** | `            elif self.state == 'run': self.current_col = 6 + (self.current_col + 1) % 2` | Jika berlari, lakukan siklus frame animasi pada rentang kolom 6 dan 7 (total 2 frame berlari). |
| **58** | *[Baris Kosong]* | Pemisah visual. |
| **59** | `    def draw(self, screen, camera=None):` | Mendefinisikan fungsi `draw` untuk merender/menggambar karakter beserta perlengkapannya ke layar monitor, mendukung parameter objek kamera. |
| **60** | `        dir_map = {'down': 0, 'up': 1, 'right': 2, 'left': 3}` | Kamus data untuk memetakan nama arah hadap menjadi indeks baris dasar pada sprite sheet. |
| **61** | `        row = dir_map[self.direction] + (0 if self.state == 'stand' else 4)` | Menghitung indeks baris yang tepat pada sprite sheet. Baris 0-3 untuk diam, sedangkan untuk kondisi berjalan/berlari ditambah 4 (menjadi baris 4-7). |
| **62** | *[Baris Kosong]* | Pemisah visual. |
| **63** | `        draw_pos = self.pos` | Mengatur posisi gambar default ke koordinat asli dunia (`self.pos`). |
| **64** | `        if camera:` | Memeriksa apakah parameter kamera disertakan. |
| **65** | `            draw_pos = camera.apply(self.pos)` | Mengonversi koordinat posisi asli dunia menjadi posisi di layar monitor yang disesuaikan dengan posisi lensa kamera. |
| **66** | *[Baris Kosong]* | Pemisah visual. |
| **67** | `        # Layer 1: Skin Base` | Komentar penjelas untuk proses penggambaran lapisan 1 (kulit dasar). |
| **68** | `        screen.blit(self.sheet.get_frame(row, self.current_col), draw_pos)` | Menggambar sprite kulit dasar ke layar pada koordinat target menggunakan fungsi `blit`. |
| **69** | *[Baris Kosong]* | Pemisah visual. |
| **70** | `        # Layer 2: Outfit / Clothing` | Komentar penjelas untuk proses penggambaran lapisan 2 (pakaian). |
| **71** | `        if self.clothing_active and self.clothing_sheet:` | Memeriksa apakah pakaian aktif dan objek sheet pakaian diisi. |
| **72** | `            screen.blit(self.clothing_sheet.get_frame(row, self.current_col), draw_pos)` | Menggambar sprite pakaian di atas kulit dasar menggunakan frame baris dan kolom yang sama agar sejajar sempurna. |
| **73** | *[Baris Kosong]* | Pemisah visual. |
| **74** | `        # Layer 3: Hair` | Komentar penjelas untuk proses penggambaran lapisan 3 (rambut). |
| **75** | `        if self.hair_sheet:` | Memeriksa apakah objek sheet rambut tersedia. |
| **76** | `            screen.blit(self.hair_sheet.get_frame(row, self.current_col), draw_pos)` | Menggambar sprite rambut di atas tumpukan sprite pakaian dan kulit dasar. |
| **77** | *[Baris Kosong]* | Pemisah visual. |
| **78** | `        # Layer 4: Hat` | Komentar penjelas untuk proses penggambaran lapisan 4 (topi). |
| **79** | `        if self.hat_sheet:` | Memeriksa apakah objek sheet topi tersedia (tidak bernilai `None`). |
| **80** | `            screen.blit(self.hat_sheet.get_frame(row, self.current_col), draw_pos)` | Menggambar sprite topi di atas tumpukan paling atas (di atas rambut). |
| **81** | *[Baris Kosong]* | Baris penutup file (baris kosong terakhir). |

---

## Alur Kerja Utama

1. **Inisialisasi (`__init__`)**:
   Saat objek `Player` dibuat, konstruktor memuat gambar aset sprite sheet untuk kulit dasar, pakaian, dan rambut. Status internal seperti posisi koordinat awal, status gerak (`stand`), arah hadap (`down`), nyawa, kecepatan, dan timer adrenalin juga diatur di sini.
   
2. **Pembaruan Logika (`update`)**:
   - Sistem memeriksa timer adrenalin dan menghitung multiplier kecepatan pemain.
   - Mengambil input tombol panah (`K_RIGHT`, `K_LEFT`, `K_UP`, `K_DOWN`) untuk mengubah posisi pemain (`self.pos`) dan memperbarui arah hadap (`self.direction`) ke kanan, kiri, atas, atau bawah.
   - Posisi dibatasi menggunakan batas lebar dan tinggi peta (`map_size`) agar pemain tidak keluar area permainan.
   - Menentukan status aksi (`self.state`): berlari (`run`) jika Shift kiri ditekan sambil berjalan, berjalan (`walk`), atau diam (`stand`).
   - Melakukan siklus pergantian kolom animasi (`self.current_col`) setelah melewati rentang durasi kecepatan animasi (`self.anim_speed`).

3. **Pemberian Tampilan Gambar (`draw`)**:
   - Menghitung koordinat rendering berdasarkan posisi kamera.
   - Memetakan arah hadap dan status gerak ke baris yang sesuai pada sprite sheet.
   - Menggambar sprite secara berlapis (layering) pada layar: dimulai dari kulit dasar (Layer 1), pakaian (Layer 2), rambut (Layer 3), dan terakhir topi (Layer 4) agar karakter terlihat lengkap secara visual dengan aksesoris bertumpuk yang selaras.
