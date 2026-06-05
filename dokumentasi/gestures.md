# Penjelasan Source Code: gestures.py

Dokumen ini berisi penjelasan detail baris demi baris dari berkas `/home/abuyyy/PemogramanLanjut/comvis/gestures.py` dalam bahasa Indonesia. Penjelasan ini disusun untuk membantu Anda mempersiapkan demo program dengan baik.

---

## Deskripsi & Tujuan File
Berkas `gestures.py` bertanggung jawab atas modul pengenalan gerakan tangan (gesture recognition) secara *real-time* menggunakan kamera. Modul ini menggabungkan pustaka **OpenCV** untuk menangkap gambar dari kamera, **MediaPipe** untuk melacak posisi sendi dan ujung jari tangan (landmark), serta model **Machine Learning** (melalui berkas `.pkl`) atau logika berbasis aturan (*rule-based*) untuk mendeteksi gerakan tertentu seperti mengepal (`FIST`) atau gestur menembak/pistol (`PISTOL`). 

Selain itu, berkas ini mengimplementasikan filter peredam getaran (**OneEuroFilter**) agar pergerakan kursor yang digerakkan oleh tangan tampak mulus di layar, serta menjalankan seluruh proses pengolahan gambar ini di *thread* terpisah (**GestureThread**) agar tidak mengganggu kinerja atau memblokir *game loop* utama.

---

## Daftar Import

Berikut adalah pustaka-pustaka yang diimpor pada berkas ini beserta kegunaannya:
* **`cv2` (OpenCV)**: Digunakan untuk membaca *input* video dari kamera (*webcam*) dan manipulasi bingkai gambar (frame).
* **`mediapipe` (mp)**: Pustaka buatan Google untuk mendeteksi dan melacak koordinat 21 titik (landmark) tangan manusia.
* **`pickle`**: Digunakan untuk memuat kembali model Machine Learning yang telah dilatih dan disimpan dalam format biner (`gesture_model.pkl`).
* **`os`**: Digunakan untuk mengelola jalur direktori file (*file path*) dan mengatur variabel lingkungan sistem.
* **`numpy` (np)**: Pustaka komputasi numerik yang sering digunakan untuk manipulasi array/matriks.
* **`threading`**: Digunakan untuk menjalankan pemrosesan kamera dan deteksi tangan secara paralel (*multithreading*) agar aplikasi utama tetap responsif.
* **`warnings`**: Digunakan untuk mengabaikan atau menyaring pesan peringatan agar konsol tetap bersih dari *output* yang tidak kritis.
* **`pandas` (pd)**: Digunakan untuk membuat struktur data DataFrame sebelum memasukkan nilai koordinat tangan ke model prediksi Machine Learning.
* **`math`**: Digunakan untuk fungsi matematika dasar seperti menghitung jarak Euclidean (`math.hypot`).
* **`collections` (deque)**: Digunakan untuk menyimpan antrean dengan kapasitas maksimal tertentu guna menghaluskan (*smoothing*) hasil pembacaan gestur.
* **`time`**: Digunakan untuk menghitung selisih waktu guna menghitung filter dan mengontrol waktu jeda (*cooldown*) tembakan.

---

## Penjelasan Baris Demi Baris

