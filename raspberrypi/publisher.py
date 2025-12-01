#!/usr/bin/env python3
import serial
import json
import time
import paho.mqtt.client as mqtt

# USB connection to Arduino
SERIAL_PORT = "/dev/ttyACM0"
BAUD = 9600

# MQTT broker running on the Pi
BROKER = "localhost"
TOPIC = "iot_final_project"

# Open serial port
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)

# MQTT client with username/password auth
client = mqtt.Client()
client.username_pw_set("student", "iot123")
client.connect(BROKER, 1883, 60)

print(f"Publishing sensor data on '{TOPIC}'")

while True:
    raw = ser.readline().decode(errors="ignore").strip()
    if not raw:
        continue

    try:
        # JSON coming from Arduino
        data = json.loads(raw)

        # QoS0 since we are submitting lots of sensor data and can afford to lose some
        client.publish(TOPIC, json.dumps(data), qos=0)
        print("PUB:", data)

    except json.JSONDecodeError:
        # Ignore incomplete lines
        pass

    time.sleep(0.1)
