#!/usr/bin/env python3
import serial, json, time
import paho.mqtt.client as mqtt

SERIAL_PORT = "/dev/ttyACM0"
BAUD = 9600
BROKER = "localhost"
TOPIC = "home/climate/data"

# Connect to Arduino via USB
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)

# Connect to local Mosquitto broker
client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print(f"Publishing Arduino data from {SERIAL_PORT} to topic '{TOPIC}'")

try:
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            payload = json.dumps({
                "temp": data.get("temp"),
                "humid": data.get("humid"),
                "ts": int(time.time())
            })
            client.publish(TOPIC, payload)
            print(f"[{time.strftime('%H:%M:%S')}] PUB:", payload)
        except json.JSONDecodeError:
            pass
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopped by user.")
    ser.close()
    client.disconnect()