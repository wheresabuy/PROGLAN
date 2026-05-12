# Project 23 - Survival with Gesture Control 🎮🧟

Game survival petualangan bertema kiamat zombie yang dikontrol menggunakan gerakan tangan (**Hand Gestures**) secara real-time. Project ini memanfaatkan **Computer Vision** untuk menerjemahkan gerakan fisik menjadi aksi di dalam game.

## 🌟 Fitur Unggulan
- **ML Gesture Control**: Menggunakan model *Random Forest* untuk mengenali bentuk tangan, bukan hanya posisi.
- **Position Invariant**: Berkat teknologi *Relative Landmarks*, sistem tetap akurat meskipun posisi tangan berpindah-pindah di depan kamera.
- **Dynamic Gameplay**: Dilengkapi sistem misi, dialog interaktif, manajemen inventori, dan efek visual *darkness* yang mencekam.
- **Seamless Performance**: Menggunakan *Multi-threading* agar pemrosesan gambar kamera tidak mengganggu kelancaran *frame rate* game.

## 📂 Struktur Proyek
- `main.py`: File utama untuk menjalankan game. Menggabungkan logika game dan thread kamera.
- `comvis/`: Otak di balik deteksi gerakan.
  - `gestures.py`: Logika pengenalan gestur menggunakan model ML.
  - `train_data.py`: Script untuk mengumpulkan dataset koordinat tangan.
  - `train_model.py`: Script untuk melatih AI mengenali gestur baru.
  - `reset_data.py`: Script untuk menghapus dataset lama jika ingin melatih ulang.
- `src/`: Mesin game (Player, NPC, Camera, Mission System, UI).
- `assets/images/`: Galeri aset pixel art untuk lingkungan dan item.

## 🛠️ Cara Instalasi

### 1. Persiapan Awal
Pastikan Anda memiliki Python 3.10+ terinstall.
```bash
git clone git@github.com:wheresabuy/PROGLAN.git
cd PemogramanLanjut
```

### 2. Setup Lingkungan (Virtual Environment)
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Install Library
```bash
pip install -r requirements.txt
```

## 🎮 Cara Bermain

1.  **Kamera**: Gunakan aplikasi **IP Webcam** di Android/iOS.
2.  **Konfigurasi**: Sesuaikan `camera_path` di `main.py` dengan IP yang muncul di aplikasi (contoh: `http://192.168.1.5:8080/video`).
3.  **Run**:
    ```bash
    python main.py
    ```

### Mapping Gestur:
- **Tangan Terbuka (DIAM)**: Karakter berhenti/Idle.
- **Tangan Menunjuk Ke Atas/Bawah/Kiri/Kanan**: Karakter bergerak sesuai arah.
- **Mengepal (AMBIL)**: Mengambil item atau melanjutkan dialog.

## 🧠 Cara Melatih Gestur Kustom

Anda bisa mengajarkan gerakan baru ke dalam game:
1.  **Kumpulkan Data**: Jalankan `python comvis/train_data.py`.
    - Tekan **'l'** untuk memberi nama gestur (misal: `JUMP`).
    - Tekan **'s'** untuk mulai merekam (ambil sekitar 200 data).
2.  **Latih AI**: Jalankan `python comvis/train_model.py`. AI akan belajar mengenali gerakan tersebut.
3.  **Gunakan**: Tambahkan logika mapping baru di `main.py`.

## ⌨️ Kontrol Keyboard (Opsional)
- **Panah**: Bergerak
- **Shift**: Lari (Sprint)
- **Enter**: Interaksi
- **J**: Jurnal | **I**: Inventori | **F**: Senter

---
*Dibuat dengan ❤️ oleh wheresabuy untuk Tugas Pemrograman Lanjut.*
