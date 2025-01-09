# reads serial input from pico
import serial
import os
import datetime
import mpremote

#ser = serial.Serial('/dev/ttyACM1')
ser = serial.Serial('COM9', 9600, 8, 'N', 1, timeout=5)

now = datetime.datetime.now()
formatted_date_time = now.strftime("%m_%d_%Y %I_%M_%S %p")
formatted_date_time = formatted_date_time + ".txt"
if (os.path.exists(formatted_date_time)):
    file = open(formatted_date_time, "a")
    file.write("\n")
else:
    file = open(formatted_date_time, "w")
    file.write("volt V, curr mA, temp1 C, temp2 C, hum%\n")

for i in range(12):
    print(ser.readline().decode("utf-8").strip())
    file.write(str(ser.readline().decode("utf-8").strip()) + "\n")
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
