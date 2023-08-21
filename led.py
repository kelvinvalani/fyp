import RPi.GPIO as GPIO
import time
from RPiMCP23S17.MCP23S17 import MCP23S17
import time

mcp = MCP23S17(0,0)
mcp.open()
for x in range(0, 16):
    mcp.setDirection(x, mcp.DIR_INPUT)
    mcp.setPullupMode(x,MCP23S17.PULLUP_ENABLED)
try:
    while True:
        # Read the state of the GPIO pin
        sensor_state = mcp.digitalRead(0)
        
        if sensor_state == MCP23S17.LEVEL_LOW:
            print("No magnetic field")
        else:
            print("Magnetic field detected!")
        
        time.sleep(0.5)  # Delay to avoid rapid reading

except KeyboardInterrupt:
    pass

# Clean up GPIO configuration
GPIO.cleanup()
