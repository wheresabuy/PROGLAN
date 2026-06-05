# Penjelasan Source Code: visual_effects.py

Dokumen ini berisi penjelasan baris demi baris dari file `visual_effects.py` yang digunakan untuk mengatur efek visual di dalam game, seperti efek kegelapan, cahaya senter (flashlight), kilatan cahaya (screen flash), dan guncangan layar (screen shake).

---

## Deskripsi & Tujuan File
File `visual_effects.py` mendefinisikan kelas `VisualEffects`. Kelas ini mengelola rendering efek lingkungan gelap di sekitar pemain, menggambar cahaya gradasi melingkar dari lampu senter pemain, serta memproses efek dramatis seperti kilatan cahaya putih (misalnya saat terjadi ledakan atau sambaran petir) disertai dengan guncangan layar (screen shake) yang memudar.

---

## Daftar Import

| Modul | Deskripsi |
| :--- | :--- |
| `import pygame` | Library utama untuk pengembangan game yang digunakan untuk menggambar bentuk, memanipulasi Surface, dan mengelola warna. |
| `import random` | Digunakan untuk menghasilkan angka acak guna menghitung offset pergeseran layar saat terjadi efek guncangan. |
| `import math` | Digunakan untuk perhitungan matematika trigonometri (fungsi `sin`) untuk menghasilkan efek berdenyut (pulsing) pada warna layar saat pemain cedera. |

---

## Penjelasan Baris Demi Baris

