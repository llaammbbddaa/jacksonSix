# Pico Instrumentality Project

# PICO SIDE
# data collection on pico side
# AS OF NOW there is one temp / hum sensor, one voltage / current sensor, and one temp sensor
# in the end there will be two of each sensor, with the excepetion of the temp / hum sensor

import time
import board
import digitalio
import busio
import adafruit_max31865
import adafruit_ina260
#import adafruit_dht

def beginSensors():

    # Initialize SPI bus and chip select pin (for temperature)
    spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)  # Specify SPI pins explicitly
    csOPC = digitalio.DigitalInOut(board.GP6)  # Chip select pin for the MAX31865
    csLASER = digitalio.DigitalInOut(board.GP5)
    tempSensorOPC = adafruit_max31865.MAX31865(spi, csOPC, wires=3, rtd_nominal=100, ref_resistor=430.0) #initialize sensor
    tempSensorLaser = adafruit_max31865.MAX31865(spi, csLASER, wires=3, rtd_nominal=100, ref_resistor=430.0) #initialize sensor

    # initialize i2c stuff and whatnot (for voltage and current)
    i2c =busio.I2C(scl=board.GP1, sda=board.GP0)
    voltSensorOPC = adafruit_ina260.INA260(i2c, address=0x41)
    voltSensorLaser = adafruit_ina260.INA260(i2c, address=0x40)

    # humidity sensor here
    # dht = adafruit_dht.DHT11(board.GP15)
    
    # return [tempSensor, voltSensor, dht]
    return [tempSensorOPC, voltSensorOPC, tempSensorLaser, voltSensorLaser]


# def beginSensing(tempSensor=None, voltSensor=None, dht=None):
def beginSensing(tempSensorOPC=None, voltSensorOPC=None, tempSensorLaser=None, voltSensorLaser=None):
    
    # if (tempSensor is not None and voltSensor is not None and dht is not None):
    if (tempSensorOPC is not None and voltSensorOPC is not None and tempSensorLaser is not None and voltSensorLaser is not None):   
       # read data, and simplify output by defining variables
        tempOPC = tempSensorOPC.temperature # in C
        voltageOPC = voltSensorOPC.voltage # in V
        currentOPC = voltSensorOPC.current # in mA
        tempLaser = tempSensorLaser.temperature # in C
        voltageLaser = voltSensorLaser.voltage # in V
        currentLaser = voltSensorLaser.current # in mA
        #temp2 = dht.temperature
        #hum = dht.humidity
        
        # print(str(voltage) + ", " + str(current) + ", " + str(temp1) + ", " + str(temp2) + ", " + str(hum))
        print(str(voltageOPC) + ", " + str(currentOPC) + ", " + str(tempOPC) + ", " + str(voltageLaser) + ", " + str(currentLaser) + ", " + str(tempLaser))
    else:
        print("something is wrong with one of the sensors")