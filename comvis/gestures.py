import cv2
import mediapipe as mp
import pickle
import os
import numpy as np
import threading
import warnings
import pandas as pd
import math
import collections
import time

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
        # --- HYPER-SENSITIVE PISTOL LOGIC ---
        lm = hand_landmarks.landmark
        
        # 1. Very loose index check (just needs to be above the index base)
        index_up = lm[8].y < lm[5].y 
        
        # 2. Minimal thumb distance (anything away from index is a pistol)
        thumb_dist = math.hypot(lm[4].x - lm[5].x, lm[4].y - lm[5].y)
        thumb_loose = thumb_dist > 0.05 
        
        # RELOAD GESTURE: Fist (All tips below bases)
        if lm[8].y > lm[6].y and lm[12].y > lm[10].y and lm[16].y > lm[14].y:
            return "FIST"

        # Hyper-loose: If index is even slightly up and thumb is moved, it's a PISTOL
        if index_up and thumb_loose:
            return "PISTOL"

        if self.model is None:
            return "None"
        
        data = []
        wrist = hand_landmarks.landmark[0]
        for lm_node in hand_landmarks.landmark:
            data.append(lm_node.x - wrist.x)
        for lm_node in hand_landmarks.landmark:
            data.append(lm_node.y - wrist.y)
        for lm_node in hand_landmarks.landmark:
            data.append(lm_node.z - wrist.z)
        
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
        self._gesture_buffer = collections.deque(maxlen=7) # Smooth out flickering
        self._hand_pos = [0.5, 0.5]
        self._velocity_y = 0.0
        self._last_y = 0.5
        self._recoil_triggered = False
        self._last_shot_time = 0 # Cooldown system
        self._lock = threading.Lock()
        self.running = True
        self.daemon = True

    @property
    def current_gesture(self):
        with self._lock: return self._current_gesture

    @property
    def hand_pos(self):
        with self._lock: return list(self._hand_pos)
            
    @property
    def recoil_active(self):
        with self._lock:
            if self._recoil_triggered:
                self._recoil_triggered = False
                return True
            return False

    @property
    def hand_velocity(self):
        with self._lock: return self._velocity_y

    def run(self):
        cap = cv2.VideoCapture(self.camera_path)
        if not cap.isOpened(): return

        alpha = 0.8 # Ultra-fast response

        while self.running:
            ret, frame = cap.read()
            if not ret: break
            
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.recognizer.hands.process(rgb_frame)
            
            smoothed_gesture = "None"
            
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                gesture = self.recognizer.recognize(hand_landmarks)
                self._gesture_buffer.append(gesture)
                
                tip = hand_landmarks.landmark[8]
                
                raw_v_y = self._last_y - tip.y 
                self._velocity_y = (alpha * raw_v_y) + (1.0 - alpha) * self._velocity_y
                
                # Get the most common gesture in the buffer to avoid flickering
                smoothed_gesture = max(set(self._gesture_buffer), key=self._gesture_buffer.count)
                
                with self._lock:
                    self._current_gesture = smoothed_gesture
                    # Smooth hand position using Exponential Moving Average (EMA) to prevent aim jitter
                    alpha_pos = 0.20  # Reduced to 0.20 to eliminate delay/lag and make aiming snappy
                    self._hand_pos[0] = (alpha_pos * self._hand_pos[0]) + ((1.0 - alpha_pos) * tip.x)
                    self._hand_pos[1] = (alpha_pos * self._hand_pos[1]) + ((1.0 - alpha_pos) * tip.y)
                    
                    # REDUCED SENSITIVITY & COOLDOWN LOGIC
                    # Threshold increased from 0.015 to 0.04
                    # Cooldown of 0.25 seconds between gesture shots
                    current_time = time.time()
                    if gesture == "PISTOL" and self._velocity_y > 0.04:
                        if current_time - self._last_shot_time > 0.25:
                            self._recoil_triggered = True
                            self._last_shot_time = current_time
                        self._velocity_y = 0 
                    self._last_y = tip.y
                
                # Draw landmarks on the frame for debugging
                self.recognizer.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.recognizer.mp_hands.HAND_CONNECTIONS
                )
            else:
                self._gesture_buffer.append("None")
                smoothed_gesture = max(set(self._gesture_buffer), key=self._gesture_buffer.count) if self._gesture_buffer else "None"
                with self._lock:
                    self._current_gesture = smoothed_gesture
                    self._velocity_y = 0
            
            # Put text and display the debug frame
            color = (0, 255, 0) if smoothed_gesture != "None" else (0, 0, 255)
            cv2.putText(frame, f"Gesture: {smoothed_gesture}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.imshow("Hand Tracking Debug", frame)
            cv2.waitKey(1)
            
        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False
