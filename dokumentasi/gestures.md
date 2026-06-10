# Penjelasan Kode: `gestures.py`

Dokumen ini berisi penjelasan mendetail baris demi baris mengenai file `/home/abuyyy/PemogramanLanjut/comvis/gestures.py` dalam bahasa Indonesia untuk membantu persiapan demo program.

---

## Deskripsi & Tujuan File
File `gestures.py` bertanggung jawab atas seluruh proses visi komputer (Computer Vision) menggunakan MediaPipe dan OpenCV. Tugas utamanya adalah:
1. Menangkap frame video dari kamera secara real-time di thread terpisah (`GestureThread`).
2. Mendeteksi landmark tangan dan membagi logika deteksi gestur menjadi dua mode:
   - **Mode Eksplorasi Sanctuary**: Menggunakan model Machine Learning (`gesture_model.pkl`) untuk mendeteksi `ATAS`, `BAWAH`, `KIRI`, `KANAN`, dan `AMBIL`.
   - **Mode Minigame**: Menggunakan perhitungan matematika rasio jari (bebas rotasi & skala) untuk mendeteksi `PISTOL` (menembak), `AIM` (membidik saja), dan `FIST` (mengisi peluru).
3. Menerapkan filter OneEuroFilter untuk menstabilkan pergerakan kursor agar sangat halus.

---

## Daftar Import

| Library | Kegunaan |
| :--- | :--- |
| `cv2` | OpenCV, digunakan untuk membaca kamera, membalik gambar, konversi warna (BGR ke RGB), serta mengubah ukuran frame. |
| `mediapipe` | Framework ML Google untuk mendeteksi 21 titik koordinat (landmark) tangan secara real-time. |
| `pickle` | Digunakan untuk memuat model Machine Learning yang telah dilatih (`gesture_model.pkl`). |
| `os` | Berinteraksi dengan sistem operasi, memuat file path model. |
| `numpy` | Penanganan komputasi matriks/array (digunakan oleh pemrosesan gambar). |
| `threading` | Menjalankan kamera pada Thread terpisah agar tidak mengganggu thread utama game. |
| `warnings` | Memblokir peringatan abaikan dari scikit-learn/mediapipe agar konsol tetap bersih. |
| `pandas` | Membuat DataFrame untuk input data ke model prediksi ML. |
| `math` | Operasi matematika dasar seperti menghitung jarak Euclidean (`math.hypot`). |
| `collections` | Menggunakan `deque` sebagai buffer geser untuk meredam kedipan (*flicker*) gestur. |
| `time` | Menghitung interval waktu untuk filter OneEuroFilter dan jeda tembakan. |

---

