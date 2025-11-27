import cv2

# ===== MODELOS PREENTRENADOS =====
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml"
)

# ===== CÁMARA =====
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer de la cámara")
        break

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
        # Dibujar cara
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        # Recortar ROI de la cara
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # === 2. DETECTAR OJOS ===
        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(20, 20)
        )

        if len(eyes) >= 1:
            ojos_detectados = True

        # Dibujar ojos detectados
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255,255,0), 2)

        break  # solo usamos la primera cara

    # === 3. TEXTO EN PANTALLA ===
    if ojos_detectados:
        cv2.putText(frame, "OJOS DETECTADOS", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    else:
        cv2.putText(frame, "OJOS NO DETECTADOS", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    # === MOSTRAR VIDEO ===
    cv2.imshow("Paso 2 - Cara + Ojos", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
