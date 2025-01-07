#!/usr/bin/python
# reads serial input from pico
import serial
import os

#ser = serial.Serial('/dev/ttyACM1')
ser = serial.Serial('COM9', 9600, 8, 'N', 1, timeout=5)

if (os.path.exists("tempData.txt")):
    file = open("tempData.txt", "a")
    file.write("\n")
else:
    file = open("tempData.txt", "w")
    file.write("volt, curr, temp1, temp2, hum%\n")

for i in range(3):
    print(ser.readline())
    file.write(str(ser.readline()) + ", ")
    #file.write("volt, curr, temp1, temp2, hum%")
file.close()
    
    
# try:
#     file = open("data.txt", "a")
#     file.write("nico\n")
#     file.write("was here\n")
#     file.close()
#     print("File written successfully!")
# except OSError as e:
#     print(f"Error: {e}")
