#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json
from datetime import datetime, timezone

# -------------------------
# Load configuration file
# -------------------------
with open("config.json", "r") as f:
    cfg = json.load(f)

MQTT_CFG = cfg["mqtt"]
INFLUX_CFG = cfg["influx"]

# -------------------------
# MQTT configuration
# -------------------------
BROKER = MQTT_CFG["broker"]
PORT = MQTT_CFG["port"]
TOPIC = MQTT_CFG["topic"]
USERNAME = MQTT_CFG["username"]
PASSWORD = MQTT_CFG["password"]

# -------------------------
# InfluxDB configuration
# -------------------------
INFLUX_HOST = INFLUX_CFG["host"]
INFLUX_PORT = INFLUX_CFG["port"]
INFLUX_DB = INFLUX_CFG["database"]

# Connect to InfluxDB
db = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT)
db.switch_database(INFLUX_DB)
print("Connected to InfluxDB.")

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker.")
    client.subscribe(TOPIC, qos=1)
    print(f"Subscribed to: {TOPIC}")

def on_message(client, userdata, msg):
    try:
        # Parse incoming JSON from MQTT
        payload = json.loads(msg.payload.decode())

        temp = float(payload.get("temp", 0))
        humid = float(payload.get("humid", 0))
        motion = int(payload.get("motion", 0))

        # Use an accurate UTC timestamp
        now = datetime.now(timezone.utc).isoformat()

        # Write a time-series point into InfluxDB
        point = [{
            "measurement": "dht11",
            "time": now,
            "fields": {
                "temp": temp,
                "humid": humid,
                "motion": motion
            }
        }]
        db.write_points(point)

        print(f"Logged → Temp={temp}°C  Humid={humid}%  Motion={motion}  @ {now}")

        # ------------------------
        # Simulated actuator behavior
        # ------------------------
        if temp > 28:
            print("ACTUATOR: Cooling fan ON")
        elif temp < 20:
            print("ACTUATOR: Heater ON")
        else:
            print("ACTUATOR: Temperature stable")

        if humid < 30:
            print("ACTUATOR: Humidifier ON")
        elif humid > 70:
            print("ACTUATOR: Dehumidifier ON")
        else:
            print("ACTUATOR: Humidity normal")

        if motion == 1:
            print("ACTUATOR: Something moved in the room")
        else:
            print("ACTUATOR: No motion detected")

    except Exception as e:
        print("Error processing message:", e)

# -------------------------
# Start MQTT client
# -------------------------
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to MQTT broker at {BROKER}:{PORT} ...")
client.connect(BROKER, PORT, 60)
client.loop_forever()
