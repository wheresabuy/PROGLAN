# Penjelasan Kode: `hud.py`

Dokumen ini berisi penjelasan mendetail baris demi baris mengenai file `/home/abuyyy/PemogramanLanjut/src/ui/hud.py` dalam bahasa Indonesia untuk membantu persiapan demo program.

---

## Deskripsi & Tujuan File
File `hud.py` mendefinisikan kelas `HUD` (Heads-Up Display). Kelas ini berfungsi untuk menggambar antarmuka informasi status di layar game (seperti di pojok kiri atas). Informasi yang ditampilkan meliputi:
1. **Mata Uang (Currency)**: Menampilkan koin emas (Gold), perak (Silver), dan perunggu (Bronze) dengan efek transisi angka yang mulus (animasi *lerp*).
2. **Status Bar**: Menampilkan bar nyawa (Health) berwarna merah dan sisa daya baterai (Battery) berwarna biru.

---

## Daftar Import

| Library | Kegunaan |
| :--- | :--- |
| `import pygame` | Library utama untuk membuat game 2D di Python. Digunakan di sini untuk menggambar bentuk geometris (lingkaran, persegi), memanipulasi permukaan grafis (*surface*), serta memuat dan merender font/teks. |
| `import time` | Modul bawaan Python untuk memanipulasi waktu. Di dalam file ini, modul diimpor tetapi belum digunakan secara aktif. |

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel analisis dari setiap baris kode di dalam `hud.py`:

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| 1 | `import pygame` | Mengimpor modul `pygame` untuk menangani rendering grafik dan teks. |
| 2 | `import time` | Mengimpor modul `time` bawaan Python. |
| 3 | *(baris kosong)* | Pemisah visual untuk kerapian penulisan kode. |
| 4 | `class HUD:` | Mendefinisikan kelas `HUD` yang bertanggung jawab merender antarmuka status pemain. |
| 5 | `    def __init__(self, currency):` | Konstruktor kelas `HUD` yang menerima parameter `currency` (objek pelacak mata uang pemain). |
| 6 | `        self.currency = currency` | Menyimpan referensi objek `currency` ke dalam atribut objek `self.currency`. |
| 7 | `        self.font_main = pygame.font.SysFont("Arial", 18, bold=True)` | Inisialisasi font Arial ukuran 18 tebal (*bold*) untuk nilai angka mata uang. |
| 8 | `        self.font_sub = pygame.font.SysFont("Arial", 12)` | Inisialisasi font Arial ukuran 12 untuk label teks kecil di atas status bar. |
| 9 | *(baris kosong)* | Pemisah visual. |
| 10 | `        # Simpan nilai untuk animasi smooth` | Komentar yang menjelaskan tujuan variabel-variabel di bawahnya. |
| 11 | `        self.display_gold = currency.gold` | Menyimpan nilai emas tampilan awal berdasarkan nilai emas aktual saat inisialisasi. |
| 12 | `        self.display_silver = currency.silver` | Menyimpan nilai perak tampilan awal berdasarkan nilai perak aktual saat inisialisasi. |
| 13 | `        self.display_bronze = currency.bronze` | Menyimpan nilai perunggu tampilan awal berdasarkan nilai perunggu aktual saat inisialisasi. |
| 14 | *(baris kosong)* | Pemisah visual. |
| 15 | `        # Warna Palette` | Komentar penanda bagian definisi palet warna. |
| 16 | `        self.CLR_BG = (20, 20, 20, 180)` | Mendefinisikan warna latar panel: abu-abu gelap transparan (RGBA, alpha=180). |
| 17 | `        self.CLR_ACCENT = (255, 215, 0)` | Warna aksen emas dalam format RGB. |
| 18 | `        self.CLR_WHITE = (240, 240, 240)` | Warna teks putih abu-abu terang dalam format RGB. |
| 19 | `        self.CLR_HEALTH = (231, 76, 60)` | Warna merah untuk status bar kesehatan (*Health*). |
| 20 | `        self.CLR_STAMINA = (46, 204, 113)` | Warna hijau untuk stamina (tidak digambar secara aktif di kode saat ini). |
| 21 | `        self.CLR_BATTERY = (52, 152, 219)` | Warna biru untuk status bar baterai (*Battery*). |
| 22 | *(baris kosong)* | Pemisah visual. |
| 23 | `    def _draw_bar(self, screen, x, y, width, label, value, max_value, color):` | Metode pembantu (*helper method*) internal untuk menggambar status bar (seperti health/battery). |
| 24 | `        # Background Bar` | Komentar penjelas bagian latar belakang bar. |
| 25 | `        pygame.draw.rect(screen, (40, 40, 40), (x, y, width, 8), border_radius=4)` | Menggambar bar latar belakang berwarna abu-abu gelap dengan tebal 8 piksel dan sudut melengkung. |
| 26 | `        # Fill Bar` | Komentar penjelas bagian isi bar. |
| 27 | `        fill_w = int((value / max_value) * width)` | Menghitung lebar isi bar secara proporsional sesuai rasio nilai saat ini terhadap nilai maksimum. |
| 28 | `        if fill_w > 0:` | Memastikan lebar isi bar lebih dari 0 sebelum melakukan penggambaran untuk menghindari bug visual. |
| 29 | `            pygame.draw.rect(screen, color, (x, y, fill_w, 8), border_radius=4)` | Menggambar isi bar sesuai warna parameter di atas bar latar belakang dengan sudut melengkung. |
| 30 | `        # Label` | Komentar penjelas bagian teks label. |
| 31 | `        lbl_surf = self.font_sub.render(label, True, (150, 150, 150))` | Membuat permukaan teks (*surface*) untuk label dengan font berukuran kecil dan warna abu-abu. |
| 32 | `        screen.blit(lbl_surf, (x, y - 15))` | Menempelkan (*blit*) permukaan label di layar pada posisi 15 piksel di atas bar. |
| 33 | *(baris kosong)* | Pemisah visual. |
| 34 | `    def draw(self, screen, player=None, battery_level=100):` | Metode utama untuk menggambar seluruh tampilan HUD ke layar. Menerima objek player dan tingkat baterai. |
| 35 | `        # 1. Background Panel (Clean Rect)` | Komentar penjelas bagian pembuatan panel latar belakang. |
| 36 | `        panel_rect = pygame.Rect(20, 20, 260, 100)` | Membuat objek `pygame.Rect` untuk menentukan ukuran dan posisi panel (posisi x=20, y=20, lebar=260, tinggi=100). |
| 37 | `        bg_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)` | Membuat *surface* baru transparan dengan format `SRCALPHA` untuk area panel. |
| 38 | `        pygame.draw.rect(bg_surf, self.CLR_BG, bg_surf.get_rect(), border_radius=10)` | Menggambar persegi panjang sudut melengkung berwarna transparan gelap di atas *surface* panel tersebut. |
| 39 | `        screen.blit(bg_surf, (panel_rect.x, panel_rect.y))` | Menempelkan panel latar belakang transparan ke layar utama game. |
| 40 | *(baris kosong)* | Pemisah visual. |
| 41 | `        # 2. Update Animasi Angka (Simple lerp)` | Komentar penjelas mekanisme interpolasi nilai mata uang untuk animasi yang lebih halus. |
| 42 | `        self.display_gold += (self.currency.gold - self.display_gold) * 0.1` | Mendekatkan nilai koin emas tampilan ke nilai koin emas aktual sebanyak 10% di setiap frame. |
| 43 | `        self.display_silver += (self.currency.silver - self.display_silver) * 0.1` | Mendekatkan nilai koin perak tampilan ke nilai koin perak aktual sebanyak 10% di setiap frame. |
| 44 | `        self.display_bronze += (self.currency.bronze - self.display_bronze) * 0.1` | Mendekatkan nilai koin perunggu tampilan ke nilai koin perunggu aktual sebanyak 10% di setiap frame. |
| 45 | *(baris kosong)* | Pemisah visual. |
| 46 | `        # 3. Currency Display (Horizontal Row)` | Komentar penjelas proses penggambaran baris mata uang secara mendatar. |
| 47 | `        currencies = [` | Memulai pendefinisian list `currencies` yang menampung data rendering untuk setiap koin. |
| 48 | `            ("G", int(self.display_gold), (255, 215, 0)),` | Data koin emas: label koin "G", nilai koin bulat (diambil dari nilai animasi), dan warna lingkaran koin (Emas). |
| 49 | `            ("S", int(self.display_silver), (192, 192, 192)),` | Data koin perak: label koin "S", nilai koin bulat, dan warna lingkaran koin (Perak). |
| 50 | `            ("B", int(self.display_bronze), (205, 127, 50))` | Data koin perunggu: label koin "B", nilai koin bulat, dan warna lingkaran koin (Perunggu). |
| 51 | `        ]` | Penutup list dari data koin. |
| 52 | *(baris kosong)* | Pemisah visual. |
| 53 | `        start_x = 40` | Menentukan titik awal koordinat X untuk menggambar koin pertama. |
| 54 | `        for icon, val, color in currencies:` | Melakukan perulangan (*looping*) untuk menggambar masing-masing koin dari list `currencies`. |
| 55 | `            # Icon Circle` | Komentar penjelas bagian pembuatan lingkaran representasi koin. |
| 56 | `            pygame.draw.circle(screen, color, (start_x, 45), 8)` | Menggambar lingkaran kecil dengan warna koin pada posisi y=45 dengan jari-jari 8 piksel. |
| 57 | `            # Value` | Komentar penjelas pembuatan teks nilai koin. |
| 58 | `            val_surf = self.font_main.render(str(val), True, self.CLR_WHITE)` | Merender teks angka nilai koin (yang sedang teranimasi) menjadi objek *surface*. |
| 59 | `            screen.blit(val_surf, (start_x + 15, 35))` | Menempelkan teks nilai koin tersebut di sebelah kanan lingkaran koin (jarak offset 15 piksel). |
| 60 | `            start_x += 75` | Menggeser posisi X ke kanan sebesar 75 piksel untuk koin berikutnya agar tidak bertumpukan. |
| 61 | *(baris kosong)* | Pemisah visual. |
| 62 | `        # 4. Status Bars (Vertical Stack)` | Komentar penjelas penggambaran bar status secara bertumpuk ke bawah. |
| 63 | `        hp = player.health if player else 100` | Mengambil nilai kesehatan pemain. Jika objek `player` bernilai `None`, nilai kesehatannya otomatis diatur ke 100. |
| 64 | `        stamina = player.stamina if hasattr(player, 'stamina') else 100` | Mengambil nilai stamina jika objek `player` memiliki atribut `stamina`, jika tidak diatur ke 100. (Catatan: variabel ini tidak digunakan di bawahnya). |
| 65 | *(baris kosong)* | Pemisah visual. |
| 66 | `        bar_x = 40` | Mengatur koordinat horizontal X awal untuk bar status (sejajar dengan posisi koin). |
| 67 | `        self._draw_bar(screen, bar_x, 80, 200, "HEALTH", hp, 100, self.CLR_HEALTH)` | Menggambar bar kesehatan berwarna merah pada posisi y=80 dengan lebar maksimal 200 piksel. |
| 68 | `        self._draw_bar(screen, bar_x, 105, 200, "BATTERY", battery_level, 100, self.CLR_BATTERY)` | Menggambar bar baterai berwarna biru pada posisi y=105 dengan lebar maksimal 200 piksel. |
| 69 | *(baris kosong)* | Akhir dari file kode program. |

