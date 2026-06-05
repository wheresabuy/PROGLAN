# Penjelasan Kode: train_data.py

Dokumen ini berisi penjelasan detail baris demi baris dari file `train_data.py` dalam bahasa Indonesia. Penjelasan ini dirancang untuk membantu Anda memahami alur dan logika program guna mempersiapkan demo aplikasi.

---

## Deskripsi & Tujuan File
File `train_data.py` adalah skrip Python yang digunakan untuk **mengumpulkan data koordinat tangan (landmarks)** guna melatih model klasifikasi gestur tangan. 
Skrip ini memanfaatkan kamera (atau aliran video IP Webcam) untuk mendeteksi tangan secara real-time menggunakan pustaka **MediaPipe Hands**. Koordinat dari 21 titik (landmark) tangan akan diekstrak, dihitung secara relatif terhadap pergelangan tangan (untuk menjaga konsistensi posisi tangan di layar), dan disimpan ke dalam file dataset berformat CSV (`gesture_data.csv`).

---

## Daftar Import

Berikut adalah modul/pustaka yang diimpor pada bagian awal kode:

| Library | Kegunaan |
| :--- | :--- |
| `cv2` (OpenCV) | Mengakses kamera, membaca frame video, memproses gambar (seperti flip dan konversi warna), menampilkan GUI windows, dan menggambar teks overlay. |
| `mediapipe` (`mp`) | Mendeteksi tangan dan mengekstrak 21 koordinat titik-titik sendi tangan (landmarks) secara real-time menggunakan Machine Learning. |
| `csv` | Menulis data landmark tangan dan label gestur ke dalam file dataset berformat `.csv`. |
| `os` | Memanipulasi path direktori dan file secara dinamis sehingga program dapat berjalan tanpa error path relatif. |

---

## Penjelasan Baris Demi Baris

Berikut adalah rincian penjelasan dari setiap baris kode di `train_data.py`:

