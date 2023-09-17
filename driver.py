from stepper import *
import time
from electromagnet import *
class Driver:
    def __init__(self,location):
        self.gantry = MotorController(motor1_in1=2, motor1_in2=3, motor1_in3=4, motor1_in4=14,motor2_in1=19, motor2_in2=26, motor2_in3=16, motor2_in4=20)
        self.steps_per_square = 50
        self.magnet = ElectromagnetController(17)
        self.location = location
        self.delay = 0.001


    def get_directions(self,start_square, target_square):
        # Define a dictionary to map letters to column indices
        column_map = {chr(ord('A') + i): i for i in range(8)}

        # Parse the start and target squares to extract row and column
        start_column, start_row = column_map[start_square[0]], int(start_square[1])
        target_column, target_row = column_map[target_square[0]], int(target_square[1])

        # Calculate the horizontal and vertical distances in millimeters
        horizontal_distance = abs(target_column - start_column)
        vertical_distance = abs(target_row - start_row)

        # Determine the direction of movement
        horizontal_direction = "right" if target_column > start_column else "left"
        vertical_direction = "up" if target_row > start_row else "down"

        # Return the distance and direction
        return {
            "horizontal_distance": horizontal_distance,
            "vertical_distance": vertical_distance,
            "horizontal_direction": horizontal_direction,
            "vertical_direction": vertical_direction,
        }

    def move_to_square(self,horizontal_distance,vertical_distance,horizontal_direction,vertical_direction):
        horizontal_steps = horizontal_distance*self.steps_per_square
        vertical_steps = vertical_distance*self.steps_per_square

        if vertical_direction == "up":
            self.gantry.move(self.delay, vertical_steps, "forward","forward")
        elif vertical_direction == "down":
            self.gantry.move(self.delay, vertical_steps, "backward","backward")
        else:
            pass

        if horizontal_direction == "right":
            self.gantry.move(self.delay, horizontal_steps, "backward","forward")
        elif horizontal_direction == "left":
            self.gantry.move(self.delay, horizontal_steps,"forward","backward")
        else:
            pass
        time.sleep(2)

    def move_piece(self,start_square,end_square):
        start_square_directions = self.get_directions(self.location,start_square)
        self.move_to_square(start_square_directions["horizontal_distance"],start_square_directions["vertical_distance"],start_square_directions["horizontal_direction"],start_square_directions["vertical_direction"])
        self.location = start_square
        self.magnet.turn_on()

        end_square_directions = self.get_directions(self.location,end_square)
        self.move_to_square(end_square_directions["horizontal_distance"],end_square_directions["vertical_distance"],end_square_directions["horizontal_direction"],end_square_directions["vertical_direction"])

        self.magnet.turn_off()

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":

    try:
        # Create instances for each motor with their respective pins
        driver = Driver("A1")
        driver.move_piece("A1","A2")
        driver.gantry.manual_control()




        time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        driver.cleanup()