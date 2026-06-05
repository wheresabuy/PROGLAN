# Penjelasan Source Code: `loot.py`

Dokumen ini berisi penjelasan detail baris demi baris dari berkas source code `loot.py` yang mendefinisikan kelas `Loot` untuk entitas item rampasan/jarahan di dalam game menggunakan Pygame.

---

## Deskripsi & Tujuan File
Berkas `loot.py` mendefinisikan kelas `Loot` yang mewakili item atau barang jarahan (loot) di dalam game yang dapat diambil oleh pemain. Kelas ini bertanggung jawab atas:
1. Inisialisasi properti item (nama, posisi, tipe item, status pengambilan, dan petunjuk teks interaksi).
2. Pemuatan dan pemrosesan visual item (baik melalui path file, objek Surface yang sudah ada, atau warna cadangan).
3. Pendeteksian jarak interaksi antara pemain dan item menggunakan rumus jarak Euclidean.
4. Penggambaran item ke layar dengan animasi melayang (*hovering*) vertikal secara dinamis menggunakan gelombang sinus, serta integrasi dengan sistem kamera (jika ada).

---

## Daftar Import (jika ada)
Berikut adalah pustaka (library) yang diimpor dan digunakan dalam berkas ini:

* **`pygame`**: Pustaka utama untuk penanganan grafis, pembuatan Surface, transformasi visual, dan penanganan waktu permainan.
* **`math`**: Pustaka bawaan Python untuk fungsi matematika, digunakan fungsi `math.sin` untuk menghasilkan pergerakan naik-turun (melayang) secara berkala dan halus.

---

## Penjelasan Baris Demi Baris

