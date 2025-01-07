# import board
# import busio
# 
# i2c =busio.I2C(scl=board.GP3, sda=board.GP2)
# #i2c.scan()
# 
# i2c.try_lock()
# 
# try:
#     print("scanning i2c bus..")
#     devices = i2c.scan()
#     if devices:
#         print(f"Found {len(devices)} devices(s):")
#         for device in devices:
#             print(f" - Adress: {hex(device)}")
#     else:
#         print("No i2c device found")
# finally:
#     i2c.unlock()

import time
import board
import digitalio
import busio
import adafruit_max31865

# Initialize SPI bus and chip select pin
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=board.GP12)  # Specify SPI pins explicitly
cs = digitalio.DigitalInOut(board.GP13)  # Chip select pin for the MAX31865

# Initialize the sensor
sensor = adafruit_max31865.MAX31865(spi, cs, wires=3, rtd_nominal=100, ref_resistor=430.0)

while True:
    # Read temperature
    temp = sensor.temperature
    print("Temperature: {0:0.3f}C".format(temp))
    time.sleep(1.0)
    

