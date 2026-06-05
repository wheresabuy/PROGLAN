# Penjelasan Source Code: `npc.py`

Dokumen ini berisi penjelasan lengkap baris demi baris dalam bahasa Indonesian mengenai kode sumber `src/entities/npc.py` untuk membantu persiapan demo program.

---

## Deskripsi & Tujuan File
File `npc.py` mendefinisikan kelas `NPC` (Non-Player Character) di dalam game. Kelas ini bertanggung jawab atas:
1. **Representasi Visual**: Memuat dan mengelola spritesheet tubuh dasar karakter, rambut, dan pakaian secara terpisah (layering/pelapisan).
2. **Kecerdasan Buatan (AI) Pergerakan Sederhana**: Membuat NPC berkeliling (*wandering*) secara acak di sekitar posisi spawn awal dengan batas radius tertentu agar tidak berjalan terlalu jauh.
3. **Pengelolaan Animasi**: Mengatur transisi animasi (berdiri dan berjalan) berdasarkan arah gerakan dan status pergerakan NPC.
4. **Rendering**: Menggambar NPC ke layar, yang posisinya dapat disesuaikan dengan kamera game.

---

## Daftar Import

Berikut adalah penjelasan pustaka (*library*) yang diimpor pada awal file:

*   **`import pygame`**: Pustaka utama untuk pembuatan game 2D di Python. Digunakan untuk merender (*blit*) sprite ke layar.
*   **`import random`**: Modul bawaan Python untuk menghasilkan nilai acak. Digunakan untuk menentukan arah jalan acak dan durasi waktu tunggu NPC secara dinamis.
*   **`import math`**: Modul matematika bawaan Python. Digunakan untuk menghitung vektor gerakan menggunakan fungsi trigonometri (`sin` dan `cos`) serta menghitung jarak geometris dengan `math.hypot`.
*   **`from src.core.spritesheet import Spritesheet`**: Kelas kustom dari proyek game ini yang mempermudah pemotongan frame individu dari file gambar spritesheet.

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel penjelasan detail untuk setiap baris kode di `npc.py`:

