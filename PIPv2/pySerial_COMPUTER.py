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

#sets up serial on COM9 (where the pico is) and at a BAUD rate of 9600
ser = serial.Serial("COM9", 9600)

while True:
    
    outputTest = input("enter command >> ")
    
    # "\r\n" are required as well as sending the string as a set of bytes
    ser.write(bytes((outputTest + "\r\n"), "utf-8"))
    
    time.sleep(1)