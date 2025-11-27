import cv2
import numpy as np

net = cv2.dnn.readNet("yunet.onnx")

import numpy as np
dummy = np.zeros((320, 320, 3), dtype=np.uint8)

blob = cv2.dnn.blobFromImage(dummy, 1.0, (320, 320), (104,117,123), swapRB=True)
net.setInput(blob)
detections = net.forward()

print("Detections type:", type(detections))
print("Detections shape:", np.array(detections).shape)
print("Raw output:", detections)
