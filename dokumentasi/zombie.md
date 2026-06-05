# Penjelasan Source Code: `zombie.py`

Dokumen ini berisi penjelasan detail baris demi baris dari berkas `zombie.py` dalam bahasa Indonesia untuk membantu persiapan demo program.

---

## Deskripsi & Tujuan File
Berkas `zombie.py` mendefinisikan kelas `ZombieNPC` yang merepresentasikan musuh berupa Zombie di dalam permainan. Kelas ini menangani inisialisasi status zombie, pergerakan mengejar pemain (jika pemain berlari), respon terhadap objek taktis (seperti terpikat oleh umpan *Decoy* atau terbakar oleh *Molotov*), siklus animasi sprite, serta penggambaran (*rendering*) karakter zombie ke layar dengan dukungan koordinat kamera.

---

## Daftar Import
Berikut adalah modul dan pustaka yang diimpor pada berkas ini beserta kegunaannya:
*   `pygame`: Pustaka utama yang digunakan untuk penanganan grafis, *rendering* permukaan (*surface*), dan penggambaran sprite ke layar.
*   `math`: Pustaka bawaan Python untuk operasi matematika. Di sini digunakan fungsi `math.hypot` untuk menghitung jarak Euclidean (jarak garis lurus) antar objek.
*   `from src.core.spritesheet import Spritesheet`: Mengimpor kelas kustom `Spritesheet` dari paket `src.core.spritesheet` untuk mempermudah proses pemotongan dan manajemen animasi berbasis grid dari lembaran gambar (*spritesheet*).

---

## Penjelasan Baris Demi Baris

