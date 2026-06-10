import cv2
import mediapipe as mp
import csv
import os

class DataCollector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Gunakan path absolut agar tidak error saat dipanggil dari mana saja
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(base_dir, 'gesture_data.csv')
        
        # Inisialisasi file CSV jika belum ada
        if not os.path.exists(self.data_file):
            print(f"Membuat file data baru di: {self.data_file}")
            with open(self.data_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                # 21 landmarks * 3 (x, y, z) + label
                header = [f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)] + ['label']
                writer.writerow(header)

    def save_landmarks(self, landmarks, label):
        data = []
        # Gunakan pergelangan tangan (landmark 0) sebagai titik referensi (0,0)
        wrist = landmarks.landmark[0]
        
        # Simpan koordinat relatif (selisih dari pergelangan tangan)
        for lm in landmarks.landmark:
            data.append(lm.x - wrist.x)
        for lm in landmarks.landmark:
            data.append(lm.y - wrist.y)
        for lm in landmarks.landmark:
            data.append(lm.z - wrist.z)
            
        data.append(label)
        
        with open(self.data_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

def main():
    path = 0
    cap = cv2.VideoCapture(path)
    collector = DataCollector()
    
    current_label = ""
    recording = False
    count = 0

    print("--- DATA COLLECTOR ---")
    print("1. Tekan 'l' untuk memasukkan nama label baru (misal: 'OK', 'SPIDERMAN')")
    print("2. Tekan 's' untuk mulai/berhenti merekam data")
    print("3. Tekan 'q' untuk keluar")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = collector.hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                collector.mp_draw.draw_landmarks(frame, hand_landmarks, collector.mp_hands.HAND_CONNECTIONS)
                
                if recording and current_label:
                    collector.save_landmarks(hand_landmarks, current_label)
                    count += 1
        
        # UI Overlay
        status = f"REC: {current_label}" if recording else "IDLE"
        cv2.putText(frame, f"Status: {status} | Samples: {count}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if recording else (0, 255, 0), 2)
        
        cv2.imshow('Data Collector', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('l'):
            current_label = input("Masukkan nama label gestur baru: ")
            count = 0
            print(f"Label diatur ke: {current_label}")
        elif key == ord('s'):
            if not current_label:
                print("Error: Masukkan label dulu (tekan 'l')")
            else:
                recording = not recording
                print(f"Recording: {recording}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
