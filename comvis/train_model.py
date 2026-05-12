import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

def train_gesture_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'gesture_data.csv')
    model_path = os.path.join(base_dir, 'gesture_model.pkl')

    if not os.path.exists(data_path):
        print(f"Error: File {data_path} tidak ditemukan. Rekam data dulu pakai train_data.py!")
        return

    # 1. Load Data
    try:
        # Coba baca baris pertama untuk cek apakah itu header
        df_check = pd.read_csv(data_path, nrows=0)
        if 'label' not in df_check.columns:
            print("Peringatan: Header tidak ditemukan. Menambahkan header manual.")
            # 21 landmarks * 3 (x, y, z) + label = 64 kolom
            columns = [f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)] + ['label']
            df = pd.read_csv(data_path, header=None, names=columns)
        else:
            df = pd.read_csv(data_path)
    except Exception as e:
        print(f"Error saat membaca file: {e}")
        return
    
    if len(df) < 10:
        print("Error: Data terlalu sedikit untuk dilatih. Rekam lebih banyak data!")
        return

    # X adalah koordinat (semua kolom kecuali 'label'), y adalah label
    X = df.drop('label', axis=1)
    y = df['label']

    # 2. Split Data (Training & Testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Train Model (Random Forest)
    print("Sedang melatih model... Mohon tunggu.")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 4. Evaluasi
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model berhasil dilatih dengan akurasi: {acc * 100:.2f}%")

    # 5. Simpan Model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model disimpan di: {model_path}")

if __name__ == "__main__":
    train_gesture_model()
