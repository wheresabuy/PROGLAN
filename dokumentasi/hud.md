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
| 3 | `class HUD:` | Mendefinisikan kelas `HUD` yang bertanggung jawab merender antarmuka status pemain. |
| 4 | `    def __init__(self, currency):` | Konstruktor kelas `HUD` yang menerima parameter `currency` (objek pelacak mata uang pemain). |
| 5 | `        self.currency = currency` | Menyimpan referensi objek `currency` ke dalam atribut objek `self.currency`. |
| 6 | `        self.font_main = pygame.font.SysFont("Arial", 18, bold=True)` | Inisialisasi font Arial ukuran 18 tebal (*bold*) untuk nilai angka mata uang. |
| 7 | `        self.font_sub = pygame.font.SysFont("Arial", 12)` | Inisialisasi font Arial ukuran 12 untuk label teks kecil di atas status bar. |
| 8 | `        self.display_gold, self.display_silver, self.display_bronze = currency.gold, currency.silver, currency.bronze` | Menginisialisasi nilai mata uang tampilan awal berdasarkan nilai aktual untuk keperluan animasi smooth. |
| 9 | `        self.CLR_BG, self.CLR_ACCENT, self.CLR_WHITE = (20, 20, 20, 180), (255, 215, 0), (240, 240, 240)` | Warna Palette: Latar panel abu-abu gelap transparan, aksen emas koin, dan warna teks putih abu-abu terang. |
| 10 | `        self.CLR_HEALTH, self.CLR_STAMINA, self.CLR_BATTERY = (231, 76, 60), (46, 204, 113), (52, 152, 219)` | Warna Palette: Status bar kesehatan merah, stamina hijau, dan baterai biru. |
| 11 | `    def _draw_bar(self, screen, x, y, width, label, value, max_value, color):` | Metode internal untuk menggambar status bar (seperti health/battery). |
| 12 | `        pygame.draw.rect(screen, (40, 40, 40), (x, y, width, 8), border_radius=4)` | Menggambar bar latar belakang berwarna abu-abu gelap dengan tebal 8 piksel dan sudut melengkung. |
| 13 | `        fill_w = int((value / max_value) * width)` | Menghitung lebar isi bar secara proporsional sesuai rasio nilai saat ini terhadap nilai maksimum. |
| 14 | `        if fill_w > 0:` | Memastikan lebar isi bar lebih dari 0 sebelum melakukan penggambaran untuk menghindari bug visual. |
| 15 | `            pygame.draw.rect(screen, color, (x, y, fill_w, 8), border_radius=4)` | Menggambar isi bar sesuai warna parameter di atas bar latar belakang dengan sudut melengkung. |
| 16 | `        lbl_surf = self.font_sub.render(label, True, (150, 150, 150))` | Membuat permukaan teks (*surface*) untuk label dengan font berukuran kecil dan warna abu-abu. |
| 17 | `        screen.blit(lbl_surf, (x, y - 15))` | Menempelkan (*blit*) permukaan label di layar pada posisi 15 piksel di atas bar. |
| 18 | `    def draw(self, screen, player=None, battery_level=100):` | Metode utama untuk menggambar seluruh tampilan HUD ke layar. Menerima objek player dan tingkat baterai. |
| 19 | `        panel_rect = pygame.Rect(20, 20, 260, 100)` | Membuat objek `pygame.Rect` untuk menentukan ukuran dan posisi panel (posisi x=20, y=20, lebar=260, tinggi=100). |
| 20 | `        bg_surf = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)` | Membuat *surface* baru transparan dengan format `SRCALPHA` untuk area panel. |
| 21 | `        pygame.draw.rect(bg_surf, self.CLR_BG, bg_surf.get_rect(), border_radius=10)` | Menggambar persegi panjang sudut melengkung berwarna transparan gelap di atas *surface* panel tersebut. |
| 22 | `        screen.blit(bg_surf, (panel_rect.x, panel_rect.y))` | Menempelkan panel latar belakang transparan ke layar utama game. |
| 23 | `        self.display_gold += (self.currency.gold - self.display_gold) * 0.1; self.display_silver += (self.currency.silver - self.display_silver) * 0.1; self.display_bronze += (self.currency.bronze - self.display_bronze) * 0.1` | Mendekatkan nilai koin emas, perak, dan perunggu tampilan ke nilai aktual sebanyak 10% di setiap frame secara smooth. |
| 24 | `        currencies = [` | Memulai pendefinisian list `currencies` yang menampung data rendering untuk setiap koin. |
| 25 | `            ("G", int(self.display_gold), (255, 215, 0)),` | Data koin emas: label koin "G", nilai koin bulat (diambil dari nilai animasi), dan warna lingkaran koin (Emas). |
| 26 | `            ("S", int(self.display_silver), (192, 192, 192)),` | Data koin perak: label koin "S", nilai koin bulat, dan warna lingkaran koin (Perak). |
| 27 | `            ("B", int(self.display_bronze), (205, 127, 50))` | Data koin perunggu: label koin "B", nilai koin bulat, dan warna lingkaran koin (Perunggu). |
| 28 | `        ]` | Penutup list dari data koin. |
| 29 | `        start_x = 40` | Menentukan titik awal koordinat X untuk menggambar koin pertama. |
| 30 | `        for icon, val, color in currencies:` | Melakukan perulangan (*looping*) untuk menggambar masing-masing koin dari list `currencies`. |
| 31 | `            pygame.draw.circle(screen, color, (start_x, 45), 8)` | Menggambar lingkaran kecil dengan warna koin pada posisi y=45 dengan jari-jari 8 piksel. |
| 32 | `            val_surf = self.font_main.render(str(val), True, self.CLR_WHITE)` | Merender teks angka nilai koin (yang sedang teranimasi) menjadi objek *surface*. |
| 33 | `            screen.blit(val_surf, (start_x + 15, 35))` | Menempelkan teks nilai koin tersebut di sebelah kanan lingkaran koin (jarak offset 15 piksel). |
| 34 | `            start_x += 75` | Menggeser posisi X ke kanan sebesar 75 piksel untuk koin berikutnya agar tidak bertumpukan. |
| 35 | `        hp = player.health if player else 100` | Mengambil nilai kesehatan pemain. Jika objek `player` bernilai `None`, nilai kesehatannya otomatis diatur ke 100. |
| 36 | `        stamina = player.stamina if hasattr(player, 'stamina') else 100` | Mengambil nilai stamina jika objek `player` memiliki atribut `stamina`, jika tidak diatur ke 100. |
| 37 | `        bar_x = 40` | Mengatur koordinat horizontal X awal untuk bar status. |
| 38 | `        self._draw_bar(screen, bar_x, 80, 200, "HEALTH", hp, 100, self.CLR_HEALTH)` | Menggambar bar kesehatan berwarna merah pada posisi y=80 dengan lebar maksimal 200 piksel. |
| 39 | `        self._draw_bar(screen, bar_x, 105, 200, "BATTERY", battery_level, 100, self.CLR_BATTERY)` | Menggambar bar baterai berwarna biru pada posisi y=105 dengan lebar maksimal 200 piksel. |
| 40 | *(baris kosong)* | Pemisah visual/akhir dari file kode program. |
