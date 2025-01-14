import time
import board
import digitalio
import busio
import adafruit_max31865

# SPI setup
spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=board.GP12)
cs = digitalio.DigitalInOut(board.GP13)  # Chip select

# MAX31865 configuration for PT100 and 3-wire RTD
sensor = adafruit_max31865.MAX31865(spi, cs, wires=3, rtd_nominal=100, ref_resistor=430.0)

while True:
    try:
        # Read temperature
        temp = sensor.temperature
        print("Temperature: {:.3f} °C".format(temp))
        
        # Check for faults
        fault = sensor.fault
        if fault:
            print("Fault detected:", fault)
            sensor.clear_faults()
        
        time.sleep(2.0)
    except Exception as e:
        print("Error:", e)
        time.sleep(1.0)
