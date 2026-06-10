# Penjelasan Kode: `main.py`

Dokumen ini berisi penjelasan detail baris demi baris untuk file `/home/abuyyy/PemogramanLanjut/main.py`. Penjelasan ini ditulis dalam bahasa Indonesia untuk membantu persiapan demo program.

---

## Deskripsi & Tujuan File
File `main.py` adalah pintu masuk utama (*entry point*) peluncuran game. File ini bertanggung jawab untuk:
1. **Inisialisasi Game**: Membuka jendela layar Pygame, memuat font, mengeset setelan dasar, dan memuat aset kustomisasi pakaian pemain (wardrobe) serta data stasiun peningkatan senjata (upgrade shop).
2. **Koordinasi Thread Kamera**: Meluncurkan thread kamera visi komputer (`GestureThread`) secara paralel agar tidak menghambat game loop utama.
3. **Menu Kustomisasi Wardrobe & Upgrade Shop**: Menangani navigasi antarmuka visual overlay menu kustomisasi sprite pemain dan toko statistik senjata (damage, amunisi, reload, firerate).
4. **Logika Input Proxy & Gestur**: Mengubah gestur navigasi tangan (`ATAS`, `BAWAH`, `KIRI`, `KANAN`, `AMBIL`) menjadi masukan keyboard simulasi (`InputProxy`), serta menskalakan koordinat tangan webcam menjadi koordinat crosshair di layar game dengan interpolasi linear (lerp) agar halus.
5. **Game Loop**: Menangani polling event, pembaruan frame, sinkronisasi status thread kamera, dan render berlapis.

---

## Penjelasan Baris Demi Baris

Berikut adalah tabel penjelasan baris demi baris dari kode sumber `main.py`:

| Baris | Kode Sumber | Penjelasan |
| :---: | :--- | :--- |
| **1** | `import pygame` | Mengimpor pustaka Pygame untuk rendering grafis, event, font, dan mixer audio. |
| **2** | `import sys` | Mengimpor modul `sys` untuk penutupan bersih aplikasi dan python. |
| **3** | `from src.entities.entities import Player` | Mengimpor kelas `Player` dari modul entitas. |
| **4** | `from src.ui.dialogue import DialogueBox` | Mengimpor kelas `DialogueBox` untuk memproses kotak teks dialog percakapan. |
| **5** | `from src.ui.hud import HUD` | Mengimpor kelas `HUD` untuk status bar nyawa, baterai, dan koin. |
| **6** | `from src.core.engine import CurrencyManager, Camera, VisualEffects, MiniGameManager` | Mengimpor manajer mata uang, kamera gulir, efek visual gelap/shake, dan manager daur hidup minigame dari core engine. |
| **7** | `from src.core.sanctuary_logic import SanctuaryLogic` | Mengimpor logika dunia aman Sanctuary. |
| **8** | `from comvis.gestures import GestureThread` | Mengimpor thread webcam visi komputer untuk pelacakan gestur tangan. |
| **9** | `class InputProxy:` | Deklarasi kelas `InputProxy` untuk memodifikasi masukan status tombol keyboard game. |
| **10** | `    def __init__(self, keys_pressed):` | Konstruktor kelas input proxy yang menerima daftar status tombol keyboard fisik saat ini. |
| **11** | `        self.keys = keys_pressed` | Menyimpan status tombol keyboard fisik. |
| **12** | `        self.overrides = {}` | Inisialisasi kamus kosong untuk menampung tombol keyboard buatan (overrides) dari gestur tangan. |
| **13** | `    def __getitem__(self, key):` | Metode pemetaan item (`__getitem__`) agar objek input proxy dapat diakses menggunakan indeks bracket `proxy[key]`. |
| **14** | `        return self.overrides.get(key, self.keys[key])` | Mengembalikan status buatan dari gestur jika terdaftar, jika tidak kembalikan status keyboard fisik. |
| **15** | `def main():` | Deklarasi fungsi utama pengeksekusi program game. |
| **16** | `    pygame.init()` | Menginisialisasi seluruh subsistem Pygame. |
| **17** | `    WIDTH, HEIGHT = 1280, 720` | Menetapkan resolusi layar game: lebar 1280px dan tinggi 720px (720p). |
| **18** | `    screen = pygame.display.set_mode((WIDTH, HEIGHT))` | Membuat jendela tampilan layar Pygame. |
| **19** | `    pygame.display.set_caption("City Under Attack - Sanctuary Defense")` | Mengeset judul jendela permainan di layar desktop. |
| **20** | `    clock = pygame.time.Clock()` | Membuat objek pewaktu Clock untuk membatasi framerate game. |
| **21** | `    font = pygame.font.SysFont("monospace", 14)` | Inisialisasi font default monospace berukuran 14px untuk UI bawah dan status. |
| **22** | `    weapon_upgrades = {"damage_level": 0, "ammo_level": 0, "reload_level": 0, "firerate_level": 0}` | Kamus level peningkatan statistik senjata awal (seluruh level mulai dari 0 s.d 3). |
| **23** | `    selected_weapon = "SCAR"` | Senjata default yang terpilih di dunia eksplorasi: "SCAR". |
| **24** | `    player = Player(500, 450)` | Membuat instansiasi karakter pemain diposisikan awal di (500, 450). |
| **25** | `    camera = Camera(WIDTH, HEIGHT, 2560, 1440)` | Membuat kamera dengan ukuran layar 1280x720 untuk peta berdimensi 2560x1440. |
| **26** | `    dialogue = DialogueBox()` | Membuat kotak dialog percakapan. |
| **27** | `    currency = CurrencyManager()` | Membuat manajer keuangan pemain. |
| **28** | `    hud = HUD(currency)` | Membuat antarmuka status HUD yang terhubung dengan data mata uang koin. |
| **29** | `    effects = VisualEffects(WIDTH, HEIGHT)` | Membuat pengelola visual efek getaran dan gelap malam. |
| **30** | `    game_logic = SanctuaryLogic(dialogue)` | Membuat instansiasi logika Sanctuary dengan menyertakan dialogue box. |
| **31** | `    dialogue.box_rect = pygame.Rect(100, 500, 1080, 150)` | Mengubah ukuran kotak dialog agar lebih lebar dan berada di bagian tengah bawah layar game. |
| **32** | `    gesture_thread = GestureThread(0)` | Membuat thread kamera webcam terpisah menggunakan webcam berindeks 0. |
| **33** | `    gesture_thread.start()` | Menjalankan thread kamera pelacak gestur di latar belakang secara paralel. |
| **34** | `    class EngineProxy:` | Deklarasi kelas perantara `EngineProxy` untuk meneruskan status game ke minigame manager. |
| **35** | `        def __init__(self, s, c, cur, upg, gt, sw):` | Konstruktor kelas proxy menerima screen, clock, currency, upgrades, thread, dan senjata terpilih. |
| **36** | `            self.screen = s` | Menyimpan referensi screen utama. |
| **37** | `            self.clock = c` | Menyimpan referensi clock utama. |
| **38** | `            self.currency = cur` | Menyimpan referensi currency manager. |
| **39** | `            self.weapon_upgrades = upg` | Menyimpan kamus upgrade senjata. |
| **40** | `            self.gesture_thread = gt` | Menyimpan referensi thread gestur. |
| **41** | `            self.selected_weapon = sw` | Menyimpan nama senjata aktif. |
| **42** | `    engine_proxy = EngineProxy(screen, clock, currency, weapon_upgrades, gesture_thread, "SCAR")` | Instansiasi objek proxy engine dengan data awal. |
| **43** | `    minigame_manager = MiniGameManager(engine_proxy)` | Membuat pengelola minigame yang terhubung dengan proxy. |
| **44** | `    smoothed_hx = WIDTH // 2` | Inisialisasi koordinat horizontal bidikan halus di tengah layar. |
| **45** | `    smoothed_hy = HEIGHT // 2` | Inisialisasi koordinat vertikal bidikan halus di tengah layar. |
| **46-50** | `SKIN_OPTIONS = [...]`, `SKIN_NAMES = [...]` | Membuat daftar pilihan 11 path spritesheet warna kulit pemain dan penamaannya. |
| **51-65** | `OUTFIT_OPTIONS = [...]` | Membuat daftar pilihan 13 baju dan celana pemain (dari pakaian forester hingga celana petani). |
| **66-80** | `OUTFIT_NAMES = [...]` | Nama tampilan untuk pilihan pakaian pemain di UI menu wardrobe. |
| **81-88** | `HAIR_OPTIONS = [...]`, `HAIR_NAMES = [...]` | Loop otomatis untuk memuat 28 pilihan file spritesheet gaya rambut pemain (Bob cut & Dapper). |
| **89-96** | `HAT_OPTIONS = [...]`, `HAT_NAMES = [...]` | Loop otomatis memuat 10 pilihan file spritesheet topi pemain (topi jerami petani & topi sihir pointy). |
| **97** | `    wardrobe_active = False` | Status keaktifan menu wardrobe kustomisasi pakaian pemain (default False). |
| **98** | `    wardrobe_category = 0` | Indeks kategori menu wardrobe yang sedang disorot (0: Kulit, 1: Pakaian, 2: Rambut, 3: Topi). |
| **99** | `    wardrobe_indices = [0, 3, 23, 0]` | Indeks item aktif yang dipilih pemain untuk masing-masing kategori kustomisasi. |
| **100** | `    upgrade_shop_active = False` | Status keaktifan menu Upgrade Senjata (default False). |
| **101** | `    upgrade_shop_category = 0` | Indeks kategori stasiun upgrade yang disorot (0: Damage, 1: Ammo, 2: Reload, 3: Firerate). |
| **102** | `    UPGRADE_COSTS = [100, 250, 500]` | Tarif biaya peningkatan: Lv 1 ke 2 butuh 100 Bronze, Lv 2 ke 3 butuh 250 Bronze, Lv 3 ke Max butuh 500 Bronze. |
| **103** | *(Komentar)* | Penjelas. |
| **104** | `    def update_player_wardrobe():` | Fungsi lokal untuk memuat ulang lembar sprite visual pemain berdasarkan wardrobe_indices. |
| **105** | `        from src.core.engine import Spritesheet` | Mengimpor kelas Spritesheet secara lokal. |
| **106** | `        player.sheet = Spritesheet(SKIN_OPTIONS[wardrobe_indices[0]], 8, 8, scale=2.0)` | Memuat ulang warna kulit tubuh dasar pemain. |
| **107** | `        outfit_path = OUTFIT_OPTIONS[wardrobe_indices[1]]` | Mendapatkan path file baju terpilih. |
| **108-113** | `        if outfit_path: ... else: ...` | Memuat baju baru jika terpilih, atau mengosongkannya jika memilih bare/tanpa baju. |
| **114-118** | `        hair_path = HAIR_OPTIONS[wardrobe_indices[2]] ...` | Memuat gaya rambut baru atau mengeset botak gundul jika None. |
| **119-123** | `        hat_path = HAT_OPTIONS[wardrobe_indices[3]] ...` | Memuat gaya topi baru atau melepas topi jika None. |
| **124** | `    update_player_wardrobe()` | Memanggil fungsi kustomisasi awal untuk memuat visual default pemain saat masuk. |
| **125** | `    while True:` | **Loop Utama Game (Game Loop)**. |
| **126** | `        dt = clock.tick(60) / 16.67` | Membatasi framerate ke 60 FPS dan menghitung delta waktu pendorong fisika gerakan. |
| **127** | `        events = pygame.event.get()` | Mengambil seluruh kejadian/event antrean input di sistem. |
| **128** | `        gesture_thread.in_minigame = minigame_manager.in_minigame` | Menyelaraskan status minigame ke thread kamera agar filter algoritma deteksi gestur tangan otomatis berubah. |
| **129** | `        current_g = gesture_thread.current_gesture` | Membaca gestur tangan terpopuler dari kamera saat ini. |
| **130** | `        h_pos = gesture_thread.hand_pos` | Membaca koordinat filtered ujung jari telunjuk dari thread. |
| **131** | `        if wardrobe_active:` | **BLOK KONTROL MENU WARDROBE AKTIF**. |
| **132-136** | `            for event in events: if event.type == pygame.QUIT: ...` | Menangani penutupan program game secara bersih (menghentikan thread kamera terlebih dahulu). |
| **137-141** | `                if event.type == pygame.KEYDOWN: if event.key == pygame.K_UP: ...` | Menavigasi pilihan kategori kustomisasi ke atas atau ke bawah. |
| **142-150** | `                    elif event.key == pygame.K_LEFT: ...` | Menekan tombol arah kiri memotong indeks pilihan pakaian (mundur ke opsi sebelumnya) dan memperbarui pakaian pemain. |
| **151-161** | `                    elif event.key == pygame.K_RIGHT: ...` | Menekan tombol arah kanan menambah indeks pilihan pakaian (maju ke opsi baru). |
| **162-163** | `                    elif event.key == pygame.K_RETURN: wardrobe_active = False` | Menekan Enter menutup menu kustomisasi dan kembali ke Sanctuary. |
| **164-169** | `            game_logic.draw_ground(screen, camera) ...` | Merender dunia Sanctuary di balik layar menu kustomisasi wardrobe. |
| **170-176** | `            overlay_w, overlay_h = 720, 440 ...` | Menggambar latar belakang transparan menu kustomisasi wardrobe di tengah layar. |
| **177-183** | `            font_title = pygame.font.SysFont("Arial", 22, bold=True) ...` | Merender judul menu kustomisasi wardrobe dan garis pembatas atas. |
| **184-188** | `            pygame.draw.rect(screen, (20, 30, 40, 255), (ox + 30, oy + 65, 180, 290) ...` | Menggambar panel bingkai preview visual karakter sebelah kiri. |
| **189-202** | `            preview_timer = getattr(player, 'preview_timer', 0) + 1 ...` | Menghitung frame langkah kaki karakter preview dan menggambar sprite berskala besar (160x160px) pemain yang sedang berjalan di panel preview. |
| **203-234** | `            categories = [...]` | Merender daftar 4 kategori pakaian dengan sorotan warna cyan cerah pada opsi yang sedang aktif dipilih. |
| **235-238** | `            help_text = ...` | Menggambar petunjuk navigasi tombol keyboard di bagian bawah panel wardrobe. |
| **239-240** | `            pygame.display.flip(); continue` | Menyegarkan frame layar menu kustomisasi dan lewati game loop utama. |
| **241** | `        if upgrade_shop_active:` | **BLOK KONTROL MENU UPGRADE SENJATA AKTIF**. |
| **242-246** | `            for event in events: if event.type == pygame.QUIT: ...` | Penutupan aman program. |
| **247-251** | `                if event.type == pygame.KEYDOWN: if event.key == pygame.K_UP: ...` | Menavigasi sorotan kategori upgrade senjata ke atas/bawah. |
| **252-259** | `                    elif event.key == pygame.K_RETURN: ...` | Membeli upgrade level senjata jika level saat ini < 3 dan saldo Bronze mencukupi. Saldo akan dikurangi dan memicu visual flash monitor. |
| **260-261** | `                    elif event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_q]:` | Menutup menu stasiun upgrade jika menekan ESC, Backspace, atau Q. |
| **262-267** | `            game_logic.draw_ground(screen, ...)` | Merender dunia Sanctuary di latar belakang menu upgrade. |
| **268-274** | `            overlay_w, overlay_h = 750, 450 ...` | Menggambar panel luar transparan menu stasiun upgrade senjata berwarna ungu kemerahan. |
| **275-285** | `            title_surf = ...` | Merender judul toko upgrade dan total saldo koin pemain di pojok kanan atas. |
| **286-295** | `            pygame.draw.rect(screen, (30, 20, 40) ...` | Menggambar bingkai preview senjata di sebelah kiri menu. |
| **296-305** | `            stat_y = oy + 280 ...` | Merender statistik persenan angka aktual senjata (Damage, Mag, Reload speed, Firerate) di bawah gambar preview. |
| **306-311** | `            categories_info = [...]` | Mendefinisikan rincian data upgrade (nama, key, kalkulator perbandingan nilai, keterangan bonus upgrade). |
| **312-328** | `            for idx, (cat_name, cat_key, val_func, bonus_desc) in enumerate(categories_info):` | Merender baris pilihan upgrade. Pilihan aktif ditandai warna merah muda cerah berpendar. |
| **329-331** | `                title_txt = f"{cat_name}  [Lv {lvl}/3]" ...` | Menampilkan nama statistik upgrade beserta level upgrade saat ini. |
| **332-341** | `                if lvl < 3: ...` | Menampilkan biaya harga upgrade. Warna teks harga akan berwarna hijau jika saldo cukup, dan berwarna merah jika uang kurang. |
| **342-345** | `                else: ...` | Menampilkan label hijau "SELESAI UPGRADE (MAX)" jika level statistik sudah berada di level 3. |
| **346-351** | `            help_text = ... ; pygame.display.flip(); continue` | Menampilkan petunjuk tombol navigasi upgrade, segarkan layar monitor, dan lompat ke frame berikutnya. |
| **352** | `        interact_pressed = False` | Mereset status pemicu interaksi Enter ke `False` pada loop utama. |
| **353** | `        if minigame_manager.in_minigame:` | **LOGIKA JIKA SEDANG DI DALAM MINIGAME (CITY UNDER ATTACK)**. |
| **354-358** | `            for event in events: if event.type == pygame.QUIT: ...` | Penutupan aman program. |
| **359-360** | `                elif event.type == pygame.MOUSEMOTION: smoothed_hx, smoothed_hy = event.pos` | Membaca kursor mouse fisik pemain jika bermain menggunakan mouse. |
| **361** | `                if minigame_manager.active_game:` | Memeriksa ketersediaan objek game sebelum meneruskan event keyboard/mouse fisik ke sistem event minigame. |
| **362** | `            if minigame_manager.active_game is None: continue` | **Penanganan Crash Keluar Awal**: Jika pemain menekan ESC/Q untuk keluar lebih awal, loop frame akan dilewati agar tidak terjadi crash AttributeError. |
| **363-364** | `            if current_g != "None": target_hx = int(h_pos[0] * WIDTH) ...` | Menghitung koordinat piksel bidikan target dari rasio normalisasi MediaPipe (0.0 s.d 1.0) dikalikan lebar/tinggi layar. |
| **365-367** | `                smoothed_hx = smoothed_hx + (target_hx - smoothed_hx) * 0.40 ...` | **Smooth Lerp Filter**: Meredam gerakan kursor sebesar 40% agar gerakan tangan goyah diredam menjadi halus. |
| **368-369** | `                fake_move = pygame.event.Event(...)` | Membuat event pergerakan kursor buatan dan mengirimkannya ke minigame agar retikel kursor bidikan bergeser. |
| **370-371** | `            if gesture_thread.recoil_active:` | Jika sinyal kejutan tembakan (recoil/sentakan telunjuk) terdeteksi aktif di thread kamera. |
| **372** | `                minigame_manager.active_game.handle_event(...)` | Membuat event klik kiri mouse buatan untuk memicu tembakan peluru senjata di minigame. |
| **373-374** | `            if minigame_manager.active_game:` | Memastikan objek minigame masih aktif sebelum memproses pembaruan logika waktu dan penggambaran grafis. |
| **375-378** | `            cam_surf = gesture_thread.frame ...` | Merender layar monitor feed webcam kecil berukuran 160x120px di pojok kanan atas minigame, beserta garis tepi cyan dan label teks nama gestur terdeteksi (`AIM`, `PISTOL`, atau `FIST`). |
| **379-380** | `            pygame.display.flip(); continue` | Segarkan layar game loop, lewati pemrosesan alur Sanctuary. |
| **381-386** | `        for event in events: if event.type == pygame.QUIT: ...` | **LOGIKA EKSPLORASI SANCTUARY**: Tangani event penutupan game. |
| **387-389** | `            if event.type == pygame.KEYDOWN: if dialogue.active: ... dialogue.next_message()` | Jika dialogue box aktif, menekan tombol `Enter` akan melangkah ke kalimat dialog selanjutnya. |
| **390-392** | `                else: if event.key == pygame.K_RETURN: interact_pressed = True` | Jika dialog tertutup, menekan tombol `Enter` menyalakan status pemicu interaksi aksi (`interact_pressed = True`). |
| **393-397** | `                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:` | Menekan tombol angka `1`-`4` untuk mengganti senjata aktif eksplorasi. Mengharuskan akumulasi `point_kill` >= 10.000 untuk UZI, dan >= 20.000 untuk SCAR. Jika terkunci, tampilkan teks melayang peringatan berwarna merah. |
| **398** | `        keys = InputProxy(pygame.key.get_pressed())` | Mengambil status tombol keyboard dibungkus input proxy. |
| **399-402** | `        if current_g == "ATAS": keys.overrides[pygame.K_UP] = True ...` | **Simulasi Gerak Gestur ML**: Menerjemahkan gestur tangan ML (`ATAS`, `BAWAH`, `KIRI`, `KANAN`) ke tombol navigasi keyboard buatan. |
| **403** | `        elif current_g in ["PISTOL", "AMBIL", "ENTER"]: interact_pressed = True` | Gestur `"AMBIL"` / `"PISTOL"` / `"ENTER"` secara otomatis memicu interaksi aksi eksplorasi. |
| **404-406** | `        if not dialogue.active: player.update(keys, map_size=(2560, 1440)) ...` | Jika tidak sedang membaca dialog: update pergerakan pemain dan arahkan kamera gulir mengikuti pemain. |
| **407** | `            signal = game_logic.update(player, interact_pressed)` | Memproses logika interaksi Sanctuary (api unggun, kasur medis, NPC, helipad, wardrobe, stasiun upgrade). |
| **408-410** | `            if signal == "START_SHOOTING":` | Jika menerima sinyal pertempuran dari Kapten Jaka. |
| **411** | `                minigame_manager.start_minigame(ShootingRangeUltimate)` | Luncurkan minigame **"City Under Attack"** dengan melock senjata yang sedang aktif dipilih saat ini. |
| **412-413** | `            elif signal == "AWARD_150_BRONZE": currency.add_bronze(150)` | Jika menerima sinyal klaim peti suplai helipad, tambahkan 150 koin Bronze. |
| **414-415** | `            elif signal == "OPEN_WARDROBE": wardrobe_active = True` | Buka menu pakaian jika pemain berinteraksi dengan loker. |
| **416-417** | `            elif signal == "OPEN_UPGRADE_SHOP": upgrade_shop_active = True` | Buka menu upgrade senjata jika pemain berinteraksi dengan komputer stasiun upgrade. |
| **418-422** | `        game_logic.draw_ground(screen, camera) ... hud.draw(screen, player, 100)` | Merender peta dasar, entitas Sanctuary (NPC, partikel, peti), sprite pemain, flash efek, dialog, dan HUD koin/nyawa di layar. |
| **423-427** | `        status = game_logic.get_status_text() ...` | Merender panel HUD status bawah berbingkai cyan setinggi 75px, menampilkan teks status objektif, total `point_kill` & status kunci UZI/SCAR, serta senjata siap pakai. |
| **428-432** | `        cam_surf = gesture_thread.frame ...` | Merender monitor kamera feed webcam kecil 160x120px beserta label nama gesturnya di pojok kanan atas layar Sanctuary. |
| **433** | `        pygame.display.flip()` | Menyegarkan buffer grafis layar utama Pygame (*Double Buffering*). |
| **434-436** | `if __name__ == "__main__": main()` | Memeriksa apakah file dijalankan langsung sebagai program utama, lalu mengeksekusi fungsi `main()`. |

---

## Hubungan Antarkomponen Utama
* **Interaksi `GestureThread` & `main.py`**: Thread gestur kamera berjalan mandiri secara asinkron. Di dalam game loop, `main.py` membaca gestur saat ini (`current_g`) untuk menggerakkan pemain (mode Sanctuary) atau membidik retikel kursor (mode Minigame).
* **Interaksi `SanctuaryLogic` & `main.py`**: `main.py` memanggil update status Sanctuary dan menangani perpindahan koordinat pemain atau pemberian hadiah Bronze berdasarkan sinyal feedback yang dikembalikan (`OPEN_WARDROBE`, `AWARD_150_BRONZE`, dll).
* **Interaksi `MiniGameManager` & `main.py`**: Manager memisahkan logika loop Sanctuary dengan Minigame. Ketika minigame aktif, manager langsung membajak proses rendering dan event polling untuk dialihkan ke `ShootingRangeUltimate`. Setelah waktu habis, manager keluar kembali ke loop Sanctuary dan memberikan Bronze hasil eliminasi zombie.
