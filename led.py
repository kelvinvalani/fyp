from RPiMCP23S17.MCP23S17 import MCP23S17
import time

mcp1 = MCP23S17(bus=0x00, pin_cs=0x00, device_id=0x00)

mcp1.open()


for x in range(0, 16):
    mcp1.setDirection(x, mcp1.DIR_INPUT)
    mcp1.setPullupMode(x,MCP23S17.PULLUP_ENABLED)


try:
    while True:
        # Read the state of the GPIO pin

        sensor_state = mcp1.digitalRead(9)
        print(sensor_state)
        
        if sensor_state == MCP23S17.LEVEL_HIGH:
            print("No magnetic field")
        else:
            print("Magnetic field detected!")
        
        time.sleep(0.5)  # Delay to avoid rapid reading

except KeyboardInterrupt:
    pass

# Clean up GPIO configuration
mcp1.close()