# Penjelasan Kode Sumber: minigame_manager.py

Dokumen ini berisi penjelasan baris demi baris dari file `minigame_manager.py` dalam bahasa Indonesia untuk membantu persiapan demo program.

---

## Deskripsi & Tujuan File
File `minigame_manager.py` berfungsi sebagai pengelola atau orkestrator (*manager*) untuk game mini (*minigames*) di dalam game utama. File ini mendefinisikan dua kelas utama:
1. **`MiniGame`**: Kelas dasar (*base class*) yang dirancang untuk diwarisi oleh semua sub-game/game mini. Kelas ini menyediakan struktur standar untuk siklus hidup game mini (inisialisasi, penanganan *event*, pembaruan logika, penggambaran visual, dan proses keluar).
2. **`MiniGameManager`**: Pengontrol transisi status (*state manager*) yang mengatur kapan game mini dimulai dan bagaimana kembali ke game utama. Kelas ini juga bertanggung jawab memproses hasil game mini dan memberikan imbalan (koin perunggu/*bronze currency*) ke dalam profil pemain di engine utama.

---

## Daftar Import
* **`import pygame`**: Mengimpor pustaka Pygame untuk rendering grafis, pembuatan game, penanganan font, dan fungsionalitas game lainnya.
* **`import sys`**: Mengimpor modul bawaan Python `sys` untuk berinteraksi dengan interpreter sistem (opsional digunakan untuk keluar program).
* **`from typing import Dict, Optional`**: Mengimpor anotasi tipe (*type hints*) `Dict` dan `Optional` untuk mendefinisikan struktur data kamus (*dictionary*) dan nilai yang bisa bernilai objek tertentu atau `None`.

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel penjelasan detail untuk setiap baris kode pada file `minigame_manager.py`:

| Baris | Kode Sumber | Penjelasan dalam Bahasa Indonesia |
|---|---|---|
| 1 | `import pygame` | Mengimpor modul `pygame` agar dapat menggunakan fungsi grafis, font, dan event. |
| 2 | `import sys` | Mengimpor modul `sys` untuk operasi interaksi sistem dasar. |
| 3 | `from typing import Dict, Optional` | Mengimpor tipe pembantu `Dict` dan `Optional` untuk anotasi tipe data agar kode lebih mudah dibaca. |
| 4 | *(Baris Kosong)* | Baris kosong sebagai pemisah visual kode sesuai standar PEP 8. |
| 5 | `class MiniGame:` | Mendefinisikan kelas induk bernama `MiniGame` untuk semua game mini. |
| 6 | `    """Base class untuk semua sub-game. Memiliki loop sendiri namun tetap dalam satu engine."""` | *Docstring* penjelas fungsi dari kelas `MiniGame`. |
| 7 | `    def __init__(self, screen, clock, manager):` | Konstruktor kelas `MiniGame` yang menerima layar utama (`screen`), penunjuk waktu FPS (`clock`), dan instansi `MiniGameManager` (`manager`). |
| 8 | `        self.screen = screen` | Menyimpan referensi layar gambar utama ke properti objek `self.screen`. |
| 9 | `        self.clock = clock` | Menyimpan objek jam (*clock*) pengatur frame rate ke properti objek `self.clock`. |
| 10 | `        self.manager = manager` | Menyimpan referensi objek pengelola ke properti `self.manager`. |
| 11 | `        self.running = True` | Menyimpan status aktif permainan. Bernilai `True` saat game mini sedang berjalan. |
| 12 | `        self.score = 0` | Menginisialisasi skor awal game mini dengan nilai `0`. |
| 13 | `        self.font = pygame.font.SysFont("Arial", 24, bold=True)` | Menginisialisasi font sistem ("Arial", ukuran 24, cetak tebal) untuk menggambar teks di layar. |
| 14 | *(Baris Kosong)* | Baris kosong sebagai pemisah. |
| 15 | `    def handle_event(self, event): pass` | Metode *placeholder* untuk penanganan input (keyboard/mouse). Fungsi ini wajib di-*override* (ditulis ulang) oleh kelas anak. |
| 16 | `    def update(self, dt): pass` | Metode *placeholder* untuk memperbarui logika game berdasarkan selang waktu delta (`dt`). Wajib di-*override* oleh kelas anak. |
| 17 | `    def draw(self): pass` | Metode *placeholder* untuk menampilkan visual game ke layar. Wajib di-*override* oleh kelas anak. |
| 18 | *(Baris Kosong)* | Baris kosong sebagai pemisah. |
| 19 | `    def exit_game(self, result_data=None):` | Metode untuk menghentikan permainan mini dan mengirimkan data hasil permainan (`result_data`) kembali ke manager. |
| 20 | `        self.running = False` | Mengubah status permainan menjadi tidak berjalan (`False`). |
| 21 | `        self.manager.return_to_main(result_data)` | Memanggil fungsi manager untuk mengembalikan kontrol permainan ke game utama dengan menyertakan hasil game mini. |
| 22 | *(Baris Kosong)* | Baris kosong sebagai pemisah antarkelas. |
| 23 | `class MiniGameManager:` | Mendefinisikan kelas `MiniGameManager` untuk mengatur alur hidup game mini. |
| 24 | `    """` | Pembuka *docstring* multi-baris untuk kelas `MiniGameManager`. |
| 25 | `    Orkestrator yang mengelola transisi antara game utama dan sub-game.` | Deskripsi fungsi kelas sebagai orkestrator/pengatur transisi game. |
| 26 | `    Memungkinkan 'Sub-Game' berjalan tanpa mengganggu state game utama.` | Deskripsi yang menerangkan bahwa status game utama aman ketika sub-game berjalan. |
| 27 | `    """` | Penutup *docstring* multi-baris. |
| 28 | `    def __init__(self, main_engine):` | Konstruktor kelas `MiniGameManager` yang menerima parameter engine game utama (`main_engine`). |
| 29 | `        self.main_engine = main_engine` | Menyimpan referensi engine game utama ke dalam atribut properti `self.main_engine`. |
| 30 | `        self.active_game: Optional[MiniGame] = None` | Menyiapkan variabel game aktif yang bertipe kelas `MiniGame` atau bernilai `None` saat game utama aktif. |
| 31 | `        self.saved_main_state = None` | Menyediakan penampung untuk menyimpan status game utama jika diperlukan di kemudian hari. |
| 32 | *(Baris Kosong)* | Baris kosong. |
| 33 | `    def start_minigame(self, game_class: type):` | Metode untuk memulai game mini baru berdasarkan kelas yang dimasukkan (`game_class`). |
| 34 | `        print(f"Switching to Mini-Game: {game_class.__name__}")` | Mencetak teks informasi perpindahan game mini ke terminal/konsol debug. |
| 35 | `        self.active_game = game_class(self.main_engine.screen, self.main_engine.clock, self)` | Menginstansiasi objek game mini baru dengan mengirimkan layar utama, clock, dan objek manager (`self`) ini, lalu menetapkannya ke variabel `self.active_game`. |
| 36 | *(Baris Kosong)* | Baris kosong. |
| 37 | `    def return_to_main(self, result_data):` | Metode untuk kembali ke game utama dan memproses hasil permainan yang dikirim oleh game mini. |
| 38 | `        print("Returning to Main Game Story...")` | Mencetak pesan debug kembali ke cerita utama di konsol. |
| 39 | `        self.active_game = None` | Menghapus instansi game mini aktif dengan menyetel nilai properti kembali ke `None`. |
| 40 | `        self.last_result = result_data` | Menyimpan data hasil terakhir dari game mini ke properti `self.last_result`. |
| 41 | `        # Handle results (e.g., reward player based on score)` | Komentar penjelasan mengenai penanganan hadiah atau koin dari skor game mini. |
| 42 | `        if result_data:` | Mengecek apakah game mini mengembalikan objek data hasil (`result_data` tidak kosong). |
| 43 | `            earned = result_data.get('bronze_earned', result_data.get('score', 0) // 10)` | Mengambil jumlah koin perunggu yang didapatkan. Menggunakan kunci `'bronze_earned'` jika ada. Jika tidak, menghitung dari pembagian skor dengan angka 10 secara pembulatan ke bawah (`// 10`). |
| 44 | `            self.main_engine.currency.add_bronze(earned)` | Memasukkan jumlah koin perunggu yang telah dihitung ke dalam akun finansial (`currency`) engine utama pemain. |
| 45 | *(Baris Kosong)* | Baris kosong. |
| 46 | `    def update(self, dt):` | Metode pembaruan logika manager secara berkala. |
| 47 | `        if self.active_game:` | Mengecek apakah ada game mini yang sedang aktif berjalan. |
| 48 | `            self.active_game.update(dt)` | Jika ada game mini aktif, jalankan fungsi `update` milik game mini tersebut dengan parameter delta time (`dt`). |
| 49 | *(Baris Kosong)* | Baris kosong. |
| 50 | `    def draw(self):` | Metode penggambaran/render visual manager secara berkala. |
| 51 | `        if self.active_game:` | Mengecek apakah ada game mini yang sedang aktif berjalan. |
| 52 | `            self.active_game.draw()` | Jika ada game mini aktif, jalankan fungsi menggambar visual (`draw`) milik game mini tersebut ke layar. |
| 53 | *(Baris Kosong)* | Baris kosong. |
| 54 | `    @property` | Dekorator properti Python agar metode di bawahnya dapat diakses langsung layaknya properti/variabel objek (tanpa tanda kurung). |
| 55 | `    def in_minigame(self):` | Metode pengecekan status apakah permainan sedang berada di mode game mini. |
| 56 | `        return self.active_game is not None` | Mengembalikan nilai `True` jika properti `self.active_game` tidak bernilai `None`, dan `False` jika bernilai `None` (berada di game utama). |
| 57 | *(Baris Kosong)* | Baris kosong penanda akhir file (standar PEP 8). |
