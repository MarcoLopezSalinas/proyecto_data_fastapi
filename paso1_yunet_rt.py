import cv2
import numpy as np

# Cargar modelo YuNet
net = cv2.dnn.readNet("yunet.onnx")

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # Preprocesamiento
    blob = cv2.dnn.blobFromImage(
        frame,
        scalefactor=1.0,
        size=(320, 320),
        mean=(104, 117, 123),
        swapRB=True
    )

    net.setInput(blob)
    detections = net.forward()

    # detections shape: [1, 1, N, 15]
    for det in detections[0][0]:
        confidence = det[2]

        if confidence > 0.6:
            x1 = int(det[3] * w)
            y1 = int(det[4] * h)
            x2 = int(det[5] * w)
            y2 = int(det[6] * h)

            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

    cv2.imshow("YuNet Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
