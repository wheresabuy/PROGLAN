import cv2
import mediapipe as mp
import collections
import time
import math

class MotionDetector:
    def __init__(self, buffer_size=15):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        
        # Buffer untuk menyimpan histori posisi pergelangan tangan (wrist)
        # deque otomatis menghapus data terlama saat data baru masuk
        self.history = collections.deque(maxlen=buffer_size)
        self.swipe_threshold = 0.15 # Minimal jarak perpindahan untuk dianggap swipe (0.0 - 1.0)
        
    def detect_motion(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        motion = "None"
        
        if results.multi_hand_landmarks:
            # Ambil koordinat Wrist (Landmark 0)
            wrist = results.multi_hand_landmarks[0].landmark[0]
            current_pos = (wrist.x, wrist.y)
            self.history.append(current_pos)
            
            # Jika buffer sudah penuh, mulai hitung pergerakan
            if len(self.history) == self.history.maxlen:
                start_pos = self.history[0] # Posisi 15 frame yang lalu
                end_pos = self.history[-1]   # Posisi sekarang
                
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                
                # Cek pergerakan horizontal (Swipe)
                if abs(dx) > self.swipe_threshold and abs(dx) > abs(dy):
                    if dx > 0:
                        motion = "SWIPE RIGHT"
                    else:
                        motion = "SWIPE LEFT"
                    self.history.clear() # Reset setelah terdeteksi agar tidak terulang
                
                # Cek pergerakan vertikal
                elif abs(dy) > self.swipe_threshold and abs(dy) > abs(dx):
                    if dy > 0:
                        motion = "SWIPE DOWN"
                    else:
                        motion = "SWIPE UP"
                    self.history.clear()
                    
        return motion

def main():
    # Contoh penggunaan mandiri menggunakan webca
    cap = cv2.VideoCapture(0) # Gunakan 0 untuk webcam lokal
    detector = MotionDetector()
    
    print("Gerakkan tanganmu ke kiri atau kanan dengan cepat!")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1)
        motion = detector.detect_motion(frame)
        
        if motion != "None":
            print(f"Action Terdeteksi: {motion}")
            cv2.putText(frame, motion, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        
        cv2.imshow("Motion Detection Demo", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
