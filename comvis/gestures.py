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
        lm = hand_landmarks.landmark
        pred_label = "None"
        if self.model is not None:
            data = []
            wrist = hand_landmarks.landmark[0]
            for lm_node in hand_landmarks.landmark: data.append(lm_node.x - wrist.x)
            for lm_node in hand_landmarks.landmark: data.append(lm_node.y - wrist.y)
            for lm_node in hand_landmarks.landmark: data.append(lm_node.z - wrist.z)
            columns = [f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)]
            df_input = pd.DataFrame([data], columns=columns)
            prediction = self.model.predict(df_input)
            pred_label = prediction[0]
            if pred_label in ["ATAS", "BAWAH", "KIRI", "KANAN", "AMBIL", "ENTER"]:
                return pred_label
        index_up = lm[8].y < lm[6].y
        thumb_dist = math.hypot(lm[4].x - lm[5].x, lm[4].y - lm[5].y)
        thumb_loose = thumb_dist > 0.05
        if lm[8].y > lm[6].y and lm[12].y > lm[10].y and lm[16].y > lm[14].y:
            return "FIST"
        if index_up and thumb_loose:
            return "PISTOL"
        return pred_label
class OneEuroFilter:
    def __init__(self, t0, x0, dx0=0.0, min_cutoff=0.8, beta=0.03, d_cutoff=1.0):
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)
        self.x_prev = float(x0)
        self.dx_prev = float(dx0)
        self.t_prev = float(t0)
    def __call__(self, t, x):
        t = float(t)
        x = float(x)
        dt = t - self.t_prev
        if dt <= 0:
            return self.x_prev
        dx = (x - self.x_prev) / dt
        a_d = 1.0 / (1.0 + 1.0 / (2 * math.pi * self.d_cutoff * dt))
        dx_hat = a_d * dx + (1.0 - a_d) * self.dx_prev
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a_s = 1.0 / (1.0 + 1.0 / (2 * math.pi * cutoff * dt))
        x_hat = a_s * x + (1.0 - a_s) * self.x_prev
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t_prev = t
        return x_hat
class GestureThread(threading.Thread):
    def __init__(self, camera_path):
        threading.Thread.__init__(self)
        self.camera_path = camera_path
        self.recognizer = GestureRecognizerML()
        self._current_gesture = "None"
        self._gesture_buffer = collections.deque(maxlen=5)
        self._hand_pos = [0.5, 0.5]
        self._velocity_y = 0.0
        self._last_y = 0.5
        self._recoil_triggered = False
        self._last_shot_time = 0
        self._lock = threading.Lock()
        self.running = True
        self.daemon = True
        t_now = time.time()
        self.filter_x = OneEuroFilter(t_now, 0.5, min_cutoff=1.5, beta=0.15)
        self.filter_y = OneEuroFilter(t_now, 0.5, min_cutoff=1.5, beta=0.15)
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
    def run(self):
        try:
            cap = cv2.VideoCapture(self.camera_path)
            if not cap.isOpened():
                print("Error: Kamera tidak dapat diakses.")
                return
            alpha = 0.7
            while self.running:
                ret, frame = cap.read()
                if not ret: break
                try:
                    rgb_frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                    results = self.recognizer.hands.process(rgb_frame)
                    smoothed_gesture = "None"
                    if results.multi_hand_landmarks:
                        hand_landmarks = results.multi_hand_landmarks[0]
                        gesture = self.recognizer.recognize(hand_landmarks)
                        self._gesture_buffer.append(gesture)
                        smoothed_gesture = max(set(self._gesture_buffer), key=self._gesture_buffer.count)
                        tip = hand_landmarks.landmark[8]
                        raw_v_y = self._last_y - tip.y
                        self._velocity_y = (alpha * raw_v_y) + (1.0 - alpha) * self._velocity_y
                        with self._lock:
                            self._current_gesture = smoothed_gesture
                            t_now = time.time()
                            self._hand_pos[0] = self.filter_x(t_now, tip.x)
                            self._hand_pos[1] = self.filter_y(t_now, tip.y)
                            if smoothed_gesture == "PISTOL" and self._velocity_y > 0.04:
                                if time.time() - self._last_shot_time > 0.25:
                                    self._recoil_triggered = True
                                    self._last_shot_time = time.time()
                        self._last_y = tip.y
                    else:
                        with self._lock: self._current_gesture = "None"
                except Exception as inner_e:
                    print(f"MediaPipe Processing Error: {inner_e}")
                    continue
            cap.release()
        except Exception as e:
            print(f"GestureThread Error: {e}")
        finally:
            if hasattr(self.recognizer, 'hands'):
                self.recognizer.hands.close()
    def stop(self):
        self.running = False
