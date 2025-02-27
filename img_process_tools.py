from ultralytics import YOLO
import cv2
import numpy as np

def load_model(path):
    model = YOLO(path) 
    return model


def detect_image(model, image):
    results = model(image, verbose=False)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, type = result
        if conf>0.5:
            return True

    return False


def annotate_image(model, image):
    results = model(image, verbose=False)[0]
    image = np.array(image)
    present = False
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, class_id = result
        if conf > 0.5:
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            label = f"{class_id}: {conf:.2f}"
            cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            present = True
            
    return present, image


