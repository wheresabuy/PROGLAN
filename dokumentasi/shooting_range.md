# Penjelasan Source Code: `shooting_range.py`

## Deskripsi & Tujuan File
File `shooting_range.py` berisi implementasi minigame tembak-menembak orang pertama (*first-person tactical shooting range*). Dalam permainan ini, pemain mengendalikan bidikan (*crosshair*) menggunakan mouse untuk mengeliminasi zombie yang muncul secara dinamis di layar. Minigame ini memiliki berbagai fitur canggih seperti:
- **Tampilan Senjata FPS**: Menggambar ilustrasi senjata di bagian kanan bawah layar yang bergoyang (*sway*) mengikuti gerakan mouse dan memiliki efek sentakan (*recoil*) saat menembak.
- **Tembakan Kepala (Headshot)**: Area kepala zombie dideteksi secara khusus untuk memberikan kerusakan ganda (*critical*) serta bonus poin dan waktu ekstra.
- **Bantuan Bidik (Aim-Assist / Auto-Lock)**: Bidikan secara otomatis mengunci (*snap*) ke arah kepala zombie terdekat jika jaraknya memenuhi batas minimum.
- **Partikel & Teks Melayang**: Efek visual percikan darah/debu dan teks nilai kerusakan serta bonus yang melayang setelah menembak.
- **Skor & Pengali (Multiplier)**: Sistem poin yang meningkat menggunakan pengali dinamis seiring jumlah eliminasi zombie bertambah.

---

## Daftar Import
| Pustaka / Modul | Deskripsi |
| :--- | :--- |
| `import pygame` | Pustaka game utama untuk menangani grafik, input mouse/keyboard, warna, dan rendering. |
| `import math` | Modul matematika bawaan untuk menghitung jarak geometris (`math.hypot`). |
| `import random` | Modul acak bawaan untuk spawn koordinat zombie, kecepatan acak partikel, dan getaran layar. |
| `import time` | Modul bawaan untuk pencatatan atau manipulasi waktu. |
| `from typing import List, Dict, Tuple, Optional` | Anotasi tipe data (*type hints*) untuk keterbacaan kode yang lebih baik. |
| `from src.core.minigame_manager import MiniGame` | Kelas induk (*parent class*) dari sistem manajemen minigame. |
| `from src.core.spritesheet import Spritesheet` | Kelas utilitas buatan untuk memotong dan mengelola animasi zombie dari lembaran gambar (*spritesheet*). |

---

## Penjelasan Baris Demi Baris
Berikut penjelasan detail mengenai setiap bagian baris kode pada file `shooting_range.py`:

