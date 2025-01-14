# PURELY FOR TESTING PURPOSES
# main file for pico side
# Johnny Sarrouf and David Jack Jackson

import pS_PICO_PIP
import dataOutput_PIP
import time

# all of the sensors in a list
# in the order of [tempSensor, voltSensor, dht]
allSensors = dataOutput_PIP.beginSensors()
tempSensor = allSensors[0]
voltSensor = allSensors[1]
dht = allSensors[2]

while True:
    pS_PICO_PIP.beginListen()
    dataOutput_PIP.beginSensing(tempSensor, voltSensor, dht)
    time.sleep(1)

