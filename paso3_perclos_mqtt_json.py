import cv2
import time
import json
from collections import deque
import paho.mqtt.client as mqtt
from datetime import datetime

# ============================
#       CONFIGURACIÓN MQTT
# ============================
MQTT_HOST = "c7c44e54b07f4423b4612de260c0bdec.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "RASPBERRY"
MQTT_PASS = "Raspberry1"
MQTT_TOPIC = "somnolencia/eventos"

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set()   # SSL obligatorio
client.connect(MQTT_HOST, MQTT_PORT)

# ============================
#      MODELOS HAAR
# ============================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml"
)

# ============================
#       PARÁMETROS
# ============================
WINDOW_SECONDS = 10
TARGET_FPS = 8
PERCLOS_THRESHOLD = 0.40

history = deque(maxlen=WINDOW_SECONDS * TARGET_FPS)
eye_state_history = deque(maxlen=WINDOW_SECONDS * TARGET_FPS)

alert_enviada = False
last_state = "normal"
last_time = time.time()

# ============================
#        CÁMARA
# ============================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

def compute_blinks(history):
    """Cuenta cuántos parpadeos hubo."""
    blinks = 0
    for i in range(1, len(history)-1):
        if history[i-1] == 0 and history[i] == 1 and history[i+1] == 0:
            blinks += 1
    return blinks

while True:

    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer la cámara.")
        break

    now = time.time()
    if now - last_time < 1.0 / TARGET_FPS:
        continue
    last_time = now

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # ========= DETECTAR CARA =========
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60)
    )

    ojos_detectados = False
    max_eye_height = 0

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # ========= DETECTAR OJOS =========
        eyes = eye_cascade.detectMultiScale(
            roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(15, 15)
        )

        if len(eyes) >= 1:
            ojos_detectados = True

        for (ex, ey, ew, eh) in eyes:
            max_eye_height = max(max_eye_height, eh)
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255,255,0), 2)

    # ========= ACTUALIZAR HISTORIAL =========
    state = 0 if ojos_detectados else 1
    history.append(state)
    eye_state_history.append(state)

    # ========= CALCULAR PERCLOS =========
    perclos = sum(history) / len(history) if len(history) > 0 else 0

    cv2.putText(frame, f"PERCLOS: {perclos:.2f}", (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

    # ========= EVENTO ACTUAL =========
    estado_actual = "somnolencia" if perclos > PERCLOS_THRESHOLD else "normal"

    # ========= CÁLCULO DE FEATURES PARA ML =========
    frames_totales = len(history)
    frames_cerrados = sum(history)
    frames_abiertos = frames_totales - frames_cerrados
    blink_count = compute_blinks(eye_state_history)
    max_cierre_seg = (max(history) * WINDOW_SECONDS) if 1 in history else 0

    # ========= JSON A ENVIAR =========
    payload = {
        "estado": estado_actual,
        "perclos": round(perclos, 3),
        "frames_cerrados": frames_cerrados,
        "frames_totales": frames_totales,
        "ventana_seg": WINDOW_SECONDS,
        "blink_count": blink_count,
        "max_cierre_seg": max_cierre_seg,
        "timestamp": datetime.now().isoformat(),
        "device": "raspberry-pi4"
    }

    # ========= ENVIAR SOLO SI CAMBIA EL ESTADO =========
    if estado_actual != last_state:
        client.publish(MQTT_TOPIC, json.dumps(payload))
        last_state = estado_actual

    # ========= MOSTRAR EN PANTALLA =========
    if estado_actual == "somnolencia":
        cv2.putText(frame, "ALERTA SOMNOLENCIA", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    else:
        cv2.putText(frame, "ESTADO NORMAL", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("PERCLOS + MQTT + JSON", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