| Baris | Kode Sumber | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import cv2` | Mengimpor pustaka OpenCV untuk pemrosesan citra dan video capture. |
| **2** | `import mediapipe as mp` | Mengimpor MediaPipe untuk melacak titik-titik koordinat tangan. |
| **3** | `import csv` | Mengimpor modul CSV bawaan Python untuk menyimpan dataset hasil ekstraksi. |
| **4** | `import os` | Mengimpor modul OS untuk mengatur path penyimpanan file data secara dinamis. |
| **5** | *(Baris Kosong)* | Pemisah estetika kode. |
| **6** | `class DataCollector:` | Mendefinisikan kelas `DataCollector` yang bertanggung jawab menginisialisasi detektor tangan dan mengelola penyimpanan data. |
| **7** | `    def __init__(self):` | Konstruktor kelas untuk menginisialisasi konfigurasi MediaPipe dan file CSV. |
| **8** | `        self.mp_hands = mp.solutions.hands` | Membuat alias/referensi ke modul deteksi tangan (`Hands`) dari MediaPipe. |
| **9** | `        self.hands = self.mp_hands.Hands(` | Menginisialisasi objek detektor tangan MediaPipe dengan parameter kustom. |
| **10** | `            static_image_mode=False,` | `False` berarti memproses aliran frame video (tracking berkelanjutan), bukan gambar statis satu per satu. Ini meningkatkan performa pelacakan. |
| **11** | `            max_num_hands=1,` | Membatasi jumlah tangan yang dideteksi maksimal hanya 1 tangan dalam satu waktu. |
| **12** | `            min_detection_confidence=0.7,` | Batas minimal akurasi deteksi pertama kali (70%) agar tangan dianggap terdeteksi. |
| **13** | `            min_tracking_confidence=0.5` | Batas minimal akurasi tracking (50%) untuk tetap melacak tangan yang sudah terdeteksi di frame berikutnya. |
| **14** | `        )` | Menutup inisialisasi objek `Hands`. |
| **15** | `        self.mp_draw = mp.solutions.drawing_utils` | Mengambil utilitas bawaan MediaPipe untuk menggambar titik koordinat (*landmarks*) dan garis penghubungnya pada layar. |
| **16** | *(Baris Kosong)* | Pemisah estetika kode. |
| **17** | `        # Gunakan path absolut agar tidak error saat dipanggil dari mana saja` | Komentar penjelasan mengenai alasan penggunaan path absolut. |
| **18** | `        base_dir = os.path.dirname(os.path.abspath(__file__))` | Mendapatkan path direktori absolut tempat file `train_data.py` berada. |
| **19** | `        self.data_file = os.path.join(base_dir, 'gesture_data.csv')` | Menggabungkan path direktori dengan nama file output `gesture_data.csv` untuk membuat path absolut file tujuan. |
| **20** | *(Baris Kosong)* | Pemisah estetika kode. |
| **21** | `        # Inisialisasi file CSV jika belum ada` | Komentar penjelas inisialisasi file dataset. |
| **22** | `        if not os.path.exists(self.data_file):` | Memeriksa apakah file `gesture_data.csv` sudah ada di direktori tersebut. |
| **23** | `            print(f"Membuat file data baru di: {self.data_file}")` | Menampilkan log ke konsol bahwa file dataset baru akan dibuat. |
| **24** | `            with open(self.data_file, mode='w', newline='') as f:` | Membuka/membuat file CSV baru dalam mode tulis (`'w'`) dengan penanganan baris baru kosong (`newline=''`). |
| **25** | `                writer = csv.writer(f)` | Membuat objek penulis CSV. |
| **26** | `                # 21 landmarks * 3 (x, y, z) + label` | Komentar penjelas struktur kolom data. Ada 21 titik, masing-masing memiliki 3 koordinat ruang (X, Y, Z), ditambah 1 kolom label. |
| **27** | `                header = [f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)] + ['label']` | Membuat daftar nama kolom header, contoh: `x0, x1..x20, y0..y20, z0..z20, label` (total 64 kolom). |
| **28** | `                writer.writerow(header)` | Menulis kolom header tersebut sebagai baris pertama di file CSV. |
| **29** | *(Baris Kosong)* | Pemisah estetika kode. |
| **30** | `    def save_landmarks(self, landmarks, label):` | Fungsi untuk memproses dan menyimpan koordinat titik tangan beserta labelnya ke CSV. |
| **31** | `        data = []` | Membuat list kosong `data` untuk menampung seluruh koordinat terproses dalam satu frame. |
| **32** | `        # Gunakan pergelangan tangan (landmark 0) sebagai titik referensi (0,0)` | Komentar penjelasan normalisasi koordinat relatif. |
| **33** | `        wrist = landmarks.landmark[0]` | Mengambil data koordinat landmark indeks ke-0 (yaitu pergelangan tangan / wrist) sebagai patokan/titik pusat (0,0). |
| **34** | *(Baris Kosong)* | Pemisah estetika kode. |
| **35** | `        # Simpan koordinat relatif (selisih dari pergelangan tangan)` | Komentar tentang cara menghitung koordinat relatif. |
| **36** | `        for lm in landmarks.landmark:` | Melakukan perulangan untuk 21 titik koordinat untuk sumbu X. |
| **37** | `            data.append(lm.x - wrist.x)` | Menghitung selisih koordinat X setiap titik terhadap koordinat X pergelangan tangan, lalu menambahkannya ke list `data`. |
| **38** | `        for lm in landmarks.landmark:` | Melakukan perulangan untuk 21 titik koordinat untuk sumbu Y. |
| **39** | `            data.append(lm.y - wrist.y)` | Menghitung selisih koordinat Y setiap titik terhadap koordinat Y pergelangan tangan, lalu menambahkannya ke list `data`. |
| **40** | `        for lm in landmarks.landmark:` | Melakukan perulangan untuk 21 titik koordinat untuk sumbu Z. |
| **41** | `            data.append(lm.z - wrist.z)` | Menghitung selisih koordinat Z setiap titik terhadap koordinat Z pergelangan tangan, lalu menambahkannya ke list `data`. |
| **42** | *(Baris Kosong)* | Pemisah estetika kode. |
| **43** | `        data.append(label)` | Memasukkan nama label gestur (misalnya "OK" atau "SPIDERMAN") di akhir list `data`. |
| **44** | *(Baris Kosong)* | Pemisah estetika kode. |
| **45** | `        with open(self.data_file, mode='a', newline='') as f:` | Membuka file CSV dengan mode tambah (`'a'` / append) agar data baru ditambahkan ke baris bawah tanpa menghapus data lama. |
| **46** | `            writer = csv.writer(f)` | Membuat objek penulis CSV. |
| **47** | `            writer.writerow(data)` | Menulis list data koordinat relatif beserta labelnya ke dalam file CSV sebagai baris baru. |
| **48** | *(Baris Kosong)* | Pemisah estetika kode. |
| **49** | `def main():` | Fungsi utama program untuk menjalankan loop kamera dan interaksi keyboard. |
| **50** | `    path = 'http://10.193.124.171:8080/video'` | String URL video stream dari IP Webcam di perangkat mobile/eksternal. |
| **51** | `    cap = cv2.VideoCapture(path)` | Membuka aliran video berdasarkan URL IP Webcam tersebut menggunakan OpenCV. |
| **52** | `    collector = DataCollector()` | Menginisialisasi objek `collector` dari kelas `DataCollector`. |
| **53** | *(Baris Kosong)* | Pemisah estetika kode. |
| **54** | `    current_label = ""` | Variabel untuk menyimpan label gestur aktif saat ini (kosong di awal). |
| **55** | `    recording = False` | Status boolean apakah data koordinat sedang direkam (`True`) atau tidak (`False`). |
| **56** | `    count = 0` | Menghitung jumlah sampel data (frame) yang berhasil disimpan selama perekaman aktif. |
| **57** | *(Baris Kosong)* | Pemisah estetika kode. |
| **58** | `    print("--- DATA COLLECTOR ---")` | Menampilkan teks sambutan di konsol. |
| **59** | `    print("1. Tekan 'l' untuk memasukkan nama label baru (misal: 'OK', 'SPIDERMAN')")` | Menampilkan petunjuk konsol untuk memasukkan label baru. |
| **60** | `    print("2. Tekan 's' untuk mulai/berhenti merekam data")` | Menampilkan petunjuk konsol untuk merekam data. |
| **61** | `    print("3. Tekan 'q' untuk keluar")` | Menampilkan petunjuk konsol untuk keluar dari program. |
| **62** | *(Baris Kosong)* | Pemisah estetika kode. |
| **63** | `    while cap.isOpened():` | Melakukan perulangan selama aliran video kamera berhasil terbuka dan aktif. |
| **64** | `        ret, frame = cap.read()` | Membaca frame gambar dari kamera. `ret` bernilai True jika berhasil membaca frame, `frame` berisi matriks gambar. |
| **65** | `        if not ret: break` | Jika gagal mengambil frame (misal koneksi putus), perulangan dihentikan (`break`). |
| **66** | *(Baris Kosong)* | Pemisah estetika kode. |
| **67** | `        frame = cv2.flip(frame, 1)` | Memutar/flip gambar secara horizontal (mirroring) agar gerakan tangan di layar sesuai dengan arah gerakan asli pengguna. |
| **68** | `        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)` | Mengonversi format warna frame dari BGR (standar OpenCV) ke RGB (standar MediaPipe). |
| **69** | `        results = collector.hands.process(rgb_frame)` | Memproses gambar RGB menggunakan MediaPipe untuk mencari keberadaan tangan. |
| **70** | *(Baris Kosong)* | Pemisah estetika kode. |
| **71** | `        if results.multi_hand_landmarks:` | Memeriksa apakah ada tangan yang terdeteksi di dalam frame. |
| **72** | `            for hand_landmarks in results.multi_hand_landmarks:` | Melakukan perulangan untuk setiap tangan yang terdeteksi (meskipun dibatasi 1 tangan di konfigurasi). |
| **73** | `                collector.mp_draw.draw_landmarks(frame, hand_landmarks, collector.mp_hands.HAND_CONNECTIONS)` | Menggambar titik-titik landmark beserta garis penghubung antar sendi tangan pada frame video. |
| **74** | *(Baris Kosong)* | Pemisah estetika kode. |
| **75** | `                if recording and current_label:` | Jika status perekaman aktif (`recording=True`) dan label gestur sudah ditentukan. |
| **76** | `                    collector.save_landmarks(hand_landmarks, current_label)` | Memanggil fungsi `save_landmarks` untuk menghitung koordinat relatif dan menyimpannya ke CSV. |
| **77** | `                    count += 1` | Menambah jumlah sampel tersimpan sebanyak 1. |
| **78** | *(Baris Kosong)* | Pemisah estetika kode. |
| **79** | `        # UI Overlay` | Komentar penjelas pembuatan visual status pada jendela video. |
| **80** | `        status = f"REC: {current_label}" if recording else "IDLE"` | Menentukan teks status ("REC: nama_label" jika sedang merekam, "IDLE" jika berhenti). |
| **81** | `        cv2.putText(frame, f"Status: {status} | Samples: {count}", (10, 30),` | Menulis status dan jumlah sampel ke frame video pada posisi koordinat (10, 30). |
| **82** | `                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if recording else (0, 255, 0), 2)` | Mengatur jenis font, ukuran, warna (merah saat merekam, hijau saat idle), dan ketebalan garis teks. |
| **83** | *(Baris Kosong)* | Pemisah estetika kode. |
| **84** | `        cv2.imshow('Data Collector', frame)` | Menampilkan frame video yang telah diproses ke dalam jendela GUI bernama 'Data Collector'. |
| **85** | *(Baris Kosong)* | Pemisah estetika kode. |
| **86** | `        key = cv2.waitKey(1) & 0xFF` | Menunggu input keyboard selama 1 milidetik dan mengambil 8 bit terakhir dari nilai input key. |
| **87** | `        if key == ord('q'):` | Jika pengguna menekan tombol `'q'`. |
| **88** | `            break` | Menghentikan loop utama untuk menutup aplikasi. |
| **89** | `        elif key == ord('l'):` | Jika pengguna menekan tombol `'l'`. |
| **90** | `            current_label = input("Masukkan nama label gestur baru: ")` | Meminta input string dari terminal konsol untuk nama label baru. |
| **91** | `            count = 0` | Mereset penghitung jumlah sampel kembali ke 0 untuk label baru tersebut. |
| **92** | `            print(f"Label diatur ke: {current_label}")` | Menampilkan pesan konfirmasi label aktif ke konsol. |
| **93** | `        elif key == ord('s'):` | Jika pengguna menekan tombol `'s'`. |
| **94** | `            if not current_label:` | Memeriksa apakah pengguna mencoba merekam tanpa mengisi nama label terlebih dahulu. |
| **95** | `                print("Error: Masukkan label dulu (tekan 'l')")` | Menampilkan pesan error di konsol jika label masih kosong. |
| **96** | `            else:` | Jika label sudah ada. |
| **97** | `                recording = not recording` | Membalik status boolean `recording` (mulai merekam jika idle, atau sebaliknya). |
| **98** | `                print(f"Recording: {recording}")` | Menampilkan status perekaman terbaru ke konsol. |
| **99** | *(Baris Kosong)* | Pemisah estetika kode. |
| **100**| `    cap.release()` | Membebaskan objek kamera/video capture dari memori sistem. |
| **101**| `    cv2.destroyAllWindows()` | Menutup semua jendela GUI OpenCV yang terbuka di layar. |
| **102**| *(Baris Kosong)* | Pemisah estetika kode. |
| **103**| `if __name__ == "__main__":` | Memastikan fungsi `main()` dijalankan hanya jika file ini dieksekusi secara langsung, bukan sebagai modul impor. |
| **104**| `    main()` | Memanggil fungsi utama program. |
| **105**| *(Baris Kosong)* | Pemisah akhir file. |

