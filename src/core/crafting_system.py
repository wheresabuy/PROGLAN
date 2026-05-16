
class CraftingSystem:
    def __init__(self):
        # Resep: { frozenset([bahan1, bahan2, ...]): { result, description, hint } }
        self.recipes = {
            # --- ELEKTRONIK & TOOLS ---
            frozenset(["Baterai Militer", "Chip Frekuensi"]): {
                "result": "Umpan Elektronik",
                "description": "Mengalihkan perhatian zombie dengan suara frekuensi tinggi.",
                "hint": "Baterai dan komponen elektronik bisa menghasilkan suara bising..."
            },
            frozenset(["Antena Radio", "Baterai Cadangan"]): {
                "result": "Signal Booster",
                "description": "Meningkatkan jangkauan radio untuk memanggil bantuan.",
                "hint": "Antena butuh daya lebih untuk mengirim sinyal jauh."
            },
            frozenset(["Kabel", "Baterai Cadangan"]): {
                "result": "Taser Rakitan",
                "description": "Menyetrum zombie yang mendekat, membuat mereka kaku sejenak.",
                "hint": "Kabel dan baterai bisa menciptakan percikan listrik yang kuat."
            },
            frozenset(["Kabel", "Lempeng Besi"]): {
                "result": "Perangkap Listrik",
                "description": "Bisa dipasang di tanah untuk menyetrum zombie yang lewat.",
                "hint": "Plat besi yang dialiri listrik bisa jadi jebakan maut."
            },
            frozenset(["Taser Rakitan", "Umpan Elektronik"]): {
                "result": "Shock Decoy",
                "description": "Umpan yang meledak dengan sengatan listrik saat disentuh zombie.",
                "hint": "Bagaimana jika umpan itu sendiri bisa menyerang balik?"
            },

            # --- SENJATA & OFFENSIVE ---
            frozenset(["Botol Kosong", "Jerigen Bensin", "Kain Bekas"]): {
                "result": "Bom Molotov",
                "description": "Membakar area kecil, efektif menghalau kerumunan zombie.",
                "hint": "Bensin di dalam botol dengan sumbu kain... klasik tapi mematikan."
            },
            frozenset(["Botol Kosong", "Cairan Pelarut", "Kabel"]): {
                "result": "Granat Kimia",
                "description": "Melepaskan gas beracun yang memperlambat semua zombie di area.",
                "hint": "Cairan kimia dalam botol tertutup bisa jadi senjata gas."
            },
            frozenset(["Lempeng Besi", "Kain Bekas"]): {
                "result": "Machete Karatan",
                "description": "Senjata jarak dekat darurat untuk memukul mundur zombie.",
                "hint": "Plat besi panjang bisa diasah dan diberi pegangan kain."
            },
            frozenset(["Machete Karatan", "Cairan Pelarut"]): {
                "result": "Acid Blade",
                "description": "Machete yang dilapisi asam, memberikan damage berkelanjutan.",
                "hint": "Melapisi bilah besi dengan asam kimia akan membuatnya lebih korosif."
            },
            frozenset(["Botol Kosong", "Baterai Cadangan", "Lempeng Besi"]): {
                "result": "Bom Serpihan",
                "description": "Ledakan yang menyebarkan potongan besi tajam ke segala arah.",
                "hint": "Botol berisi serpihan besi dan pemicu baterai bisa meledak hebat."
            },

            # --- SURVIVAL & LIGHTING ---
            frozenset(["Kain Bekas", "Cairan Pelarut"]): {
                "result": "Obor Darurat",
                "description": "Memberikan cahaya tanpa menghabiskan baterai senter.",
                "hint": "Cairan kimia ini sangat mudah terbakar jika dioleskan ke kain."
            },
            frozenset(["Obor Darurat", "Lempeng Besi"]): {
                "result": "Lentera Besi",
                "description": "Cahaya yang lebih stabil dan tahan lama daripada obor.",
                "hint": "Melindungi api dengan rangka besi agar tidak mudah mati."
            },
            frozenset(["Baju Survival", "Kain Bekas", "Cairan Pelarut"]): {
                "result": "Ghillie Suit",
                "description": "Sangat sulit dideteksi zombie selama tidak bergerak.",
                "hint": "Menyamarkan baju dengan kain dan bahan kimia agar bau manusia hilang."
            },

            # --- MEDIKAL & BUFFS ---
            frozenset(["Tanaman Obat", "Cairan Pelarut"]): {
                "result": "Antiseptik Kuat",
                "description": "Menyembuhkan luka lebih cepat dan menghilangkan infeksi.",
                "hint": "Mengekstrak sari tanaman dengan cairan kimia bisa memperkuat efek."
            },
            frozenset(["Pembalut Lukaku", "Antiseptik Kuat"]): {
                "result": "Medkit Medis",
                "description": "Memulihkan kesehatan secara penuh secara instan.",
                "hint": "Pembalut bersih dan antiseptik adalah kombinasi medis standar."
            },
            frozenset(["Tanaman Obat", "Mata Air"]): {
                "result": "Teh Herbal",
                "description": "Meningkatkan stamina maksimal untuk sementara.",
                "hint": "Tanaman obat yang diseduh air segar bisa menyegarkan tubuh."
            },
            frozenset(["Antiseptik Kuat", "Jerigen Bensin"]): {
                "result": "Stimulan Adrenalin",
                "description": "Berlari tanpa lelah selama 30 detik.",
                "hint": "Kombinasi kimia yang sangat tidak stabil tapi memicu energi instan."
            },
            frozenset(["Mata Air", "Botol Kosong"]): {
                "result": "Air Bersih",
                "description": "Memulihkan stamina dengan cepat.",
                "hint": "Mengisi botol kosong dengan air segar untuk minum."
            },
            frozenset(["Air Bersih", "Antiseptik Kuat"]): {
                "result": "Energy Drink",
                "description": "Memulihkan stamina dan memberikan kecepatan gerak.",
                "hint": "Air yang diperkaya nutrisi kimia untuk energi tambahan."
            },

            # --- PERTAHANAN & EQUIPMENT ---
            frozenset(["Baju Survival", "Lempeng Besi"]): {
                "result": "Armor Diperkuat",
                "description": "Mengurangi kerusakan yang diterima dari serangan zombie.",
                "hint": "Menempelkan plat besi pada baju bisa memberikan perlindungan ekstra."
            },
            frozenset(["Armor Diperkuat", "Kabel"]): {
                "result": "Shock Armor",
                "description": "Zombie yang menggigitmu akan terkena setruman.",
                "hint": "Bagaimana jika baju besimu dialiri arus listrik?"
            },
            frozenset(["Sepatu Tua", "Kain Bekas"]): {
                "result": "Sepatu Senyap",
                "description": "Membuat langkah kaki tidak terdengar oleh zombie saat berlari.",
                "hint": "Membungkus sepatu dengan kain tebal akan meredam suara."
            },
            frozenset(["Sepatu Tua", "Lempeng Besi"]): {
                "result": "Sepatu Safety",
                "description": "Tidak akan terlambat (slow) saat melewati area beracun atau lumpur.",
                "hint": "Memperkuat alas sepatu dengan besi untuk medan berat."
            },
            frozenset(["Lempeng Besi", "Lempeng Besi"]): {
                "result": "Perisai Besi",
                "description": "Menahan serangan zombie dari depan sepenuhnya (daya tahan terbatas).",
                "hint": "Dua lempeng besi besar bisa disatukan menjadi pelindung."
            },

            # --- ADVANCED CRAFTING ---
            frozenset(["Signal Booster", "Chip Frekuensi"]): {
                "result": "Hacking Tool",
                "description": "Bisa digunakan untuk membuka pintu elektronik atau mematikan alarm.",
                "hint": "Sinyal kuat dan chip canggih bisa menembus sistem keamanan."
            },
            frozenset(["Hacking Tool", "Kabel"]): {
                "result": "Remote Detonator",
                "description": "Meledakkan jebakan dari jarak jauh.",
                "hint": "Alat peretas yang dimodifikasi bisa jadi pemicu ledakan jarak jauh."
            }
        }
        self.discovered_recipes = [] # List of result names

    def check_recipe(self, selected_items):
        """
        selected_items: list of item names
        return: (result_name, description) atau None
        """
        items_set = frozenset(selected_items)
        if items_set in self.recipes:
            recipe = self.recipes[items_set]
            return recipe["result"], recipe["description"]
        return None, None

    def get_hints(self, inventory_items):
        """Mengembalikan list hint berdasarkan item yang dimiliki pemain"""
        hints = []
        for ingredients, data in self.recipes.items():
            # Jika pemain punya salah satu bahan, berikan hint
            for item in inventory_items:
                if item in ingredients:
                    hints.append(data["hint"])
                    break
        return list(set(hints))
