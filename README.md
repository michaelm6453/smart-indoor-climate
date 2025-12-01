# Smart Indoor Climate Monitoring and Control

This project is a simple indoor-climate IoT system built using an Arduino UNO, a DHT11 temperature/humidity sensor, a Raspberry Pi as an MQTT publisher, and a Linux VM running InfluxDB + Grafana for visualization. The system reads live sensor data, publishes it through MQTT, logs it into InfluxDB, and displays it in real time on a Grafana dashboard.

Arduino → Pi → MQTT → VM → InfluxDB → Grafana

---

## 1. Project Structure

### Diagram of System
<img width="540" height="1052" alt="Diagram1IoT" src="https://github.com/user-attachments/assets/314b1c1c-fa3d-4d51-9de7-1742c7640d50" />
<br>
### Data Flow
<img width="1681" height="369" alt="EndToEndFlowIoT" src="https://github.com/user-attachments/assets/ecc37d3e-14d1-493d-9cd7-dc1c6ff58262" />

---

## 2. Hardware Used

- Arduino UNO  
- DHT11 temperature & humidity sensor  
- Raspberry Pi (running Mosquitto + serial publisher)
- Ubuntu VM (running InfluxDB + Grafana)

---

## 3. How the System Works

1. The Arduino reads temperature and humidity from the DHT11 sensor.  
2. It sends these readings as JSON over USB serial to the Raspberry Pi.  
3. The Raspberry Pi publishes the JSON readings to MQTT topic  
   **`lab4_sensor_data`**.  
4. The Ubuntu VM subscribes to this topic, parses the data, and writes it into the **climate** InfluxDB database.
5. Grafana reads from InfluxDB and displays a real-time dashboard.

This gives us a complete pipeline:
**Arduino → Raspberry Pi → MQTT → VM → InfluxDB → Grafana**

---

## 4. Running the System

### Raspberry Pi (MQTT Broker + Publisher)

Install everything needed:

```bash
sudo apt update
sudo apt install -y python3-pip mosquitto mosquitto-clients
sudo pip3 install paho-mqtt pyserial
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

Run the publisher script:

```bash
python3 raspberrypi/publisher.py
```

This reads serial data and publishes it to the MQTT topic.

---

### Ubuntu VM (Subscriber + InfluxDB Writer)

Install the InfluxDB Python client:

```bash
sudo apt install -y python3-influxdb
```

Run the subscriber:

```bash
python3 vm/subscriber_control.py
```

This script listens for incoming MQTT data and writes each reading into the climate database under the dht11 measurement.
<img width="808" height="351" alt="actuator and subscriber control" src="https://github.com/user-attachments/assets/b87768f9-76c3-486d-b671-8603efb4ade5" />

---

## 5. Grafana Dashboard

The dashboard instructions and configuration are stored in:

```bash
grafana/current_dashboard.md
```

The dashboard includes:
- Current temperature card
- Current humidity card
- Real-time line graph with thresholds
- Data sourced from InfluxDB (InfluxQL)
<img width="2225" height="596" alt="Grafana Output" src="https://github.com/user-attachments/assets/0cafdbc4-fffd-45dc-b4a5-4ca5dcbafe90" />

---

## 6. Future Additions
- [x] Add motion sensor readings to the Arduino JSON payload
- [x] Add actuators such as a fan or LED controlled by MQTT
- [x] Add Grafana alerts for high temperatures or humidity
- [x] Improve documentation and diagrams
