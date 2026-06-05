# Penjelasan Kode: `reset_data.py`

## Deskripsi & Tujuan File
File `reset_data.py` digunakan untuk mereset atau menghapus seluruh data rekaman gestur (`gesture_data.csv`) dan model hasil latihan (`gesture_model.pkl`) yang berada di direktori yang sama dengan skrip ini. Tujuannya adalah untuk memudahkan pengguna jika ingin merekam atau melatih model gestur dari awal (bersih) dengan memberikan konfirmasi keamanan terlebih dahulu agar data tidak terhapus secara tidak sengaja.

## Daftar Import
*   **`import os`**: Modul bawaan Python yang digunakan untuk berinteraksi dengan sistem operasi, seperti mendeteksi keberadaan file (`os.path.exists`), menghapus file (`os.remove`), dan memanipulasi jalur direktori (`os.path.join`, `os.path.abspath`, `os.path.dirname`).

## Penjelasan Baris Demi Baris

| Baris | Kode | Penjelasan |
| :--- | :--- | :--- |
| **1** | `import os` | Mengimpor modul `os` untuk mengelola file dan direktori pada sistem operasi. |
| **2** | *[Baris Kosong]* | Digunakan sebagai pemisah kode agar lebih mudah dibaca sesuai standar PEP 8. |
| **3** | `def reset_gesture_data():` | Mendefinisikan fungsi utama bernama `reset_gesture_data` yang berisi logika untuk mereset data. |
| **4** | `base_dir = os.path.dirname(os.path.abspath(__file__))` | Mengambil jalur folder/direktori tempat file `reset_data.py` berada secara absolut. |
| **5** | `data_path = os.path.join(base_dir, 'gesture_data.csv')` | Menggabungkan `base_dir` dengan `'gesture_data.csv'` untuk mendapatkan lokasi file data gestur. |
| **6** | `model_path = os.path.join(base_dir, 'gesture_model.pkl')` | Menggabungkan `base_dir` dengan `'gesture_model.pkl'` untuk mendapatkan lokasi file model yang disimpan. |
| **7** | *[Baris Kosong]* | Digunakan sebagai pemisah visual antar bagian kode. |
| **8** | `print("--- RESET DATA GESTUR ---")` | Menampilkan judul/header proses reset di terminal. |
| **9** | `confirm = input("Apakah Anda yakin ingin menghapus semua data rekaman dan model? (y/n): ")` | Meminta konfirmasi dari pengguna melalui input terminal berupa teks (y/n). |
| **10** | *[Baris Kosong]* | Digunakan sebagai pemisah visual antar bagian kode. |
| **11** | `if confirm.lower() == 'y':` | Mengevaluasi input pengguna. Jika pengguna memasukkan huruf 'y' atau 'Y' (diubah ke huruf kecil dengan `.lower()`), maka proses penghapusan dimulai. |
| **12** | `removed = []` | Menginisialisasi list kosong `removed` untuk menampung nama file yang berhasil dihapus. |
| **13** | `if os.path.exists(data_path):` | Memeriksa apakah file `gesture_data.csv` benar-benar ada di direktori tersebut. |
| **14** | `os.remove(data_path)` | Menghapus file `gesture_data.csv` dari sistem penyimpanan jika file tersebut ditemukan. |
| **15** | `removed.append("gesture_data.csv")` | Menambahkan nama file `"gesture_data.csv"` ke dalam list `removed` untuk dicatat. |
| **16** | *[Baris Kosong]* | Digunakan sebagai pemisah visual antar blok pengecekan file. |
| **17** | `if os.path.exists(model_path):` | Memeriksa apakah file model `gesture_model.pkl` ada di direktori tersebut. |
| **18** | `os.remove(model_path)` | Menghapus file model `gesture_model.pkl` jika file tersebut ditemukan. |
| **19** | `removed.append("gesture_model.pkl")` | Menambahkan nama file `"gesture_model.pkl"` ke dalam list `removed` untuk dicatat. |
| **20** | *[Baris Kosong]* | Digunakan sebagai pemisah visual antar blok. |
| **21** | `if removed:` | Memeriksa apakah list `removed` memiliki isi (berarti ada minimal satu file yang berhasil dihapus). |
| **22** | `print(f"Berhasil menghapus: {', '.join(removed)}")` | Menampilkan pesan konfirmasi berupa daftar file yang berhasil dihapus dengan menggabungkannya menggunakan tanda koma. |
| **23** | `print("Sekarang Anda bisa mulai merekam data dari awal.")` | Menampilkan instruksi lanjutan bahwa data gestur siap direkam kembali dari awal. |
| **24** | `else:` | Bagian alternatif jika list `removed` kosong (tidak ada file yang berhasil dihapus). |
| **25** | `print("Tidak ada data atau model yang ditemukan untuk dihapus.")` | Menampilkan pesan bahwa file data dan model memang belum ada atau sudah dihapus sebelumnya. |
| **26** | `else:` | Bagian alternatif jika input konfirmasi pengguna bukan `'y'` atau `'Y'`. |
| **27** | `print("Reset dibatalkan.")` | Menampilkan pesan bahwa proses penghapusan dibatalkan. |
| **28** | *[Baris Kosong]* | Digunakan sebagai pemisah visual sebelum blok eksekusi utama. |
| **29** | `if __name__ == "__main__":` | Memastikan skrip dijalankan secara langsung (sebagai program utama), bukan karena diimpor oleh modul lain. |
| **30** | `reset_gesture_data()` | Memanggil fungsi `reset_gesture_data()` untuk memulai proses penghapusan. |
| **31** | *[Baris Kosong]* | Karakter baris kosong standar di akhir berkas Python. |

## Alur Kerja Utama
1. **Inisialisasi Path**: Program mendeteksi direktori aktif dan menentukan lokasi absolut file data (`gesture_data.csv`) dan model (`gesture_model.pkl`).
2. **Konfirmasi Pengguna**: Program menampilkan prompt konfirmasi tindakan berbahaya (menghapus file) kepada pengguna.
3. **Pengecekan & Penghapusan**:
   * Jika pengguna mengonfirmasi (`y`/`Y`), program memeriksa keberadaan masing-masing file satu per satu.
   * Jika file ditemukan, program menghapusnya dari penyimpanan lokal dan mencatatnya ke list keberhasilan.
   * Program memberikan laporan tentang file apa saja yang telah berhasil dihapus.
4. **Pembatalan**: Jika pengguna mengurungkan niat (`n` atau input lain), program menghentikan proses reset dan menampilkan pesan pembatalan.
