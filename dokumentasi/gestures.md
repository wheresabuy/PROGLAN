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
| 35 | `        if in_minigame:` | **LOGIKA MINIGAME (Bebas Rotasi/Skala)**: |
| 36 | `            hand_scale = math.hypot(lm[9].x - lm[0].x, lm[9].y - lm[0].y)` | Menghitung jarak pergelangan tangan (0) ke pangkal jari tengah (9) sebagai skala ukuran tangan. |
| 37 | `            if hand_scale < 0.01:` | Mencegah pembagian dengan nol dengan menetapkan batas ukuran minimal. |
| 38 | `                hand_scale = 0.01` | Nilai batas minimal skala tangan. |
| 39 | `            d_index = math.hypot(lm[8].x - lm[5].x, lm[8].y - lm[5].y)` | Mengukur panjang jari telunjuk (jarak titik 5 ke 8). |
| 40 | `            d_middle = math.hypot(lm[12].x - lm[9].x, lm[12].y - lm[9].y)` | Mengukur panjang jari tengah (jarak titik 9 ke 12). |
| 41 | `            d_ring = math.hypot(lm[16].x - lm[13].x, lm[16].y - lm[13].y)` | Mengukur panjang jari manis (jarak titik 13 ke 16). |
| 42 | `            d_pinky = math.hypot(lm[20].x - lm[17].x, lm[20].y - lm[17].y)` | Mengukur panjang jari kelingking (jarak titik 17 ke 20). |
| 43 | `            thumb_dist = math.hypot(lm[4].x - lm[5].x, lm[4].y - lm[5].y)` | Mengukur jarak ujung jempol (4) ke pangkal telunjuk (5). |
| 44 | `            r_index = d_index / hand_scale` | Menghitung rasio panjang telunjuk terhadap skala tangan. |
| 45 | `            r_middle = d_middle / hand_scale` | Menghitung rasio panjang jari tengah terhadap skala tangan. |
| 46 | `            r_ring = d_ring / hand_scale` | Menghitung rasio panjang jari manis terhadap skala tangan. |
| 47 | `            r_pinky = d_pinky / hand_scale` | Menghitung rasio panjang kelingking terhadap skala tangan. |
| 48 | `            r_thumb = thumb_dist / hand_scale` | Menghitung rasio jarak jempol terhadap skala tangan. |
| 49 | `            is_index_open = r_index > 0.5` | Telunjuk dianggap terbuka jika rasionya > 0.5. |
| 50 | `            is_middle_folded = r_middle < 0.45` | Jari tengah dianggap menekuk jika rasionya < 0.45. |
| 51 | `            is_ring_folded = r_ring < 0.45` | Jari manis dianggap menekuk jika rasionya < 0.45. |
| 52 | `            is_pinky_folded = r_pinky < 0.45` | Kelingking dianggap menekuk jika rasionya < 0.45. |
| 53 | `            is_thumb_loose = r_thumb > 0.65` | Jempol dianggap tegak terbuka (rileks) jika rasionya > 0.65. |
| 54 | `            if is_index_open and is_middle_folded and is_ring_folded and is_pinky_folded:` | Jika telunjuk lurus menunjuk dan 3 jari lainnya tertekuk. |
| 55 | `                return "PISTOL" if is_thumb_loose else "AIM"` | Jika jempol tegak kembalikan `"PISTOL"` (Tembak), jika jempol menekuk kembalikan `"AIM"` (Bidik saja). |
| 56 | `            is_index_folded = r_index < 0.4` | Telunjuk dianggap menekuk jika rasionya < 0.4. |
| 57 | `            is_middle_folded_strict = r_middle < 0.4` | Jari tengah menekuk ketat jika rasionya < 0.4. |
| 58 | `            is_ring_folded_strict = r_ring < 0.4` | Jari manis menekuk ketat jika rasionya < 0.4. |
| 59 | `            is_pinky_folded_strict = r_pinky < 0.4` | Kelingking menekuk ketat jika rasionya < 0.4. |
| 60 | `            if is_index_folded and is_middle_folded_strict and is_ring_folded_strict and is_pinky_folded_strict:` | Jika keempat jari ditekuk semua (mengepal). |
| 61 | `                return "FIST"` | Mengembalikan status `"FIST"` (Reload). |
| 62 | `            return "None"` | Jika gestur tangan acak lainnya, kembalikan `"None"`. |
| 63 | `        else:` | **LOGIKA EKSPLORASI UTAMA (Menggunakan Model ML)**: |
| 64 | `            pred_label = "None"` | Default label adalah `"None"`. |
| 65 | `            if self.model is not None:` | Jika model ML berhasil dimuat. |
| 66 | `                data = []` | Inisialisasi list untuk menampung koordinat input. |
| 67 | `                wrist = hand_landmarks.landmark[0]` | Mengambil koordinat pergelangan tangan sebagai titik nol referensi. |
| 68 | `                for lm_node in hand_landmarks.landmark: data.append(lm_node.x - wrist.x)` | Menyimpan koordinat selisih X dari wrist untuk ke-21 titik. |
| 69 | `                for lm_node in hand_landmarks.landmark: data.append(lm_node.y - wrist.y)` | Menyimpan koordinat selisih Y dari wrist untuk ke-21 titik. |
| 70 | `                for lm_node in hand_landmarks.landmark: data.append(lm_node.z - wrist.z)` | Menyimpan koordinat selisih Z dari wrist untuk ke-21 titik. |
| 71 | `                columns = [f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)]` | Membuat nama kolom koordinat (x0..x20, y0..y20, z0..z20). |
| 72 | `                df_input = pd.DataFrame([data], columns=columns)` | Membuat DataFrame pandas dengan data relatif tersebut sebagai input model. |
| 73 | `                prediction = self.model.predict(df_input)` | Memprediksi gestur menggunakan model RandomForest yang sudah dilatih. |
| 74 | `                pred_label = prediction[0]` | Mengambil label gestur hasil prediksi. |
| 75 | `                if pred_label in ["ATAS", "BAWAH", "KIRI", "KANAN", "AMBIL"]:` | Memastikan hasil prediksi merupakan bagian dari aksi navigasi luar game. |
| 76 | `                    return pred_label` | Kembalikan label navigasi tersebut. |
| 77 | `            return "None"` | Kembalikan `"None"` jika model tidak memprediksi navigasi terdaftar. |
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