| Baris | Kode | Penjelasan |
|---|---|---|
| **1** | `import pygame` | Mengimpor pustaka Pygame untuk keperluan grafis dan rendering gambar zombie. |
| **2** | `import math` | Mengimpor modul matematika standar Python untuk menghitung jarak Euclidean (menggunakan `math.hypot`). |
| **3** | `from src.core.spritesheet import Spritesheet` | Mengimpor kelas `Spritesheet` dari paket `src.core.spritesheet` untuk memotong dan mengelola animasi karakter zombie dari berkas gambar spritesheet. |
| **4** | *(Baris Kosong)* | Pemisah visual antar baris kode. |
| **5** | `class ZombieNPC:` | Mendefinisikan kelas `ZombieNPC` yang merepresentasikan musuh Zombie di dalam permainan. |
| **6** | `    def __init__(self, x, y):` | Konstruktor kelas untuk menginisialisasi objek Zombie baru pada koordinat `(x, y)`. |
| **7** | `        self.pos = [x, y]` | Menyimpan koordinat posisi Zombie dalam bentuk list `[x, y]` agar nilainya dapat diperbarui saat bergerak. |
| **8** | `        self.sheet = Spritesheet("assets/enemies/zombie_new.png", 8, 8, scale=2.0)` | Membuat objek `Spritesheet` dari berkas gambar `"assets/enemies/zombie_new.png"` dengan ukuran grid frame 8x8 dan perbesaran gambar 2.0 kali. |
| **9** | `        self.direction = 'down'` | Menyimpan arah hadap Zombie, secara *default* diset menghadap ke bawah (`'down'`). |
| **10** | `        self.state = 'stand'` | Menyimpan status/state perilaku Zombie, secara *default* diset berdiri diam (`'stand'`). |
| **11** | `        self.current_col = 0` | Menyimpan indeks kolom frame animasi saat ini untuk mengambil frame yang tepat dari spritesheet. |
| **12** | `        self.frame_timer = 0` | Penghitung waktu (timer) untuk mengontrol kapan frame animasi berikutnya harus berganti. |
| **13** | `        self.anim_speed = 10` | Batas nilai timer animasi (kecepatan animasi). Semakin kecil nilainya, semakin cepat pergantian frame. |
| **14** | `        self.speed = 2.5` | Kecepatan gerak/perpindahan Zombie. |
| **15** | `        self.stun_timer = 0` | Timer efek *stun* (pusing/lumpuh). Jika nilainya di atas 0, zombie tidak dapat bertindak. |
| **16** | `        self.health = 100` | Nilai kesehatan (darah) awal milik Zombie. |
| **17** | *(Baris Kosong)* | Pemisah visual antar bagian kode. |
| **18** | `    def update(self, player_pos, player_state, tactical_items=[]):` | Method untuk memperbarui logika zombie setiap frame. Menerima posisi pemain, state pemain saat ini, dan daftar item taktis yang aktif. |
| **19** | `        if self.stun_timer > 0:` | Mengecek apakah Zombie sedang terkena efek *stun* (`stun_timer > 0`). |
| **20** | `            self.stun_timer -= 1` | Mengurangi nilai timer *stun* sebanyak 1 pada setiap frame. |
| **21** | `            self.state = 'stand'` | Mengubah state perilaku Zombie menjadi berdiri diam (`'stand'`). |
| **22** | `            return` | Keluar dari method `update` lebih awal agar Zombie tidak melakukan pergerakan atau mendeteksi item lain saat lumpuh. |
| **23** | *(Baris Kosong)* | Pemisah visual antar blok logika. |
| **24** | `        # Prioritas: Cek apakah ada Decoy aktif` | Komentar penjelas bahwa umpan *Decoy* memiliki prioritas target yang paling utama. |
| **25** | `        target_pos = player_pos` | Menentukan target awal pergerakan zombie ke arah koordinat pemain. |
| **26** | `        is_aggressive = (player_state == 'run')` | Zombie secara default menjadi agresif (mengejar target) hanya jika pemain berlari (`'run'`). |
| **27** | *(Baris Kosong)* | Pemisah visual. |
| **28** | `        for item in tactical_items:` | Melakukan iterasi untuk setiap item taktis yang ada di arena permainan. |
| **29** | `            if item.item_type == "Decoy" and item.active and item.reached_target:` | Memeriksa apakah item tersebut merupakan "Decoy" (umpan), sedang aktif, dan sudah mendarat di posisi targetnya. |
| **30** | `                dx = item.pos[0] - self.pos[0]` | Menghitung selisih koordinat X antara Decoy dengan Zombie. |
| **31** | `                dy = item.pos[1] - self.pos[1]` | Menghitung selisih koordinat Y antara Decoy dengan Zombie. |
| **32** | `                if math.hypot(dx, dy) < 400: # Radius dengar decoy` | Menghitung jarak langsung (hipotenusa) ke Decoy dan memeriksa apakah berada dalam radius dengar zombie (400 unit). |
| **33** | `                    target_pos = item.pos` | Jika terdengar, target pergerakan zombie dialihkan ke posisi Decoy. |
| **34** | `                    is_aggressive = True` | Mengubah status menjadi agresif (`True`) agar zombie bergerak menghampiri Decoy tersebut. |
| **35** | `                    break` | Menghentikan perulangan karena target prioritas (Decoy terdekat yang terdengar) sudah ditemukan. |
| **36** | *(Baris Kosong)* | Pemisah visual antar blok logika. |
| **37** | `        # Cek apakah terkena api Molotov` | Komentar penjelas untuk bagian pendeteksian kerusakan akibat Molotov. |
| **38** | `        for item in tactical_items:` | Melakukan iterasi kembali pada daftar item taktis untuk mengecek interaksi dengan Molotov. |
| **39** | `            if item.item_type == "Molotov" and item.reached_target and item.active:` | Memeriksa jika ada item "Molotov" yang telah mendarat di target dan apinya masih aktif membakar area. |
| **40** | `                dx = item.pos[0] - self.pos[0]` | Menghitung selisih koordinat X antara Molotov dengan Zombie. |
| **41** | `                dy = item.pos[1] - self.pos[1]` | Menghitung selisih koordinat Y antara Molotov dengan Zombie. |
| **42** | `                if math.hypot(dx, dy) < 50:` | Menghitung jarak langsung dan mengecek jika zombie berdiri di dalam radius api Molotov (50 unit). |
| **43** | `                    self.health -= 2 # Terbakar!` | Mengurangi kesehatan (*health*) zombie sebanyak 2 poin per frame karena terbakar api. |
| **44** | `                    self.stun_timer = 20 # Panik kena api` | Memicu efek *stun* selama 20 frame agar zombie panik dan berhenti bergerak sementara saat terbakar. |
| **45** | *(Baris Kosong)* | Pemisah visual antar blok logika. |
| **46** | `        if is_aggressive and self.health > 0:` | Mengecek apakah zombie dalam status agresif mengejar target dan masih hidup (kesehatan > 0). |
| **47** | `            dx = target_pos[0] - self.pos[0]` | Menghitung selisih jarak horizontal (X) dari zombie ke posisi target. |
| **48** | `            dy = target_pos[1] - self.pos[1]` | Menghitung selisih jarak vertikal (Y) dari zombie ke posisi target. |
| **49** | `            dist = math.hypot(dx, dy)` | Menghitung jarak total garis lurus (Euclidean distance) antara zombie dan target. |
| **50** | *(Baris Kosong)* | Pemisah visual. |
| **51** | `            if dist > 10:` | Memeriksa jika jarak ke target masih lebih besar dari 10 unit (belum terlalu dekat/menempel). |
| **52** | `                self.pos[0] += (dx / dist) * self.speed` | Menggerakkan posisi X zombie mendekati target secara proporsional menggunakan kecepatan zombie. |
| **53** | `                self.pos[1] += (dy / dist) * self.speed` | Menggerakkan posisi Y zombie mendekati target secara proporsional menggunakan kecepatan zombie. |
| **54** | `                self.state = 'walk'` | Mengubah state zombie menjadi berjalan (`'walk'`). |
| **55** | `                if abs(dx) > abs(dy): self.direction = 'right' if dx > 0 else 'left'` | Jika jarak horizontal lebih dominan, arahkan hadap ke kanan (`'right'`) jika arah pergeseran positif, atau ke kiri (`'left'`). |
| **56** | `                else: self.direction = 'down' if dy > 0 else 'up'` | Jika jarak vertikal lebih dominan, arahkan hadap ke bawah (`'down'`) jika arah pergeseran positif, atau ke atas (`'up'`). |
| **57** | `            else:` | Jika jarak ke target sudah sangat dekat (kurang dari atau sama dengan 10 unit). |
| **58** | `                self.state = 'stand'` | Menghentikan gerakan zombie dan mengubah state menjadi berdiri diam (`'stand'`). |
| **59** | `        else:` | Jika zombie tidak dalam kondisi agresif (pemain tidak berlari/berisik dan tidak ada decoy) atau zombie telah mati. |
| **60** | `            self.state = 'stand'` | Mengubah state zombie menjadi berdiri diam (`'stand'`). |
| **61** | *(Baris Kosong)* | Pemisah visual. |
| **62** | `        # Animasi` | Komentar penjelas dimulainya proses pembaruan animasi visual zombie. |
| **63** | `        self.frame_timer += 1` | Menambah timer frame animasi sebanyak 1 setiap frame permainan diperbarui. |
| **64** | `        if self.frame_timer >= self.anim_speed:` | Mengecek apakah timer frame animasi sudah mencapai atau melewati batas kecepatan animasi. |
| **65** | `            self.frame_timer = 0` | Mereset timer frame kembali ke 0. |
| **66** | `            if self.state == 'stand': self.current_col = 0` | Jika zombie sedang berdiri diam, tetapkan kolom gambar spritesheet ke frame pertama (indeks 0). |
| **67** | `            else: self.current_col = (self.current_col + 1) % 6` | Jika zombie bergerak, geser kolom frame animasi ke berikutnya secara berulang (modulo 6 untuk siklus animasi jalan). |
| **68** | *(Baris Kosong)* | Pemisah visual. |
| **69** | `    def draw(self, screen, camera=None):` | Method untuk me-render visual zombie pada layar. Menerima parameter permukaan layar (`screen`) dan kamera opsional (`camera`). |
| **70** | `        dir_map = {'down': 0, 'up': 1, 'right': 2, 'left': 3}` | Pemetaan arah hadap zombie ke indeks baris dasar pada berkas spritesheet. |
| **71** | `        row = dir_map[self.direction] + (0 if self.state == 'stand' else 4)` | Menghitung baris spritesheet yang digunakan. Baris 0-3 untuk diam/berdiri, dan baris 4-7 untuk berjalan (ditambah offset 4). |
| **72** | *(Baris Kosong)* | Pemisah visual. |
| **73** | `        draw_pos = self.pos` | Menetapkan posisi gambar awal di koordinat dunia. |
| **74** | `        if camera:` | Memeriksa jika ada objek kamera yang digunakan dalam rendering permainan. |
| **75** | `            draw_pos = camera.apply(self.pos)` | Menyesuaikan posisi render relatif terhadap kamera (koordinat layar). |
| **76** | *(Baris Kosong)* | Pemisah visual. |
| **77** | `        screen.blit(self.sheet.get_frame(row, self.current_col), draw_pos)` | Menggambar potongan frame spritesheet yang sesuai ke layar pada posisi koordinat yang telah disesuaikan. |
| **78** | *(Baris Kosong)* | Akhir dari berkas program. |

