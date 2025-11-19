#!/usr/bin/env python3
import serial
import time
import json
import paho.mqtt.client as mqtt

SERIAL_PORT = "/dev/ttyACM0"
BAUD = 9600

# Pi is running the MQTT broker locally
BROKER = "localhost"
TOPIC = "lab4_sensor_data"

# Open serial connection to Arduino (JSON lines from DHT11)
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)

# MQTT client setup
client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print(f"Publishing Arduino JSON data from {SERIAL_PORT} to topic '{TOPIC}'")

try:
    while True:
        raw = ser.readline().decode(errors="ignore").strip()
        if not raw:
            continue

        # Try to parse JSON from Arduino, e.g. {"temp":27.6,"humid":33.0}
        try:
            data = json.loads(raw)

            if "temp" in data and "humid" in data:
                payload = json.dumps(data)
                client.publish(TOPIC, payload)
                print("PUB:", payload)

        except json.JSONDecodeError:
            # Ignore partial or malformed lines
            pass

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopped by user.")
    ser.close()
    client.disconnect()