| Nomor Baris | Kode | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import pygame` | Mengimpor pustaka Pygame untuk kebutuhan grafis dan visual game. |
| **2** | `import math` | Mengimpor modul matematika untuk menghitung efek gelombang sinus (melayang). |
| **3** | *(Baris Kosong)* | Baris kosong sebagai pemisah visual antar bagian kode. |
| **4** | `class Loot:` | Mendefinisikan kelas `Loot` untuk entitas item jarahan. |
| **5** | `def __init__(self, name, x, y, item_type, image=None, prompt=None):` | Konstruktor kelas untuk menginisialisasi atribut-atribut objek `Loot`. |
| **6** | `self.name = name` | Menyimpan nama item ke dalam variabel instance `self.name`. |
| **7** | `self.pos = (x, y)` | Menyimpan posisi koordinat item sebagai *tuple* `(x, y)` pada `self.pos`. |
| **8** | `self.item_type = item_type` | Menyimpan tipe item (misalnya untuk menentukan jenis item saat dimasukkan ke inventaris). |
| **9** | `self.prompt = prompt or f"Tekan [ENTER] untuk ambil {name}"` | Menentukan teks petunjuk interaksi. Menggunakan teks default jika parameter `prompt` tidak diberikan. |
| **10** | `self.collected = False` | Inisialisasi status pengambilan item menjadi `False` karena saat game dimulai item belum diambil. |
| **11** | `self.hover_offset = 0` | Menginisialisasi variabel penyimpangan posisi vertikal (untuk efek melayang). |
| **12** | *(Baris Kosong)* | Baris kosong pemisah. |
| **13** | `if image:` | Mengecek apakah parameter gambar `image` dikirim (bukan `None`). |
| **14** | `if isinstance(image, str): # Jika yang dikirim adalah path file` | Memeriksa apakah parameter `image` bertipe data string (menandakan path file). |
| **15** | `try:` | Memulai blok penanganan kesalahan (*try-except*) saat memuat gambar dari berkas eksternal. |
| **16** | `self.image = pygame.image.load(image).convert_alpha()` | Memuat gambar dari path dan mengonversinya ke format piksel yang dioptimalkan dengan transparansi alpha. |
| **17** | `self.image = pygame.transform.scale(self.image, (64, 64))` | Mengubah ukuran gambar yang dimuat menjadi 64x64 piksel. |
| **18** | `except Exception as e:` | Blok yang menangani jika terjadi kesalahan saat memuat gambar (misal file tidak ditemukan). |
| **19** | `self.image = pygame.Surface((40, 40))` | Membuat Surface default berukuran 40x40 piksel sebagai cadangan jika terjadi kesalahan. |
| **20** | `self.image.fill((255, 0, 0))` | Mengisi Surface cadangan tersebut dengan warna merah polos (RGB: 255, 0, 0). |
| **21** | `else: # Jika yang dikirim adalah object Surface (hasil slicing)` | Blok jika `image` yang dikirim bukan string melainkan langsung objek `pygame.Surface` (hasil pemotongan spritesheet). |
| **22** | `self.image = pygame.transform.scale(image, (64, 64))` | Mengubah ukuran objek `Surface` tersebut menjadi 64x64 piksel. |
| **23** | `else:` | Blok alternatif jika parameter `image` bernilai `None` (tidak disertakan saat instansiasi). |
| **24** | `self.image = pygame.Surface((40, 40))` | Membuat Surface kosong berukuran 40x40 piksel sebagai visual default. |
| **25** | `self.image.fill((255, 215, 0))` | Mewarnai Surface default dengan warna kuning emas (RGB: 255, 215, 0). |
| **26** | *(Baris Kosong)* | Baris kosong pemisah. |
| **27** | `self.rect = self.image.get_rect(topleft=(x, y))` | Mendapatkan objek persegi pembatas (`pygame.Rect`) dari gambar dan menempatkannya di koordinat `(x, y)`. |
| **28** | *(Baris Kosong)* | Baris kosong pemisah. |
| **29** | `def check_interaction(self, player_pos):` | Metode untuk memeriksa apakah pemain berada cukup dekat untuk berinteraksi/mengambil item. |
| **30** | `dx = self.pos[0] - player_pos[0]` | Menghitung jarak horizontal antara item dan posisi pemain. |
| **31** | `dy = self.pos[1] - player_pos[1]` | Menghitung jarak vertikal antara item dan posisi pemain. |
| **32** | `return (dx**2 + dy**2)**0.5 < 100` | Menghitung jarak lurus (Euclidean). Mengembalikan `True` jika jarak pemain kurang dari 100 piksel, dan `False` jika tidak. |
| **33** | *(Baris Kosong)* | Baris kosong pemisah. |
| **34** | `def get_interaction_prompt(self):` | Metode untuk mengambil string petunjuk pengambilan item. |
| **35** | `return self.prompt` | Mengembalikan nilai dari variabel `self.prompt`. |
| **36** | *(Baris Kosong)* | Baris kosong pemisah. |
| **37** | `def draw(self, screen, player_pos, camera=None):` | Metode untuk menggambar item ke layar. Menerima layar tujuan, posisi pemain, dan sistem kamera opsional. |
| **38** | `if not self.collected:` | Memeriksa apakah item belum diambil. Item hanya akan dirender jika nilai `self.collected` adalah `False`. |
| **39** | `self.hover_offset = math.sin(pygame.time.get_ticks() * 0.005) * 10` | Menghitung efek naik-turun menggunakan fungsi sinus berdasarkan waktu berjalan game dalam milidetik. Menghasilkan animasi melayang lembut dengan tinggi simpangan sebesar 10 piksel. |
| **40** | `draw_pos = self.pos` | Menentukan posisi render dasar sesuai posisi asli item. |
| **41** | `if camera:` | Memeriksa apakah parameter kamera aktif diberikan. |
| **42** | `draw_pos = camera.apply(self.pos)` | Menyesuaikan posisi gambar item di layar relatif terhadap pergeseran kamera saat peta bergulir. |
| **43** | `screen.blit(self.image, (draw_pos[0], draw_pos[1] + self.hover_offset))` | Merender gambar item ke layar (`screen`) pada koordinat X yang sesuai dan koordinat Y yang telah ditambahkan dengan efek melayang. |

---

## Alur Kerja Utama
1. **Inisialisasi Objek**: Ketika game memuat peta atau musuh menjatuhkan item, objek `Loot` dibuat. Sistem memuat gambar item (atau menggunakan fallback merah/kuning emas jika gambar gagal dimuat/tidak disediakan) dan menaruhnya pada koordinat tertentu.
2. **Pemeriksaan Kedekatan Pemain**: Di setiap frame permainan, posisi pemain dibandingkan dengan posisi item. Jika jarak pemain berada dalam radius 100 piksel, game akan tahu bahwa pemain bisa berinteraksi untuk mengambil item dan dapat memunculkan petunjuk teks (`self.prompt`).
3. **Penggambaran & Animasi**: Selama item belum diambil (`self.collected == False`), item akan terus digambar di layar. Animasi melayang dihitung secara dinamis di setiap frame menggunakan waktu sistem (`pygame.time.get_ticks()`) dan fungsi sinus (`math.sin`), memberikan efek visual menarik yang memperjelas keberadaan item tersebut kepada pemain. Jika ada kamera, posisinya disesuaikan agar item tetap berada di tempatnya di dunia game saat kamera bergeser.
