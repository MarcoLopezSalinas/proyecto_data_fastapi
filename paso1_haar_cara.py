import cv2

# 1. Cargar el modelo PRE-ENTRENADO de cara (Haar Cascade)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# 2. Inicializar la cámara
cap = cv2.VideoCapture(0)  # si no funciona, prueba con 1

# Opcional: bajar resolución para que vaya suave
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer de la cámara")
        break

    # Pasar a escala de grises (el modelo Haar trabaja así)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 3. Detectar caras con el modelo entrenado
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,   # cuánto se reduce la imagen en cada escala
        minNeighbors=5,    # cuántos vecinos necesita para confirmar
        minSize=(80, 80)   # tamaño mínimo de cara
    )

    # 4. Dibujar rectángulos en las caras detectadas
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostrar el frame
    cv2.imshow("Paso 1 - Cara con Haar", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

