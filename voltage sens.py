import board
import busio
import adafruit_ina219
from time import sleep

i2c =busio.I2C(scl=board.GP3, sda=board.GP2)
sensor = adafruit_ina219.INA219(i2c)

while True:
    print("voltage:", sensor.bus_voltage, "volts")
    print("current", sensor.current*1000, "m amps")
    print("power", sensor.power, "watts")
    print("resistance", (sensor.bus_voltage/sensor.current)*1000, "ohm")
    print("\n")
    sleep(1)