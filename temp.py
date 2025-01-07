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
    
