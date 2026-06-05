# Penjelasan Source Code: spritesheet.py

Dokumen ini berisi penjelasan detail baris demi baris dari file `spritesheet.py` dalam bahasa Indonesia. Penjelasan ini dirancang untuk membantu Anda memahami logika internal pemotongan spritesheet menggunakan Pygame guna persiapan demo proyek.

---

## Deskripsi & Tujuan File
File `spritesheet.py` adalah sebuah modul utilitas yang mendefinisikan kelas `Spritesheet`. Tujuan utama dari kelas ini adalah untuk memuat satu gambar besar yang berisi sekumpulan frame animasi (biasa disebut *spritesheet*), memotongnya menjadi frame-frame individual (sub-gambar/subsurface), melakukan perbesaran atau perkecil skala gambar (scaling), dan menyimpannya ke dalam struktur data matriks (list 2 dimensi) agar dapat diakses dengan mudah selama permainan berlangsung (misalnya untuk animasi karakter).

---

## Daftar Import
Modul ini hanya membutuhkan satu pustaka eksternal:

*   **`import pygame`**: Pustaka utama yang digunakan untuk membuat game 2D di Python. Dalam file ini, Pygame digunakan untuk memuat gambar (`pygame.image.load`), merepresentasikan gambar di memori (`pygame.Surface`), memotong bagian gambar (`subsurface`), serta mengubah resolusi/ukuran gambar (`pygame.transform.scale`).

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel penjelasan detail untuk setiap baris kode dalam `spritesheet.py`:

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| **1** | `import pygame` | Mengimpor pustaka Pygame agar modul dapat menggunakan fitur grafis dan manipulasi gambar. |
| **2** | *(Kosong)* | Baris kosong untuk menjaga kerapihan struktur kode (pemisah visual). |
| **3** | `class Spritesheet:` | Mendefinisikan kelas bernama `Spritesheet` sebagai cetak biru (blueprint) untuk objek pemotong gambar animasi. |
| **4** | `def __init__(self, filename, cols, rows, scale=1.5):` | Konstruktor kelas. Menerima argumen: `filename` (jalur file gambar), `cols` (jumlah kolom sprite), `rows` (jumlah baris sprite), dan `scale` (faktor skala pembesaran, default 1.5). |
| **5** | `self.sheet = pygame.image.load(filename).convert_alpha()` | Memuat file gambar spritesheet dan mengonversinya menggunakan `.convert_alpha()`. Langkah konversi ini penting agar Pygame dapat merender transparansi (saluran alpha) secara cepat dan optimal. |
| **6** | `self.cols = cols` | Menyimpan nilai jumlah kolom ke dalam variabel instansi `self.cols`. |
| **7** | `self.rows = rows` | Menyimpan nilai jumlah baris ke dalam variabel instansi `self.rows`. |
| **8** | `self.scale = scale` | Menyimpan faktor skala pembesaran gambar ke dalam variabel instansi `self.scale`. |
| **9** | `self.fw = self.sheet.get_width() // cols` | Menghitung lebar satu frame gambar (`fw` = *frame width*) dengan membagi lebar total spritesheet dengan jumlah kolom menggunakan pembagian bulat (`//`). |
| **10** | `self.fh = self.sheet.get_height() // rows` | Menghitung tinggi satu frame gambar (`fh` = *frame height*) dengan membagi tinggi total spritesheet dengan jumlah baris menggunakan pembagian bulat (`//`). |
| **11** | `self.frames = [[None for _ in range(cols)] for _ in range(rows)]` | Membuat matriks (list 2 dimensi) berukuran `rows x cols` yang diisi dengan nilai `None`. Matriks ini nantinya akan menampung potongan gambar hasil olahan. |
| **12** | `self._slice()` | Memanggil metode privat helper `_slice()` untuk langsung memotong spritesheet ketika objek diinstansiasi. |
| **13** | *(Kosong)* | Baris kosong untuk memisahkan konstruktor dengan metode lainnya. |
| **14** | `def _slice(self):` | Mendefinisikan metode helper internal (ditandai dengan garis bawah `_`) untuk memotong gambar spritesheet menjadi frame-frame individual. |
| **15** | `for r in range(self.rows):` | Melakukan iterasi (perulangan) sebanyak jumlah baris sprite (`r` berkisar dari `0` hingga `rows - 1`). |
| **16** | `for c in range(self.cols):` | Melakukan iterasi bersarang sebanyak jumlah kolom sprite (`c` berkisar dari `0` hingga `cols - 1`). |
| **17** | `frame = self.sheet.subsurface((c * self.fw, r * self.fh, self.fw, self.fh))` | Memotong bagian gambar tertentu menggunakan metode `.subsurface()` berdasarkan koordinat kotak pembatas: `(x_mulai, y_mulai, lebar, tinggi)`. Di mana `x_mulai = c * fw` dan `y_mulai = r * fh`. |
| **18** | `self.frames[r][c] = pygame.transform.scale(frame, (int(self.fw * self.scale), int(self.fh * self.scale)))` | Mengubah ukuran gambar hasil potongan (`frame`) sesuai dengan faktor skala yang diinginkan (dikonversi ke tipe data `int` karena ukuran piksel harus berupa bilangan bulat), lalu menyimpannya ke dalam matriks `self.frames` pada koordinat baris `r` dan kolom `c`. |
| **19** | *(Kosong)* | Baris kosong sebagai pemisah visual antar-metode. |
| **20** | `def get_frame(self, row, col):` | Mendefinisikan metode publik yang dapat dipanggil dari luar kelas untuk mengambil satu frame spesifik. |
| **21** | `return self.frames[row][col]` | Mengembalikan objek gambar (`pygame.Surface`) yang berada pada baris `row` dan kolom `col` dalam matriks `self.frames`. |
| **22** | *(Kosong)* | Baris kosong di akhir file sesuai dengan standar penulisan kode Python (PEP 8). |

---

## Alur Kerja Utama

Ketika kelas `Spritesheet` digunakan, berikut adalah alur kerja logisnya:

1.  **Inisialisasi (`__init__`)**: Objek dibuat dengan memberikan path gambar dan konfigurasi baris/kolom. Lebar dan tinggi tiap frame dihitung secara otomatis berdasarkan resolusi total gambar.
2.  **Pemotongan Gambar (`_slice`)**:
    *   Iterasi melintasi baris dan kolom.
    *   Fungsi `subsurface` digunakan untuk mengambil bagian gambar dari koordinat tertentu tanpa menyalin data piksel ke memori baru secara berlebihan (lebih efisien).
    *   Setiap potongan gambar langsung diubah ukurannya berdasarkan konstanta `scale`.
    *   Gambar hasil pemotongan disimpan di list dua dimensi `self.frames`.
3.  **Pengambilan Frame (`get_frame`)**: Ketika game sedang berjalan, komponen animasi akan memanggil fungsi ini secara terus-menerus berdasarkan indeks baris dan kolom yang diinginkan untuk menampilkan animasi berjalan, menyerang, atau diam.
