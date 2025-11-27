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
    if now - last_time < 1.0 / TARGET_FPS:
        continue
    last_time = now

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # === 1. DETECTAR CARA ===
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(80, 80)
    )

    ojos_detectados = False

    for (x, y, w, h) in faces:
        # Dibujar recuadro de la cara
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # === ZONA SUPERIOR DE LA CARA (donde realmente están los ojos) ===
        eye_region_gray = roi_gray[0:int(h * 0.45), :]
        eye_region_color = roi_color[0:int(h * 0.45), :]

        # === 2. DETECTAR OJOS EN ZONA RESTRINGIDA ===
        eyes = eye_cascade.detectMultiScale(
            eye_region_gray,
            scaleFactor=1.12,     # equilibrado
            minNeighbors=4,        # reduce falsos positivos
            minSize=(20, 20)       # tamaño mínimo de ojos realistas
        )

        if len(eyes) >= 1:
            ojos_detectados = True

        # Dibujar ojos detectados
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(eye_region_color, (ex, ey),
                          (ex+ew, ey+eh), (255,255,0), 2)

        break  # solo usar la primera cara detectada

    # === 3. ACTUALIZAR HISTORIAL ===
    history.append(0 if ojos_detectados else 1)

    # === 4. CALCULAR PERCLOS ===
    perclos = sum(history) / len(history) if len(history) > 0 else 0

    cv2.putText(frame, f"PERCLOS: {perclos:.2f}", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

    # === 5. ALERTA DE SOMNOLENCIA ===
    if perclos > PERCLOS_THRESHOLD and len(history) == history.maxlen:
        cv2.putText(frame, "ALERTA: SOMNOLENCIA", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    else:
        cv2.putText(frame, "ESTADO NORMAL", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    # === MOSTRAR ===
    cv2.imshow("Paso 3 - PERCLOS (Optimizado)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
