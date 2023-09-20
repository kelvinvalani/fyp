import spidev
import time

# Define MCP23S17 registers
IODIRB = 0x01  # I/O Direction register for port B
GPIOB = 0x13   # Input/output register for port B
GPPUB = 0x0D   # Pull-Up resistor enable register for port B
GPIOA = 0x12   # Input/output register for port A

# Specify the pin to read
READ_PIN = 0   # Pin B0

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Use SPI bus 0, device 0
spi.max_speed_hz = 1000000  # Set SPI speed (can adjust as needed)

# Configure the specified pin as input
spi.xfer2([0x40, IODIRB, 0x01])  # Set pin B0 as input

# Enable the pull-up resistor for the specified pin
spi.xfer2([0x40, GPPUB, 0x01])  # Enable pull-up for pin B0

# Read the state of the specified pin
def read_pin_state(pin):
    data = spi.xfer2([0x41, GPIOA, 0x00])  # Read port B data
    return (data[2] >> pin) & 1  # Extract the state of the specified pin

def read_pin_stateB(pin):
    data = spi.xfer2([0x41, GPIOB, 0x00])  # Read port B data
    return (data[2] >> pin) & 1  # Extract the state of the specified pin
try:
    while True:
        pin_statea = read_pin_state(READ_PIN)
        
        if pin_statea == 1:
            pass
        else:
            print("A detected")
        
        time.sleep(0.5)


        pin_stateb = read_pin_stateB(READ_PIN)
        
        if pin_stateb == 1:
            pass
        else:
            print("b detected")
        
        time.sleep(0.5)
        
except KeyboardInterrupt:
    pass

# Clean up
spi.close()
