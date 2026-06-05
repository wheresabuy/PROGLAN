# Penjelasan SpriteSheetSlicer

## Deskripsi & Tujuan File
File `spritesheet_slicer.py` adalah sebuah utilitas dalam pengembangan game menggunakan Pygame yang berfungsi untuk memotong (slice) gambar lembaran sprite (sprite sheet) menjadi potongan-potongan sprite kecil individual secara otomatis. Utilitas ini juga mendukung penghapusan warna latar belakang tertentu (colorkey) agar sprite tersebut memiliki latar belakang transparan.

---

## Daftar Import
*   `import pygame`: Library utama yang digunakan untuk pengolahan grafis, pembuatan surface, dan fungsi-fungsi game.
*   `import os`: Library bawaan Python yang umumnya digunakan untuk berinteraksi dengan sistem operasi (misalnya manajemen path file), meskipun pada file ini modul tersebut tidak secara langsung dipanggil atau digunakan.

---

## Penjelasan Baris Demi Baris

| Baris | Kode | Penjelasan |
| :--- | :--- | :--- |
| 1 | `import pygame` | Mengimpor pustaka Pygame untuk keperluan pemrosesan grafis dan gambar. |
| 2 | `import os` | Mengimpor modul `os` untuk interaksi dengan sistem operasi (seperti operasi path file). |
| 3 | *(Kosong)* | Baris kosong untuk pemisah visual dan kerapihan kode. |
| 4 | `class SpriteSheetSlicer:` | Mendefinisikan kelas `SpriteSheetSlicer` yang membungkus semua fungsi pemotong sprite sheet. |
| 5-7 | `""" ... """` | Docstring penjelasan kelas yang mendeskripsikan tujuan kelas ini. |
| 8 | `def __init__(self, filename, sprite_width, sprite_height, colorkey=None):` | Konstruktor kelas untuk menginisialisasi objek slicer dengan parameter: path file (`filename`), lebar tiap sprite (`sprite_width`), tinggi tiap sprite (`sprite_height`), dan warna transparansi (`colorkey`). |
| 9-14 | `""" ... """` | Docstring penjelasan parameter konstruktor. |
| 15 | `try:` | Blok `try` untuk menangani potensi error saat memuat file gambar. |
| 16 | `self.sheet = pygame.image.load(filename).convert_alpha()` | Memuat gambar sprite sheet dari path `filename` dan mengubah format pikselnya menggunakan `convert_alpha()` agar mendukung transparansi piksel dengan lebih optimal dan cepat. |
| 17 | `except pygame.error as e:` | Menangkap error Pygame jika file gambar gagal dimuat (misalnya karena file tidak ditemukan atau format tidak didukung). |
| 18 | `print(f"Gagal memuat sprite sheet: {filename}")` | Menampilkan pesan error ke konsol jika proses pemuatan gambar gagal. |
| 19 | `self.sheet = None` | Menetapkan atribut `self.sheet` menjadi `None` agar method lain tahu bahwa gambar gagal dimuat. |
| 20 | `return` | Menghentikan eksekusi konstruktor lebih awal karena terjadi error pemuatan berkas. |
| 21 | *(Kosong)* | Baris kosong untuk pemisah visual. |
| 22 | `self.sw = sprite_width` | Menyimpan lebar sprite ke dalam atribut objek `self.sw`. |
| 23 | `self.sh = sprite_height` | Menyimpan tinggi sprite ke dalam atribut objek `self.sh`. |
| 24 | `self.colorkey = colorkey` | Menyimpan warna latar belakang yang ingin dihilangkan ke dalam atribut objek `self.colorkey`. |
| 25 | *(Kosong)* | Baris kosong untuk pemisah visual. |
| 26 | `def get_sprite(self, col, row):` | Mendefinisikan method `get_sprite` untuk mengambil satu sprite spesifik berdasarkan indeks kolom (`col`) dan baris (`row`) pada grid sprite sheet (dimulai dari indeks 0). |
| 27-29 | `""" ... """` | Docstring penjelasan method `get_sprite`. |
| 30 | `if not self.sheet: return None` | Validasi awal: jika sprite sheet tidak berhasil dimuat (bernilai `None`), method langsung mengembalikan `None`. |
| 31 | *(Kosong)* | Baris kosong. |
| 32 | `rect = pygame.Rect(col * self.sw, row * self.sh, self.sw, self.sh)` | Membuat objek `pygame.Rect` yang mendefinisikan area koordinat (x, y, lebar, tinggi) sprite yang ingin dipotong berdasarkan kolom dan baris. |
| 33 | `image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()` | Membuat objek `pygame.Surface` baru yang kosong dengan ukuran sesuai area potongan, menggunakan flag `pygame.SRCALPHA` dan `convert_alpha()` untuk mendukung transparansi penuh (alpha channel). |
| 34 | `image.blit(self.sheet, (0, 0), rect)` | Menggambar (menyalin) bagian gambar dari `self.sheet` pada area `rect` ke permukaan `image` baru pada posisi koordinat `(0, 0)`. |
| 35 | *(Kosong)* | Baris kosong. |
| 36 | `# Jika colorkey ditentukan, hapus background tersebut` | Komentar yang menjelaskan bahwa jika `colorkey` disetel, maka warna background tersebut akan dibuat transparan. |
| 37 | `if self.colorkey is not None:` | Memeriksa apakah parameter `colorkey` telah ditentukan (tidak bernilai `None`). |
| 38 | `image.set_colorkey(self.colorkey)` | Mengatur warna transparansi pada gambar menggunakan `set_colorkey()`, membuat warna yang cocok dengan `self.colorkey` menjadi transparan. |
| 39 | *(Kosong)* | Baris kosong. |
| 40 | `return image` | Mengembalikan surface sprite yang telah dipotong dan diproses. |
| 41 | *(Kosong)* | Baris kosong. |
| 42 | `def get_all_sprites(self, rows, cols):` | Mendefinisikan method `get_all_sprites` untuk mengambil seluruh sprite di dalam grid berukuran baris `rows` dan kolom `cols`. |
| 43-45 | `""" ... """` | Docstring penjelasan method `get_all_sprites`. |
| 46 | `sprites = []` | Inisialisasi list kosong `sprites` untuk menampung semua sprite hasil pemotongan. |
| 47 | `for r in range(rows):` | Melakukan perulangan untuk setiap baris (`r`) dari 0 hingga `rows - 1`. |
| 48 | `for c in range(cols):` | Melakukan perulangan bersarang untuk setiap kolom (`c`) dari 0 hingga `cols - 1` pada baris tersebut. |
| 49 | `sprites.append(self.get_sprite(c, r))` | Memotong sprite pada posisi baris `r` dan kolom `c` menggunakan `get_sprite()`, lalu menambahkannya ke dalam list `sprites`. |
| 50 | `return sprites` | Mengembalikan list yang berisi seluruh sprite hasil pemotongan. |
| 51 | *(Kosong)* | Baris kosong. |
| 52 | `def map_to_dict(self, item_names_grid):` | Mendefinisikan method `map_to_dict` untuk memetakan sprite hasil potongan ke sebuah dictionary berdasarkan nama item yang diberikan dalam bentuk grid 2 dimensi. |
| 53-56 | `""" ... """` | Docstring penjelasan method `map_to_dict`. |
| 57 | `mapping = {}` | Inisialisasi dictionary kosong `mapping` untuk menampung pasangan `nama_item: sprite_surface`. |
| 58 | `for r, row_names in enumerate(item_names_grid):` | Mengiterasi grid nama item baris demi baris, menggunakan `enumerate` untuk mendapatkan indeks baris (`r`) dan daftar nama pada baris tersebut (`row_names`). |
| 59 | `for c, name in enumerate(row_names):` | Mengiterasi setiap nama item pada baris tersebut, menggunakan `enumerate` untuk mendapatkan indeks kolom (`c`) dan nama item (`name`). |
| 60 | `if name: # Jika nama tidak kosong` | Mengecek apakah `name` valid (tidak berupa string kosong atau bernilai palsu). |
| 61 | `mapping[name] = self.get_sprite(c, r)` | Memotong sprite pada posisi koordinat kolom `c` dan baris `r` melalui `get_sprite(c, r)`, lalu menyimpannya ke dictionary `mapping` dengan kunci berupa `name`. |
| 62 | `return mapping` | Mengembalikan dictionary `mapping` yang memuat relasi antara nama item dengan objek sprite-nya. |
| 63 | *(Kosong)* | Baris kosong di akhir berkas. |

