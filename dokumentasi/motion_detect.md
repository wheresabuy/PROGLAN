# Penjelasan Source Code: `motion_detect.py`

Dokumen ini berisi penjelasan detail dan baris demi baris dari file Python `motion_detect.py`. File ini mendeteksi gerakan tangan (gesture swipe) menggunakan webcam berbasis pustaka OpenCV dan MediaPipe.

---

## Deskripsi & Tujuan File
File `motion_detect.py` mendefinisikan kelas `MotionDetector` yang memantau pergerakan posisi pergelangan tangan (*wrist*) pengguna. Dengan menganalisis perubahan posisi *wrist* selama 15 frame terakhir, program dapat mengidentifikasi empat gerakan gesekan tangan (*swipe*):
1. **SWIPE LEFT** (Geser ke Kiri)
2. **SWIPE RIGHT** (Geser ke Kanan)
3. **SWIPE UP** (Geser ke Atas)
4. **SWIPE DOWN** (Geser ke Bawah)

Program ini juga memiliki fungsi `main()` yang memungkinkan skrip dijalankan langsung untuk mendemonstrasikan pendeteksian secara *real-time* menggunakan kamera/webcam laptop.

---

## Daftar Import
Berikut adalah modul dan pustaka yang digunakan dalam kode ini beserta penjelasannya:

| Pustaka / Modul | Deskripsi |
| :--- | :--- |
| `cv2` | Pustaka OpenCV (Open Source Computer Vision Library) yang digunakan untuk menangkap video dari webcam, pemrosesan frame gambar (konversi warna, membalik gambar), menampilkan gambar pada jendela, dan menuliskan teks deteksi ke layar. |
| `mediapipe` (sebagai `mp`) | Framework buatan Google untuk mendeteksi *landmarks* (titik acuan) tubuh manusia secara *real-time*. Di sini digunakan modul deteksi tangan (*Hands tracking*). |
| `collections` | Modul bawaan Python yang digunakan untuk struktur data `deque` (antrean ujung ganda) dengan kapasitas maksimum tetap (*fixed-size buffer*) untuk menyimpan koordinat riwayat gerakan. |
| `time` | Modul bawaan Python untuk manipulasi waktu (misalnya menghitung FPS atau jeda waktu jika diperlukan). |
| `math` | Modul bawaan Python untuk operasi matematika tingkat lanjut. |

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel penjelasan detail untuk setiap baris kode:

