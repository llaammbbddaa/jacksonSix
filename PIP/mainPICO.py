# PURELY FOR TESTING PURPOSES
# main file for pico side
# Johnny Sarrouf and David Jack Jackson

import pS_PICO_PIP
import dataOutput_PIP
import time

# all of the sensors in a list
# in the order of [tempSensor, voltSensor, dht]
allSensors = dataOutput_PIP.beginSensors()
tempSensor = allSensors[0]# MAX31865 temperature sensor
voltSensor = allSensors[1]# INA219 voltage/current sensor
dht = allSensors[2] # DHT11 temperature/humidity sensor

# Infinite loop for continuous operation
while True:
    # Listen for commands sent to the Pico (e.g., over serial)
    pS_PICO_PIP.beginListen()
    # Collect and print data from sensors
    dataOutput_PIP.beginSensing(tempSensor, voltSensor, dht)
    time.sleep(1)

