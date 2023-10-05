import spidev
import time

# Define MCP23S17 registers
IODIRB = 0x01  # I/O Direction register for port B
GPIOB = 0x13   # Input/output register for port B
GPPUB = 0x0D   # Pull-Up resistor enable register for port B
GPIOA = 0x12   # Input/output register for port A
IODIRA = 0x00  # I/O Direction register for port A
GPIOA = 0x12   # Input/output register for port A
GPPUA = 0x0C   # Pull-Up resistor enable register for port A
address = 0x42
readAddress = 0x43
# Specify the pin to read
READ_PIN = 0   # Pin B0

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Use SPI bus 0, device 0
spi.max_speed_hz = 1000000  # Set SPI speed (can adjust as needed)

# Enable IOCON HAEN
spi.xfer([0x05, 0x08])
spi.xfer([0x15, 0x08])

# Configure the specified pin as input
spi.xfer2([address, IODIRB, 0xFF])  # Set pin B0 as input

# Enable the pull-up resistor for the specified pin
spi.xfer2([address, GPPUB, 0xFF])  # Enable pull-up for pin B0

# Configure the specified pin as input
spi.xfer2([address, IODIRA, 0xFF])  # Set pin B0 as input

# Enable the pull-up resistor for the specified pin
spi.xfer2([address, GPPUA, 0xFF])  # Enable pull-up for pin B0

# Read the state of the specified pin
def read_pin_state(pin,port,readAddress):
    data = spi.xfer2([readAddress, port,0x00])  # Read port B data
    return (data[2] >> pin) & 1  # Extract the state of the specified pin


if __name__ == "__main__":
    try:
        while True:
            pin_state = read_pin_state(READ_PIN,GPIOB,readAddress)
            
            if pin_state == 1:
                print("Pin is high.")
            else:
                print("Pin is low.")

            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        pass

    # Clean up
    spi.close()