| No. Baris | Kode Sumber | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import cv2` | Mengimpor pustaka OpenCV untuk menangani kamera dan pengolahan citra/video. |
| **2** | `import mediapipe as mp` | Mengimpor MediaPipe untuk mendeteksi koordinat tangan. |
| **3** | `import collections` | Mengimpor modul `collections` untuk menggunakan objek `deque` sebagai buffer. |
| **4** | `import time` | Mengimpor pustaka waktu Python. |
| **5** | `import math` | Mengimpor pustaka matematika Python. |
| **6** | *(baris kosong)* | Pemisah visual antarkode. |
| **7** | `class MotionDetector:` | Mendefinisikan kelas utama `MotionDetector`. |
| **8** | `    def __init__(self, buffer_size=15):` | Konstruktor kelas dengan parameter kapasitas histori frame (`buffer_size` bawaan bernilai 15). |
| **9** | `        self.mp_hands = mp.solutions.hands` | Mengambil modul API tangan (*Hands*) dari pustaka MediaPipe. |
| **10** | `        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)` | Menginisialisasi objek deteksi tangan dengan batas maksimal 1 tangan dan kepercayaan pendeteksian minimal 70% (0.7) agar lebih akurat. |
| **11** | *(baris kosong)* | Pemisah visual. |
| **12** | `        # Buffer untuk menyimpan histori posisi pergelangan tangan (wrist)` | Komentar penjelasan fungsi *buffer* histori pergelangan tangan. |
| **13** | `        # deque otomatis menghapus data terlama saat data baru masuk` | Komentar cara kerja `deque` berukuran tetap. |
| **14** | `        self.history = collections.deque(maxlen=buffer_size)` | Membuat objek antrean `deque` dengan kapasitas maksimum `buffer_size` (15 frame) untuk melacak pergerakan koordinat pergelangan tangan. |
| **15** | `        self.swipe_threshold = 0.15 # Minimal jarak perpindahan untuk dianggap swipe (0.0 - 1.0)` | Menetapkan batas minimal jarak perpindahan *wrist* sebesar 0.15 (dalam skala koordinat ter-normalisasi 0 hingga 1) untuk memicu deteksi gerakan *swipe*. |
| **16** | *(baris kosong)* | Pemisah visual. |
| **17** | `    def detect_motion(self, frame):` | Mendefinisikan metode utama `detect_motion` yang menerima frame gambar masukan untuk mendeteksi gerakan. |
| **18** | `        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)` | Mengubah format warna gambar dari BGR (format bawaan OpenCV) ke RGB (format yang dibutuhkan MediaPipe). |
| **19** | `        results = self.hands.process(rgb_frame)` | Memproses frame RGB dengan model deteksi tangan MediaPipe untuk mengekstrak *landmarks* tangan. |
| **20** | *(baris kosong)* | Pemisah visual. |
| **21** | `        motion = "None"` | Menyiapkan nilai *default* gerakan yang terdeteksi sebagai `"None"`. |
| **22** | *(baris kosong)* | Pemisah visual. |
| **23** | `        if results.multi_hand_landmarks:` | Memeriksa apakah ada objek tangan yang berhasil dideteksi dalam frame tersebut. |
| **24** | `            # Ambil koordinat Wrist (Landmark 0)` | Komentar penjelasan untuk mengambil titik koordinat pergelangan tangan (*wrist* / titik landmark ke-0). |
| **25** | `            wrist = results.multi_hand_landmarks[0].landmark[0]` | Mengakses tangan pertama yang terdeteksi (`[0]`) lalu mengambil objek koordinat pergelangan tangan (`landmark[0]`). |
| **26** | `            current_pos = (wrist.x, wrist.y)` | Mengambil nilai koordinat X dan Y pergelangan tangan dalam bentuk tuple `(x, y)`. |
| **27** | `            self.history.append(current_pos)` | Memasukkan tuple koordinat saat ini ke dalam buffer riwayat `self.history`. |
| **28** | *(baris kosong)* | Pemisah visual. |
| **29** | `            # Jika buffer sudah penuh, mulai hitung pergerakan` | Komentar yang menunjukkan perhitungan gerakan baru dimulai saat data buffer telah penuh. |
| **30** | `            if len(self.history) == self.history.maxlen:` | Mengecek apakah buffer histori sudah terisi penuh sesuai ukuran maksimum (15 elemen). |
| **31** | `                start_pos = self.history[0] # Posisi 15 frame yang lalu` | Mengambil titik koordinat wrist pada frame terlama (15 frame yang lalu) di dalam buffer. |
| **32** | `                end_pos = self.history[-1]   # Posisi sekarang` | Mengambil titik koordinat wrist pada frame terbaru (saat ini) di dalam buffer. |
| **33** | *(baris kosong)* | Pemisah visual. |
| **34** | `                dx = end_pos[0] - start_pos[0]` | Menghitung selisih koordinat X (horizontal). Hasil positif berarti gerak ke kanan, negatif ke kiri. |
| **35** | `                dy = end_pos[1] - start_pos[1]` | Menghitung selisih koordinat Y (vertikal). Hasil positif berarti gerak ke bawah (karena titik 0,0 berada di sudut kiri atas layar), negatif ke atas. |
| **36** | *(baris kosong)* | Pemisah visual. |
| **37** | `                # Cek pergerakan horizontal (Swipe)` | Komentar penjelasan untuk deteksi gerakan horizontal. |
| **38** | `                if abs(dx) > self.swipe_threshold and abs(dx) > abs(dy):` | Mengecek apakah jarak horizontal mutlak (`abs(dx)`) melebihi ambang batas, dan pergerakan horizontal lebih dominan/besar daripada pergerakan vertikal (`abs(dx) > abs(dy)`). |
| **39** | `                    if dx > 0:` | Mengecek apakah pergerakan menuju ke arah kanan (nilai selisih positif). |
| **40** | `                        motion = "SWIPE RIGHT"` | Mengubah status gerakan terdeteksi menjadi `"SWIPE RIGHT"`. |
| **41** | `                    else:` | Jika pergerakan menuju ke arah kiri (nilai selisih negatif). |
| **42** | `                        motion = "SWIPE LEFT"` | Mengubah status gerakan terdeteksi menjadi `"SWIPE LEFT"`. |
| **43** | `                    self.history.clear() # Reset setelah terdeteksi agar tidak terulang` | Mengosongkan buffer histori agar gerakan yang sama tidak terdeteksi berkali-kali pada frame berikutnya. |
| **44** | *(baris kosong)* | Pemisah visual. |
| **45** | `                # Cek pergerakan vertikal` | Komentar penjelasan untuk deteksi gerakan vertikal. |
| **46** | `                elif abs(dy) > self.swipe_threshold and abs(dy) > abs(dx):` | Mengecek apakah jarak vertikal mutlak (`abs(dy)`) melebihi ambang batas, dan pergerakan vertikal lebih dominan daripada pergerakan horizontal. |
| **47** | `                    if dy > 0:` | Mengecek apakah pergerakan menuju ke arah bawah (nilai selisih positif). |
| **48** | `                        motion = "SWIPE DOWN"` | Mengubah status gerakan terdeteksi menjadi `"SWIPE DOWN"`. |
| **49** | `                    else:` | Jika pergerakan menuju ke arah atas (nilai selisih negatif). |
| **50** | `                        motion = "SWIPE UP"` | Mengubah status gerakan terdeteksi menjadi `"SWIPE UP"`. |
| **51** | `                    self.history.clear()` | Mengosongkan buffer histori setelah mendeteksi swipe vertikal. |
| **52** | *(baris kosong)* | Pemisah visual. |
| **53** | `        return motion` | Mengembalikan status gerakan yang terdeteksi (`motion`). |
| **54** | *(baris kosong)* | Pemisah visual. |
| **55** | `def main():` | Mendefinisikan fungsi utama untuk eksekusi mandiri program demo. |
| **56** | `    # Contoh penggunaan mandiri menggunakan webca` | Komentar penjelasan demo menggunakan kamera/webcam. |
| **57** | `    cap = cv2.VideoCapture(0) # Gunakan 0 untuk webcam lokal` | Mengakses dan membuka kamera/webcam default bawaan komputer menggunakan OpenCV. |
| **58** | `    detector = MotionDetector()` | Membuat objek `detector` dari kelas `MotionDetector`. |
| **59** | *(baris kosong)* | Pemisah visual. |
| **60** | `    print("Gerakkan tanganmu ke kiri atau kanan dengan cepat!")` | Mencetak teks panduan awal pada jendela terminal. |
| **61** | *(baris kosong)* | Pemisah visual. |
| **62** | `    while cap.isOpened():` | Memulai loop berkelanjutan selama kamera/webcam terhubung dan terbuka dengan baik. |
| **63** | `        ret, frame = cap.read()` | Membaca frame terbaru dari video webcam. `ret` adalah status keberhasilan (True/False), `frame` adalah gambar yang ditangkap. |
| **64** | `        if not ret: break` | Menghentikan loop jika pembacaan frame gagal (misal kamera terputus). |
| **65** | *(baris kosong)* | Pemisah visual. |
| **66** | `        frame = cv2.flip(frame, 1)` | Membalik frame secara horizontal (efek cermin) agar interaksi terasa natural bagi pengguna. |
| **67** | `        motion = detector.detect_motion(frame)` | Memanggil metode deteksi gerakan pada frame saat ini untuk mengecek gerakan swipe. |
| **68** | *(baris kosong)* | Pemisah visual. |
| **69** | `        if motion != "None":` | Mengecek jika terdeteksi adanya gerakan tertentu (bukan `"None"`). |
| **70** | `            print(f"Action Terdeteksi: {motion}")` | Mencetak informasi gerakan yang terdeteksi ke konsol terminal. |
| **71** | `            cv2.putText(frame, motion, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)` | Menggambar teks gerakan di atas frame video dengan ukuran font 2, warna hijau, dan ketebalan garis 3. |
| **72** | *(baris kosong)* | Pemisah visual. |
| **73** | `        cv2.imshow("Motion Detection Demo", frame)` | Menampilkan jendela baru dengan nama "Motion Detection Demo" yang memuat visualisasi video langsung dari webcam. |
| **74** | `        if cv2.waitKey(1) & 0xFF == ord('q'):` | Menunggu input keyboard selama 1 milidetik dan mengecek apakah pengguna menekan tombol `'q'`. |
| **75** | `            break` | Keluar dari loop dan mengakhiri demo jika tombol `'q'` ditekan. |
| **76** | *(baris kosong)* | Pemisah visual. |
| **77** | `    cap.release()` | Melepaskan hak akses ke perangkat webcam agar bisa digunakan oleh aplikasi lain. |
| **78** | `    cv2.destroyAllWindows()` | Menutup dan membersihkan seluruh jendela GUI OpenCV yang terbuka. |
| **79** | *(baris kosong)* | Pemisah visual. |
| **80** | `if __name__ == "__main__":` | Memastikan blok kode di bawahnya hanya dieksekusi jika file dijalankan secara langsung, bukan sebagai modul impor. |
| **81** | `    main()` | Memanggil fungsi `main()` untuk menjalankan demo program. |
| **82** | *(baris kosong)* | Akhir baris kosong file. |

