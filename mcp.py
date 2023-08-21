import spidev
import time

# Define MCP23S17 registers
GPIOB = 0x13   # Input/output register for port B

# Specify the pin to check
CHECK_PIN = 0  # Pin B0

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 1)  # Use SPI bus 0, device 0
spi.max_speed_hz = 1000000  # Set SPI speed (can adjust as needed)

# Read the state of the specified pin
def read_pin_state(pin):
    data = spi.xfer2([0x41, GPIOB, 0x00])  # Read port B data
    print(data)
    return (data[2] >> pin) & 1  # Extract the state of the specified pin

try:
    while True:
        pin_state = read_pin_state(CHECK_PIN)
        
        # if pin_state == 1:
        #     print("Pin is high.")
        # else:
        #     print("Pin is low.")
        
        time.sleep(0.5)
        
except KeyboardInterrupt:
    pass

# Clean up
spi.close()