| Baris | Kode Sumber | Penjelasan |
| :--- | :--- | :--- |
| **1** | `import cv2` | Mengimpor pustaka OpenCV untuk pemrosesan video dan gambar. |
| **2** | `import mediapipe as mp` | Mengimpor MediaPipe untuk pelacakan landmark tangan. |
| **3** | `import pickle` | Mengimpor pustaka Pickle untuk memuat model ML yang disimpan. |
| **4** | `import os` | Mengimpor pustaka OS untuk menangani direktori dan berkas. |
| **5** | `import numpy as np` | Mengimpor Numpy untuk operasi matriks/matematika cepat. |
| **6** | `import threading` | Mengimpor modul threading untuk eksekusi paralel. |
| **7** | `import warnings` | Mengimpor pustaka warnings untuk mengontrol peringatan sistem. |
| **8** | `import pandas as pd` | Mengimpor Pandas untuk menampung data fitur masukan model ML. |
| **9** | `import math` | Mengimpor pustaka Math untuk perhitungan matematika dasar. |
| **10** | `import collections` | Mengimpor modul collections (khususnya untuk struktur data `deque`). |
| **11** | `import time` | Mengimpor modul time untuk pencatatan waktu dan jeda. |
| **12** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **13** | `# Suppress warnings` | Komentar penjelas bahwa bagian di bawahnya berfungsi menyembunyikan peringatan. |
| **14** | `warnings.filterwarnings("ignore", category=UserWarning)` | Menginstruksikan Python untuk mengabaikan semua peringatan kategori `UserWarning` agar konsol lebih bersih. |
| **15** | `os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'` | Mengatur tingkat log TensorFlow ke tingkat '3' (hanya menampilkan pesan error fatal) agar tidak mengotori layar konsol. |
| **16** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **17** | `class GestureRecognizerML:` | Mendefinisikan kelas `GestureRecognizerML` untuk mengenali gerakan tangan. |
| **18** | `    def __init__(self):` | Konstruktor inisialisasi kelas `GestureRecognizerML`. |
| **19** | `        self.mp_hands = mp.solutions.hands` | Mengambil solusi pelacakan tangan (Hands) dari pustaka MediaPipe. |
| **20** | `        self.hands = self.mp_hands.Hands(` | Membuat instansi detektor tangan MediaPipe dengan beberapa parameter. |
| **21** | `            static_image_mode=False,` | Mengatur mode gambar dinamis (`False`), artinya dioptimalkan untuk memproses aliran video (real-time). |
| **22** | `            max_num_hands=1,` | Membatasi deteksi tangan maksimal hanya 1 tangan saja. |
| **23** | `            min_detection_confidence=0.7,` | Batas kepercayaan minimal deteksi tangan awal sebesar 70%. Di bawah itu, tangan dianggap tidak terdeteksi. |
| **24** | `            min_tracking_confidence=0.5` | Batas kepercayaan minimal pelacakan tangan setelah deteksi awal sebesar 50%. |
| **25** | `        )` | Penutup argumen inisialisasi objek `Hands`. |
| **26** | `        self.mp_draw = mp.solutions.drawing_utils` | Menyimpan utilitas penggambaran MediaPipe untuk menggambar titik koordinat jika diperlukan. |
| **27** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **28** | `        base_dir = os.path.dirname(os.path.abspath(__file__))` | Mengambil jalur direktori absolut dari lokasi berkas `gestures.py` disimpan saat ini. |
| **29** | `        self.model_path = os.path.join(base_dir, 'gesture_model.pkl')` | Membuat jalur absolut yang mengarah ke berkas model `gesture_model.pkl`. |
| **30** | `        self.model = None` | Menyiapkan atribut `self.model` dengan nilai awal kosong (`None`). |
| **31** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **32** | `        if os.path.exists(self.model_path):` | Memeriksa apakah berkas model `gesture_model.pkl` benar-benar ada di direktori tersebut. |
| **33** | `            with open(self.model_path, 'rb') as f:` | Jika ada, buka berkas model tersebut dalam mode baca biner (`'rb'`). |
| **34** | `                self.model = pickle.load(f)` | Menggunakan `pickle.load()` untuk memuat kembali model pengenal gestur yang telah dilatih. |
| **35** | `            print("Model Machine Learning berhasil dimuat.")` | Menampilkan pesan keberhasilan pemuatan model di konsol. |
| **36** | `        else:` | Blok alternatif jika berkas model tidak ditemukan. |
| **37** | `            print("Peringatan: Model belum dilatih. Gunakan train_model.py!")` | Menampilkan peringatan bahwa model belum ada dan menyarankan untuk melatihnya terlebih dahulu. |
| **38** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **39** | `    def recognize(self, hand_landmarks):` | Metode `recognize` untuk mendeteksi jenis gestur berdasarkan titik landmark tangan yang diterima. |
| **40** | `        lm = hand_landmarks.landmark` | Mengambil daftar titik landmark koordinat tangan (21 titik). |
| **41** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **42** | `        index_up = lm[8].y < lm[6].y` | Memeriksa apakah ujung jari telunjuk (titik 8) berada di atas sendi tengahnya (titik 6). Karena nilai koordinat Y MediaPipe mengecil ke atas, tanda `<` berarti ujung jari lebih tinggi. |
| **43** | `        thumb_dist = math.hypot(lm[4].x - lm[5].x, lm[4].y - lm[5].y)` | Menghitung jarak Euclidean (hipotenusa) antara ujung jempol (titik 4) dan pangkal telunjuk (titik 5). |
| **44** | `        thumb_loose = thumb_dist > 0.05` | Jika jarak jempol lebih dari 0.05, maka jempol dianggap dalam posisi terbuka lebar / merenggang (`loose`). |
| **45** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **46** | `        if lm[8].y > lm[6].y and lm[12].y > lm[10].y and lm[16].y > lm[14].y:` | Logika manual untuk mendeteksi kepalan tangan (`FIST`): jika ujung telunjuk (8), jari tengah (12), dan manis (16) berada di bawah sendinya masing-masing (nilai Y lebih besar). |
| **47** | `            return "FIST"` | Jika benar, langsung kembalikan gestur `"FIST"`. |
| **48** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **49** | `        if index_up and thumb_loose:` | Logika manual untuk gestur pistol (`PISTOL`): jika telunjuk mengacung ke atas dan jempol terbuka merenggang. |
| **50** | `            return "PISTOL"` | Jika benar, kembalikan gestur `"PISTOL"`. |
| **51** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **52** | `        if self.model is None:` | Jika logika manual tidak terpenuhi dan ternyata model ML tidak ada/tidak termuat. |
| **53** | `            return "None"` | Kembalikan nilai default `"None"`. |
| **54** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **55** | `        data = []` | Membuat list kosong `data` untuk menampung fitur masukan (features) model ML. |
| **56** | `        wrist = hand_landmarks.landmark[0]` | Mengambil koordinat pergelangan tangan (landmark 0) sebagai titik acuan (offset). |
| **57** | `        for lm_node in hand_landmarks.landmark: data.append(lm_node.x - wrist.x)` | Memasukkan selisih posisi sumbu X dari semua 21 landmark terhadap pergelangan tangan ke dalam `data`. |
| **58** | `        for lm_node in hand_landmarks.landmark: data.append(lm_node.y - wrist.y)` | Memasukkan selisih posisi sumbu Y dari semua 21 landmark terhadap pergelangan tangan ke dalam `data`. |
| **59** | `        for lm_node in hand_landmarks.landmark: data.append(lm_node.z - wrist.z)` | Memasukkan selisih posisi sumbu Z dari semua 21 landmark terhadap pergelangan tangan ke dalam `data`. |
| **60** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **61** | `        columns = [f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)]` | Membuat daftar nama kolom (x0-x20, y0-y20, z0-z20) agar sesuai dengan struktur saat model ML dilatih. |
| **62** | `        df_input = pd.DataFrame([data], columns=columns)` | Membuat objek Pandas DataFrame dari list data tersebut dengan nama kolom yang sudah dibuat. |
| **63** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **64** | `        prediction = self.model.predict(df_input)` | Melakukan prediksi gestur dengan mengirimkan DataFrame tersebut ke model ML. |
| **65** | `        return prediction[0]` | Mengembalikan hasil label prediksi pertama (elemen ke-0) dari model ML. |
| **66** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **67** | `class OneEuroFilter:` | Mendefinisikan kelas `OneEuroFilter` yang digunakan untuk menyaring sinyal koordinat agar kursor bergerak mulus tanpa getaran (jitter). |
| **68** | `    def __init__(self, t0, x0, dx0=0.0, min_cutoff=0.8, beta=0.03, d_cutoff=1.0):` | Konstruktor inisialisasi filter dengan parameter waktu awal (`t0`), posisi awal (`x0`), kecepatan awal (`dx0`), frekuensi cutoff minimum (`min_cutoff`), sensitivitas kecepatan (`beta`), dan cutoff turunan (`d_cutoff`). |
| **69** | `        self.min_cutoff = float(min_cutoff)` | Menyimpan nilai frekuensi cutoff minimum. |
| **70** | `        self.beta = float(beta)` | Menyimpan nilai sensitivitas kecepatan (beta). |
| **71** | `        self.d_cutoff = float(d_cutoff)` | Menyimpan nilai cutoff turunan kecepatan. |
| **72** | `        self.x_prev = float(x0)` | Menyimpan nilai posisi sebelumnya. |
| **73** | `        self.dx_prev = float(dx0)` | Menyimpan nilai kecepatan perubahan posisi sebelumnya. |
| **74** | `        self.t_prev = float(t0)` | Menyimpan stempel waktu pembacaan sebelumnya. |
| **75** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **76** | `    def __call__(self, t, x):` | Fungsi ajaib (magic method) `__call__` agar objek kelas bisa dipanggil langsung seperti fungsi biasa dengan parameter waktu saat ini (`t`) dan posisi baru (`x`). |
| **77** | `        t = float(t)` | Mengonversi waktu `t` ke tipe data float. |
| **78** | `        x = float(x)` | Mengonversi posisi `x` ke tipe data float. |
| **79** | `        dt = t - self.t_prev` | Menghitung selisih waktu (`dt`) dari pembacaan sebelumnya. |
| **80** | `        if dt <= 0:` | Jika selisih waktu kurang dari atau sama dengan nol (tidak ada waktu berlalu). |
| **81** | `            return self.x_prev` | Kembalikan posisi sebelumnya tanpa melakukan penyaringan. |
| **82** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **83** | `        # Calculate derivative` | Komentar penjelas untuk penghitungan turunan pertama (kecepatan). |
| **84** | `        dx = (x - self.x_prev) / dt` | Menghitung kecepatan perubahan posisi sesaat (`dx`) dengan membagi selisih jarak dengan selisih waktu. |
| **85** | `        # Smooth derivative` | Komentar penjelas untuk penghalusan kecepatan. |
| **86** | `        a_d = 1.0 / (1.0 + 1.0 / (2 * math.pi * self.d_cutoff * dt))` | Menghitung koefisien filter lolos-rendah (low-pass filter) untuk kecepatan berdasarkan `d_cutoff` dan `dt`. |
| **87** | `        dx_hat = a_d * dx + (1.0 - a_d) * self.dx_prev` | Menghitung kecepatan rata-rata terfilter (`dx_hat`) dengan menggabungkan kecepatan saat ini dan kecepatan sebelumnya. |
| **88** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **89** | `        # Calculate cutoff frequency based on velocity` | Komentar penjelas penghitungan frekuensi cutoff dinamis berdasarkan kecepatan. |
| **90** | `        cutoff = self.min_cutoff + self.beta * abs(dx_hat)` | Menghitung frekuensi cutoff adaptif. Jika kecepatan tinggi (`dx_hat` besar), cutoff meningkat agar responsif (mengurangi lag). Jika diam, cutoff mengecil agar getaran diredam. |
| **91** | `        # Smooth signal` | Komentar penjelas untuk pemulusan sinyal posisi. |
| **92** | `        a_s = 1.0 / (1.0 + 1.0 / (2 * math.pi * cutoff * dt))` | Menghitung koefisien filter untuk posisi menggunakan frekuensi cutoff yang baru saja dihitung. |
| **93** | `        x_hat = a_s * x + (1.0 - a_s) * self.x_prev` | Menghitung estimasi posisi baru yang sudah mulus (`x_hat`). |
| **94** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **95** | `        # Store values` | Komentar penjelas penyimpanan nilai untuk iterasi berikutnya. |
| **96** | `        self.x_prev = x_hat` | Memperbarui posisi sebelumnya dengan posisi mulus saat ini. |
| **97** | `        self.dx_prev = dx_hat` | Memperbarui kecepatan sebelumnya dengan kecepatan mulus saat ini. |
| **98** | `        self.t_prev = t` | Memperbarui waktu sebelumnya dengan waktu saat ini. |
| **99** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **100** | `        return x_hat` | Mengembalikan nilai posisi akhir yang telah dihaluskan. |
| **101** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **102** | `class GestureThread(threading.Thread):` | Mendefinisikan kelas `GestureThread` yang diturunkan dari `threading.Thread` untuk menjalankan pembacaan kamera di latar belakang. |
| **103** | `    def __init__(self, camera_path):` | Konstruktor kelas menerima argumen `camera_path` (indeks kamera atau berkas video). |
| **104** | `        threading.Thread.__init__(self)` | Memanggil inisialisasi superclass `Thread`. |
| **105** | `        self.camera_path = camera_path` | Menyimpan path kamera ke atribut objek. |
| **106** | `        self.recognizer = GestureRecognizerML()` | Membuat objek instansi `GestureRecognizerML` untuk pemrosesan gestur. |
| **107** | `        self._current_gesture = "None"` | Inisialisasi gestur aktif saat ini sebagai `"None"`. |
| **108** | `        self._gesture_buffer = collections.deque(maxlen=5)` | Membuat buffer antrean maksimum 5 elemen untuk menampung riwayat gestur agar fluktuasi deteksi dapat diredam. |
| **109** | `        self._hand_pos = [0.5, 0.5]` | Inisialisasi posisi koordinat tangan di tengah layar secara relatif `[X=0.5, Y=0.5]`. |
| **110** | `        self._velocity_y = 0.0` | Inisialisasi kecepatan vertikal awal bernilai `0.0`. |
| **111** | `        self._last_y = 0.5` | Menyimpan koordinat Y terakhir (posisi frame sebelumnya) bernilai awal `0.5`. |
| **112** | `        self._recoil_triggered = False` | Menandai status apakah efek hentakan pistol/sentak (recoil) sedang terpicu. |
| **113** | `        self._last_shot_time = 0` | Menyimpan waktu tembakan terakhir untuk sistem jeda menembak (cooldown). |
| **114** | `        self._lock = threading.Lock()` | Membuat objek Thread Lock guna menghindari tabrakan data (race condition) antara thread deteksi dan thread game utama saat mengakses variabel bersama. |
| **115** | `        self.running = True` | Menyimpan bendera status jalannya thread. |
| **116** | `        self.daemon = True` | Mengeset properti daemon thread menjadi `True` agar thread otomatis berhenti saat program utama ditutup. |
| **117** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **118** | `        # OneEuroFilters for smooth cursor movement` | Komentar penjelas mengenai inisialisasi OneEuroFilter untuk kursor yang mulus. |
| **119** | `        t_now = time.time()` | Mendapatkan stempel waktu saat ini. |
| **120** | `        self.filter_x = OneEuroFilter(t_now, 0.5, min_cutoff=1.5, beta=0.15)` | Inisialisasi filter penyaring koordinat X tangan dengan parameter cutoff 1.5 dan beta 0.15. |
| **121** | `        self.filter_y = OneEuroFilter(t_now, 0.5, min_cutoff=1.5, beta=0.15)` | Inisialisasi filter penyaring koordinat Y tangan dengan parameter serupa. |
| **122** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **123** | `    @property` | Dekorator properti untuk membuat fungsi `current_gesture` dapat diakses seperti atribut biasa (getter). |
| **124** | `    def current_gesture(self):` | Metode properti untuk mengambil gestur saat ini dengan aman. |
| **125** | `        with self._lock: return self._current_gesture` | Mengamankan pembacaan `self._current_gesture` menggunakan thread lock. |
| **126** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **127** | `    @property` | Dekorator properti untuk mempermudah akses properti koordinat posisi tangan. |
| **128** | `    def hand_pos(self):` | Metode properti untuk mengambil koordinat tangan dengan aman. |
| **129** | `        with self._lock: return list(self._hand_pos)` | Mengunci thread lalu mengembalikan salinan koordinat tangan dalam bentuk list baru. |
| **130** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **131** | `    @property` | Dekorator properti untuk mempermudah akses status sentakan (recoil). |
| **132** | `    def recoil_active(self):` | Metode properti untuk mendeteksi dan mengambil status recoil secara langsung. |
| **133** | `        with self._lock:` | Mengamankan akses variabel dengan thread lock. |
| **134** | `            if self._recoil_triggered:` | Jika status hentakan terpicu bernilai `True`. |
| **135** | `                self._recoil_triggered = False` | Segera ubah kembali nilainya menjadi `False` (mengonsumsi efek sentakan). |
| **136** | `                return True` | Mengembalikan `True` untuk memberi tahu game bahwa ada tembakan yang menghasilkan recoil. |
| **137** | `            return False` | Jika tidak terpicu, kembalikan `False`. |
| **138** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **139** | `    def run(self):` | Metode utama thread yang otomatis dieksekusi saat thread dimulai (`start()`). |
| **140** | `        try:` | Blok penanganan error eksekusi utama thread. |
| **141** | `            cap = cv2.VideoCapture(self.camera_path)` | Membuka perangkat kamera berdasarkan indeks/path yang telah disimpan di `self.camera_path`. |
| **142** | `            if not cap.isOpened():` | Jika kamera gagal diakses atau dibuka. |
| **143** | `                print("Error: Kamera tidak dapat diakses.")` | Menampilkan pesan kesalahan di konsol. |
| **144** | `                return` | Keluar dari fungsi dan menghentikan jalannya thread. |
| **145** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **146** | `            alpha = 0.7` | Koefisien alpha untuk filter Exponential Moving Average (EMA) guna menghitung kecepatan vertikal tangan. |
| **147** | `            while self.running:` | Melakukan perulangan terus menerus selama bendera `self.running` bernilai `True`. |
| **148** | `                ret, frame = cap.read()` | Membaca bingkai gambar (frame) dari kamera. |
| **149** | `                if not ret: break` | Jika gagal membaca frame (misalnya kamera terputus), hentikan perulangan. |
| **150** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **151** | `                try:` | Blok try-except internal untuk memastikan kesalahan pemrosesan frame tunggal tidak merusak jalannya thread. |
| **152** | `                    rgb_frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)` | Membalik bingkai secara horizontal (seperti cermin) menggunakan `cv2.flip`, lalu mengubah sistem warna dari BGR ke RGB karena MediaPipe memerlukan format RGB. |
| **153** | `                    results = self.recognizer.hands.process(rgb_frame)` | Memproses frame RGB dengan pendeteksi tangan MediaPipe untuk menemukan koordinat landmark tangan. |
| **154** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **155** | `                    smoothed_gesture = "None"` | Menyiapkan nilai default gestur halus sebagai `"None"`. |
| **156** | `                    if results.multi_hand_landmarks:` | Memeriksa apakah ada tangan terdeteksi dalam frame. |
| **157** | `                        hand_landmarks = results.multi_hand_landmarks[0]` | Mengambil data landmark dari tangan pertama yang terdeteksi. |
| **158** | `                        gesture = self.recognizer.recognize(hand_landmarks)` | Memanggil fungsi recognizer untuk menganalisis dan mengenali gestur tangan saat ini. |
| **159** | `                        self._gesture_buffer.append(gesture)` | Memasukkan hasil identifikasi gestur ke dalam buffer antrean `self._gesture_buffer`. |
| **160** | `                        smoothed_gesture = max(set(self._gesture_buffer), key=self._gesture_buffer.count)` | Mengambil gestur yang paling sering muncul (modus) di dalam buffer untuk menghaluskan dan menstabilkan deteksi. |
| **161** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **162** | `                        tip = hand_landmarks.landmark[8]` | Mengambil referensi objek landmark nomor 8 (ujung jari telunjuk). |
| **163** | `                        raw_v_y = self._last_y - tip.y` | Menghitung kecepatan vertikal mentah (`raw_v_y`). Karena koordinat Y bernilai makin kecil di atas, jika Y saat ini (`tip.y`) lebih kecil daripada sebelumnya (`self._last_y`), hasilnya akan positif (berarti tangan digerakkan dengan cepat ke atas). |
| **164** | `                        self._velocity_y = (alpha * raw_v_y) + (1.0 - alpha) * self._velocity_y` | Menghitung kecepatan terfilter menggunakan Exponential Moving Average (EMA) agar grafik perubahan kecepatannya mulus. |
| **165** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **166** | `                        with self._lock:` | Membuka blok aman thread lock untuk memperbarui koordinat dan status. |
| **167** | `                            self._current_gesture = smoothed_gesture` | Memperbarui gestur terdeteksi saat ini dengan hasil gestur yang telah dihaluskan. |
| **168** | `                            t_now = time.time()` | Mendapatkan waktu saat ini. |
| **169** | `                            self._hand_pos[0] = self.filter_x(t_now, tip.x)` | Memasukkan koordinat X ujung telunjuk ke filter OneEuroFilter X dan menyimpan hasilnya ke posisi X kursor. |
| **170** | `                            self._hand_pos[1] = self.filter_y(t_now, tip.y)` | Memasukkan koordinat Y ujung telunjuk ke filter OneEuroFilter Y dan menyimpan hasilnya ke posisi Y kursor. |
| **171** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **172** | `                            if smoothed_gesture == "PISTOL" and self._velocity_y > 0.04:` | Memeriksa kondisi tembakan: jika gesturnya `"PISTOL"` dan terdeteksi gerakan sentakan ke atas dengan kecepatan melebihi ambang batas `0.04`. |
| **173** | `                                if time.time() - self._last_shot_time > 0.25:` | Memeriksa apakah jeda waktu dari tembakan terakhir sudah melebihi 0.25 detik (cooldown tembakan). |
| **174** | `                                    self._recoil_triggered = True` | Jika lolos semua kondisi, aktifkan flag `self._recoil_triggered` (tembakan sukses terpicu). |
| **175** | `                                    self._last_shot_time = time.time()` | Perbarui stempel waktu tembakan terakhir menjadi waktu sekarang. |
| **176** | `                        self._last_y = tip.y` | Memperbarui koordinat Y terakhir dengan koordinat Y saat ini untuk pembacaan frame berikutnya. |
| **177** | `                    else:` | Blok alternatif jika tidak ada tangan terdeteksi pada frame saat ini. |
| **178** | `                        with self._lock: self._current_gesture = "None"` | Mengunci thread lalu menyetel gestur aktif saat ini menjadi `"None"`. |
| **179** | `                except Exception as inner_e:` | Menangkap jika ada kesalahan pemrosesan internal di dalam loop frame. |
| **180** | `                    print(f"MediaPipe Processing Error: {inner_e}")` | Mencetak kesalahan pemrosesan MediaPipe ke konsol. |
| **181** | `                    continue` | Melanjutkan proses ke perulangan frame berikutnya tanpa menghentikan thread. |
| **182** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **183** | `            cap.release()` | Melepaskan objek kamera OpenCV setelah keluar dari loop utama. |
| **184** | `        except Exception as e:` | Menangkap kesalahan utama pada alur thread jika ada. |
| **185** | `            print(f"GestureThread Error: {e}")` | Mencetak pesan error thread utama ke konsol. |
| **186** | `        finally:` | Blok yang selalu dijalankan ketika thread selesai/keluar baik normal maupun saat terjadi error. |
| **187** | `            if hasattr(self.recognizer, 'hands'):` | Memeriksa apakah objek recognizer memiliki atribut `hands`. |
| **188** | `                self.recognizer.hands.close()` | Menutup modul MediaPipe Hands dengan aman untuk membebaskan memori. |
| **189** | `            # cv2.destroyAllWindows()` | Baris komentar opsional untuk menutup semua jendela OpenCV (tidak digunakan). |
| **190** | *(Kosong)* | Baris kosong untuk kerapian kode. |
| **191** | `    def stop(self):` | Metode untuk menghentikan pemrosesan thread secara terkendali dari luar thread. |
| **192** | `        self.running = False` | Menyetel bendera `self.running` menjadi `False` untuk mengakhiri perulangan pembacaan kamera secara aman. |
| **193** | *(Kosong)* | Baris kosong untuk kerapian kode. |

