# Project 23 - Survival with Gesture Control

Game survival petualangan yang dikontrol menggunakan gerakan tangan (Hand Gestures) secara real-time melalui kamera. Project ini menggabungkan Pygame untuk engine game dan MediaPipe + Scikit-Learn untuk sistem Computer Vision.

## 🚀 Fitur Utama
- **Real-time Gesture Recognition**: Kontrol karakter menggunakan tangan melalui IP Webcam atau kamera laptop.
- **Machine Learning Powered**: Sistem deteksi gestur menggunakan Random Forest Classifier untuk akurasi tinggi.
- **Adventure Gameplay**: Sistem misi, inventori, dialog, dan efek visual kegelapan.
- **Multi-threading**: Kamera dan Game berjalan di thread terpisah agar performa tetap lancar.

## 📁 Struktur Folder
- `src/`: Logika inti game (Player, Mission, UI, Core).
- `comvis/`: Sistem Computer Vision (Gestures, Training, Data Collection).
- `assets/images/`: Semua aset gambar game.
- `main.py`: Entry point utama untuk menjalankan game.

## 🛠️ Persiapan Lingkungan

### 1. Clone Repository
```bash
git clone <url-repo-kamu>
cd PemogramanLanjut
```

### 2. Buat Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🎮 Cara Menjalankan Game

1.  Aktifkan **IP Webcam** di HP kamu dan tekan "Start Server".
2.  Buka `comvis/gestures.py` dan `main.py`, pastikan `camera_path` sesuai dengan alamat IP yang muncul di HP kamu.
3.  Jalankan game:
    ```bash
    python main.py
    ```

## 🧠 Melatih Gestur Baru

Jika ingin menambah atau melatih ulang gestur:
1.  **Rekam Data**: Jalankan `python comvis/train_data.py`. Tekan 'l' untuk beri label, 's' untuk rekam.
2.  **Latih Model**: Jalankan `python comvis/train_model.py`. Ini akan mengupdate file `gesture_model.pkl`.
3.  **Reset Data**: Jika ingin mengulang dari awal, jalankan `python comvis/reset_data.py`.

## ⌨️ Kontrol Alternatif (Keyboard)
- **Panah**: Bergerak
- **Shift**: Lari
- **Enter**: Ambil barang / Lanjut dialog
- **J**: Buka Jurnal
- **I**: Buka Inventori
- **F**: Senter (Flashlight)

---
*Dibuat untuk tugas Pemrograman Lanjut.*
