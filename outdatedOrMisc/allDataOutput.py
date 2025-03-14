import time
import board
import digitalio
import busio
import adafruit_max31865
import adafruit_ina219
import adafruit_dht

# Initialize SPI bus and chip select pin (for temperature)
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=board.GP12)  # Specify SPI pins explicitly
cs = digitalio.DigitalInOut(board.GP13)  # Chip select pin for the MAX31865
tempSensor = adafruit_max31865.MAX31865(spi, cs, wires=3, rtd_nominal=100, ref_resistor=430.0) #initialize sensor

# initialize i2c stuff and whatnot (for voltage and current)
i2c =busio.I2C(scl=board.GP17, sda=board.GP16)
voltSensor = adafruit_ina219.INA219(i2c)

# humidity sensor here
dht = adafruit_dht.DHT11(board.GP15)


while True:
    
    # read data, and simplify output by defining variables
    temp1 = tempSensor.temperature # in C
    voltage = voltSensor.bus_voltage # in V
    current = (voltSensor.current) # in mA
    temp2 = dht.temperature
    hum = dht.humidity
    
    print(str(voltage) + ", " + str(current) + ", " + str(temp1) + ", " + str(temp2) + ", " + str(hum))

    time.sleep(1.0)


