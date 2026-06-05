# Penjelasan Tactical Item (`tactical_item.py`)

Dokumen ini berisi penjelasan baris demi baris mengenai modul `tactical_item.py` yang mendefinisikan perilaku dan visualisasi item taktis dalam permainan.

---

## Deskripsi & Tujuan File
File `tactical_item.py` mendefinisikan kelas `TacticalItem`. Kelas ini digunakan untuk mengelola berbagai jenis item taktis (seperti **Molotov**, **Decoy**, dan **Taser**) yang dapat dilempar atau digunakan oleh pemain. Kelas ini bertanggung jawab atas pergerakan item menuju posisi target, melacak durasi aktif item menggunakan penghitung waktu (timer), serta menggambar visualisasi efek masing-masing item di layar permainan.

---

## Daftar Import
File ini mengimpor beberapa modul standar dan pustaka eksternal:
*   `import pygame`: Pustaka utama untuk penanganan grafis 2D, yang digunakan di sini untuk menggambar lingkaran, garis, dan mengelola representasi visual dari setiap item taktis.
*   `import math`: Modul matematika bawaan Python yang digunakan untuk menghitung jarak geometris (`math.hypot`) guna menggerakkan item taktis secara presisi ke koordinat target.

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel penjelasan untuk setiap baris kode di dalam berkas `tactical_item.py`:

| No. Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| **1** | `import pygame` | Mengimpor pustaka Pygame untuk menangani kebutuhan rendering grafis permainan. |
| **2** | `import math` | Mengimpor pustaka matematika Python untuk menghitung jarak pergerakan item. |
| **3** | *(Baris Kosong)* | Pemisah visual antara bagian import dan definisi kelas. |
| **4** | `class TacticalItem:` | Mendefinisikan kelas `TacticalItem` sebagai cetak biru untuk objek item taktis. |
| **5** | `    def __init__(self, x, y, item_type, target_pos=None):` | Konstruktor kelas untuk membuat objek item taktis baru dengan posisi awal `(x, y)`, jenis item `item_type`, dan posisi target `target_pos` (jika ada/dilempar). |
| **6** | `        self.pos = [x, y]` | Menyimpan posisi koordinat saat ini dalam tipe list `[x, y]` agar nilainya mudah diperbarui saat item bergerak. |
| **7** | `        self.item_type = item_type` | Menyimpan tipe item taktis yang bersangkutan (misalnya: `"Molotov"`, `"Decoy"`, atau `"Taser"`). |
| **8** | `        self.timer = 0` | Menginisialisasi penghitung frame/waktu untuk membatasi durasi aktif item. |
| **9** | `        self.active = True` | Status keaktifan item. Jika bernilai `False`, item akan dihapus dari permainan oleh manajer objek. |
| **10** | `        self.target_pos = target_pos # Untuk item yang dilempar` | Menyimpan posisi tujuan pendaratan/target lemparan dari item tersebut. |
| **11** | `        self.speed = 8` | Menentukan kecepatan terbang item menuju target sebesar 8 piksel per frame. |
| **12** | `        self.reached_target = False if target_pos else True` | Menentukan status apakah item sudah sampai ke target. Jika item dilempar (memiliki `target_pos`), status diatur ke `False`, selain itu langsung `True`. |
| **13** | *(Baris Kosong)* | Pemisah visual sebelum definisi metode `update`. |
| **14** | `    def update(self):` | Metode pembaruan berkala (per frame) untuk menghitung pergerakan dan durasi aktif item. |
| **15** | `        if not self.reached_target and self.target_pos:` | Memeriksa apakah item belum sampai di tujuan tetapi memiliki target posisi yang dituju. |
| **16** | `            dx = self.target_pos[0] - self.pos[0]` | Menghitung jarak horizontal (selisih sumbu X) antara posisi target dan posisi item saat ini. |
| **17** | `            dy = self.target_pos[1] - self.pos[1]` | Menghitung jarak vertikal (selisih sumbu Y) antara posisi target dan posisi item saat ini. |
| **18** | `            dist = math.hypot(dx, dy)` | Menghitung jarak garis lurus (sisi miring segitiga) menggunakan rumus Pythagoras. |
| **19** | `            if dist < self.speed:` | Memeriksa jika jarak tersisa ke target lebih kecil dari kecepatan pergerakan item. |
| **20** | `                self.pos = list(self.target_pos)` | Jika sangat dekat, posisikan item tepat pada koordinat target untuk akurasi. |
| **21** | `                self.reached_target = True` | Mengubah status `reached_target` menjadi `True` menandakan item sudah sampai. |
| **22** | `            else:` | Blok alternatif jika jarak ke target masih lebih besar dari kecepatan item. |
| **23** | `                self.pos[0] += (dx / dist) * self.speed` | Menggerakkan koordinat X item mendekati target secara proporsional. |
| **24** | `                self.pos[1] += (dy / dist) * self.speed` | Menggerakkan koordinat Y item mendekati target secara proporsional. |
| **25** | *(Baris Kosong)* | Pemisah visual di dalam fungsi `update`. |
| **26** | `        self.timer += 1` | Menambahkan nilai penghitung waktu (timer) sebanyak 1 unit pada setiap frame. |
| **27** | *(Baris Kosong)* | Pemisah visual sebelum pemeriksaan jenis item. |
| **28** | `        # Durasi item` | Komentar penjelasan untuk logika penentuan batas durasi aktif setiap jenis item taktis. |
| **29** | `        if self.item_type == "Molotov":` | Kondisi khusus jika item tersebut adalah bom molotov. |
| **30** | `            if self.timer > 180: self.active = False # 3 detik api` | Molotov akan mati (`active = False`) jika timer melebihi 180 frame (sekitar 3 detik pada 60 FPS). |
| **31** | `        elif self.item_type == "Decoy":` | Kondisi khusus jika item tersebut adalah alat umpan (Decoy). |
| **32** | `            if self.timer > 600: self.active = False # 10 detik umpan` | Decoy akan mati jika timer melebihi 600 frame (sekitar 10 detik pada 60 FPS). |
| **33** | `        elif self.item_type == "Taser":` | Kondisi khusus jika item tersebut adalah alat kejut listrik (Taser). |
| **34** | `            if self.timer > 10: self.active = False # Sekejap` | Taser akan mati dengan sangat cepat setelah 10 frame karena hanya memberikan sengatan instan. |
| **35** | *(Baris Kosong)* | Pemisah visual sebelum definisi metode `draw`. |
| **36** | `    def draw(self, screen, camera):` | Metode untuk merender (menggambar) visualisasi item taktis pada layar. |
| **37** | `        draw_pos = camera.apply(self.pos)` | Menyesuaikan posisi koordinat dunia/map item dengan posisi kamera layar saat ini. |
| **38** | `        if self.item_type == "Molotov" and self.reached_target:` | Memeriksa apakah item adalah Molotov dan sudah mendarat di target untuk menampilkan efek area terbakar. |
| **39** | `            # Gambar api (lingkaran berkedip)` | Komentar penjelasan bahwa efek api digambar menggunakan lingkaran yang berkedip. |
| **40** | `            color = (255, 100, 0) if self.timer % 10 < 5 else (255, 200, 0)` | Mengubah warna lingkaran secara dinamis antara warna oranye kemerahan dan oranye kekuningan setiap 5 frame untuk memberi efek api yang berkedip. |
| **41** | `            pygame.draw.circle(screen, color, draw_pos, 50, 0)` | Menggambar lingkaran area api dengan radius 50 piksel pada layar. |
| **42** | `        elif self.item_type == "Decoy":` | Memeriksa jika tipe item yang sedang di-render adalah Decoy. |
| **43** | `            # Gambar gadget berkedip biru` | Komentar penjelasan bahwa visualisasi Decoy adalah gadget kecil berkedip biru. |
| **44** | `            color = (0, 0, 255) if self.timer % 20 < 10 else (100, 100, 255)` | Mengubah warna gadget secara berkala setiap 10 frame antara biru pekat dan biru terang agar terlihat berkedip. |
| **45** | `            pygame.draw.circle(screen, color, draw_pos, 10, 0)` | Menggambar badan fisik gadget Decoy berupa lingkaran kecil dengan radius 10 piksel. |
| **46** | `            # Gelombang suara` | Komentar penjelasan untuk visualisasi pancaran suara dari Decoy. |
| **47** | `            pygame.draw.circle(screen, color, draw_pos, (self.timer % 40) * 2, 1)` | Menggambar lingkaran tipis (outline) yang radiusnya terus membesar secara berkala untuk mensimulasikan riak gelombang suara palsu. |
| **48** | `        elif self.item_type == "Taser":` | Memeriksa jika tipe item yang di-render adalah efek kejut listrik (Taser). |
| **49** | `            # Efek setrum petir` | Komentar penjelasan bahwa visualisasi taser menggunakan efek sambaran kilat/petir kecil. |
| **50** | `            pygame.draw.line(screen, (255, 255, 255), draw_pos, (draw_pos[0]+10, draw_pos[1]-10), 2)` | Menggambar garis putih tipis sepanjang 10 piksel secara diagonal dengan ketebalan 2 piksel untuk mensimulasikan kilatan listrik kejut. |
| **51** | *(Baris Kosong)* | Akhir dari berkas kode sumber. |

