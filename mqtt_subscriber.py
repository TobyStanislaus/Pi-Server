import paho.mqtt.client as mqtt
import subprocess
import os

# MQTT Configuration
BROKER = "192.168.0.155"  # Change this to your MQTT broker's IP
TOPIC = "run/script"

# Path to your Python script
SCRIPT_PATH = r"C:\Users\toby\OneDrive\Documents\Github\Pi-Server\image_processing.py"

def on_message(client, userdata, message):
    try:
        script = message.payload.decode("utf-8")  # Decode the message
        #print(f"Received request to run: {script}")

        # Ensure the correct script is being executed
        if script == "image_processing.py":
            result = subprocess.run(["python", SCRIPT_PATH], capture_output=True, text=True, shell=True)

            # Print output and errors
            print("Output:", result.stdout)
            print("Error:", result.stderr)
        else:
            print("Unknown script requested.")
    except Exception as e:
        print(f"Error running script: {e}")

# Set up MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to MQTT broker
client.connect(BROKER, 1883, 60)

# Subscribe to the topic
client.subscribe(TOPIC)
print(f"Subscribed to topic: {TOPIC}")

# Keep listening
client.loop_forever()