| Baris | Potongan Kode | Penjelasan |
| :--- | :--- | :--- |
| **1-7** | `import pygame`, `import math`, dll. | Mengimpor pustaka eksternal (Pygame) dan internal Python yang dibutuhkan oleh game. |
| **13-18** | `class PixelPalette:` ... | Menyediakan konstanta palet warna RGB seperti emas (GOLD), kilau sian (CYAN_GLOW), api (FIRE_GLOW), dan merah darah (BLOOD). |
| **20-27** | `class Particle:` ... `__init__` | Inisialisasi partikel untuk efek visual. Menyimpan posisi, arah kecepatan acak (`vel`), warna, ukuran acak, dan nilai hidup (`life = 1.0`). |
| **28-32** | `def update(self):` ... | Memperbarui posisi partikel berdasarkan kecepatannya dan mengurangi nilai hidup sebesar 0.02 per frame. Mengembalikan `True` jika partikel masih hidup. |
| **34-36** | `def draw(self, screen, offset=(0,0)):` ... | Menggambar partikel berbentuk lingkaran. Ukurannya menyusut seiring berkurangnya `life`. Ditambahkan koordinat `offset` untuk efek getaran layar. |
| **37-38** | `class WeaponType:` ... | Mendefinisikan tipe senjata default (`RIFLE` / M4-A1 TACTICAL) lengkap dengan spesifikasi damage (40), kapasitas peluru (30), recoil (15), dan jeda tembak (5). |
| **40-48** | `class TacticalWeapon:` ... `__init__` | Inisialisasi sistem senjata taktis. Menyimpan sisa peluru, status isi ulang (*reloading*), timer isi ulang, dan jeda antar tembakan. |
| **49-56** | `def update(self):` ... | Memperbarui timer jeda tembakan dan isi ulang. Jika timer isi ulang selesai, peluru diisi penuh kembali dan status isi ulang dimatikan. |
| **57-58** | `def can_shoot(self):` | Memeriksa apakah senjata siap ditembakkan (peluru masih ada, tidak sedang isi ulang, dan jeda tembak sudah habis). |
| **60-63** | `def shoot(self):` | Mengurangi jumlah peluru sebanyak 1 dan mengatur ulang jeda tembakan berdasarkan tipe senjata. |
| **64-68** | `def reload(self):` | Memulai proses isi ulang peluru jika peluru belum penuh dan senjata tidak sedang dalam proses pengisian ulang. Mengatur timer isi ulang selama 60 frame. |
| **73-75** | `class ShootingRangeUltimate(MiniGame):` ... | Mendefinisikan kelas utama minigame yang diwarisi dari `MiniGame`. |
| **76-82** | `self.width, self.height = 1280, 720` ... | Mengatur ukuran layar internal, koordinat awal bidikan di tengah, skor awal (0), sisa waktu permainan (90.0 detik), statistik kill, headshot, dan uang perolehan. |
| **84-91** | `try: self.bg_img = ... except:` | Mencoba memuat gambar latar kota (`city_bg.png`) dan menyesuaikan ukurannya ke 1280x720. Jika gagal, digantikan dengan warna latar biru gelap polos. |
| **92-98** | `try: self.weapon_img = ... except:` | Mencoba memuat gambar pistol FPS (`fps_pistol_tactical.png`) berukuran 500x500 piksel dengan transparansi alpha. |
| **100-106** | `try: self.zombie_sheet = ... except:` | Mencoba memuat lembar sprite zombie (`zombie_new.png`) untuk dianimasikan dengan skala pembesaran 2.5 kali. |
| **107-112** | `self.weapon = ... self.targets = []` ... | Menginisialisasi objek senjata, daftar kosong untuk target, partikel, teks melayang, serta timer efek kilatan tembakan (*flash*) dan getaran layar (*shake*). |
| **113-116** | `self.font_header = ...` | Memuat jenis font teks monospace dengan berbagai ukuran untuk tampilan antarmuka (HUD). |
| **117-120** | `def handle_event(self, event):` ... | Fungsi menangani kejadian (*event*). Jika mouse digerakkan, koordinat bidikan (`crosshair`) diperbarui. |
| **121-126** | `if event.type == pygame.MOUSEBUTTONDOWN ...` | Menangani klik kiri mouse untuk menembak. Senjata menembak, memicu efek kilatan layar selama 5 frame, dan mengatur intensitas getaran layar sesuai recoil senjata. |
| **127-133** | `for t in self.targets:` ... | Melakukan iterasi ke seluruh zombie aktif untuk mendeteksi apakah peluru mengenai target. Menghitung posisi dan jari-jari kepala zombie. |
| **134-136** | `dist_head = math.hypot(...)` ... | Menghitung jarak bidikan mouse ke pusat kepala zombie (`dist_head`) dan pusat tubuh zombie (`dist_body`). |
| **137-143** | `if dist_head < head_radius or dist_body < t['size']:` ... | Memeriksa apakah tembakan mengenai kepala atau badan. Jika mengenai kepala (*headshot*), damage dikalikan 2, memunculkan teks emas "CRITICAL!" melayang, dan menaburkan partikel merah api. |
| **144-150** | `else:` ... | Jika tembakan mengenai badan, memunculkan teks kerusakan melayang berwarna abu-abu dan menaburkan partikel darah di posisi tubuh. |
| **151-152** | `t['hp'] -= damage` ... | Mengurangi HP zombie berdasarkan damage. Jika HP habis (<= 0), jumlah eliminasi (`kills`) bertambah. |
| **153-166** | `if self.kills < 10: multiplier = 1.0` ... | Menentukan nilai pengali (*multiplier*) poin berdasarkan jumlah total zombie yang telah dieliminasi (berkisar antara 1.0x hingga 5.0x). |
| **167-178** | `if is_headshot:` ... | Jika musuh mati akibat headshot: jumlah headshot bertambah, skor bertambah 150, uang perunggu bertambah (15 dikali pengali), waktu bertambah 4 detik (maksimal 180 detik), dan menampilkan teks info bonus. |
| **179-190** | `else:` ... | Jika musuh mati biasa: skor bertambah 100, uang perunggu bertambah (10 dikali pengali), waktu bertambah 2.5 detik, dan menampilkan teks info bonus. |
| **191-193** | `t['active'] = False` ... | Menonaktifkan target zombie yang telah mati, menandai tembakan berhasil (`hit = True`), dan keluar dari perulangan agar satu peluru tidak mengenai banyak zombie sekaligus. |
| **194-198** | `if not hit:` ... | Jika tembakan meleset (tidak mengenai zombie mana pun), munculkan partikel debu abu-abu di lokasi bidikan mouse untuk menandai peluru membentur tembok latar. |
| **199-200** | `if event.type == pygame.KEYDOWN ...` | Menangani tombol keyboard. Jika tombol 'R' ditekan, senjata akan memicu proses isi ulang (*reload*). |
| **202-206** | `def update(self, dt):` ... | Mengurangi waktu tersisa sesuai waktu per frame (`dt`). Jika waktu habis (<= 0), permainan berakhir dengan mengembalikan skor dan perolehan uang perunggu ke manajer minigame. |
| **207-210** | `self.weapon.update()` ... | Memperbarui status senjata, mengurangi timer kilatan, dan meredam getaran layar secara eksponensial (`shake_v *= 0.85`). |
| **211-213** | `max_targets = 8 + ...` | Menghitung jumlah maksimal target zombie yang bisa aktif secara bersamaan dan persentase peluang munculnya zombie baru (*spawn chance*) yang meningkat seiring meningkatnya jumlah eliminasi. |
| **214-223** | `if len(self.targets) < max_targets ...` | Menentukan posisi awal zombie secara acak. Tipe gerakan zombie ditentukan berdasarkan baris animasi yang terpilih secara acak. Zombie tipe jalan horizontal (baris 6 & 7) di-spawn dari tepi layar. |
| **224-233** | `self.targets.append({ ... })` | Memasukkan data zombie baru ke dalam daftar target, termasuk status HP (100), sisa waktu hidup target, serta variabel penanganan indeks frame animasi. |
| **234-238** | `speed_mult = 1.0 + (self.kills / 25.0)` | Menghitung pengali kecepatan gerakan zombie. Semakin banyak zombie yang dieliminasi, gerakan zombie berikutnya akan semakin cepat. |
| **239-245** | `for t in self.targets:` ... | Memperbarui sisa waktu hidup zombie dan memperbarui bingkai gambar animasi setiap 8 frame agar sprite terlihat berjalan. |
| **246-253** | `if t['anim_row'] == 4:` ... | Menggerakkan zombie: berjalan ke bawah jika baris 4, ke kanan jika baris 6, dan ke kiri jika baris 7, disesuaikan dengan pengali kecepatan. |
| **254-258** | `if t['anim_row'] == 6 and ...` | Mengubah arah gerak horizontal zombie (membalikkan arah jalan) ketika menyentuh batas tepi kiri atau kanan layar. |
| **259-261** | `self.targets = ...` | Memfilter daftar zombie dan partikel untuk mempertahankan objek yang masih aktif/hidup saja di memori. |
| **262-266** | `for ft in self.floating_texts:` ... | Menggerakkan teks melayang ke atas secara perlahan dan menyusutkan sisa durasinya. Teks yang kedaluwarsa dibuang dari daftar. |
| **267-278** | `closest_target = None` ... | Sistem bantuan bidik (*aim-assist*). Mencari kepala zombie terdekat yang berada dalam radius 90 piksel dari bidikan mouse pemain. |
| **279-283** | `if closest_target:` ... | Jika kepala zombie terdekat ditemukan, posisi bidikan mouse digeser perlahan (*linear interpolation* dengan kecepatan 0.55) menuju titik kepala tersebut agar pemain lebih mudah melakukan headshot. |
| **284-290** | `def _draw_pistol_fps(self, screen, offset):` ... | Fungsi menggambar senjata di kanan bawah. Menghitung efek goyangan senjata (*sway*) yang sedikit tertinggal dari pergerakan bidikan mouse. |
| **291-294** | `base_x = self.width * 0.7 + ...` | Menentukan koordinat dasar senjata di sisi kanan bawah layar dengan menerapkan efek goyangan, guncangan getar (*shake offset*), dan sentakan hentakan peluru (`self.shake_v * 2`). |
| **295-298** | `if self.weapon_img:` ... | Jika gambar senjata berhasil dimuat, gambar tersebut digambar langsung ke layar dengan penyesuaian posisi agar presisi. |
| **299-305** | `else:` ... | Blok cadangan jika gambar gagal dimuat. Menggambar bentuk kepalan tangan berkulit menggunakan elips Pygame. |
| **306-319** | `gun_dark = ...` | Blok cadangan untuk menggambar badan pistol, pegangan (*grip*), serta detail gesekan logam (*slide*) menggunakan bentuk persegi panjang dan garis. |
| **320-330** | `sight_x = base_x - 100` ... | Blok cadangan untuk menggambar alat bidik titik merah (*reflex red dot sight*) dengan warna titik merah yang berkedip secara periodik. |
| **331-334** | `pygame.draw.circle(...)` | Blok cadangan untuk menggambar lubang ujung laras senjata hitam. |
| **335-337** | `def draw(self):` ... | Fungsi utama menggambar seluruh visual minigame. Menghitung offset getaran layar acak berdasarkan intensitas `shake_v`. |
| **338-341** | `self.screen.blit(self.bg_img, offset)` | Menggambar gambar latar belakang kota yang sedikit bergeser mengikuti getaran layar. |
| **342-345** | `for t in self.targets:` ... | Melakukan perulangan untuk menggambar setiap zombie yang aktif di layar lengkap dengan offset getarannya. |
| **346-357** | `if self.zombie_sheet:` ... | Jika spritesheet zombie aktif: menggambar lingkaran indikator merah tipis di kaki zombie terlebih dahulu, lalu menggambar sprite zombie beranimasi di tengah-tengah posisinya. |
| **358-366** | `hp_pct = max(0, t['hp']) / 100.0` ... | Menggambar bilah nyawa (*HP bar*) berwarna merah gelap (dasar) dan hijau (nyawa tersisa) di atas kepala zombie. |
| **367-371** | `else:` | Blok cadangan jika spritesheet gagal dimuat: menggambar zombie sebagai lingkaran hijau dengan inti merah. |
| **372-374** | `for p in self.particles: p.draw(...)` | Menggambar seluruh partikel visual aktif di layar. |
| **375-380** | `for ft in self.floating_texts:` ... | Menggambar teks melayang. Menggambar bayangan hitam terlebih dahulu sedikit melenceng ke kanan bawah, lalu menggambar teks berwarna utama di atasnya agar lebih kontras. |
| **381-386** | `if self.flash_timer > 0:` ... | Jika senjata baru saja ditembakkan, gambar bidang kuning-putih transparan di seluruh layar dengan efek blending `BLEND_ADD` untuk mensimulasikan cahaya silau tembakan. |
| **387-394** | `pygame.draw.circle(...)` | Menggambar bola cahaya kuning acak besar di ujung laras pistol sebagai efek semburan api (*muzzle flash*). |
| **395-398** | `self._draw_pistol_fps(...)` | Memanggil fungsi untuk menggambar senjata taktis FPS pemain. |
| **399-402** | `pygame.draw.rect(...)` ... | Menggambar panel hitam transparan di bagian atas layar sebagai latar belakang antarmuka (HUD) utama dengan garis pembatas merah. |
| **403-413** | `if self.kills < 10: ...` | Menghitung kembali nilai pengali skor saat ini untuk ditampilkan secara dinamis di teks HUD. |
| **414-416** | `self.screen.blit(...)` | Menampilkan teks judul misi besar "CITY UNDER ATTACK" berwarna merah menyala di sisi kiri HUD. |
| **417-420** | `stat_lbl = ...` | Menampilkan jumlah eliminasi musuh, jumlah tembakan kepala (headshot), dan tingkat pengali skor saat ini di sisi kiri bawah judul HUD. |
| **421-424** | `self.screen.blit(...)` | Menampilkan total skor (diformat 8 digit angka dengan nol di depan) dan total koin perunggu yang diraih di sisi kanan atas layar HUD. |
| **425-427** | `self.screen.blit(...)` | Menampilkan indikator sisa peluru senjata (misal: "AMMO: 30/30") tepat di bawah garis batas HUD. |
| **428-432** | `mins, secs = ...` | Memisahkan waktu permainan menjadi menit dan detik. Jika waktu tersisa kurang dari atau sama dengan 20 detik, warna teks berganti menjadi merah sebagai peringatan kritis. |
| **433-444** | `is_locked = False` ... | Memeriksa kembali apakah bidikan pemain terkunci pada kepala zombie (jarak sangat dekat, yaitu di bawah 12 piksel setelah bidikan otomatis menempel). |
| **445-450** | `ch_color = ...` | Menentukan warna bidikan: merah jika terkunci (*lock-on*) pada kepala zombie, hijau jika bidikan bebas biasa. Menggambar lingkaran bidik dan garis salib di sekitar mouse. |
| **451-455** | `if is_locked and locked_pos:` ... | Menggambar braket persegi merah di sekeliling kepala zombie yang sedang terkunci untuk memandu pemain melepaskan tembakan headshot. |

