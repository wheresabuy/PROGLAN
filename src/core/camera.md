# Penjelasan Source Code: camera.py

Dokumen ini berisi penjelasan baris demi baris dari file `camera.py` yang digunakan untuk mengatur pergerakan kamera (viewport) pada game berbasis Pygame. Kamera ini berfungsi agar layar permainan mengikuti pergerakan karakter utama (player) dan membatasi pandangan agar tidak keluar dari peta (map).

---

## Deskripsi & Tujuan File
File `camera.py` mendefinisikan kelas `Camera`. Kelas ini bertanggung jawab untuk:
1. Menghitung posisi kamera berdasarkan posisi target (seperti koordinat pemain).
2. Memastikan kamera tetap berada di dalam batas-batas ukuran peta (*map boundaries*).
3. Menyesuaikan posisi gambar (*rendering position*) dari seluruh objek/entitas di dalam game ke layar (*viewport*) berdasarkan posisi kamera saat ini.

---

## Daftar Import (jika ada)

| Library | Deskripsi |
| :--- | :--- |
| `pygame` | Library utama untuk pengembangan game 2D di Python. Digunakan di sini untuk manipulasi objek segiempat (`pygame.Rect`). |

---

## Penjelasan Baris Demi Baris

Berikut adalah penjelasan detail dari setiap baris kode di dalam `camera.py`:

| Baris | Kode | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import pygame` | Mengimpor modul `pygame` untuk memanfaatkan fungsi/kelas yang disediakan seperti `pygame.Rect`. |
| **2** | *(Baris Kosong)* | Pemisah baris untuk estetika/keterbacaan kode sesuai standar PEP 8. |
| **3** | `class Camera:` | Mendefinisikan kelas bernama `Camera` yang akan menampung logika pergerakan kamera. |
| **4** | `    def __init__(self, width, height, map_width, map_height):` | Konstruktor kelas `Camera` yang menerima parameter: ukuran viewport/layar (`width`, `height`) serta ukuran peta permainan (`map_width`, `map_height`). |
| **5** | `        self.camera = pygame.Rect(0, 0, width, height)` | Menginisialisasi atribut `self.camera` sebagai objek `pygame.Rect` pada koordinat awal (0, 0) dengan lebar dan tinggi layar. |
| **6** | `        self.width = width` | Menyimpan lebar layar viewport ke dalam atribut objek (`self.width`). |
| **7** | `        self.height = height` | Menyimpan tinggi layar viewport ke dalam atribut objek (`self.height`). |
| **8** | `        self.map_width = map_width` | Menyimpan total lebar peta permainan ke dalam atribut objek (`self.map_width`). |
| **9** | `        self.map_height = map_height` | Menyimpan total tinggi peta permainan ke dalam atribut objek (`self.map_height`). |
| **10** | *(Baris Kosong)* | Pemisah baris antar metode dalam kelas. |
| **11** | `    def apply(self, entity_pos):` | Mendefinisikan metode `apply` yang berguna untuk mengubah posisi riil suatu objek di dunia game menjadi posisi relatif di layar monitor pengguna. |
| **12** | `        # Mengembalikan posisi yang sudah disesuaikan dengan kamera` | Komentar penjelasan fungsi metode `apply`. |
| **13** | `        if isinstance(entity_pos, pygame.Rect):` | Mengecek apakah parameter `entity_pos` bertipe `pygame.Rect` (objek kotak Pygame). |
| **14** | `            return entity_pos.move(self.camera.topleft)` | Jika bertipe `Rect`, mengembalikan objek `Rect` baru yang posisinya telah digeser sesuai koordinat kiri-atas (`topleft`) kamera. |
| **15** | `        return (entity_pos[0] + self.camera.x, entity_pos[1] + self.camera.y)` | Jika bertipe tuple/list koordinat `(x, y)`, mengembalikan koordinat baru yang dijumlahkan dengan posisi kamera saat ini (`self.camera.x` dan `self.camera.y`). |
| **16** | *(Baris Kosong)* | Pemisah baris antar metode dalam kelas. |
| **17** | `    def update(self, target_pos):` | Mendefinisikan metode `update` untuk memperbarui posisi kamera berdasarkan posisi target (biasanya karakter pemain). |
| **18** | `        # Mengikuti target (player)` | Komentar penjelasan fungsi metode `update`. |
| **19** | `        x = -target_pos[0] + int(self.width / 2)` | Menghitung posisi koordinat X kamera. Kita menggunakan nilai negatif dari target agar dunia game bergeser berlawanan arah dengan pergerakan karakter, dan menambahkan setengah lebar layar agar target berada di tengah. |
| **20** | `        y = -target_pos[1] + int(self.height / 2)` | Menghitung posisi koordinat Y kamera dengan prinsip yang sama seperti sumbu X agar target berada di tengah vertikal layar. |
| **21** | *(Baris Kosong)* | Pemisah baris untuk kerapian kode. |
| **22** | `        # Batasan kamera agar tidak keluar map` | Komentar penjelasan untuk pembatasan wilayah gerak kamera. |
| **23** | `        x = min(0, x) # kiri` | Menggunakan fungsi `min(0, x)` untuk memastikan nilai `x` tidak lebih dari `0` (mencegah kamera memperlihatkan area kosong di luar batas kiri peta). |
| **24** | `        y = min(0, y) # atas` | Menggunakan fungsi `min(0, y)` untuk memastikan nilai `y` tidak lebih dari `0` (mencegah kamera memperlihatkan area kosong di luar batas atas peta). |
| **25** | `        x = max(-(self.map_width - self.width), x) # kanan` | Memastikan kamera tidak bergeser terlalu jauh ke kanan melampaui lebar peta dikurangi lebar layar (batas kanan peta). |
| **26** | `        y = max(-(self.map_height - self.height), y) # bawah` | Memastikan kamera tidak bergeser terlalu jauh ke bawah melampaui tinggi peta dikurangi tinggi layar (batas bawah peta). |
| **27** | *(Baris Kosong)* | Pemisah baris untuk kerapian kode. |
| **28** | `        self.camera = pygame.Rect(x, y, self.width, self.height)` | Memperbarui objek Rect `self.camera` dengan posisi koordinat baru `x` dan `y` yang sudah disesuaikan dan dibatasi tersebut. |
| **29** | *(Baris Kosong)* | Akhir file / baris kosong di akhir dokumen. |

---

## Alur Kerja Utama

1. **Inisialisasi (`__init__`)**: Kamera dibuat dengan ukuran viewport tertentu (misalnya $800 \times 600$) dan batas ukuran peta (misalnya $2000 \times 2000$).
2. **Pembaruan Posisi (`update`)**: Di setiap frame game, posisi target (koordinat X dan Y pemain) dikirim ke metode `update`. Kamera akan dihitung posisinya agar target berada di tengah layar, kemudian posisi tersebut disesuaikan (dibatasi/clamped) agar kamera tidak menampilkan area di luar koordinat peta game.
3. **Penerapan Transformasi Kamera (`apply`)**: Saat melakukan *rendering* objek ke layar, metode `apply` dipanggil untuk setiap entitas agar koordinat aslinya diubah ke koordinat layar yang sesuai dengan pergeseran kamera saat itu.
