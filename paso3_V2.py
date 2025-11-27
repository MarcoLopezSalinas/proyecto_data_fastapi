import cv2
import time
from collections import deque

# ===== MODELOS HAAR =====
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml"
)

# ===== PARÁMETROS =====
WINDOW_SECONDS = 10          # ventana de tiempo para PERCLOS
TARGET_FPS = 8               # FPS real para Raspberry Pi
PERCLOS_THRESHOLD = 0.4      # umbral clásico de somnolencia
history = deque(maxlen=WINDOW_SECONDS * TARGET_FPS)

# ===== CÁMARA =====
cap = cv2.VideoCapture(0)   # cambia a 1 si tu Logitech es /dev/video1
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 15)

last_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer de la cámara")
        break

    now = time.time()
    if now - last_time <_