---

## Alur Kerja Utama
1. **Inisialisasi (`__init__`)**: Pengguna instansiasi objek `SpriteSheetSlicer` dengan menyuplai path gambar sprite sheet, ukuran potongan sprite (lebar dan tinggi), serta warna transparansi (`colorkey`). Program memuat gambar tersebut dan mengoptimalkannya dengan format pixel Pygame.
2. **Pemotongan Sprite Satuan (`get_sprite`)**: Ketika ingin mengambil sprite di baris/kolom tertentu, objek menghitung koordinat batas wilayah (`pygame.Rect`) dari sprite sheet asal, memotongnya ke permukaan (`pygame.Surface`) kosong baru yang memiliki kanal transparansi (alpha channel), serta menghapus warna latar belakang jika `colorkey` didefinisikan.
3. **Pemotongan Massal & Pemetaan (`get_all_sprites` & `map_to_dict`)**:
   - `get_all_sprites` menyapu seluruh grid baris dan kolom untuk memotong semua sprite dan menaruhnya ke dalam sebuah list sederhana.
   - `map_to_dict` menerima layout grid 2D berupa nama-nama objek/item, memotong sprite di posisi grid yang bersesuaian, dan menyimpannya ke dalam dictionary. Langkah ini memudahkan kode game lain memanggil sprite dengan kata kunci nama item (misal: `sprites['pedang']`) alih-alih koordinat koordinat (kolom, baris).