---

## Alur Kerja Utama
1. **Inisialisasi (`__init__`)**:
   - Memuat latar belakang, sprite zombie, serta gambar senjata taktis FPS.
   - Mengatur variabel game: sisa waktu awal (90 detik), skor (0), perolehan koin, dan membuat objek senjata (`TacticalWeapon`).
2. **Penerimaan Input (`handle_event`)**:
   - Pemain mengarahkan mouse untuk memindahkan bidikan.
   - Pemain melakukan klik kiri untuk menembak, yang mengonsumsi peluru, memicu hentakan getar layar, dan mendeteksi tabrakan peluru dengan zombie.
   - Deteksi memisahkan area lingkaran kepala (bonus damage/poin/waktu) dan area lingkaran badan.
   - Menekan tombol 'R' memicu pemulihan kapasitas peluru.
3. **Pemainan Logika (`update`)**:
   - Waktu terus berjalan mundur. Jika habis, game ditutup dan datanya dikembalikan ke kelas manajer.
   - Zombie bermunculan secara bertahap. Seiring dengan naiknya tingkat eliminasi, batas maksimal zombie meningkat, kecepatan berjalan zombie bertambah, dan peluang kemunculan zombie baru juga meningkat.
   - Sistem *aim-assist* bekerja aktif di setiap frame untuk menarik bidikan ke arah titik terdekat kepala zombie.
   - Menggerakkan posisi partikel visual dan teks melayang, serta meredakan efek guncangan layar.
4. **Penggambaran Visual (`draw`)**:
   - Menggambar latar belakang berguncang, zombie beserta bilah nyawa di atas kepala mereka, partikel darah, serta teks melayang.
   - Menggambar kilasan cahaya di layar dan di moncong pistol saat terjadi tembakan.
   - Menggambar senjata taktis FPS dengan efek goyangan alami mengikuti mouse.
   - Menggambar panel HUD lengkap dengan info amunisi, skor, koin, pengali aktif, sisa waktu, serta indikator bidikan target terdeteksi.