| Baris | Kode Sumber | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import pygame` | Mengimpor pustaka Pygame untuk keperluan grafis dan rendering game. |
| **2** | `import random` | Mengimpor modul random untuk menentukan arah jalan dan waktu tunggu acak. |
| **3** | `import math` | Mengimpor modul matematika untuk perhitungan jarak dan trigonometri (sudut gerakan). |
| **4** | `from src.core.spritesheet import Spritesheet` | Mengimpor kelas `Spritesheet` untuk membagi-bagi gambar sheet menjadi frame animasi. |
| **5** | *(Baris Kosong)* | Pemisah visual kode program. |
| **6** | `class NPC:` | Deklarasi kelas `NPC` untuk membuat objek Non-Player Character. |
| **7** | `    def __init__(self, name, x, y, role, base_path, outfit_path=None, hair_path=None):` | Konstruktor kelas `NPC` yang menerima parameter nama, posisi awal (x, y), peran/role, dan path untuk gambar spritesheet (dasar, pakaian, dan rambut). |
| **8** | `        self.name = name` | Menyimpan nama NPC ke variabel instansi `self.name`. |
| **9** | `        self.pos = [x, y]` | Menyimpan posisi koordinat saat ini `[x, y]` dalam bentuk list agar nilainya dapat diubah-ubah. |
| **10** | `        self.role = role` | Menyimpan peran/pekerjaan NPC ke atribut `self.role`. |
| **11** | *(Baris Kosong)* | Pemisah visual kode program. |
| **12** | `        # Load sheets` | Komentar penjelas proses pemuatan spritesheet karakter. |
| **13** | `        self.sheet = Spritesheet(base_path, 8, 8, scale=2.0)` | Membuat objek Spritesheet utama untuk tubuh dasar karakter dengan skala perbesaran 2.0 kali. Grid spritesheet berupa 8 baris dan 8 kolom. |
| **14** | `        self.outfit_sheet = Spritesheet(outfit_path, 8, 8, scale=2.0) if outfit_path else None` | Membuat objek Spritesheet pakaian jika parameter `outfit_path` diberikan, jika tidak diatur sebagai `None`. |
| **15** | `        self.hair_sheet = Spritesheet(hair_path, 8, 8, scale=2.0) if hair_path else None` | Membuat objek Spritesheet rambut jika parameter `hair_path` diberikan, jika tidak diatur sebagai `None`. |
| **16** | *(Baris Kosong)* | Pemisah visual kode program. |
| **17** | `        self.direction = 'down'` | Arah default hadap NPC di awal, yaitu menghadap ke bawah (`'down'`). |
| **18** | `        self.state = 'stand'` | Status awal pergerakan NPC diatur sebagai diam (`'stand'`). |
| **19** | `        self.current_col = 0` | Indeks kolom frame animasi saat ini yang sedang aktif (dimulai dari indeks 0). |
| **20** | `        self.frame_timer = 0` | Penghitung waktu (timer) internal untuk mengendalikan kecepatan pembaruan frame animasi. |
| **21** | `        self.anim_speed = 8` | Kecepatan animasi, menandakan frame game diperbarui setiap 8 iterasi permainan untuk berpindah ke frame berikutnya. |
| **22** | *(Baris Kosong)* | Pemisah visual kode program. |
| **23** | `        # Movement/Wandering AI variables` | Komentar penjelas untuk bagian inisialisasi variabel kecerdasan buatan (AI) pergerakan acak. |
| **24** | `        self.wander_timer = random.randint(30, 90)` | Waktu jeda acak dalam jumlah frame (30 hingga 90) sebelum NPC memutuskan tindakan/arah jalan baru. |
| **25** | `        self.target_dir = [0, 0]` | Menyimpan vektor arah gerakan saat ini `[dx, dy]`, awalnya bernilai `[0, 0]` (diam). |
| **26** | `        self.speed = 1.0` | Nilai kecepatan berjalan NPC (1.0 piksel per pembaruan frame). |
| **27** | *(Baris Kosong)* | Pemisah visual kode program. |
| **28** | `        # Spawn anchor (for keeping them in a certain area)` | Komentar penjelas mengenai penggunaan penahan/jangkar lokasi kemunculan. |
| **29** | `        self.spawn_pos = [x, y]` | Menyimpan posisi awal spawn `[x, y]` sebagai jangkar agar NPC tidak pergi terlalu jauh dari area asalnya. |
| **30** | `        self.max_wander_dist = 100 # Radius they can wander around their spawn anchor` | Batas jarak radius maksimal berkeliling (wander) NPC sebesar 100 piksel dari titik spawn awal. |
| **31** | *(Baris Kosong)* | Pemisah visual kode program. |
| **32** | `    def update(self, map_size=None):` | Mendefinisikan method `update` untuk memperbarui kecerdasan buatan, pergerakan, dan animasi frame NPC. |
| **33** | `        # AI Logic: Wandering around spawn anchor` | Komentar penjelas bahwa bagian di bawah memproses logika pergerakan AI. |
| **34** | `        self.wander_timer -= 1` | Mengurangi timer pergerakan acak (`self.wander_timer`) sebesar 1 pada setiap frame pembaruan. |
| **35** | `        if self.wander_timer <= 0:` | Memeriksa apakah timer pergerakan acak telah habis (bernilai $\le 0$). |
| **36** | `            self.wander_timer = random.randint(60, 180)` | Jika habis, atur ulang timer dengan durasi acak baru yang lebih lama (antara 60 hingga 180 frame). |
| **37** | `            if random.random() < 0.5:` | Memiliki peluang acak 50% untuk menentukan apakah NPC akan diam atau berjalan. |
| **38** | `                # Stand still` | Komentar penjelas kondisi jika NPC memutuskan untuk diam berdiri. |
| **39** | `                self.state = 'stand'` | Mengatur status pergerakan NPC menjadi diam (`'stand'`). |
| **40** | `                self.target_dir = [0, 0]` | Menghentikan pergerakan dengan mengeset vektor arah target menjadi `[0, 0]`. |
| **41** | `            else:` | Blok alternatif jika peluang acak 50% memutuskan NPC untuk berjalan. |
| **42** | `                # Pick a random direction` | Komentar penjelas bahwa NPC akan memilih arah acak untuk berjalan. |
| **43** | `                angle = random.uniform(0, 2 * math.pi)` | Memilih sudut pergerakan acak dalam radian (dari $0$ hingga $2\pi$ atau 360 derajat). |
| **44** | `                self.target_dir = [math.cos(angle), math.sin(angle)]` | Menghitung vektor arah pergerakan `[dx, dy]` dari sudut radian acak menggunakan fungsi trigonometri cosinus dan sinus. |
| **45** | `                self.state = 'walk'` | Mengubah status pergerakan NPC menjadi berjalan (`'walk'`). |
| **46** | `                ` | Baris kosong. |
| **47** | `                # Determine animation direction facing` | Komentar penjelas penentuan arah hadap animasi karakter berdasarkan arah berjalan. |
| **48** | `                dx, dy = self.target_dir` | Memecah vektor arah target menjadi variabel horizontal `dx` dan vertikal `dy`. |
| **49** | `                if abs(dx) > abs(dy):` | Memeriksa apakah gerakan horizontal (ke kiri/kanan) lebih dominan dibandingkan gerakan vertikal (ke atas/bawah). |
| **50** | `                    self.direction = 'right' if dx > 0 else 'left'` | Jika gerakan horizontal dominan, hadapkan NPC ke `'right'` jika `dx` bernilai positif, atau `'left'` jika negatif. |
| **51** | `                else:` | Kondisi jika gerakan vertikal lebih dominan atau sama besar dengan gerakan horizontal. |
| **52** | `                    self.direction = 'down' if dy > 0 else 'up'` | Hadapkan NPC ke `'down'` jika `dy` bernilai positif, atau `'up'` jika negatif. |
| **53** | *(Baris Kosong)* | Pemisah visual kode program. |
| **54** | `        # Apply movement` | Komentar penjelas bagian mengaplikasikan perpindahan posisi karakter. |
| **55** | `        if self.state == 'walk':` | Mengevaluasi jika status NPC sedang berjalan (`'walk'`). |
| **56** | `            # Calculate next position` | Komentar penjelas kalkulasi posisi berikutnya yang akan dituju. |
| **57** | `            next_x = self.pos[0] + self.target_dir[0] * self.speed` | Menghitung perkiraan posisi X berikutnya berdasarkan posisi X saat ini ditambah perkalian arah target X dengan kecepatan. |
| **58** | `            next_y = self.pos[1] + self.target_dir[1] * self.speed` | Menghitung perkiraan posisi Y berikutnya berdasarkan posisi Y saat ini ditambah perkalian arah target Y dengan kecepatan. |
| **59** | `            ` | Baris kosong. |
| **60** | `            # Check anchor distance to stay within boundaries` | Komentar penjelas pengecekan jarak ke jangkar agar tetap di dalam batas radius maksimal. |
| **61** | `            dist_to_anchor = math.hypot(next_x - self.spawn_pos[0], next_y - self.spawn_pos[1])` | Menghitung jarak Euclid dari perkiraan posisi berikutnya ke titik awal spawn NPC menggunakan rumus Pythagoras (`math.hypot`). |
| **62** | `            if dist_to_anchor < self.max_wander_dist:` | Memeriksa apakah jarak perkiraan baru tersebut masih berada di bawah batas jarak radius berkeliling maksimal. |
| **63** | `                self.pos[0] = next_x` | Jika ya, maka posisi X baru yang aman diaplikasikan ke posisi NPC. |
| **64** | `                self.pos[1] = next_y` | Mengaplikasikan posisi Y baru ke posisi NPC. |
| **65** | `            else:` | Kondisi jika posisi baru melampaui batas radius dari jangkar spawn. |
| **66** | `                # Turn back / stand still if too far` | Komentar penjelas tindakan berbalik arah atau diam karena sudah terlalu jauh dari batas. |
| **67** | `                self.state = 'stand'` | Mengubah status NPC menjadi diam berdiri (`'stand'`). |
| **68** | `                self.target_dir = [0, 0]` | Mereset vektor arah target menjadi `[0, 0]`. |
| **69** | `                self.wander_timer = 15` | Memotong sisa waktu tunggu menjadi 15 frame agar NPC lebih cepat menentukan keputusan arah gerakan baru yang sah kembali ke dalam area. |
| **70** | *(Baris Kosong)* | Pemisah visual kode program. |
| **71** | `        # Clamp position to map size if provided` | Komentar penjelas proses membatasi posisi koordinat NPC agar tidak melewati batas dimensi peta game. |
| **72** | `        if map_size:` | Memeriksa apakah variabel batas ukuran peta `map_size` dikirimkan ke fungsi update. |
| **73** | `            self.pos[0] = max(0, min(self.pos[0], map_size[0] - 32))` | Menggunakan fungsi `min` dan `max` untuk menahan koordinat X agar tetap di rentang 0 hingga lebar peta dikurangi 32 piksel (dimensi lebar sprite NPC). |
| **74** | `            self.pos[1] = max(0, min(self.pos[1], map_size[1] - 32))` | Menahan koordinat Y agar tetap di rentang 0 hingga tinggi peta dikurangi 32 piksel (dimensi tinggi sprite NPC). |
| **75** | *(Baris Kosong)* | Pemisah visual kode program. |
| **76** | `        # Update Frame Animation (using same logic as player)` | Komentar penjelas bahwa pembaruan frame animasi menggunakan logika yang sama dengan animasi milik pemain. |
| **77** | `        self.frame_timer += 1` | Menambahkan nilai timer frame animasi sebesar 1 pada setiap frame permainan. |
| **78** | `        if self.frame_timer >= self.anim_speed:` | Memeriksa apakah timer animasi sudah mencapai atau melampaui ambang kecepatan animasi (`self.anim_speed`). |
| **79** | `            self.frame_timer = 0` | Mengembalikan timer frame animasi ke 0 untuk siklus pergantian frame berikutnya. |
| **80** | `            if self.state == 'stand':` | Jika NPC sedang diam berdiri (`'stand'`). |
| **81** | `                self.current_col = 0` | Atur indeks kolom frame animasi ke 0 (kolom pertama spritesheet untuk pose diam). |
| **82** | `            elif self.state == 'walk':` | Jika NPC sedang berjalan (`'walk'`). |
| **83** | `                self.current_col = (self.current_col + 1) % 6` | Mengiterasi indeks kolom ke kolom berikutnya secara berulang (dari kolom 0 hingga 5) menggunakan operasi modulo `% 6` (karena gerakan jalan terdiri dari 6 kolom sprite). |
| **84** | *(Baris Kosong)* | Pemisah visual kode program. |
| **85** | `    def draw(self, screen, camera=None):` | Mendefinisikan method `draw` untuk menggambar sprite NPC ke layar game, opsional menyesuaikan posisi relatif terhadap objek `camera`. |
| **86** | `        dir_map = {'down': 0, 'up': 1, 'right': 2, 'left': 3}` | Kamus pemetaan arah hadap berbasis string ke nilai baris spritesheet (arah bawah di baris ke-0, atas ke-1, kanan ke-2, kiri ke-3). |
| **87** | `        row = dir_map[self.direction] + (0 if self.state == 'stand' else 4)` | Menentukan indeks baris spritesheet yang akan dibaca. Baris dasar adalah 0-3 jika sedang diam. Jika sedang berjalan, tambahkan offset 4 baris sehingga menggunakan baris ke 4-7. |
| **88** | *(Baris Kosong)* | Pemisah visual kode program. |
| **89** | `        draw_pos = self.pos` | Mengatur koordinat gambar default sesuai dengan posisi koordinat aktual dari NPC. |
| **90** | `        if camera:` | Memeriksa apakah objek kamera dilewatkan pada fungsi ini. |
| **91** | `            draw_pos = camera.apply(self.pos)` | Jika ya, ubah posisi gambar ke koordinat viewport layar berdasarkan kalkulasi kamera. |
| **92** | `            ` | Baris kosong. |
| **93** | `        # Draw base character` | Komentar penjelas penggambaran base body (tubuh dasar) karakter NPC. |
| **94** | `        screen.blit(self.sheet.get_frame(row, self.current_col), draw_pos)` | Mengambil frame sprite tubuh dasar yang sesuai menggunakan `get_frame` dan menggambarnya (*blit*) ke permukaan layar pada koordinat `draw_pos`. |
| **95** | `        ` | Baris kosong. |
| **96** | `        # Draw outfit` | Komentar penjelas penggambaran pakaian karakter NPC. |
| **97** | `        if self.outfit_sheet:` | Memeriksa apakah NPC dilengkapi dengan spritesheet pakaian. |
| **98** | `            screen.blit(self.outfit_sheet.get_frame(row, self.current_col), draw_pos)` | Jika ya, gambar layer pakaian tepat di atas tubuh dasar NPC pada posisi koordinat yang sama. |
| **99** | `            ` | Baris kosong. |
| **100** | `        # Draw hair` | Komentar penjelas penggambaran rambut karakter NPC. |
| **101** | `        if self.hair_sheet:` | Memeriksa apakah NPC dilengkapi dengan spritesheet rambut. |
| **102** | `            screen.blit(self.hair_sheet.get_frame(row, self.current_col), draw_pos)` | Jika ya, gambar layer rambut tepat di atas tubuh dan pakaian NPC pada posisi koordinat yang sama. |
| **103** | *(Baris Kosong)* | Baris kosong penutup akhir file. |