---

## Alur Kerja Utama
1. **Inisialisasi**: Program mengaktifkan pustaka MediaPipe Hands untuk memproses citra tangan dan membuat objek `deque` berukuran maksimum 15 untuk melacak pergerakan koordinat pergelangan tangan (*wrist*).
2. **Pengambilan Frame**: Gambar dari webcam ditangkap satu per satu, kemudian dibalik secara horizontal (efek cermin) agar gerakan terasa natural.
3. **Deteksi Tangan & Koordinat**: Frame dikonversi ke format RGB. MediaPipe mendeteksi tangan dan mengambil koordinat `(x, y)` titik pergelangan tangan (*wrist* / landmark index 0). Koordinat ini disimpan ke dalam buffer histori.
4. **Analisis Gerakan (Gestur)**: Setelah buffer terisi penuh (15 koordinat terakhir), program menghitung selisih koordinat terkini dengan koordinat 15 frame sebelumnya (`dx` dan `dy`).
   - Jika pergerakan horizontal dominan dan melebihi batas toleransi (`swipe_threshold`), program menetapkan gerakan sebagai **SWIPE RIGHT** atau **SWIPE LEFT**.
   - Jika pergerakan vertikal dominan dan melebihi batas toleransi, program menetapkan gerakan sebagai **SWIPE DOWN** atau **SWIPE UP**.
5. **Aksi & Reset**: Ketika suatu gerakan terdeteksi, program mencetaknya di layar dan terminal, lalu segera mengosongkan buffer histori (`history.clear()`) agar gerakan tersebut tidak terdeteksi ganda secara terus-menerus.
6. **Siklus Loop**: Proses di atas diulangi terus-menerus hingga pengguna menekan tombol `'q'` untuk menutup aplikasi.
