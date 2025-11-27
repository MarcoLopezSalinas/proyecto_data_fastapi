import cv2
import time
from collections import deque

# ===== MODELOS PREENTRENADOS =====
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml"
)

# ===== PARÁMETROS =====
WINDOW_SECONDS = 10       # Ventana de tiempo para PERCLOS
TARGET_FPS = 8            # Suave para Raspberry
PERCLOS_THRESHOLD = 0.4   # Umbral de alerta

history = deque(maxlen=WINDOW_SECONDS * TARGET_FPS)

# ===== CÁMARA =====
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

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
        minSize=(60, 60)
    )

    ojos_detectados = False

    for (x, y, w, h) in faces:
        # Rectángulo en la cara
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        # ROI cara
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # === 2. DETECTAR OJOS ===
        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(15, 15)
        )

        if len(eyes) >= 1:
            ojos_detectados = True

        # Dibujar ojos
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255,255,0), 2)

        break  # solo la primera cara

    # === 3. ACTUALIZAR HISTORIAL ===
    # 0 = ojo abierto, 1 = ojo cerrado
    history.append(0 if ojos_detectados else 1)

    # === 4. CALCULAR PERCLOS ===
    perclos = sum(history) / len(history) if len(history) > 0 else 0

    # Mostrar PERCLOS en pantalla
    cv2.putText(frame, f"PERCLOS: {perclos:.2f}", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

    # === 5. ALERTA DE SOMNOLENCIA ===
    if perclos > PERCLOS_THRESHOLD and len(history) == history.maxlen:
        cv2.putText(frame, "ALERTA: SOMNOLENCIA", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    else:
        cv2.putText(frame, "ESTADO NORMAL", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    # === MOSTRAR VIDEO ===
    cv2.imshow("Paso 3 - PERCLOS", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
