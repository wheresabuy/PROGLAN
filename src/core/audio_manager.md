# Penjelasan Baris Demi Baris: `audio_manager.py`

Dokumen ini memberikan penjelasan mendetail tentang kode program di dalam berkas `/home/abuyyy/PemogramanLanjut/src/core/audio_manager.py` untuk membantu persiapan demo proyek game Anda.

---

## 1. Deskripsi & Tujuan File

Berkas `audio_manager.py` mendefinisikan kelas **`AudioManager`** yang berfungsi sebagai pengelola suara (audio) dalam game. Pengelolaan audio ini dibagi menjadi dua bagian:
- **BGM (Background Music)**: Musik latar belakang berdurasi panjang yang umumnya diputar secara berulang (*looping*).
- **SFX (Sound Effects)**: Efek suara pendek (seperti saat memungut item, suara tembakan, atau flashbang) yang diputar satu kali dan bisa bertumpuk (*overlapping*) dengan suara lain.

Penggunaan kelas ini memudahkan pengaturan volume, menghentikan musik latar, dan mencegah lagu yang sama dimuat ulang dari awal secara tidak sengaja ketika sedang diputar.

---

## 2. Daftar Import

```python
1: import pygame
2: import os
```

- **`pygame` (Baris 1)**: Pustaka utama yang digunakan untuk pengembangan game. Sub-modul `pygame.mixer` digunakan di dalam kelas ini untuk memproses pemutaran audio digital.
- **`os` (Baris 2)**: Pustaka bawaan (*built-in*) Python untuk interaksi dengan sistem operasi (misalnya manajemen direktori/berkas). Pada file ini diimpor namun belum digunakan secara aktif.

---

## 3. Penjelasan Baris Demi Baris

Berikut adalah tabel penjelasan untuk setiap baris kode pada berkas `audio_manager.py`:

| Baris | Kode Sumber | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import pygame` | Mengimpor pustaka Pygame untuk menangani multimedia game, termasuk audio. |
| **2** | `import os` | Mengimpor modul `os` bawaan Python untuk operasi sistem (misalnya manipulasi path/berkas). |
| **3** | *(Baris Kosong)* | Digunakan sebagai pemisah visual demi keterbacaan kode (sesuai standar PEP 8). |
| **4** | `class AudioManager:` | Mendefinisikan kelas `AudioManager` yang membungkus semua fungsi audio. |
| **5** | `    def __init__(self):` | Konstruktor kelas. Dipanggil secara otomatis saat objek/instance baru dari kelas ini dibuat. |
| **6** | `        pygame.mixer.init()` | Menginisialisasi modul mixer audio Pygame agar fungsi pemutaran suara siap dijalankan. |
| **7** | `        self.bgm_volume = 0.5` | Menentukan volume awal default untuk musik latar belakang (BGM) sebesar `0.5` (skala `0.0` sampai `1.0`). |
| **8** | `        self.sfx_volume = 0.7` | Menentukan volume awal default untuk efek suara pendek (SFX) sebesar `0.7` (skala `0.0` sampai `1.0`). |
| **9** | `        self.current_bgm = None` | Inisialisasi variabel untuk mencatat berkas musik latar yang sedang diputar (awal mula bernilai `None`). |
| **10** | *(Baris Kosong)* | Pemisah visual antara metode inisialisasi dengan metode pemutar BGM. |
| **11** | `    def play_bgm(self, filename, loops=-1):` | Mendefinisikan metode `play_bgm` untuk memutar musik latar. Menerima parameter `filename` (berkas suara) dan `loops` (default `-1` untuk mengulang tanpa batas). |
| **12** | `        """Memutar musik latar. loops=-1 berarti looping selamanya."""` | *Docstring* (dokumentasi teks) untuk menjelaskan perilaku dari metode `play_bgm`. |
| **13** | `        try:` | Memulai blok pemeriksaan kesalahan `try-except` agar game tidak mendadak keluar/crash bila berkas musik tidak ditemukan atau rusak. |
| **14** | `            if self.current_bgm == filename:` | Memeriksa apakah berkas lagu yang ingin dimainkan sama dengan lagu yang saat ini sedang aktif berbunyi. |
| **15** | `                return` | Jika lagunya sama, fungsi langsung selesai (`return`) agar pemutaran tidak terinterupsi atau terulang dari awal. |
| **16** | `            pygame.mixer.music.load(filename)` | Memuat berkas audio dari lokasi `filename` ke mixer streaming musik latar Pygame. |
| **17** | `            pygame.mixer.music.set_volume(self.bgm_volume)` | Mengatur kekerasan suara pemutaran musik latar sesuai nilai volume global `self.bgm_volume`. |
| **18** | `            pygame.mixer.music.play(loops)` | Memulai pemutaran musik latar sebanyak `loops` kali. |
| **19** | `            self.current_bgm = filename` | Menyimpan nama berkas musik latar yang baru saja dimuat ke dalam penanda lagu aktif `self.current_bgm`. |
| **20** | `        except Exception as e:` | Menangkap semua bentuk galat/kesalahan yang terjadi selama proses pemuatan dan pemutaran BGM. |
| **21** | `            print(f"Error playing BGM {filename}: {e}")` | Mencetak pesan kegagalan pemutaran musik latar ke terminal untuk keperluan debugging. |
| **22** | *(Baris Kosong)* | Pemisah visual antar metode dalam kelas. |
| **23** | `def stop_bgm(self):` | Mendefinisikan metode `stop_bgm` untuk menghentikan pemutaran musik latar secara paksa. |
| **24** | `        pygame.mixer.music.stop()` | Menghentikan aliran musik latar yang sedang diputar oleh Pygame. |
| **25** | `        self.current_bgm = None` | Menghapus penanda lagu aktif dengan menyetel nilainya kembali ke `None`. |
| **26** | *(Baris Kosong)* | Pemisah visual antar metode dalam kelas. |
| **27** | `    def play_sfx(self, filename):` | Mendefinisikan metode `play_sfx` untuk memutar efek suara pendek secara langsung dengan input berupa lokasi berkas suara. |
| **28** | `        """Memutar efek suara sekali (misal: ambil item, flashbang)."""` | *Docstring* penjelasan singkat mengenai metode `play_sfx`. |
| **29** | `        try:` | Memulai blok pengaman `try-except` untuk menangkap potensi galat ketika memuat berkas suara efek. |
| **30** | `            sound = pygame.mixer.Sound(filename)` | Membuat objek kelas `Sound` Pygame dari berkas audio. Objek ini disimpan sepenuhnya di memori RAM agar bisa diputar instan. |
| **31** | `            sound.set_volume(self.sfx_volume)` | Mengatur kekerasan efek suara individual ini berdasarkan volume efek suara global `self.sfx_volume`. |
| **32** | `            sound.play()` | Memainkan suara pendek tersebut sekali. Pemutaran ini bersifat asinkron (tidak menahan proses game lain). |
| **33** | `        except Exception as e:` | Menangkap galat jika pembuatan objek suara atau pemutarannya bermasalah. |
| **34** | `            print(f"Error playing SFX {filename}: {e}")` | Mencetak pesan galat pemutaran efek suara pendek ke terminal. |
| **35** | *(Baris Kosong)* | Pemisah visual antar metode dalam kelas. |
| **36** | `    def set_volumes(self, bgm_vol, sfx_vol):` | Mendefinisikan metode `set_volumes` guna memperbarui volume audio global (BGM dan SFX) secara dinamis. |
| **37** | `        self.bgm_volume = bgm_vol` | Memperbarui variabel penampung volume musik latar belakang dengan nilai baru `bgm_vol`. |
| **38** | `        self.sfx_volume = sfx_vol` | Memperbarui variabel penampung volume efek suara dengan nilai baru `sfx_vol`. |
| **39** | `        pygame.mixer.music.set_volume(bgm_vol)` | Menerapkan volume baru tersebut secara langsung pada musik latar (BGM) yang saat ini sedang aktif dimainkan. |
| **40** | *(Baris Kosong)* | Baris kosong akhir berkas sebagai standar kebersihan kode program Python. |

---

## 4. Alur Kerja Utama

1. **Inisialisasi Sistem Suara (`__init__`)**:
   Ketika objek `AudioManager` dibuat pertama kali, sistem audio Pygame (`pygame.mixer`) dinyalakan. Volume musik latar disetel ke `0.5` dan efek suara ke `0.7`.
   
2. **Memutar Musik Latar (`play_bgm`)**:
   Metode ini memeriksa apakah lagu yang diminta sudah dimainkan. Jika belum, lagu baru akan dimuat ke memori streaming, disetel volumenya, diputar (biasanya berulang tanpa henti), dan namanya dicatat pada status sistem.
   
3. **Memutar Efek Suara (`play_sfx`)**:
   Efek suara langsung dibuat sebagai objek `Sound` terpisah di memori dan diputar sekali. Karena sifatnya asinkron, beberapa efek suara dapat berbunyi bersamaan di waktu yang sama (misal suara tembakan beruntun).

4. **Pengaturan Volume Dinamis (`set_volumes`)**:
   Jika pengguna mengubah volume di pengaturan menu game, metode ini dipanggil untuk memperbarui volume BGM yang sedang berjalan serta volume SFX untuk pemutaran selanjutnya.