---

## Alur Kerja Utama

Berikut adalah diagram alur kerja logis bagaimana berkas `gestures.py` beroperasi saat digunakan dalam game:

1. **Inisialisasi**:
   - `GestureThread` dibuat dan dijalankan sebagai *daemon thread* latar belakang.
   - Detektor tangan MediaPipe Hands diinisialisasi dalam `GestureRecognizerML`.
   - Berkas model `gesture_model.pkl` dimuat jika tersedia di direktori lokal.
   - Filter `OneEuroFilter` disiapkan untuk menghaluskan pergerakan koordinat kursor.

2. **Looping Pembacaan Frame (di latar belakang)**:
   - Kamera dibaca frame demi frame oleh OpenCV.
   - Setiap frame dibalik (mirror) dan dikonversi ke format RGB.
   - MediaPipe mendeteksi apakah ada koordinat tangan.

3. **Pengenalan Gestur**:
   - Jika tangan terdeteksi, koordinat ujung jari telunjuk (landmark 8) digunakan sebagai penentu posisi kursor.
   - Gestur dideteksi terlebih dahulu menggunakan aturan logika sederhana (misal, mendeteksi `"FIST"` atau `"PISTOL"`).
   - Jika logika sederhana tidak terpenuhi, koordinat relatif tangan diubah menjadi fitur numerik (relatif terhadap pergelangan tangan) dan diprediksi dengan model ML (`gesture_model.pkl`).
   - Hasil deteksi dimasukkan ke buffer antrean sepanjang 5 frame dan dicari nilai terbanyak (modus) untuk mencegah kursor atau status berkedip tidak stabil.

4. **Pemulusan Posisi (Filtering)**:
   - Koordinat X dan Y ujung jari telunjuk dimasukkan ke objek `OneEuroFilter` masing-masing untuk meredam jitter (getaran halus) tangan di depan kamera.
   - Posisi mulus disimpan di `self._hand_pos` agar dapat diambil oleh game utama melalui properti `hand_pos`.

5. **Deteksi Tembakan & Recoil**:
   - Program menghitung selisih koordinat Y ujung telunjuk dengan frame sebelumnya untuk mendeteksi sentakan vertikal ke atas (kecepatan gerakan vertikal, `velocity_y`).
   - Jika gestur yang terdeteksi aktif adalah `"PISTOL"`, dan tangan digerakkan ke atas dengan cepat (melebihi ambang batas kecepatan), serta waktu jeda menembak (cooldown) 0.25 detik terlewati, maka flag `self._recoil_triggered` disetel ke `True`.
   - Game utama dapat membaca status tembakan/recoil ini secara aman melalui properti thread `recoil_active`.
