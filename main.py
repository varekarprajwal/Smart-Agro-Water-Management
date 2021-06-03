#Smart Agro Water Management System

import time
import network
import urequests
import machine
from machine import Pin, ADC, I2C
from dht import DHT11
# You will need to find and upload a suitable I2C LCD library.
# We'll assume one named 'i2c_lcd' for this example.
from i2c_lcd import I2cLcd
import config # Import settings from the config.py file

# --- Function to connect to WiFi ---
def connect_wifi():
    """Establishes a connection to the WiFi network."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f'Connecting to network {config.WIFI_SSID}...')
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        # Wait for connection
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            print('.', end='')
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print('\nNetwork connected! IP address:', wlan.ifconfig()[0])
        return True
    else:
        print('\nFailed to connect to WiFi.')
        return False

# --- Hardware Initialization ---
print("Initializing hardware components...")
# Analog-to-Digital Converter for soil moisture sensor
soil_adc = ADC(machine.Pin(config.SOIL_MOISTURE_PIN))
soil_adc.atten(ADC.ATTN_11DB) # Set full 3.3V range

# DHT11 temperature and humidity sensor
dht_sensor = DHT11(Pin(config.DHT_PIN))

# Relay to control the water pump
relay = Pin(config.RELAY_PIN, Pin.OUT)
relay.value(1) # Start with pump OFF (1 for high-level trigger relay)

# I2C LCD Display
i2c = I2C(scl=Pin(config.I2C_SCL_PIN), sda=Pin(config.I2C_SDA_PIN))
lcd = I2cLcd(i2c, config.LCD_I2C_ADDR, 2, 16) # 2 rows, 16 columns
lcd.putstr("System Starting...")
time.sleep(2)

# --- Core Functions ---
def get_soil_moisture():
    """Reads sensor and converts raw value to a percentage."""
    raw_value = soil_adc.read()
    # Calibrate these values for your specific sensor and soil
    # 4095 is max reading (very dry), 0 is min (very wet)
    moisture_percent = 100 - (raw_value / 4095 * 100)
    return max(0, min(100, moisture_percent)) # Clamp value between 0-100

def update_firebase(data):
    """Sends a dictionary of sensor data to Firebase."""
    url = f"{config.FIREBASE_URL}/sensor_data.json"
    print(f"Sending data to Firebase: {data}")
    try:
        response = urequests.put(url, json=data)
        response.close()
        print("Firebase update successful.")
    except Exception as e:
        print(f"Error updating Firebase: {e}")

# --- Main Loop ---
if connect_wifi():
    while True:
        try:
            # 1. Read from sensors
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            moisture = get_soil_moisture()

            print(f"Data - Temp: {temp}°C, Humidity: {humidity}%, Moisture: {moisture:.1f}%")

            # 2. Display on LCD
            lcd.clear()
            lcd.putstr(f"T:{temp}C  H:{humidity}%")
            lcd.move_to(0, 1) # Move to the second line
            lcd.putstr(f"Moisture: {moisture:.1f}%")

            # 3. Update Firebase
            sensor_data = {
                "temperature": temp,
                "humidity": humidity,
                "soilMoisture": moisture,
                "lastUpdate": time.time()
            }
            update_firebase(sensor_data)

            # 4. Check irrigation logic
            if moisture < config.MOISTURE_THRESHOLD:
                print(f"Moisture {moisture:.1f}% is below threshold {config.MOISTURE_THRESHOLD}%. Starting pump.")
                lcd.move_to(0, 1)
                lcd.putstr("Watering plant...")
                relay.value(0) # Turn pump ON
                time.sleep(config.PUMP_DURATION_SECONDS)
                relay.value(1) # Turn pump OFF
                print("Pump finished.")
                lcd.move_to(0, 1)
                lcd.putstr("Watering done. ")

            # 5. Wait for the next cycle
            print(f"Waiting for {config.READ_INTERVAL_SECONDS} seconds...")
            time.sleep(config.READ_INTERVAL_SECONDS)

        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
            lcd.clear()
            lcd.putstr("An error occurred!")
            time.sleep(10) # Wait before retrying
else:
    lcd.clear()
    lcd.putstr("WiFi Failed.")
    print("Could not connect to WiFi. Halting.")
