import paho.mqtt.client as mqtt
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


client = mqtt.Client(CLIENT_ID)
client.on_connect = lambda c, u, f, r: on_connect(c, u, f, r, TOPIC_IMAGE)
client.on_message = lambda c, u, m: on_message(c, u, m, model, TOPIC_RESPONSE)

client.connect(BROKER_IP, BROKER_PORT)
client.loop_forever()
