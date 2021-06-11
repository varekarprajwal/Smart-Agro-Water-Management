# 🌱 Smart Agro Water Management System

This repository contains the source code and documentation for the **Smart Agro Water Management System**, a B.E. mini-project developed by students of **Sahyadri College of Engineering & Management**.  
The IoT-based system automates irrigation, conserves water, and provides real-time monitoring of soil and environmental conditions.

---

## 📅 Project Duration  
**May 2021 - October 2021**

---

## 👨‍💻 Team Members
- **Prajwal Purushotham Varekar** (4SF18EC069)  
- **Abhishek Hegde** (4SF18EC112)  
- **Vijay Mohan Hosmane** (4SF18EC123)  
- **Keerthan M Shettigar** (4SF18EC041)  

---

## 📖 Abstract  
Modern agriculture relies on **data-driven decision-making** to maximize productivity and sustainability. This project introduces a **smart irrigation system** using the Internet of Things (IoT).  

- The system continuously monitors **soil moisture, temperature, and humidity** in real-time.  
- When the soil moisture drops below a set threshold, a **water pump is automatically activated**.  
- All sensor data is uploaded to a **Firebase Realtime Database** for **remote monitoring**.  
- A local **LCD display** shows live readings and system status.  

✅ Benefits:  
- Conserves water  
- Reduces manual labor  
- Improves crop yield  

---

## 🚀 Key Features
- **Real-time Monitoring** – Soil moisture, temperature, and humidity tracking.  
- **Automated Irrigation** – A 5V relay controls the water pump based on soil conditions.  
- **IoT Cloud Integration** – Data stored in Firebase for remote access.  
- **Local Display** – 16x2 I2C LCD shows live data.  
- **Configurable Settings** – WiFi, Firebase URL, and thresholds in `config.py`.  
- **Low Power** – Built on NodeMCU ESP8266.  

---

## 🛠️ Hardware Components
- NodeMCU ESP8266  
- FC-28 Soil Moisture Sensor  
- DHT11 Temperature & Humidity Sensor  
- 5V Single Channel Relay Module  
- 16x2 I2C LCD Display (PCF8574 controller)  
- 3–6V Mini Water Pump  
- Power Supply (e.g., 18650 battery holder)  
- Jumper Wires  

---

## ⚡ Circuit Diagram
The components are connected as shown in the following diagram:  
*(Add your circuit diagram image here, e.g., `circuit_diagram.png`)*  

## 💻 Software & Setup

This project uses MicroPython.

🔑 Prerequisites
	•	Flash NodeMCU with latest MicroPython firmware
	•	Install required host tools:
```bash
pip install esptool adafruit-ampy
```
## 📚 Required Libraries

Upload these libraries to the NodeMCU root directory:
	•	dht.py → Driver for DHT11/22
	•	urequests.py → For Firebase HTTP requests
	•	i2c_lcd.py → Driver for I2C LCD

⚙️ Installation Steps
	1.	Flash Firmware
```bash
esptool.py --port /dev/ttyUSB0 write_flash 0x00000 esp8266-<version>.bin
```
2.	Configure Settings
Edit config.py with:
	•	WiFi SSID & Password
	•	Firebase project URL
	•	Moisture threshold & pump duration

3.	Upload Files
```bash
ampy --port /dev/ttyUSB0 put main.py
ampy --port /dev/ttyUSB0 put config.py
ampy --port /dev/ttyUSB0 put dht.py
ampy --port /dev/ttyUSB0 put i2c_lcd.py
```
4.	Reset Board
Press the RST button. main.py will run automatically.

## 🔄 How It Works
	1.	Connects to WiFi.
	2.	Reads temperature, humidity, soil moisture.
	3.	Displays data on the LCD screen.
	4.	Sends data to Firebase.
	5.	If soil moisture < threshold → Relay activates pump.
	6.	Pump runs for PUMP_DURATION_SECONDS.
	7.	Waits for READ_INTERVAL_SECONDS before repeating.

## 🌾 Future Improvements
	•	Mobile app for monitoring and control
	•	Solar-powered version for sustainability
	•	Support for multiple crop zones
	•	AI-based irrigation prediction

