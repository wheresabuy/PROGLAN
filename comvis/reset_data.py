import os

def reset_gesture_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'gesture_data.csv')
    model_path = os.path.join(base_dir, 'gesture_model.pkl')

    print("--- RESET DATA GESTUR ---")
    confirm = input("Apakah Anda yakin ingin menghapus semua data rekaman dan model? (y/n): ")
    
    if confirm.lower() == 'y':
        removed = []
        if os.path.exists(data_path):
            os.remove(data_path)
            removed.append("gesture_data.csv")
        
        if os.path.exists(model_path):
            os.remove(model_path)
            removed.append("gesture_model.pkl")
            
        if removed:
            print(f"Berhasil menghapus: {', '.join(removed)}")
            print("Sekarang Anda bisa mulai merekam data dari awal.")
        else:
            print("Tidak ada data atau model yang ditemukan untuk dihapus.")
    else:
        print("Reset dibatalkan.")

if __name__ == "__main__":
    reset_gesture_data()