| Baris | Kode Sumber | Penjelasan (Bahasa Indonesia) |
| :---: | :--- | :--- |
| **1** | `import pygame` | Mengimpor pustaka Pygame untuk keperluan grafis dan manajemen game. |
| **2** | `import random` | Mengimpor pustaka bawaan Python `random` untuk menghasilkan angka acak (dipakai pada screen shake). |
| **3** | `import math` | Mengimpor pustaka `math` untuk melakukan kalkulasi matematis seperti fungsi sinus. |
| **4** | *(Baris Kosong)* | Pemisah visual antar bagian kode. |
| **5** | `class VisualEffects:` | Mendefinisikan kelas utama `VisualEffects` untuk memproses seluruh efek visual dalam game. |
| **6** | `    def __init__(self, width, height):` | Konstruktor kelas yang menerima ukuran lebar (`width`) dan tinggi (`height`) dari layar game. |
| **7** | `        self.width = width` | Menyimpan lebar layar ke variabel objek `self.width`. |
| **8** | `        self.height = height` | Menyimpan tinggi layar ke variabel objek `self.height`. |
| **9** | `        self.darkness_surf = pygame.Surface((width, height), pygame.SRCALPHA)` | Membuat Surface baru untuk menampung efek kegelapan yang mendukung saluran transparansi (Alpha) menggunakan flag `pygame.SRCALPHA`. |
| **10** | `        self.flash_surf = pygame.Surface((width, height))` | Membuat Surface baru yang digunakan untuk efek kilatan layar (flash). |
| **11** | `        self.flash_surf.fill((255, 255, 255))` | Mewarnai seluruh Surface kilatan dengan warna putih bersih `(255, 255, 255)`. |
| **12** | `        self.flash_timer = 0` | Menginisialisasi timer kilatan layar ke angka 0 (tidak aktif). |
| **13** | `        self.flash_duration = 60` | Menetapkan durasi default efek kilatan cahaya sebanyak 60 frame. |
| **14** | `        self.shake_amount = 0` | Menginisialisasi intensitas guncangan layar ke angka 0 (tidak berguncang). |
| **15** | *(Baris Kosong)* | Pemisah visual. |
| **16** | `    def draw_darkness(self, screen, player_pos, camera, flashlight_on, battery_level, is_injured):` | Fungsi untuk menggambar efek kegelapan di sekitar pemain berdasarkan koordinat pemain, kamera, kondisi senter, baterai, dan status cedera. |
| **17** | `        dark_color = (15, 15, 25)` | Warna dasar kegelapan, yaitu warna biru malam yang sangat gelap `(15, 15, 25)`. |
| **18** | `        if is_injured:` | Memeriksa apakah pemain sedang dalam keadaan terluka (`is_injured` bernilai `True`). |
| **19** | `            # Pulse effect for injury` | Komentar penjelas bahwa bagian ini membuat efek berdenyut saat terluka. |
| **20** | `            pulse = int(abs(math.sin(pygame.time.get_ticks() * 0.003)) * 40)` | Menggunakan fungsi sinus (`math.sin`) terhadap waktu berjalan game dalam milidetik (`pygame.time.get_ticks()`) untuk menghasilkan nilai berosilasi naik-turun secara mulus antara 0 s.d 40. |
| **21** | `            dark_color = (25+pulse, 15, 15)` | Mengubah warna dasar kegelapan menjadi kemerahan yang berdenyut (menambahkan nilai `pulse` ke kanal Merah/Red) untuk menggambarkan kondisi kritis pemain. |
| **22** | *(Baris Kosong)* | Pemisah visual. |
| **23** | `        self.darkness_surf.fill((*dark_color, 255))` | Mengisi seluruh permukaan `darkness_surf` dengan warna kegelapan yang telah ditentukan beserta nilai alpha penuh (255 / solid). |
| **24** | `        if flashlight_on and battery_level > 0:` | Mengecek apakah lampu senter sedang dinyalakan dan baterai senter masih tersisa (lebih dari 0). |
| **25** | `            light_radius = 200` | Menetapkan radius lingkaran cahaya senter sebesar 200 piksel. |
| **26** | `            screen_pos = camera.apply(player_pos)` | Menerjemahkan koordinat dunia pemain (`player_pos`) ke koordinat layar menggunakan kamera. |
| **27** | `            # Center of the light on the player` | Komentar penjelas posisi pusat cahaya senter pada pemain. |
| **28** | `            cx, cy = int(screen_pos[0] + 32), int(screen_pos[1] + 32)` | Menghitung titik tengah koordinat pemain (ditambah offset 32 piksel ke kanan dan bawah, berasumsi ukuran sprite pemain adalah 64x64) sebagai pusat lingkaran cahaya. |
| **29** | *(Baris Kosong)* | Pemisah visual. |
| **30** | `            for r in range(light_radius, 0, -8):` | Melakukan iterasi dari jari-jari terbesar (200) mengecil ke 0 dengan decrement 8 piksel untuk menggambar lingkaran bertingkat. |
| **31** | `                # Calculate alpha based on radius for smooth gradient` | Komentar penjelas kalkulasi transparansi untuk menghasilkan gradasi yang halus. |
| **32** | `                alpha = max(0, min(255, int(255 * (1.0 - (r / light_radius)))))` | Menghitung tingkat transparansi (alpha) secara terbalik terhadap radius: semakin dekat ke pusat lingkaran (radius `r` kecil), nilai alpha mendekati 0 (sepenuhnya transparan). |
| **33** | `                pygame.draw.circle(self.darkness_surf, (0, 0, 0, alpha), (cx, cy), r)` | Menggambar lingkaran hitam transparan pada permukaan kegelapan di titik pusat pemain. Karena bagian tengah bernilai alpha kecil (transparan), kegelapan akan berlubang (terang). |
| **34** | *(Baris Kosong)* | Pemisah visual. |
| **35** | `        screen.blit(self.darkness_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)` | Menempelkan permukaan kegelapan ke layar utama dengan mode campuran (blend flag) pengurangan (`pygame.BLEND_RGBA_SUB`), yang memotong kecerahan piksel layar utama berdasarkan tingkat kegelapan yang digambar. |
| **36** | *(Baris Kosong)* | Pemisah visual. |
| **37** | `    def trigger_flash(self, duration=120):` | Fungsi untuk memulai efek kilatan cahaya layar dengan parameter durasi opsional (bawaannya 120 frame). |
| **38** | `        self.flash_timer = duration` | Mengatur sisa frame kilatan dengan durasi yang diberikan. |
| **39** | `        self.flash_duration = max(1, duration)` | Menyimpan total durasi kilatan untuk referensi persentase transparansi, dipastikan minimal 1 agar tidak membagi dengan nol. |
| **40** | `        self.shake_amount = 15` | Mengeset intensitas guncangan layar awal sebesar 15 piksel. |
| **41** | *(Baris Kosong)* | Pemisah visual. |
| **42** | `    def draw_flash(self, screen):` | Fungsi untuk memperbarui sisa durasi kilatan cahaya, meredakan guncangan layar, dan menggambar efek kilatan tersebut. |
| **43** | `        shake_offset = [0, 0]` | Menginisialisasi offset guncangan layar ke posisi `[0, 0]` (kondisi normal). |
| **44** | `        if self.shake_amount > 0:` | Mengecek apakah masih ada intensitas guncangan layar yang tersisa. |
| **45** | `            shake_offset = [random.randint(-self.shake_amount, self.shake_amount),` | Memilih pergeseran sumbu X secara acak antara `-self.shake_amount` dan `self.shake_amount`. |
| **46** | `                            random.randint(-self.shake_amount, self.shake_amount)]` | Memilih pergeseran sumbu Y secara acak antara `-self.shake_amount` dan `self.shake_amount`. |
| **47** | `            self.shake_amount = max(0, self.shake_amount - 1)` | Mengurangi nilai intensitas guncangan sebesar 1 frame per pemanggilan (redaman guncangan) hingga kembali ke 0. |
| **48** | *(Baris Kosong)* | Pemisah visual. |
| **49** | `        if self.flash_timer > 0:` | Mengecek apakah timer efek kilatan layar masih aktif (lebih dari 0). |
| **50** | `            alpha = max(0, min(255, int((self.flash_timer / self.flash_duration) * 255)))` | Menghitung tingkat transparansi (alpha) kilatan putih secara linear berdasarkan sisa timer, sehingga efek memudar secara perlahan (fade-out). |
| **51** | `            self.flash_surf.set_alpha(alpha)` | Menyesuaikan transparansi permukaan kilatan putih (`flash_surf`) dengan nilai alpha yang dihitung. |
| **52** | `            screen.blit(self.flash_surf, shake_offset)` | Menempelkan permukaan kilatan cahaya putih ke layar utama dengan menerapkan offset guncangan layar. |
| **53** | `            self.flash_timer -= 1` | Mengurangi penghitung timer kilatan cahaya sebesar 1. |
| **54** | `        return tuple(shake_offset)` | Mengembalikan nilai offset pergeseran layar dalam bentuk tuple koordinat X dan Y agar bisa digunakan oleh sistem render kamera utama game. |
| **55** | *(Baris Kosong)* | Pemisah visual di akhir file. |

