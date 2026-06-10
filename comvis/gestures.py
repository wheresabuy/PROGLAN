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
    def recognize(self, hand_landmarks, in_minigame=False):
        lm = hand_landmarks.landmark
        if in_minigame:
            # Cek apakah model ML sudah dilatih untuk gestur minigame (PISTOL, AIM, FIST)
            has_ml_minigame = False
            if self.model is not None and hasattr(self.model, 'classes_'):
                has_ml_minigame = any(c in self.model.classes_ for c in ["PISTOL", "AIM", "FIST"])
            
            if has_ml_minigame:
                data = []
                wrist = hand_landmarks.landmark[0]
                for lm_node in hand_landmarks.landmark: data.append(lm_node.x - wrist.x)
                for lm_node in hand_landmarks.landmark: data.append(lm_node.y - wrist.y)
                for lm_node in hand_landmarks.landmark: data.append(lm_node.z - wrist.z)
                columns = [f'x{i}' for i in range(21)] + [f'y{i}' for i in range(21)] + [f'z{i}' for i in range(21)]
                df_input = pd.DataFrame([data], columns=columns)
                prediction = self.model.predict(df_input)
                pred_label = prediction[0]
                if pred_label in ["PISTOL", "AIM", "FIST"]:
                    return pred_label
                return "None"
            else:
                # Logika matematika (heuristik) sebagai fallback jika model ML belum dilatih
                hand_scale = math.hypot(lm[9].x - lm[0].x, lm[9].y - lm[0].y)
                if hand_scale < 0.01:
                    hand_scale = 0.01
                d_index = math.hypot(lm[8].x - lm[5].x, lm[8].y - lm[5].y)
                d_middle = math.hypot(lm[12].x - lm[9].x, lm[12].y - lm[9].y)
                d_ring = math.hypot(lm[16].x - lm[13].x, lm[16].y - lm[13].y)
                d_pinky = math.hypot(lm[20].x - lm[17].x, lm[20].y - lm[17].y)
                thumb_dist = math.hypot(lm[4].x - lm[5].x, lm[4].y - lm[5].y)
                r_index = d_index / hand_scale
                r_middle = d_middle / hand_scale
                r_ring = d_ring / hand_scale
                r_pinky = d_pinky / hand_scale
                r_thumb = thumb_dist / hand_scale
                is_index_open = r_index > 0.5
                is_middle_folded = r_middle < 0.45
                is_ring_folded = r_ring < 0.45
                is_pinky_folded = r_pinky < 0.45
                is_thumb_loose = r_thumb > 0.65
                if is_index_open and is_middle_folded and is_ring_folded and is_pinky_folded:
                    return "PISTOL" if is_thumb_loose else "AIM"
                is_index_folded = r_index < 0.4
                is_middle_folded_strict = r_middle < 0.4
                is_ring_folded_strict = r_ring < 0.4
                is_pinky_folded_strict = r_pinky < 0.4
                if is_index_folded and is_middle_folded_strict and is_ring_folded_strict and is_pinky_folded_strict:
                    return "FIST"
                return "None"
        else:
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
                if pred_label in ["ATAS", "BAWAH", "KIRI", "KANAN", "AMBIL"]:
                    return pred_label
            return "None"
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
        self._prev_gesture = "None"
        self._gesture_buffer = collections.deque(maxlen=5)
        self._hand_pos = [0.5, 0.5]
        self._velocity_y = 0.0
        self._last_y = 0.5
        self._recoil_triggered = False
        self._last_shot_time = 0
        self.latest_frame = None
        self._lock = threading.Lock()
        self.running = True
        self.daemon = True
        self.in_minigame = False
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
    @property
    def frame(self):
        with self._lock: return self.latest_frame
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
                    flipped_frame = cv2.flip(frame, 1)
                    rgb_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
                    results = self.recognizer.hands.process(rgb_frame)
                    smoothed_gesture = "None"
                    if results.multi_hand_landmarks:
                        hand_landmarks = results.multi_hand_landmarks[0]
                        self.recognizer.mp_draw.draw_landmarks(
                            flipped_frame, hand_landmarks, self.recognizer.mp_hands.HAND_CONNECTIONS)
                        gesture = self.recognizer.recognize(hand_landmarks, self.in_minigame)
                        self._gesture_buffer.append(gesture)
                        smoothed_gesture = max(set(self._gesture_buffer), key=self._gesture_buffer.count)
                        is_shooting_g = smoothed_gesture == "PISTOL"
                        was_shooting_g = self._prev_gesture == "PISTOL"
                        transition_to_shoot = is_shooting_g and not was_shooting_g
                        self._prev_gesture = smoothed_gesture
                        tip = hand_landmarks.landmark[8]
                        raw_v_y = self._last_y - tip.y
                        self._velocity_y = (alpha * raw_v_y) + (1.0 - alpha) * self._velocity_y
                        with self._lock:
                            self._current_gesture = smoothed_gesture
                            t_now = time.time()
                            self._hand_pos[0] = self.filter_x(t_now, tip.x)
                            self._hand_pos[1] = self.filter_y(t_now, tip.y)
                            jerk_fired = (is_shooting_g and self._velocity_y > 0.025)
                            if (transition_to_shoot or jerk_fired):
                                if time.time() - self._last_shot_time > 0.25:
                                    self._recoil_triggered = True
                                    self._last_shot_time = time.time()
                        self._last_y = tip.y
                    else:
                        with self._lock: self._current_gesture = "None"
                    import pygame
                    small = cv2.resize(flipped_frame, (160, 120))
                    rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
                    surf = pygame.surfarray.make_surface(rgb_small.swapaxes(0, 1))
                    with self._lock:
                        self.latest_frame = surf
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
