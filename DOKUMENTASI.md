# 📂 MENU DOKUMENTASI & PENJELASAN KODE (LINE-BY-LINE)

Halo! Karena proyek ini akan didemokan, semua berkas penjelasan baris-demi-baris (`.md`) telah dikumpulkan ke dalam satu folder terpusat yaitu **`dokumentasi/`** di direktori utama agar mudah diakses.

Gunakan menu di bawah ini untuk langsung membuka dokumen penjelasan untuk setiap berkas kode:

---

## 🎮 1. Alur Utama Game (Root)
* 🚀 **Main Entry Point**: [main.md](./dokumentasi/main.md) *(Menjelaskan inisialisasi game loop, kustomisasi wardrobe, gesture control, dan integrasi minigame)*

---

## 🧠 2. Modul Computer Vision (Gesture Kamera)
* ✋ **Gestures Thread Tracker**: [gestures.md](./dokumentasi/gestures.md) *(Thread pelacakan landmark tangan MediaPipe & klasifikasi gestur real-time)*
* 🔫 **Visualisasi Logika Pistol**: [visualisasi_logika_pistol.md](./dokumentasi/visualisasi_logika_pistol.md) *(Visualisasi geometris dan logika pemicu tembakan recoil)*
* ↔️ **Motion/Swipe Detector**: [motion_detect.md](./dokumentasi/motion_detect.md) *(Mendeteksi gerakan sapuan tangan swipe kiri/kanan/atas/bawah)*
* 💾 **Data Collector**: [train_data.md](./dokumentasi/train_data.md) *(Skrip perekaman dataset koordinat tangan ke file CSV)*
* 🤖 **Model Trainer**: [train_model.md](./dokumentasi/train_model.md) *(Melatih model Random Forest Classifier untuk mengenali gestur tangan)*
* 🧹 **Reset Dataset**: [reset_data.md](./dokumentasi/reset_data.md) *(Membersihkan data rekaman gestur lama)*


---

## 🏛️ 3. Inti Logika Game (src/core/)
* 🗺️ **Sanctuary Logic**: [sanctuary_logic.md](./dokumentasi/sanctuary_logic.md) *(Logika interaksi map, api unggun, kasur medis, helipad drop, loker pakaian)*
* 🎥 **Camera Viewport**: [camera.md](./dokumentasi/camera.md) *(Mengatur pergerakan kamera mengikuti posisi koordinat pemain)*
* 💰 **Currency Manager**: [currency.md](./dokumentasi/currency.md) *(Mengelola koin perunggu/perak/emas dan konversi otomatis)*
* 🌟 **Visual Effects (VFX)**: [visual_effects.md](./dokumentasi/visual_effects.md) *(Menghasilkan senter/gelap, screen shake recoil, dan kilatan cahaya)*
* 🔊 **Audio System**: [audio_manager.md](./dokumentasi/audio_manager.md) *(Mengontrol pemutaran musik latar BGM dan efek suara SFX)*
* 🕹️ **Sub-Game Orchestrator**: [minigame_manager.md](./dokumentasi/minigame_manager.md) *(Mengatur pergantian state dari game utama ke minigame dan pembagian koin)*
* 🎯 **Shooting Minigame**: [shooting_range.md](./dokumentasi/shooting_range.md) *(FPS Zombie Shooter, aim-assist lock, progressive multiplier, time extension)*

---

## 🏃 4. Karakter & Entitas (src/entities/)
* 👤 **Player Character**: [player.md](./dokumentasi/player.md) *(Logika gerak pemain, efek adrenalin, dan render baju-kulit-rambut-topi berlapis)*
* 👥 **Civilian/Guard AI**: [npc.md](./dokumentasi/npc.md) *(AI berkeliaran random/wandering untuk Kapten Jaka, Penatua Aris, dll.)*
* 🧟 **Zombie NPC**: [zombie.md](./dokumentasi/zombie.md) *(Perilaku zombie mengejar, terkena taser/molotov/decoy)*
* 🎒 **Loot/Bronze Drops**: [loot.md](./dokumentasi/loot.md) *(Deteksi jarak dan animasi melayang koin jarahan)*
* 💣 **Tactical Throwables**: [tactical_item.md](./dokumentasi/tactical_item.md) *(Fisika lemparan Molotov, Decoy, dan Taser)*

---

## 🖥️ 5. Antarmuka Layar (src/ui/)
* 📊 **HUD (Heads-Up Display)**: [hud.md](./dokumentasi/hud.md) *(Menggambar bar darah, baterai senter, dan animasi angka koin)*
* 💬 **Dialogue System**: [dialogue.md](./dokumentasi/dialogue.md) *(Menampilkan kotak dialog narasi cerita)*

---

*Tips: Anda dapat membuka folder `dokumentasi/` untuk melihat semua file secara langsung, atau mengeklik tautan di atas jika Anda membukanya di VS Code / GitHub.*
