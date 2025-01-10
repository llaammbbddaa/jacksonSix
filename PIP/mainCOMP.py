# PURELY FOR TESTING PURPOSES
# mainCOMP.py file
# main file for computer side
# Johnny Sarrouf and David Jack Jackson
# 1 / 9 / 25

import pS_COMP_PIP
import serialSave_PIP
import time
 
# various setups
pico = pS_COMP_PIP.beginSerial()
file = serialSave_PIP.beginFile()

try:
    
    # while loop is in the pS_COMP_PIP
    # loops until "stop" is inputted
    pS_COMP_PIP.beginSend(pico)
    
    while True:
        
        serialSave_PIP.beginWrite(pico, file)
        time.sleep(1)
 
# if the user inputs something like ctrl + c, then the program will simply stop and NOT crash
# also, it will close the file and turn off the laser, while letting the user know that all is well
except KeyboardInterrupt:
    file.close()
    pS_COMP_PIP.pleaseStop(pico)
    print("program safely exited")
    