---

## Alur Kerja Utama

1. **Inisialisasi (`__init__`)**:
   Saat kelas `HUD` dibentuk, kelas ini menerima objek `currency` milik pemain. Font didefinisikan untuk teks, warna-warna disiapkan (seperti hitam transparan untuk panel belakang, merah untuk HEALTH, dan biru untuk BATTERY), serta menyalin status jumlah koin awal.
2. **Pembaruan Animasi Nilai Koin**:
   Di setiap frame (ketika metode `draw` dipanggil), kelas HUD akan membandingkan jumlah koin tampilan saat ini (`self.display_gold` dkk.) dengan jumlah koin yang dimiliki pemain sesungguhnya (`self.currency.gold` dkk.). Nilai tampilan ini didekatkan secara perlahan ke nilai sesungguhnya menggunakan rumus interpolasi linier sederhana (`value += (target - value) * 0.1`). Ini membuat perubahan angka tampak "mengalir" secara berurutan alih-alih langsung berubah seketika.
3. **Penggambaran Panel Latar Belakang**:
   Persegi panjang hitam transparan digambar di sudut kiri atas layar untuk menjadi wadah informasi HUD agar teks dan grafik mudah dibaca di atas latar belakang permainan apa pun.
4. **Penggambaran Ikon Koin & Nilai**:
   Sebuah perulangan menggambar koin emas, perak, dan perunggu secara horizontal dari kiri ke kanan. Masing-masing digambarkan menggunakan lingkaran kecil berwarna khusus dan diikuti oleh teks angkanya di samping kanan.
5. **Penggambaran Status Bar (Health & Battery)**:
   Bar kesehatan (merah) dan bar baterai (biru) digambar secara bertumpuk ke bawah di bawah baris informasi koin. Metode pembantu `_draw_bar` akan menghitung berapa lebar bar berwarna yang harus digambar berdasarkan persentase nilai saat ini terhadap nilai maksimumnya.
