# City Under Attack: Sanctuary Defense

Game survival pasca-apokaliptik yang dikembangkan dengan **Pygame** dan **Computer Vision (MediaPipe)** untuk kontrol interaktif.

## Fitur Utama
- **Top-Down Exploration:** Jelajahi "The Sanctuary", benteng terakhir kemanusiaan.
- **Dynamic NPC Interaction:** Berinteraksi dengan warga dan pemimpin kota.
- **Tactical Shooting Mode:** Mode "City Under Attack" di mana pemain harus bertahan dari serangan zombie.
- **Gesture Control (Computer Vision):** Gunakan gerakan tangan untuk menggerakkan karakter dan menembak (PISTOL gesture).

## Struktur Proyek
- `main.py`: Entry point dan main game loop.
- `src/core/`:
  - `sanctuary_logic.py`: Logika dunia, NPC, dan transisi ke pertempuran.
  - `minigame_manager.py`: Mengelola pergantian ke mode shooting.
  - `camera.py` & `visual_effects.py`: Sistem kamera dan efek visual.
- `src/entities/`: Kelas untuk Player dan NPC.
- `src/ui/`: Sistem HUD dan Dialog Box.
- `comvis/`: Sistem pengenalan gestur menggunakan MediaPipe.

## Cara Menjalankan
1. Install dependensi: `pip install -r requirements.txt`
2. Jalankan game: `python main.py`

## Kontrol
- **Keyboard:** Panah (Gerak), Enter (Interaksi), Shift (Lari).
- **Gestur:**
  - Gerakkan tangan untuk mengontrol kursor/karakter.
  - Gestur "PISTOL" (Telunjuk ke atas) + sentakan ke atas untuk menembak.