## Penjelasan Baris Demi Baris

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| 1 | `import cv2` | Mengimpor OpenCV untuk operasi video dan gambar. |
| 2 | `import mediapipe as mp` | Mengimpor MediaPipe untuk pelacakan tangan. |
| 3 | `import pickle` | Mengimpor pickle untuk deserialisasi model ML. |
| 4 | `import os` | Mengimpor os untuk penanganan path file. |
| 5 | `import numpy as np` | Mengimpor numpy untuk penanganan data array. |
| 6 | `import threading` | Mengimpor threading untuk memisahkan proses kamera. |
| 7 | `import warnings` | Mengimpor warnings untuk mengabaikan UserWarning. |
| 8 | `import pandas as pd` | Mengimpor pandas untuk konversi data input model ML. |
| 9 | `import math` | Mengimpor math untuk kalkulasi koordinat dan jarak. |
| 10 | `import collections` | Mengimpor collections untuk antrean geser (`deque`). |
| 11 | `import time` | Mengimpor time untuk pengukuran waktu filter. |
| 12 | `warnings.filterwarnings("ignore", category=UserWarning)` | Menonaktifkan peringatan UserWarning agar output konsol tetap bersih. |
| 13 | `os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'` | Membatasi log TensorFlow agar hanya menampilkan error fatal. |
| 14 | `class GestureRecognizerML:` | Mendefinisikan kelas deteksi gestur menggunakan Machine Learning & Heuristik. |
| 15 | `    def __init__(self):` | Konstruktor kelas deteksi gestur. |
| 16 | `        self.mp_hands = mp.solutions.hands` | Mengambil referensi modul Hands dari MediaPipe. |
| 17 | `        self.hands = self.mp_hands.Hands(...)` | Konfigurasi detektor tangan MediaPipe (max 1 tangan, konfidensi deteksi 70%). |
| 23 | `        self.mp_draw = mp.solutions.drawing_utils` | Mengambil utilitas penggambaran garis landmark tangan dari MediaPipe. |
| 24 | `        base_dir = os.path.dirname(os.path.abspath(__file__))` | Mencari path direktori dari file `gestures.py`. |
| 25 | `        self.model_path = os.path.join(base_dir, 'gesture_model.pkl')` | Menentukan lokasi file model ML (`gesture_model.pkl`). |
| 26 | `        self.model = None` | Menginisialisasi model dengan nilai `None`. |
| 27 | `        if os.path.exists(self.model_path):` | Mengecek apakah file model ML ada di penyimpanan disk. |
| 28 | `            with open(self.model_path, 'rb') as f:` | Membuka file model biner tersebut untuk dibaca. |
| 29 | `                self.model = pickle.load(f)` | Memuat file model biner ke atribut `self.model`. |
| 30 | `            print("Model Machine Learning berhasil dimuat.")` | Cetak status sukses memuat model ke terminal. |
| 31 | `        else:` | Jika file model tidak ditemukan. |
| 32 | `            print("Peringatan: Model belum dilatih. Gunakan train_model.py!")` | Cetak status peringatan ke terminal. |
| 33 | `    def recognize(self, hand_landmarks, in_minigame=False):` | Metode utama untuk mengenali gestur berdasarkan status permainan. |
| 34 | `        lm = hand_landmarks.landmark` | Menyimpan referensi 21 titik koordinat tangan. |
| 35 | `        if in_minigame:` | **LOGIKA MINIGAME**: |
| 36 | `            has_ml_minigame = False` | Inisialisasi status apakah model ML sudah memiliki kelas minigame. |
| 37 | `            if self.model is not None and hasattr(self.model, 'classes_'):` | Memeriksa apakah model dimuat dan memiliki daftar kelas terlatih. |
| 38 | `                has_ml_minigame = any(c in self.model.classes_ for c in ["PISTOL", "AIM", "FIST"])` | Memeriksa keberadaan kelas PISTOL, AIM, dan FIST di dalam model ML. |
| 40 | `            if has_ml_minigame:` | Jika model ML mendukung gestur minigame, gunakan ML untuk prediksi. |
| 41 | `                # ML Prediction logic ...` | Mengekstrak landmark, membuat DataFrame, memprediksi label dengan Random Forest. |
| 48 | `                if pred_label in ["PISTOL", "AIM", "FIST"]: return pred_label` | Mengembalikan label minigame jika terdeteksi. |
| 50 | `            else:` | **LOGIKA FALLBACK (Heuristik Matematika)**: Terpilih jika model belum dilatih. |
| 51 | `                hand_scale = math.hypot(...)` | Menghitung skala ukuran tangan. |
| 62 | `                if is_index_open and is_middle_folded and is_ring_folded and is_pinky_folded:` | Aturan deteksi: telunjuk lurus dan jari lain tertekuk. |
| 63 | `                    return "PISTOL" if is_thumb_loose else "AIM"` | Kembalikan PISTOL jika jempol terbuka, AIM jika jempol ditekuk. |
| 69 | `                if is_index_folded and is_middle_folded_strict and is_ring_folded_strict and is_pinky_folded_strict:` | Aturan deteksi: genggaman tangan (fist). |
| 70 | `                    return "FIST"` | Mengembalikan status FIST (Reload). |
| 71 | `                return "None"` | Default kembali ke None. |
| 72 | `        else:` | **LOGIKA EKSPLORASI SANCTUARY (Selalu ML)**: |
| 73 | `            pred_label = "None"` | Inisialisasi default label. |
| 74 | `            if self.model is not None:` | Jika model ML aktif. |
| 77-80 | `                for lm_node in hand_landmarks.landmark: data.append(...)` | Mengumpulkan koordinat X, Y, Z relatif terhadap pergelangan tangan (wrist). |
| 81 | `                columns = ...` | Membuat nama kolom dataset. |
| 82 | `                df_input = pd.DataFrame([data], columns=columns)` | Mengonversi ke DataFrame Pandas. |
| 83 | `                prediction = self.model.predict(df_input)` | Memprediksi gestur dengan RandomForest. |
| 84 | `                pred_label = prediction[0]` | Mengambil label hasil prediksi. |
| 85 | `                if pred_label in ["ATAS", "BAWAH", "KIRI", "KANAN", "AMBIL"]:` | Memastikan hasil prediksi adalah tombol navigasi yang valid. |
| 86 | `                    return pred_label` | Mengembalikan hasil label navigasi. |
| 87 | `            return "None"` | Mengembalikan None jika tidak terdeteksi. |
| 78 | `class OneEuroFilter:` | Mendefinisikan kelas filter One Euro untuk melembutkan fluktuasi koordinat. |
| 102 | `class GestureThread(threading.Thread):` | Kelas Thread untuk menangkap frame kamera dan melakukan deteksi tangan secara terpisah. |
| 103 | `    def __init__(self, camera_path):` | Inisialisasi thread dengan path kamera (index 0). |
| 119 | `        self.in_minigame = False` | Status apakah pemain sedang berada di dalam minigame (default False). |
| 123 | `    @property def current_gesture(self):` | Properti thread untuk mengambil gestur aktif saat ini secara aman (*thread-safe*). |
| 126 | `    @property def hand_pos(self):` | Properti thread untuk mengambil koordinat X dan Y ujung telunjuk secara aman. |
| 129 | `    @property def recoil_active(self):` | Mendeteksi apakah sentakan/tembakan baru saja terpicu, lalu langsung mereset status recoil tersebut ke False. |
| 139 | `    def run(self):` | Fungsi utama loop kamera yang berjalan di latar belakang. |
| 141 | `            cap = cv2.VideoCapture(self.camera_path)` | Membuka akses kamera menggunakan OpenCV. |
| 146 | `            while self.running:` | Selama status thread berjalan. |
| 147 | `                ret, frame = cap.read()` | Membaca frame terbaru dari kamera. |
| 150 | `                    flipped_frame = cv2.flip(frame, 1)` | Membalik gambar secara horizontal agar bertindak seperti cermin. |
| 151 | `                    rgb_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)` | Mengonversi warna BGR (OpenCV) ke RGB (MediaPipe). |
| 152 | `                    results = self.recognizer.hands.process(rgb_frame)` | Memproses gambar RGB untuk mencari titik koordinat tangan. |
| 154 | `                    if results.multi_hand_landmarks:` | Jika ada tangan terdeteksi di dalam frame. |
| 158 | `                        gesture = self.recognizer.recognize(hand_landmarks, self.in_minigame)` | Mengenali gestur tangan frame saat ini. |
| 159 | `                        self._gesture_buffer.append(gesture)` | Memasukkan hasil ke dalam buffer deque berkapasitas 5. |
| 160 | `                        smoothed_gesture = max(set(self._gesture_buffer), key=self._gesture_buffer.count)` | Mengambil gestur terpopuler di buffer untuk meredam noise (majority vote). |
| 161 | `                        is_shooting_g = smoothed_gesture == "PISTOL"` | Cek apakah gestur saat ini adalah `"PISTOL"` (Tembak). |
| 162 | `                        was_shooting_g = self._prev_gesture == "PISTOL"` | Cek apakah gestur sebelumnya adalah `"PISTOL"`. |
| 163 | `                        transition_to_shoot = is_shooting_g and not was_shooting_g` | Terpicu jika baru saja berubah dari tidak menembak ke `"PISTOL"` (tembakan pertama). |
| 164 | `                        self._prev_gesture = smoothed_gesture` | Menyimpan gestur saat ini untuk pengecekan frame berikutnya. |
| 165 | `                        tip = hand_landmarks.landmark[8]` | Titik landmark 8 (ujung jari telunjuk). |
| 166 | `                        raw_v_y = self._last_y - tip.y` | Menghitung kecepatan gerakan Y jari telunjuk. |
| 167 | `                        self._velocity_y = (alpha * raw_v_y) + (1.0 - alpha) * self._velocity_y` | Menerapkan eksponensial moving average pada kecepatan gerakan Y. |
| 168 | `                        with self._lock:` | Mengamankan variabel bersama menggunakan lock mutex. |
| 169 | `                            self._current_gesture = smoothed_gesture` | Menyimpan gestur ke atribut thread. |
| 170 | `                            t_now = time.time()` | Mengambil waktu saat ini. |
| 171 | `                            self._hand_pos[0] = self.filter_x(t_now, tip.x)` | Menyaring koordinat X ujung telunjuk menggunakan OneEuroFilter. |
| 172 | `                            self._hand_pos[1] = self.filter_y(t_now, tip.y)` | Menyaring koordinat Y ujung telunjuk menggunakan OneEuroFilter. |
| 173 | `                            jerk_fired = (is_shooting_g and self._velocity_y > 0.025)` | Sentakan terpicu jika gestur menembak aktif dan ada gerakan kejutan telunjuk ke atas > 0.025. |
| 174 | `                            if (transition_to_shoot or jerk_fired):` | Jika tembakan pertama terpicu ATAU ada sentakan tangan ke atas. |
| 175 | `                                if time.time() - self._last_shot_time > 0.25:` | Mencegah tembakan bertumpuk terlalu cepat (jeda minimal 250ms). |
| 176 | `                                    self._recoil_triggered = True` | Aktifkan sinyal tembakan/recoil untuk dibaca game. |
| 177 | `                                    self._last_shot_time = time.time()` | Perbarui pencatatan waktu tembakan terakhir. |
| 178 | `                        self._last_y = tip.y` | Simpan koordinat Y telunjuk saat ini untuk frame berikutnya. |
| 179 | `                    else:` | Jika tidak ada tangan terdeteksi. |
| 180 | `                        with self._lock: self._current_gesture = "None"` | Atur gestur ke `"None"`. |
| 181 | `                    import pygame` | Mengimpor pygame secara lokal untuk membuat surface gambar. |
| 182 | `                    small = cv2.resize(flipped_frame, (160, 120))` | Memperkecil resolusi frame video menjadi 160x120 piksel untuk overlay layar. |
| 183 | `                    rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)` | Mengonversi format warna frame kecil ke RGB. |
| 184 | `                    surf = pygame.surfarray.make_surface(rgb_small.swapaxes(0, 1))` | Membuat surface pygame dari numpy array gambar kecil tersebut. |
| 185 | `                    with self._lock:` | Mengunci thread. |
| 186 | `                        self.latest_frame = surf` | Menyimpan surface frame video terbaru untuk digambar di layar game. |
| 190 | `            cap.release()` | Melepas perangkat kamera setelah loop berhenti. |
| 197 | `        self.running = False` | Mengubah status bendera loop menjadi mati untuk menghentikan thread kamera. |
