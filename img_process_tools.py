from ultralytics import YOLO
import cv2
import numpy as np
import base64


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


def on_connect(client, userdata, flags, rc, TOPIC_IMAGE):
    if rc == 0:
        client.subscribe(TOPIC_IMAGE)


def on_message(client, userdata, msg,  model, TOPIC_RESPONSE):
    #start = time.time()
    encoded_image = msg.payload.decode()
    img_data = base64.b64decode(encoded_image)
    np_img = np.frombuffer(img_data, dtype=np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    present = detect_image(model, img)
    #present, image = annotate_image(model, img)
    
    img = cv2.resize(img, (640, 480))  # Change to desired size
    cv2.imshow("Video Stream", img)
    cv2.waitKey(1)  # Prevents freezing

    response = "yes" if present else "no"
    client.publish(TOPIC_RESPONSE, response)


    #end = time.time()
    #print(f"Frame processed in {end - start:.2f} seconds.")

