# file name -> pS_COMP_PIP -> python Serial Computer Pico Instrumentality Project

# new build - pico instrumentality project
# transferStuff is just to test whether or not the program is working, otherwise useless
# beginSerial initializes the ser object for serial communication on the pico port, and then returns said object
# beginSend allows commands to be inputted which are then sent to the pico to be interpreted
# pico is the ser object, which will likely be initialized in the main project
# 1 / 9 / 2025

# pySerial on COMPUTER side
# Johnny Sarrouf and David Jack Jackson
# 1 / 8 / 2025
# to emit commands from COMPUTER and send them to PICO
# takes user input, and sends said string to pico
# assumably pico is on COM9 and BAUD rate is 9600
# ALL COMMANDS
# test() - blinks red led - "test"
# laser_on() - turns laser on - "laser_on"
# laser_off() - turns laser off - "laser_off"
# set_current(newCurrent) - sets current to newCurrent double in mA - "set_current 300"
# YOU NEED TO ENTER A SINGULAR SPACE INBETWEEN "set_current" AND THE DESIRED CURRENT

import serial
import time

# for testing
# Function to initialize the serial communication with the Pico
def transferStuff(pico=None):
    if pico != None:
        pico.write(bytes(("test" + "\r\n"), "utf-8"))
    else:
        print("pico not found")

#sets up serial on COM9 (where the pico is) and at a BAUD rate of 9600
def beginSerial():
    ser = serial.Serial("COM9", 9600)
    return ser

# for when the keyboardInturrupt happens
# the laser can be turned off
def pleaseStop(pico=None):
    if pico != None:
        pico.write(bytes(("laser_off" + "\r\n"), "utf-8"))
    else:
        print("pico is none")

# begin command sending sequence, as a def statement
def beginSend(pico=None):
    
    if pico != None: # Check if a Pico serial object is provided
            
        while True:
            
            outputTest = input("enter command >> ")
            if ("stop" in outputTest):
                break
                        
            # "\r\n" are required as well as sending the string as a set of bytes
            pico.write(bytes((outputTest + "\r\n"), "utf-8"))
            time.sleep(1)
    else:
        print("pico not found")
    