---

## Alur Kerja Utama

1. **Inisialisasi**:
   - Detektor MediaPipe Hands disiapkan untuk memproses 1 tangan secara real-time.
   - File dataset `gesture_data.csv` diperiksa. Jika belum ada, program akan otomatis membuatnya lengkap dengan baris pertama berupa nama kolom-kolom koordinat (`x0..x20, y0..y20, z0..z20, label`).
2. **Koneksi Kamera / IP Stream**:
   - Program menghubungkan koneksi video capture ke alamat IP kamera lokal.
3. **Loop Utama (Frame by Frame Processing)**:
   - Setiap frame dibaca dari kamera, dibalik secara horizontal (mirroring), dan format warnanya dikonversi ke RGB.
   - Frame dikirim ke MediaPipe Hands untuk mendeteksi landmark tangan.
   - Jika tangan terdeteksi, titik koordinatnya digambar di atas frame.
4. **Penyimpanan Koordinat Relatif**:
   - Jika status perekaman aktif (`recording=True`) dan label aktif (`current_label` tidak kosong), setiap frame yang memiliki deteksi tangan akan memicu ekstraksi 21 koordinat X, Y, dan Z.
   - Koordinat yang disimpan **bukanlah nilai piksel mentah di layar**, melainkan **jarak relatif** setiap titik landmark dari titik pergelangan tangan (landmark indeks 0 / wrist). Cara ini menjaga data tetap konsisten dan akurat terlepas dari posisi tangan pengguna di dalam area tangkapan kamera.
   - Data koordinat relatif dan nama label yang aktif disimpan sebagai satu baris baru di file CSV.
5. **Kontrol Interaktif**:
   - **Tombol 'l'**: Menentukan atau mengubah nama kategori gestur saat ini melalui input teks di terminal.
   - **Tombol 's'**: Toggle untuk menyalakan/mematikan perekaman data landmark secara real-time.
   - **Tombol 'q'**: Menutup program dengan aman.
