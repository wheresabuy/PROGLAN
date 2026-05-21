# 🧟 Project 23: The Survival - Hybrid AI-Gesture Action RPG 🎮

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pygame](https://img.shields.io/badge/Engine-Pygame-green)
![OpenCV](https://img.shields.io/badge/Vision-OpenCV%20%7C%20Mediapipe-red)
![ML](https://img.shields.io/badge/AI-Random%20Forest-orange)

**Project 23** adalah sebuah game survival post-apocalyptic yang menggabungkan mekanisme RPG tradisional dengan teknologi **Computer Vision** masa kini. Bertahan hidup di dunia yang dipenuhi zombie bukan lagi sekadar menekan tombol, tapi juga menggunakan gerakan tangan nyata Anda.

---

## 🌌 Latar Belakang Cerita
Dunia telah runtuh. Sebuah virus misterius bernama "23" telah mengubah mayoritas populasi menjadi makhluk haus darah. Anda berperan sebagai penyintas yang harus melewati berbagai zona bahaya—mulai dari reruntuhan kota hingga terowongan Metro yang gelap—demi mencapai satu-satunya tempat aman yang tersisa: **The Sanctuary**.

---

## 🌟 Fitur Utama

### 1. 🖐️ Hybrid ML Gesture Control
Game ini menggunakan **Hand Tracking** tingkat lanjut yang ditenagai oleh **Mediapipe** dan model **Random Forest Classifier**.
- **Position Invariant**: Berkat teknologi *Relative Landmarks*, sistem tetap akurat meskipun Anda menjauh atau mendekat ke kamera.
- **Multi-threaded**: Proses deteksi AI berjalan di thread terpisah, memastikan frame rate game tetap mulus (60 FPS).
- **Custom Training**: Developer dapat melatih gestur baru hanya dalam hitungan menit.

### 2. 🛠️ Sistem Crafting Tingkat Lanjut
Lebih dari 25+ resep rahasia untuk bertahan hidup. Campurkan item yang Anda temukan di dunia untuk membuat peralatan tempur:
- **Offensive**: Molotov, Granat Kimia, Acid Blade, Bom Serpihan.
- **Defensive**: Armor Diperkuat, Shock Armor (menyetrum zombie yang menggigit), Sepatu Senyap.
- **Survival**: Obor Darurat, Ghillie Suit (kamuflase), Stimulan Adrenalin.
- **Electronics**: Umpan Elektronik (Decoy), Hacking Tool, Remote Detonator.

### 3. 🧠 AI Zombie & Tactical Gameplay
Zombie dalam Project 23 tidak hanya berjalan lurus. Mereka bereaksi terhadap:
- **Suara**: Berlari saat Anda sprint (Shift) atau mendengar suara Umpan Elektronik.
- **Api**: Panik dan terhenti saat terkena Molotov.
- **Listrik**: Menjadi kaku (stun) jika terkena Taser atau jebakan listrik.

### 4. 🎭 Sistem Narasi & UI Interaktif
- **Dialogue System**: Cerita yang mendalam dengan kotak dialog interaktif.
- **Journal & Codex**: Catat misi Anda dan temukan lore setiap item yang Anda kumpulkan.
- **Dynamic HUD**: Pantau kesehatan, stamina, dan status misi secara real-time.
- **Visual Effects**: Sistem kegelapan dinamis dengan senter yang memiliki jangkauan terbatas.

---

## 📂 Struktur Proyek

| Folder | Deskripsi |
| :--- | :--- |
| `main.py` | Entry point utama. Mengatur inisialisasi game dan thread AI. |
| `comvis/` | Modul Computer Vision: deteksi, perekaman data, dan pelatihan model. |
| `src/core/` | Engine utama: Crafting, Mission Manager, Camera, Audio, dan Visual Effects. |
| `src/entities/` | Logika Player, NPC Zombie, Loot, dan Tactical Items. |
| `src/ui/` | Seluruh komponen interface (Inventory, Journal, Dialogue Box, HUD). |
| `assets/` | Koleksi aset pixel art, audio SFX, dan musik latar (BGM). |

---

## 🛠️ Panduan Instalasi

### 1. Prasyarat
- Python 3.10 atau lebih tinggi.
- Kamera (Webcam Laptop atau IP Webcam di Android).

### 2. Setup Lingkungan
```bash
# Clone repository
git clone git@github.com:wheresabuy/PROGLAN.git
cd PemogramanLanjut

# Buat Virtual Environment
python -m venv venv

# Aktivasi Venv
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt
```

---

## 🎮 Cara Bermain

### Konfigurasi Kamera
Jika menggunakan HP sebagai kamera (IP Webcam), ubah URL di `main.py`:
```python
# main.py
camera_path = "http://192.168.1.5:8080/video" # Sesuaikan IP Anda
```

### Mapping Gestur (Default)
| Gestur | Aksi |
| :--- | :--- |
| **Tangan Terbuka** | Idle / Berhenti |
| **Telunjuk ke Atas** | Gerak Atas |
| **Telunjuk ke Bawah** | Gerak Bawah |
| **Telunjuk ke Kiri/Kanan** | Gerak Kiri / Kanan |
| **Mengepal** | Ambil Item / Lanjut Dialog |

### Kontrol Keyboard (Manual)
- **Panah**: Bergerak
- **Shift (Tahan)**: Lari (Sprint)
- **Enter / Space**: Interaksi / Ambil
- **I**: Buka Inventori
- **J**: Buka Jurnal
- **F**: Nyalakan/Matikan Senter
- **C**: Crafting Menu (via Item Codex)

---

## 🎓 Panduan Pengembang: Melatih AI Baru

Anda bisa menambahkan gestur kustom sendiri dengan mudah:

1. **Rekam Data**: Jalankan `python comvis/train_data.py`.
   - Tekan `L` untuk memberi label (misal: `RELOAD`).
   - Tekan `S` untuk mulai merekam landmarks tangan Anda.
2. **Latih Model**: Jalankan `python comvis/train_model.py`. Script ini akan menghasilkan file `gesture_model.pkl` yang baru.
3. **Implementasi**: Tambahkan label baru tersebut ke dalam logika kontrol di `main.py`.

---

## 📜 Lisensi & Penulis
Dibuat dengan dedikasi untuk **Tugas Besar Pemrograman Lanjut**.

**Author:** [wheresabuy](https://github.com/wheresabuy)
**Special Thanks:**
- Mana Seed (Pixel Art Assets)
- Mediapipe Community (Hand Tracking API)

---
*Stay quiet. Stay alert. Survive.* 🧟‍♂️🔦

## 🛠️ Technical Deep Dive: Analisis Kode & Arsitektur

Project ini menggunakan arsitektur modular di mana setiap file memiliki tanggung jawab spesifik. Berikut adalah rincian fungsionalitas dan highlight baris kode krusial:

### 🧠 1. Modul Computer Vision (`comvis/`)
Modul ini adalah "mata" dari game, bertanggung jawab atas interaksi gestur.

- **`gestures.py`**: Berisi thread utama pengenalan gestur.
  - *Crucial Logic*: Penggunaan `threading.Lock()` untuk sinkronisasi data antar thread.
  ```python
  @property
  def current_gesture(self):
      with self._lock: # Mencegah race condition saat diakses game loop
          return self._current_gesture
  ```
- **`train_data.py`**: Alat untuk merekam koordinat koordinat tangan (landmarks) ke file CSV.
- **`train_model.py`**: Melatih model AI menggunakan algoritma **Random Forest** dari `scikit-learn`.
- **`reset_data.py`**: Membersihkan dataset untuk pelatihan ulang.

### 🏗️ 2. Mesin Inti (`src/core/`)
Jantung dari logika permainan, mengelola sistem global.

- **`crafting_system.py`**: Mengelola resep item menggunakan `frozenset` untuk pencocokan bahan tanpa urutan.
  - *Crucial Logic*: `frozenset([bahan1, bahan2])` memungkinkan crafting berhasil meskipun urutan klik pemain berbeda.
- **`mission_manager.py`**: State machine yang mengontrol transisi antar misi (Misi 1 ke Misi 2, dst).
- **`smart_slicer.py`**: Slicer aset yang canggih menggunakan algoritma **Flood Fill** untuk mendeteksi "pulau" pixel non-transparan secara otomatis.
  ```python
  def _find_bounding_box(self, start_x, start_y, visited):
      # Algoritma Flood Fill untuk auto-detect bounding box item pixel-art
  ```
- **`visual_effects.py`**: Mengelola sistem kegelapan dinamis, guncangan layar (shake), dan flash visual.
- **`camera.py`**: Sistem kamera 2D yang mengikuti pemain dengan pembatasan (clamping) di tepi peta.
- **`spritesheet.py`**: Memotong gambar spritesheet standar menjadi frame-frame animasi.
- **`audio_manager.py`**: Mixer suara untuk background music (BGM) dan efek suara (SFX).

### 👥 3. Entitas & Objek (`src/entities/`)
Mendefinisikan perilaku makhluk dan benda di dunia game.

- **`player.py`**: Mengelola status pemain (HP, Stamina), animasi, dan pergerakan yang kini telah di-*harden* dengan world-boundary clamping.
- **`zombie.py`**: AI musuh yang memiliki mekanisme "Dengar" dan "Lihat".
  - *Crucial Logic*: Zombie beralih dari mode `stand` ke `walk` jika mendengar suara lari atau decoy elektronik.
- **`tactical_item.py`**: Logika untuk item yang dilempar/dipasang seperti Molotov dan Taser.
- **`loot.py`**: Definisi item yang bisa diambil di map dengan deteksi jarak interaksi.

### 🖥️ 4. Antarmuka Pengguna (`src/ui/`)
Seluruh sistem HUD dan Menu.

- **`inventory.py`**: Sistem grid inventori yang mendukung navigasi gestur dan selection logic untuk crafting.
- **`item_codex.py`**: Database internal untuk memberikan info rarity dan kegunaan setiap item.
- **`dialogue.py`**: Kotak dialog naratif yang mendukung mode "Thinking" (saat memanggil AI).
- **`journal.py`**: Mencatat setiap progres misi agar pemain tidak tersesat.
- **`hud.py`**: Menampilkan bar HP, Baterai, dan animasi smooth pada perolehan mata uang.
- **`text_input.py`**: Komponen UI untuk input teks, digunakan pada puzzle atau interaksi khusus.

---
*Dibuat oleh wheresabuy - Dokumentasi teknis versi 2.1*

## 🧩 Arsitektur Modular: Mengapa File Bisa Terhubung?

Mungkin kamu bertanya-tanya, bagaimana file di `src/core/` bisa tahu apa yang terjadi di `src/entities/`? Project ini menggunakan pola **Modular Package & Composition**:

### 1. Sistem Package Python
Setiap folder di dalam `src/` memiliki file `__init__.py`. Ini memberi tahu Python bahwa folder tersebut adalah sebuah **Package**. Dengan ini, kita bisa melakukan import seperti:
```python
from src.entities.player import Player
```
Artinya: "Pergi ke folder `src`, masuk ke folder `entities`, buka file `player.py`, dan ambil class `Player`."

### 2. Pola Komposisi (Composition)
Di dalam `main.py`, kita tidak membuat satu file raksasa. Sebaliknya, `main.py` bertindak sebagai **Manager** yang menyatukan "potongan puzzle":
- Ia mengambil sistem kamera dari `core`.
- Ia mengambil logika pemain dari `entities`.
- Ia mengambil tampilan dari `ui`.
Semua objek ini kemudian dimasukkan ke dalam **Game Loop** utama untuk saling berinteraksi.

---

## 🏃 Logika Animasi: Bagaimana Sprite Bergerak?

Animasi dalam game ini tidak menggunakan file video, melainkan **Frame-based Sprite Slicing**. Berikut logikanya:

### 1. Pemotongan (Slicing)
Class `Spritesheet` memotong satu gambar besar menjadi grid (misal: 8 kolom, 8 baris). Setiap kotak kecil adalah satu **Frame**.

### 2. State & Direction
Pemain memiliki variabel `state` (stand, walk, run) dan `direction` (up, down, left, right).
- **Baris (Row)** ditentukan oleh `direction`.
- **Kolom (Column)** ditentukan oleh waktu.

### 3. Frame Timer Logic (Crucial!)
Agar animasi tidak bergerak terlalu cepat, kita menggunakan sistem **Timer**.
```python
self.frame_timer += 1
if self.frame_timer >= self.anim_speed: # anim_speed mengontrol FPS animasi
    self.frame_timer = 0
    # Loop kolom 0 sampai 5 untuk animasi jalan
    self.current_col = (self.current_col + 1) % 6 
```
Setiap kali `frame_timer` mencapai batas tertentu, kolom gambar akan bergeser ke kanan. Saat mencapai akhir, ia kembali ke nol (Modulo `%`). Inilah yang menciptakan ilusi gerakan yang mulus.
