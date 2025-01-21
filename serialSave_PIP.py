# Pico Instrumentality Project
# ser / pico object is initialized in mainPICO so no need to do it here, the var name is pico

# Reading Serial Data from Raspberry Pico, and writing said data onto a formatted text file
# Johnny Sarrouf and David Jack Jackson
# 1 / 9 / 2025

# COMPUTER SIDE
# reads serial input from pico
import serial
import os
import datetime

# creates file and whatnot
def beginFile():
    
    # current data
    now = datetime.datetime.now()
    
    #data is formatted for file name
    formatted_date_time = now.strftime("%m_%d_%Y %I_%M_%S %p")
    formatted_date_time = formatted_date_time + ".txt"
    
    # checks if file exists, and if not creates one
    if (os.path.exists(formatted_date_time)):
        file = open(formatted_date_time, "a")
        file.write("\n")
    else:
        file = open(formatted_date_time, "w")
        # if file is brand new, add the formatting stuff
        file.write("volt V, curr mA, temp1 C, temp2 C, hum%\n")
    
    # returns file such that it can be used all around
    return file

# begin writing to text file
def beginWrite(pico=None, file=None):
    
    # if either pico or file arent present, the code doesnt run to ensure that no errors occur
    if pico != None and file != None:
        print(pico.readline().decode("utf-8").strip())
        file.write(str(pico.readline().decode("utf-8").strip()) + "\n")
        
        # to reduce risk of program crashing and losing data
        # force writes data to drive without closing the file entirely
        file.flush()
    else:
        if pico == None:
            print("pico is none")
        else:
            print("file is none")