---

## Alur Kerja Utama

1. **Inisialisasi (`__init__`)**: Objek zombie dibuat dengan posisi `(x, y)` tertentu. Spritesheet dimuat dengan skala 2 kali lipat dari aset aslinya. Default arah awal diatur ke `'down'` (bawah) dan status berdiri diam (`'stand'`).
2. **Pengecekan Stun**: Pada fungsi `update`, program terlebih dahulu mengecek `stun_timer`. Jika zombie ter-stun (misalnya akibat terkena api Molotov), timer akan dikurangi, status diubah menjadi berdiri diam, dan proses update langsung selesai (zombie membeku).
3. **Prioritas Umpan (Decoy)**: Jika tidak sedang ter-stun, zombie akan memindai apakah ada item taktis bertipe `"Decoy"` yang aktif dan sudah mendarat. Jika jarak zombie ke Decoy kurang dari 400 piksel, zombie akan mengalihkan fokus targetnya ke Decoy dan berpindah status ke agresif.
4. **Efek Kerusakan Api (Molotov)**: Zombie mengecek apakah ada item taktis `"Molotov"` aktif di dekatnya (radius kurang dari 50 piksel). Jika ada, darah zombie berkurang sebesar 2 poin dan ia akan ter-stun selama 20 frame karena panik terbakar.
5. **Pergerakan ke Target**:
    * Jika zombie berada dalam status agresif (karena pemain berlari atau terpicu Decoy) dan masih hidup: Zombie bergerak mendekati koordinat target.
    * Sistem menghitung arah hadap zombie berdasarkan komponen jarak `dx` dan `dy` terbesar.
    * Jika jarak sudah dekat ($\le 10$ piksel), zombie berhenti bergerak dan status diatur kembali menjadi `'stand'`.
6. **Pengendalian Animasi**: Timer bertambah terus-menerus. Saat batas `anim_speed` terlampaui, indeks frame kolom (`current_col`) digeser untuk membuat efek gerakan (berjalan) atau dikembalikan ke 0 jika zombie diam.
7. **Rendering Visual (`draw`)**: Menggunakan peta arah hadap (`dir_map`) untuk memilih baris spritesheet yang tepat (ditambah baris offset jika berjalan). Jika ada kamera yang aktif, koordinat dunia zombie dikonversi terlebih dahulu ke koordinat layar sebelum digambar menggunakan `screen.blit`.
