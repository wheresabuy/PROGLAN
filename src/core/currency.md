# Penjelasan Kode: `currency.py`

Dokumen ini berisi penjelasan detail baris demi baris mengenai file `currency.py` yang digunakan untuk mengelola sistem mata uang dalam game.

---

### Deskripsi & Tujuan File
File `currency.py` mendefinisikan kelas `CurrencyManager` yang digunakan untuk mengelola sistem koin atau mata uang dalam permainan. Sistem mata uang ini menggunakan tiga jenis pecahan:
1. **Bronze (Perunggu)**: Koin bernilai paling rendah.
2. **Silver (Perak)**: Koin tingkat menengah (100 Bronze = 1 Silver).
3. **Gold (Emas)**: Koin tingkat tertinggi (100 Silver = 1 Gold).

Kelas ini mengotomatiskan konversi pecahan koin dari unit yang lebih rendah ke unit yang lebih tinggi setiap kali koin baru ditambahkan.

---

### Daftar Import (jika ada)
Tidak ada library atau modul eksternal yang diimpor pada file ini. Seluruh fungsionalitas menggunakan pustaka standar dan operasi bawaan Python.

---

### Penjelasan Baris Demi Baris

| No. Baris | Kode Sumber | Penjelasan |
| :---: | :--- | :--- |
| **1** | `class CurrencyManager:` | Mendefinisikan kelas `CurrencyManager` yang berfungsi untuk mengatur jumlah dan konversi mata uang. |
| **2** | `    def __init__(self):` | Inisialisasi method (`constructor`) yang akan dijalankan secara otomatis saat objek baru dibuat dari kelas ini. |
| **3** | `        self.bronze = 0` | Mendeklarasikan atribut `bronze` untuk menyimpan jumlah koin perunggu dengan nilai awal `0`. |
| **4** | `        self.silver = 0` | Mendeklarasikan atribut `silver` untuk menyimpan jumlah koin perak dengan nilai awal `0`. |
| **5** | `        self.gold = 0` | Mendeklarasikan atribut `gold` untuk menyimpan jumlah koin emas dengan nilai awal `0`. |
| **6** | *(Baris Kosong)* | Baris kosong untuk pemisah visual antar method agar kode lebih mudah dibaca. |
| **7** | `    def add_bronze(self, amount):` | Mendefinisikan method publik `add_bronze` untuk menambahkan koin perunggu berdasarkan argumen `amount`. |
| **8** | `        self.bronze += amount` | Menambahkan nilai dari parameter `amount` ke atribut `self.bronze` saat ini. |
| **9** | `        self._convert()` | Memanggil method internal `_convert()` untuk memperbarui konversi koin setelah terjadi penambahan koin. |
| **10** | *(Baris Kosong)* | Baris kosong untuk menjaga kerapian struktur kode. |
| **11** | `    def _convert(self):` | Mendefinisikan method internal (ditandai dengan prefix `_`) yang bertugas mengonversi koin ke pecahan di atasnya jika memenuhi jumlah minimal (100). |
| **12** | `        # 100 Bronze = 1 Silver` | Komentar penjelasan aturan konversi pertama: 100 koin perunggu setara dengan 1 koin perak. |
| **13** | `        if self.bronze >= 100:` | Memeriksa apakah jumlah koin perunggu (`bronze`) saat ini bernilai 100 atau lebih. |
| **14** | `            self.silver += self.bronze // 100` | Melakukan pembagian bulat (`//`) jumlah koin perunggu dengan 100, lalu menambahkan hasilnya ke atribut `silver`. |
| **15** | `            self.bronze %= 100` | Menghitung sisa koin perunggu menggunakan operasi modulo (`%`) 100, lalu menyimpannya kembali ke atribut `bronze`. |
| **16** | `        # 100 Silver = 1 Gold` | Komentar penjelasan aturan konversi kedua: 100 koin perak setara dengan 1 koin emas. |
| **17** | `        if self.silver >= 100:` | Memeriksa apakah jumlah koin perak (`silver`) saat ini bernilai 100 atau lebih. |
| **18** | `            self.gold += self.silver // 100` | Melakukan pembagian bulat (`//`) jumlah koin perak dengan 100, lalu menambahkan hasilnya ke atribut `gold`. |
| **19** | `            self.silver %= 100` | Menghitung sisa koin perak menggunakan operasi modulo (`%`) 100, lalu menyimpannya kembali ke atribut `silver`. |
| **20** | *(Baris Kosong)* | Baris kosong di akhir file sesuai standar penulisan kode Python (PEP 8). |

---

### Alur Kerja Utama
1. **Inisialisasi Objek**: `CurrencyManager` dibuat dengan seluruh jenis koin bernilai 0.
2. **Penambahan Bronze**: Pengguna memanggil method `add_bronze(amount)` untuk memasukkan koin perunggu baru ke dalam sistem.
3. **Pemicuan Konversi**: Sistem langsung menjalankan method internal `_convert()`.
4. **Evaluasi Pecahan**:
   - Jika perunggu $\ge 100$, kelipatan seratusnya dialihkan menjadi perak dan sisa satuannya tetap disimpan di perunggu.
   - Jika perak hasil konversi (atau yang sudah ada) $\ge 100$, kelipatan seratusnya dialihkan menjadi emas dan sisa satuannya tetap disimpan di perak.
