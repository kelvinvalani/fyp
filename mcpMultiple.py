import spidev
import time

# Define MCP23S17 registers
IODIRA = 0x00  # I/O Direction register for port A
GPIOA = 0x12   # Input/output register for port A
GPPUA = 0x0C   # Pull-Up resistor enable register for port A
IODIRB = 0x01  # I/O Direction register for port B
GPIOB = 0x13   # Input/output register for port B
GPPUB = 0x0D   # Pull-Up resistor enable register for port B
CHIP_ADDRESS = 0x40
# Specify the pin to read
READ_PIN = 7   # Pin B0

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Use SPI bus 0, device 0
spi.max_speed_hz = 1000000  # Set SPI speed (can adjust as needed)

# Configure all pins as inputs
spi.xfer2([CHIP_ADDRESS, IODIRA, 0xFF])  # Set all pins of port B as input

# Enable pull-up resistors for all pins
spi.xfer2([CHIP_ADDRESS, GPPUA, 0xFF])  # Enable pull-up for all pins of port B

# Configure all pins as inputs
spi.xfer2([CHIP_ADDRESS, IODIRB, 0xFF])  # Set all pins of port A as input

# Enable pull-up resistors for all pins
spi.xfer2([CHIP_ADDRESS, GPPUB, 0xFF])  # Enable pull-up for all pins of port A

# Read the state of the specified pin
def read_pin_state(pin,port,address):
    data = spi.xfer2([0x41, port, 0x00])  # Read port B data
    return (data[2] >> pin) & 1 # Extract the state of the specified pin

def read_board():
    statesA = []
    statesB = []

    for i in range(0,8):
        statesA.append(read_pin_state(i,GPIOA,CHIP_ADDRESS))
        statesB.append(read_pin_state(i,GPIOB,CHIP_ADDRESS))
    return statesA,statesB

try:
    while True:
        statesA,statesB = read_board()
        boardState = [statesA,statesB]
        print(boardState)
        time.sleep(0.5)
        
except KeyboardInterrupt:
    pass

# Clean up
spi.close()
