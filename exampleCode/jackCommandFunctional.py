import board # type: ignore
import busio # type: ignore
import digitalio # type: ignore
import adafruit_max31865 
import adafruit_ina260
import adafruit_ds3502
import adafruit_bus_device 
import usb_cdc
from time import monotonic, sleep

# Variables for LED flashing
flash_count = 0
led_on = False
last_flash_time = monotonic()
flashing = True
desired_flash_time = 0.25
number_flashes = 6; number_flashes *= 2
number_flashes = int(number_flashes)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

led.value = True
sleep(0.25)

laser_control = digitalio.DigitalInOut(board.GP15)
laser_control.direction = digitalio.Direction.OUTPUT
laser_control.value = True

# Initialize SPI bus
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

# Configure chip select (CS) pin for laser
laser_cs = digitalio.DigitalInOut(board.GP5)
laser_cs.direction = digitalio.Direction.OUTPUT
laser_cs.value = True  # Set CS high to start

# Configure chip select (CS) pin for opc
opc_cs = digitalio.DigitalInOut(board.GP6)
opc_cs.direction = digitalio.Direction.OUTPUT
opc_cs.value = False  # Set CS high to start

# Initialize MAX31865 and INA260 for laser and opc
laser_temp = adafruit_max31865.MAX31865(spi=spi, cs=laser_cs, rtd_nominal=100, ref_resistor=430.0)
opc_temp = adafruit_max31865.MAX31865(spi=spi, cs=opc_cs, rtd_nominal=100, ref_resistor=430.0)

laser_power = adafruit_ina260.INA260(i2c, address=0x40)
opc_power = adafruit_ina260.INA260(i2c, address=0x41)

control_voltage = adafruit_ds3502.DS3502(i2c)

def scan_i2c_addresses(i2c_bus = i2c):
#testing 
    # Wait for the I2C bus to be ready
    while not i2c.try_lock():
        pass

    try:
        # Scan for devices on the I2C bus
        devices = i2c.scan()
        if devices:
            print("I2C addresses found:", [hex(device) for device in devices])
        else:
            print("No I2C devices found")
    finally:
        # Release the I2C bus
        i2c.unlock()

def get_header():
    led.value = True
    print("Laser Power (W), OPC Power (W), Laser Voltage (V), OPC Voltage (V), Laser Current (mA), OPC Current (mA), Laser Temperature (C), OPC Temperature (C)")
    led.value = False

def get_reading():
    led.value = True
    # Read temperature from MAX31865
    temp_laser = laser_temp.temperature
    temp_opc = opc_temp.temperature
    led.value = False
    # Read power from INA260
    power_laser = laser_power.power
    laser_voltage = laser_power.voltage
    laser_current = laser_power.current
    led.value = True
    power_opc = opc_power.power
    opc_voltage = opc_power.voltage
    opc_current = opc_power.current
    led.value = False
    data = f"{power_laser:.2f}, {power_opc:.2f}, {laser_voltage:.2f}, {opc_voltage:.2f}, {laser_current:.2f}, {opc_current:.2f}"
    data = data + f"{temp_laser:.2f}, {temp_opc:.2f}\n"

    led.value = True
    print(data)

    led.value = False
    return data#.split(",")

def flash_led():
    global flash_count, led_on, last_flash_time, flashing
    if flashing:
        current_time = monotonic()
        if current_time - last_flash_time >= desired_flash_time:  # Check if 0.5 seconds have passed
            led_on = flash_count % 2 == 0
            led.value = led_on  # Toggle the LED
            last_flash_time = current_time
            flash_count += 1
            if flash_count >= number_flashes:  # 3 on-off cycles
                flashing = False  # Stop flashing after 3 times
    

# Define your functions that will be called based on the commands
def led_on():
    led.value = True
    print("LED turned ON")  # Print feedback for the PC to read

def led_off():
    led.value = False
    print("LED turned OFF")  # Print feedback for the PC to read
    
def clear_serial_buffer():
    led.value = True
    while usb_cdc.console.in_waiting > 0:
        usb_cdc.console.read()  # Read and discard any data in the buffer
    led.value = False
    
def set_voltage(voltage = 0):
    if voltage < 0 or voltage > 5:
        print("Voltage must be between 0 and 5 V")
        return
    
    else:
        led.value = True
        voltage_wiper = voltage_to_wiper(voltage)
        control_voltage.wiper = voltage_wiper
        calculated_voltage = wiper_to_voltage(control_voltage.wiper)
        print(f"Current wiper value for {voltage}V is {voltage_wiper}. Digital pot set to {control_voltage.wiper}. Calculated value is {calculated_voltage}V")
        #wiper_voltage = wiper_to_voltage(58)
        #print(f"Current voltage for wiper value 127 is {wiper_voltage}V.")
        led.value = False
   
def wiper_to_voltage(wiper_value):
    """
    Convert the DS3502 wiper value to a voltage range from 0V to 5V.
    
    Parameters:
    wiper_value (int): The wiper value (0 to 127).
    
    Returns:
    float: The corresponding voltage (0V to 5V).
    """
    if wiper_value < 0 or wiper_value > 127:
        raise ValueError("Wiper value must be between 0 and 127")
    
    voltage = (5.0 / 127.0) * wiper_value
    return voltage


def voltage_to_wiper(voltage):
    """
    Convert a voltage value (0V to 5V) to the DS3502 wiper value.
    
    Parameters:
    voltage (float): The voltage value (0V to 5V).
    
    Returns:
    int: The corresponding wiper value (0 to 127).
    """
    if voltage < 0 or voltage > 5:
        raise ValueError("Voltage must be between 0 and 5 V")
    
    wiper_value = int((voltage / 5.0) * 127)
    return wiper_value


def listen_for_commands():
    #clear_serial_buffer()  # Clear the buffer at the start
    # flash_led()
    # led_off()
    while True:

        try:
            # Use usb_cdc.console instead of usb_cdc.data
            if usb_cdc.console.in_waiting > 0:
                led.value = True
                led.value = False
                # Read the incoming command
                command = usb_cdc.console.readline().decode('utf-8').strip()
                #print(command)
                if command == "led_on":
                    led_on()
                elif command == "led_off":
                    led_off()
                elif command == "get_reading":
                    get_reading()
                elif command == "flash_led":
                    flash_led()
                elif command == "get_header":
                    get_header()
                    
                elif "set_voltage" in command:
                    voltage = float(command.split(" ")[1])
                    set_voltage(voltage)
                    #print(f"Setting voltage to {voltage} V")
                    
                else:
                    print("Unknown command")
        except Exception as e:
            print(f"Error: {e}")


try:
    # Print the header for the data
    get_header()
    get_reading()
    set_voltage(0)
except Exception as e:
    print(f"Error: {e}")


set_voltage(voltage_to_wiper(0))
laser_control.value = False

# counter = 0
# wiper_max = 127
# while counter <= wiper_max:

#     voltage = get_reading()
#     voltage = voltage.split(",")
#     #print("VOLTAGE IS", voltage)
#     print(f"DS3502 wiper step value: {control_voltage.wiper} - Calculated voltage: {wiper_to_voltage(control_voltage.wiper)}V - Measured voltage: {voltage[3]}V") #Calculated Resistance: {wiper_to_voltage(control_voltage.wiper) / 0.002}\u03A9", )
   
#     counter += 1
    
#     if counter == wiper_max or counter > wiper_max:
#         counter = 0
#         control_voltage.wiper = 0
#     else:
#         control_voltage.wiper += 1
#     sleep(0.1)
    
# Start listening for commands
listen_for_commands()

