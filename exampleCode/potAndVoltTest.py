# potAndVoltTest.py
# to test the functionality of the digital potentiometer
# as well as to display the voltage through the ina260

# Mimi and  Johnny Sarrouf
# 1 / 15 / 2025

import time
import board
import adafruit_ds3502
import adafruit_ina260
from analogio import AnalogIn
import busio

def mapVolt(voltage):
    ratio = 25.4
    return int(voltage * ratio)

# example initialization for ina219 for reference
# initialize i2c stuff and whatnot (for voltage and current)
# i2c = busio.I2C(scl=board.GP17, sda=board.GP16)
# voltSensor = adafruit_ina219.INA219(i2c)

# initialize potentiometer and volt/curr sensor
i2cPot = busio.I2C(scl=board.GP17, sda=board.GP16)
ds3502 = adafruit_ds3502.DS3502(i2cPot)
i2cSense = busio.I2C(scl=board.GP17, sda=board.GP16)
ina260 = adafruit_ina260.INA260(i2c)

while True:
    
    # takes input 
    tempVolt = input("enter voltage (0 -> 5)")
    inputVoltage = mapVolt(tempVolt)
    ds3502.wiper = inputVoltage

    # outputs wiper data
    print("Current:", ina260.current)
    print("Voltage:", ina260.voltage)
    print("Power:", ina260.power)
    
    time.sleep(1)

