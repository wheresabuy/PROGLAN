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
