import cv2
import mediapipe as mp
import pyautogui
import time
from collections import deque
import math

# ================== SYSTEM CONFIG ==================
SCREEN_W, SCREEN_H = pyautogui.size()
CAM_W, CAM_H = 640, 480

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# ================== MEDIAPIPE ==================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
    model_complexity=0
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, CAM_W)
cap.set(4, CAM_H)

# ================== SMOOTHING ==================
cursor_history = deque(maxlen=5)

def smooth_cursor(x, y):
    cursor_history.append((x, y))
    avg_x = sum(p[0] for p in cursor_history) // len(cursor_history)
    avg_y = sum(p[1] for p in cursor_history) // len(cursor_history)
    return avg_x, avg_y

# ================== UTILITIES ==================
def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

CLICK_THRESHOLD = 30
CLICK_COOLDOWN = 0.35
last_click_time = 0

SCROLL_COOLDOWN = 0.2
last_scroll_time = 0
prev_scroll_y = None

# ================== MAIN LOOP ==================
while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark

        # Landmark coordinates
        ix, iy = int(lm[8].x * CAM_W), int(lm[8].y * CAM_H)     # Index
        tx, ty = int(lm[4].x * CAM_W), int(lm[4].y * CAM_H)     # Thumb
        mx, my = int(lm[12].x * CAM_W), int(lm[12].y * CAM_H)   # Middle

        # Map index finger to screen
        screen_x = int(ix * SCREEN_W / CAM_W)
        screen_y = int(iy * SCREEN_H / CAM_H)

        screen_x, screen_y = smooth_cursor(screen_x, screen_y)
        pyautogui.moveTo(screen_x, screen_y)

        now = time.time()

        # ---------- LEFT CLICK ----------
        if distance((ix, iy), (tx, ty)) < CLICK_THRESHOLD:
            if now - last_click_time > CLICK_COOLDOWN:
                pyautogui.click()
                last_click_time = now

        # ---------- RIGHT CLICK ----------
        if distance((mx, my), (tx, ty)) < CLICK_THRESHOLD:
            if now - last_click_time > CLICK_COOLDOWN:
                pyautogui.rightClick()
                last_click_time = now

        # ---------- SCROLL ----------
        if prev_scroll_y is not None:
            dy = iy - prev_scroll_y
            if abs(dy) > 15 and now - last_scroll_time > SCROLL_COOLDOWN:
                pyautogui.scroll(-dy)
                last_scroll_time = now

        prev_scroll_y = iy

        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    else:
        prev_scroll_y = None

    cv2.imshow("Virtual Mouse - Press Q to Exit", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ================== CLEANUP ==================
cap.release()
cv2.destroyAllWindows()
