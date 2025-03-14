# file name -> pS_PICO_PIP -> python Serial Pico Pico Instrumentality Project

# new build - pico instrumentality project
# this build is still incomplete as the laser is not ready for testing or implementation
# fortunately, the def statements are for the most part explained
# 1 / 9 / 2025

# pySerial on PICO side
# Johnny Sarrouf and David Jack Jackson
# 1 / 8 / 2025
# to receive commands from pc and respond accordingly
# commands are functions that are defined here
# to control the laser system, laser_on and laser_off
# as well as collecting data, get_readings
# assumably pico is on COM9 and BAUD rate is 9600
# ideally you would save this to the pico's code.py file such that it can run on its own
# ALL COMMANDS
# test() - blinks red led - "test"
# laser_on() - turns laser on - "laser_on"
# laser_off() - turns laser off - "laser_off"
# set_current(newCurrent) - sets current to newCurrent double in mA - "set_current 300"

import board
import busio
import digitalio
import usb_cdc
import time

#initialize led on PIN1 or GP0
red = digitalio.DigitalInOut(board.GP0)
red.direction = digitalio.Direction.OUTPUT

# Function to blink the LED as a basic functionality test
def test():
    red.value = True
    time.sleep(1)
    red.value = False
    time.sleep(1)

# Placeholder function for turning the laser on
def laser_on():
    print("laser_on")

def laser_off():
    print("laser_off")
    
def set_current(nC):
    print("set_current")
    for i in range(nC):
        test()

# Placeholder function for collecting readings
def get_readings():
    print("get_readings") # Print feedback to indicate data collection

# continually listens to serial for commands
def beginListen():
    try:
        # Use usb_cdc.console instead of usb_cdc.data
        if usb_cdc.console.in_waiting > 0:
            
            # Read the incoming command
            # because its from serial, it is required that we clean it up a bit for use
            command = usb_cdc.console.readline().decode('utf-8').strip()
            
            if command == "test":
                test()
            elif ("laser_on" in command):
                laser_on()
            elif ("laser_off" in command):
                laser_off()
            elif ("set_current" in command):
                newCurrent = float(command[command.index(" "):])
                set_current(newCurrent)
            elif ("get_readings" in command):
                get_readings()
            else:
                print("Unknown command")
                
        # meant to test for proper connection - delete later
#         else:
#             test()
    except Exception as e:
        print(f"Error: {e}")
        

