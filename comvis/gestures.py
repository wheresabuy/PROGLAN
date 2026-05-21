import cv2
import mediapipe as mp
import pickle
import os
import numpy as np
import threading
import warnings
import pandas as pd

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class GestureRecognizerML:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_dir, 'gesture_model.pkl')
        self.model = None
        
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print("Model Machine Learning berhasil dimuat.")
        else:
            print("Peringatan: Model belum dilatih. Gunakan train_model.py!")

    def recognize(self, hand_landmarks):
        if self.model is None:
            return "None"
        
        data = []
        wrist = hand_landmarks.landmark[0]
        
        for lm in hand_landmarks.landmark:
            data.append(lm.x - wrist.x)
        for lm in hand_landmarks.landmark:
            data.append(lm.y - wrist.y)
        for lm in hand_landmarks.landmark:
            data.append(lm.z - wrist.z)
        
        columns = [f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)]
        df_input = pd.DataFrame([data], columns=columns)
        
        prediction = self.model.predict(df_input)
        return prediction[0]

class GestureThread(threading.Thread):
    def __init__(self, camera_path):
        threading.Thread.__init__(self)
        self.camera_path = camera_path
        self.recognizer = GestureRecognizerML()
        self._current_gesture = "None"
        self._lock = threading.Lock()
        self.running = True
        self.daemon = True

    @property
    def current_gesture(self):
        with self._lock:
            return self._current_gesture

    @current_gesture.setter
    def current_gesture(self, value):
        with self._lock:
            self._current_gesture = value

    def run(self):
        cap = cv2.VideoCapture(self.camera_path)
        if not cap.isOpened():
            print(f"Error: Tidak bisa membuka stream video dari {self.camera_path}")
            return

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.recognizer.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                gesture = self.recognizer.recognize(hand_landmarks)
                self.current_gesture = gesture
            else:
                self.current_gesture = "None"

        cap.release()

    def stop(self):
        self.running = False

def main():
    recognizer_thread = GestureThread(0)
    recognizer_thread.start()
    
    print("Starting Gesture Thread... Press Ctrl+C to stop.")
    try:
        while True:
            if recognizer_thread.current_gesture != "None":
                print(f"Detected: {recognizer_thread.current_gesture}")
    except KeyboardInterrupt:
        recognizer_thread.stop()

if __name__ == "__main__":
    main()