---

## Alur Kerja Utama

1.  **Inisialisasi (`__init__`)**: Objek dibuat dengan koordinat asal `(x, y)` dan jenis item tertentu. Jika memiliki `target_pos`, status `reached_target` akan diatur sebagai `False`.
2.  **Pembaruan Status (`update`)**:
    *   Jika item belum mencapai tujuannya (`reached_target` bernilai `False`), ia akan terus terbang lurus secara bertahap menuju target tujuan (`target_pos`) menggunakan fungsi trigonometri (`math.hypot`).
    *   Setiap frame, variabel `timer` bertambah. Ketika durasi aktif untuk jenis item tersebut terlewati (Molotov: 180 frame, Decoy: 600 frame, Taser: 10 frame), status `active` diubah menjadi `False` agar permainan tahu bahwa item ini harus dihapus dari daftar entitas aktif.
3.  **Penggambaran Visual (`draw`)**:
    *   Posisi item diubah ke koordinat layar permainan menggunakan kamera (`camera.apply`).
    *   Setiap jenis item digambar dengan gaya visual unik:
        *   **Molotov**: Lingkaran api besar (radius 50) yang warnanya berkedip-kedip oranye/kuning (hanya digambar setelah mendarat di target).
        *   **Decoy**: Titik gadget kecil (radius 10) berwarna biru berkedip beserta riak lingkaran gelombang suara yang membesar di sekitarnya.
        *   **Taser**: Garis diagonal berwarna putih yang mensimulasikan percikan/sengatan listrik sesaat.
