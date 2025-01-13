import board
import busio
import adafruit_ina219
from time import sleep

# Initialize I2C communication on the specified pins (SCL and SDA)
i2c =busio.I2C(scl=board.GP3, sda=board.GP2)
# Create an instance of the INA219 sensor to read voltage, current, and power data
sensor = adafruit_ina219.INA219(i2c)

# Infinite loop to continuously read and print data from the sensor
while True:
    # Read and print the bus voltage in volts
    print("voltage:", sensor.bus_voltage, "volts")
    # Read and print the current in milliamps (mA), sensor returns value in amps
    print("current", sensor.current*1000, "m amps")
    # Read and print the power in watts
    print("power", sensor.power, "watts")
    # Calculate and print the resistance in ohms (Ohm's Law: R = V / I)
    # Multiply the current by 1000 to convert from amps to milliamps
    print("resistance", (sensor.bus_voltage/sensor.current)*1000, "ohm")
    print("\n")
    sleep(1)
