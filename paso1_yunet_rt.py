import cv2
import numpy as np

net = cv2.dnn.readNetFromONNX("yunet.onnx")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    blob = cv2.dnn.blobFromImage(frame, 1.0, (320, 320))
    net.setInput(blob)
    out = net.forward()

    for det in out[0]:
        conf = det[2]
        if conf > 0.6:  # confianza mínima
            x1 = int(det[3] * w)
            y1 = int(det[4] * h)
            x2 = int(det[5] * w)
            y2 = int(det[6] * h)

            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

    cv2.imshow("YuNet - Face Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
