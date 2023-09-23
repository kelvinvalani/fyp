
import spidev
import time

class HallEffectBoard:
    def __init__(self,chipAddress):
        # Define MCP23S17 registers
        self.IODIRA = 0x00  # I/O Direction register for port A
        self.GPIOA = 0x12   # Input/output register for port A
        self.GPPUA = 0x0C   # Pull-Up resistor enable register for port A
        self.IODIRB = 0x01  # I/O Direction register for port B
        self.GPIOB = 0x13   # Input/output register for port B
        self.GPPUB = 0x0D   # Pull-Up resistor enable register for port B
        self.CHIP_ADDRESS = chipAddress

        # SPI setup
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Use SPI bus 0, device 0
        self.spi.max_speed_hz = 1000000  # Set SPI speed (can adjust as needed)


        # Configure all pins as inputs
        self.spi.xfer2([self.CHIP_ADDRESS, self.IODIRA, 0xFF])  # Set all pins of port B as input

        # Enable pull-up resistors for all pins
        self.spi.xfer2([self.CHIP_ADDRESS, self.GPPUA, 0xFF])  # Enable pull-up for all pins of port B

        # Configure all pins as inputs
        self.spi.xfer2([self.CHIP_ADDRESS, self.IODIRB, 0xFF])  # Set all pins of port A as input

        # Enable pull-up resistors for all pins
        self.spi.xfer2([self.CHIP_ADDRESS, self.GPPUB, 0xFF])  # Enable pull-up for all pins of port A

    # Read the state of the specified pin
    def read_pin_state(self,pin,port):
        data = self.spi.xfer2([0x41, port, 0x00])  # Read port B data
        return (data[2] >> pin) & 1 # Extract the state of the specified pin

    def read_board(self):
        statesA = []
        statesB = []

        for i in range(0,8):
            statesA.append(self.read_pin_state(i,self.GPIOA))
            statesB.append(self.read_pin_state(i,self.GPIOB))
        return statesA,statesB

if __name__ == "__main__":
    try:
        chessboard = HallEffectBoard(0x30)
        while True:
            chessboardState = []
            statesA,statesB = chessboard.read_board()
            chessboardState.append(statesA)
            chessboardState.append(statesB)
            time.sleep(0.5)
            print("\n")
            print(chessboardState)

            
    except KeyboardInterrupt:
        pass