---

## Alur Kerja Utama

1. **Inisialisasi (`__init__`)**:
   Saat kelas `VisualEffects` dibuat, sebuah permukaan kegelapan dengan kemampuan transparansi (`SRCALPHA`) dan permukaan putih solid untuk kilatan cahaya disiapkan.

2. **Efek Kegelapan & Senter (`draw_darkness`)**:
   * Setiap frame, permukaan kegelapan dibersihkan dengan warna kegelapan dasar (biru gelap). Jika pemain cedera, warna dasar diubah menjadi kemerahan dan berdenyut naik-turun menggunakan rumus fungsi sinus.
   * Jika senter aktif dan baterai mencukupi, program menggambar serangkaian lingkaran hitam dari luar ke dalam di atas pemain dengan nilai transparansi yang semakin berkurang (gradasi) sehingga membiarkan area di sekitar pemain terlihat.
   * Permukaan kegelapan digabungkan ke layar utama menggunakan metode pengurangan blending (`BLEND_RGBA_SUB`), membuat bagian luar lingkaran cahaya senter menjadi gelap gulita.

3. **Pemicu Kilatan & Guncangan (`trigger_flash`)**:
   * Ketika aksi tertentu terjadi (seperti ledakan atau jumpscare), fungsi ini dipanggil untuk mengisi timer kilatan layar dan menentukan seberapa kuat getaran awal layar (`shake_amount`).

4. **Penggambaran Kilatan & Guncangan Layar (`draw_flash`)**:
   * Selama `shake_amount` > 0, offset acak dihitung untuk menggoyang layar secara dinamis, dan intensitas goyangan perlahan dikurangi (redaman).
   * Selama `flash_timer` > 0, permukaan putih digambar dengan opacity (alpha) yang memudar hingga akhirnya hilang sepenuhnya.
   * Fungsi ini mengembalikan nilai pergeseran (`shake_offset`) agar sisa tampilan peta (map) dan karakter dalam game ikut bergeser mengikuti getaran kamera.
