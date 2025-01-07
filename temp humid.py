import time
import board
import adafruit_dht

# Set up the DHT11 sensor on a GPIO pin (e.g., GP15)
dht = adafruit_dht.DHT11(board.GP15)

while True:
    try:
        # Read temperature and humidity
        temperature = dht.temperature
        humidity = dht.humidity

        print(f"Temp: {temperature:.1f}°C    Humidity: {humidity:.1f}%")
    except RuntimeError as e:
        # Errors happen fairly often with DHT sensors, just retry
        print(f"Error reading sensor: {e}")
    time.sleep(2)  # Delay between readings