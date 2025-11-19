#!/usr/bin/env python3
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json
import datetime

# Program to subscribe to sensor data and control topics,
# log sensor readings to InfluxDB, and simulate actuator control.

# MQTT broker (on the Pi)
MQTT_BROKER = "10.0.0.124"
SENSOR_TOPIC = "lab4_sensor_data"
CONTROL_TOPIC = "home/climate/control"

# InfluxDB (on the VM)
INFLUX_HOST = "localhost"
INFLUX_PORT = 8086
INFLUX_DB   = "climate"

# Set up InfluxDB client
db = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT)
db.switch_database(INFLUX_DB)

print("Connected to InfluxDB.")

# Prepare MQTT client up front so we can publish control commands from inside handlers
client = mqtt.Client()

def log_sensor_reading(temp, humid):
    """Write one reading into InfluxDB and print it"""
    now_iso = datetime.datetime.utcnow().isoformat()

    point = [{
        "measurement": "dht11",
        "time": now_iso,
        "fields": {
            "temp": float(temp),
            "humid": float(humid)
        }
    }]

    db.write_points(point)
    print(f"Logged: temp={temp} humid={humid} at {now_iso}")

def apply_rules(temp, humid):
    """Simple automation rules for simulation/demo"""
    # Example rule: temp too high → fan_on
    if temp > 28:
        client.publish(CONTROL_TOPIC, "fan_on")
        print("Rule: temp > 28 → fan_on")

    # Example rule: temp low → fan_off
    elif temp < 26:
        client.publish(CONTROL_TOPIC, "fan_off")
        print("Rule: temp < 26 → fan_off")

def handle_control_command(cmd):
    """Fake actuator behavior for now; replace with GPIO later"""
    print("CONTROL CMD:", cmd)

    if cmd == "fan_on":
        print("Pretend: FAN ON (would drive GPIO here)")
    elif cmd == "fan_off":
        print("Pretend: FAN OFF (would drive GPIO here)")
    elif cmd == "led_on":
        print("Pretend: LED ON")
    elif cmd == "led_off":
        print("Pretend: LED OFF")
    else:
        print("Unknown control command")

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker.")
    client.subscribe(SENSOR_TOPIC)
    client.subscribe(CONTROL_TOPIC)
    print(f"Subscribed to: {SENSOR_TOPIC} and {CONTROL_TOPIC}")

def on_message(client, userdata, msg):
    if msg.topic == SENSOR_TOPIC:
        try:
            data = json.loads(msg.payload.decode())
            temp = float(data["temp"])
            humid = float(data["humid"])

            # Log reading to InfluxDB
            log_sensor_reading(temp, humid)

            # Apply simple automation
            apply_rules(temp, humid)

        except Exception as e:
            print("Error handling sensor message:", e)

    elif msg.topic == CONTROL_TOPIC:
        cmd = msg.payload.decode()
        handle_control_command(cmd)

# Attach callbacks and connect
client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to {MQTT_BROKER} ...")
client.connect(MQTT_BROKER, 1883, 60)

client.loop_forever()