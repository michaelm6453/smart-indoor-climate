# Smart Indoor Climate Monitoring and Control

A simple IoT system using **Arduino UNO**, **DHT11 sensor**, and a **Raspberry Pi** with MQTT communication.  
The project monitors temperature and humidity and controls two simulated actuators (fan and humidifier) based on live readings. The project is in-progress and will continue in the coming weeks.

---

## Components
- Arduino UNO + DHT11 Sensor  
- Raspberry Pi (Mosquitto Broker)  
- Python Publisher + Subscriber scripts  
- MQTT Topic: `home/climate/data`

---

## Running the System
### On the Raspberry Pi
1. Install dependencies:
   ```
   sudo apt update
   sudo apt install -y python3-pip mosquitto mosquitto-clients
   sudo pip3 install paho-mqtt pyserial
   sudo systemctl enable mosquitto
   sudo systemctl start mosquitto
   ```

2. Run publisher (reads Arduino to MQTT):
   ```
   python3 raspberrypi/publisher.py
   ```

3. In a second terminal, run subscriber (controls GPIO):
    ```
    python3 raspberrypi/subscriber_control.py
    ```
4. Optionally subscribe from another device:
    ```
    mosquitto_sub -t home/climate/data -h <pi_ip>
    ```

---

## Next Steps
- [ ] Add motion sensor to Arduino JSON payload.
- [ ] Add InfluxDB + Grafana for live visualization.
- [ ] Secure MQTT with passwords or TLS.