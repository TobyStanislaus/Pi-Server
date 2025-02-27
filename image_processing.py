import paho.mqtt.client as mqtt
import cv2
import base64
import numpy as np
from img_process_tools import *
import uuid
import os

BROKER_IP = "192.168.0.155"
BROKER_PORT = 1883
TOPIC_IMAGE = "image/stream"
TOPIC_RESPONSE = "response/decision"
CLIENT_ID = f"pc-image-processor-{uuid.uuid4()}"


script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "model", "yolov8n-face.pt")

model = load_model(model_path)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker.")
        client.subscribe(TOPIC_IMAGE)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        #start = time.time()
        encoded_image = msg.payload.decode()
        img_data = base64.b64decode(encoded_image)
        np_img = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if img is None:
            print("Failed to decode image.")
            return
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        present = detect_image(model, img)
        #present, image = annotate_image(model, img)
        
        #image = cv2.resize(image, (640, 480))  # Change to desired size
        
        #cv2.imshow("Video Stream", image)
        #cv2.waitKey(1)  # Prevents freezing

        response = "yes" if present else "no"
        client.publish(TOPIC_RESPONSE, response)


        #end = time.time()
        #print(f"Frame processed in {end - start:.2f} seconds.")

    except Exception as e:
        print(f"Error processing frame: {e}")

client = mqtt.Client(CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_IP, BROKER_PORT)
client.loop_forever()
