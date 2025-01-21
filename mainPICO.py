# PURELY FOR TESTING PURPOSES
# main file for pico side
# Johnny Sarrouf and David Jack Jackson

import pS_PICO_PIP
import dataOutput_PIP
import time

# all of the sensors in a list
# in the order of [tempSensor, voltSensor, dht]
allSensors = dataOutput_PIP.beginSensors()
tempSensorOPC = allSensors[0]
voltSensorOPC = allSensors[1]
tempSensorLaser = allSensors[2]
voltSensorLaser = allSensors[3]
# dht = allSensors[2]

while True:
    pS_PICO_PIP.beginListen()
    
    # JUST FOR TESTING
    #print("voltageOPC, currentOPC, tempOPC, voltageLaser, currentLaser, tempLaser")
    
    # dataOutput_PIP.beginSensing(tempSensor, voltSensor, dht)
    dataOutput_PIP.beginSensing(tempSensorOPC, voltSensorOPC, tempSensorLaser, voltSensorLaser)
    
    time.sleep(1)

