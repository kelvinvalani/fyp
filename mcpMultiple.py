import spidev
import time

# MCP23S17 Registers
IODIRA = 0x00  # I/O Direction Register A
GPPUA = 0x0C   # GPIO Pull-Up Register A
GPIOA = 0x12   # GPIO Port Register A

# Hall Effect Sensor Pin
SENSOR_PIN = 0  # GPA0

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI bus 0, device 0

# Setup MCP23S17
def setup_mcp23s17():
    spi.xfer2([0x40, IODIRA, 0xFF])   # IODIRA = 0xFF (All inputs)
    spi.xfer2([0x40, GPPUA, 0xFF])    # GPPUA = 0xFF (Enable pull-up on all pins)

# Read sensor status
def read_sensor_status():
    response = spi.xfer2([0x41, GPIOA, 0x00])
    return (response[2] >> SENSOR_PIN) & 0x01  # Extract and check the sensor pin's value

if __name__ == "__main__":
    setup_mcp23s17()

    try:
        while True:
            sensor_value = read_sensor_status()
            if sensor_value:
                print("Hall effect sensor detected magnetic field.")
            else:
                print("No magnetic field detected.")
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
