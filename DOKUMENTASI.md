# 📂 MENU DOKUMENTASI & PENJELASAN KODE (LINE-BY-LINE)

Halo! Karena proyek ini akan didemokan, semua file kode (`.py`) telah dibuatkan file penjelasan baris-demi-baris (`.md`) pendamping di folder masing-masing agar mudah dipelajari.

Dokumen penjelasan terletak tepat di samping file kodenya (misal: `player.md` berada di folder `src/entities/` berdampingan dengan `player.py`).

Gunakan menu di bawah ini untuk membuka dokumentasi penjelasan setiap file secara langsung:

---

## 🎮 1. Alur Utama Game (Root)
* 🚀 **Main Entry Point**: [main.md](./main.md) *(Menjelaskan inisialisasi game loop, kustomisasi wardrobe, gesture control, dan integrasi minigame)*

---

## 🧠 2. Modul Computer Vision (Gesture Kamera)
Semua file deteksi gestur berbasis kamera dan machine learning berada di dalam folder `comvis/`:
* ✋ **Gestures Thread Tracker**: [gestures.md](./comvis/gestures.md) *(Thread pelacakan landmark tangan MediaPipe & klasifikasi gestur real-time)*
* ↔️ **Motion/Swipe Detector**: [motion_detect.md](./comvis/motion_detect.md) *(Mendeteksi gerakan sapuan tangan swipe kiri/kanan/atas/bawah)*
* 💾 **Data Collector**: [train_data.md](./comvis/train_data.md) *(Skrip perekaman dataset koordinat tangan ke file CSV)*
* 🤖 **Model Trainer**: [train_model.md](./comvis/train_model.md) *(Melatih model Random Forest Classifier untuk mengenali gestur tangan)*
* 🧹 **Reset Dataset**: [reset_data.md](./comvis/reset_data.md) *(Membersihkan data rekaman gestur lama)*

---

## 🏛️ 3. Inti Logika Game (src/core/)
Sistem peta, kamera, audio, koin, efek, dan transisi minigame:
* 🗺️ **Sanctuary Logic**: [sanctuary_logic.md](./src/core/sanctuary_logic.md) *(Logika interaksi map, api unggun, kasur medis, helipad drop, loker pakaian)*
* 🎥 **Camera Viewport**: [camera.md](./src/core/camera.md) *(Mengatur pergerakan kamera mengikuti posisi koordinat pemain)*
* 💰 **Currency Manager**: [currency.md](./src/core/currency.md) *(Mengelola koin perunggu/perak/emas dan konversi otomatis)*
* 🌟 **Visual Effects (VFX)**: [visual_effects.md](./src/core/visual_effects.md) *(Menghasilkan senter/gelap, screen shake recoil, dan kilatan cahaya)*
* 🔊 **Audio System**: [audio_manager.md](./src/core/audio_manager.md) *(Mengontrol pemutaran musik latar BGM dan efek suara SFX)*
* 🕹️ **Sub-Game Orchestrator**: [minigame_manager.md](./src/core/minigame_manager.md) *(Mengatur pergantian state dari game utama ke minigame dan pembagian koin)*
* 🎯 **Shooting Minigame**: [shooting_range.md](./src/core/minigames/shooting_range.md) *(FPS Zombie Shooter, aim-assist lock, progressive multiplier, time extension)*

---

## 🏃 4. Karakter & Entitas (src/entities/)
Logika pergerakan pemain, kecerdasan buatan NPC, zombie, item taktis, dan jarahan:
* 👤 **Player Character**: [player.md](./src/entities/player.md) *(Logika gerak pemain, efek adrenalin, dan render baju-kulit-rambut-topi berlapis)*
* 👥 **Civilian/Guard AI**: [npc.md](./src/entities/npc.md) *(AI berkeliaran random/wandering untuk Kapten Jaka, Penatua Aris, dll.)*
* 🧟 **Zombie NPC**: [zombie.md](./src/entities/zombie.md) *(Perilaku zombie mengejar, terkena taser/molotov/decoy)*
* 🎒 **Loot/Bronze Drops**: [loot.md](./src/entities/loot.md) *(Deteksi jarak dan animasi melayang koin jarahan)*
* 💣 **Tactical Throwables**: [tactical_item.md](./src/entities/tactical_item.md) *(Fisika lemparan Molotov, Decoy, dan Taser)*

---

## 🖥️ 5. Antarmuka Layar (src/ui/)
* 📊 **HUD (Heads-Up Display)**: [hud.md](./src/ui/hud.md) *(Menggambar bar darah, baterai senter, dan animasi angka koin)*
* 💬 **Dialogue System**: [dialogue.md](./src/ui/dialogue.md) *(Menampilkan kotak dialog narasi cerita)*

---

*Tips: Klik tautan relatif di atas di VS Code atau GitHub untuk membuka penjelasan file tersebut secara instan.*
