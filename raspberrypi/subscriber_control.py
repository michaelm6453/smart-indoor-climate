#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json, time

# GPIO pins for simulation (connect LEDs or pins later)
FAN_PIN = 17
HUMIDIFIER_PIN = 27

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.setup(HUMIDIFIER_PIN, GPIO.OUT)
GPIO.output(FAN_PIN, False)
GPIO.output(HUMIDIFIER_PIN, False)

# Current readings
state = {"temp": None, "humid": None}

# Thresholds
TEMP_HIGH = 28.0
HUMID_LOW = 30.0

def control_logic():
    """Decide when to activate fan/humidifier based on readings."""
    t = state["temp"]
    h = state["humid"]

    if t is None or h is None:
        return

    # Temperature control
    if t > TEMP_HIGH:
        GPIO.output(FAN_PIN, True)
        print(f"[{time.strftime('%H:%M:%S')}] [ACTUATOR] FAN ON (Temp: {t:.1f}°C > {TEMP_HIGH}°C)")
    else:
        GPIO.output(FAN_PIN, False)
        print(f"[{time.strftime('%H:%M:%S')}] [ACTUATOR] FAN OFF (Temp: {t:.1f}°C)")

    # Humidity control
    if h < HUMID_LOW:
        GPIO.output(HUMIDIFIER_PIN, True)
        print(f"[{time.strftime('%H:%M:%S')}] [ACTUATOR] HUMIDIFIER ON (Humidity: {h:.1f}% < {HUMID_LOW}%)")
    else:
        GPIO.output(HUMIDIFIER_PIN, False)
        print(f"[{time.strftime('%H:%M:%S')}] [ACTUATOR] HUMIDIFIER OFF (Humidity: {h:.1f}%)")

def on_message(client, userdata, msg):
    """Handle incoming MQTT messages."""
    try:
        payload = json.loads(msg.payload.decode())
        state["temp"] = payload.get("temp")
        state["humid"] = payload.get("humid")
        print(f"[{time.strftime('%H:%M:%S')}] [DATA] Temp: {state['temp']:.1f}°C, Humidity: {state['humid']:.1f}%")
        control_logic()
    except Exception as e:
        print("Message error:", e)

def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("home/climate/data")
    print("Subscriber running... waiting for data.")
    client.loop_forever()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()
