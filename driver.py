import math
from stepper import *
import time
from electromagnet import *
class Driver:
    def __init__(self,location):
        self.gantry = MotorController(motor1_in1=2, motor1_in2=3, motor1_in3=4, motor1_in4=14,motor2_in1=19, motor2_in2=26, motor2_in3=16, motor2_in4=20)
        self.steps_per_square = 50
        self.steps_per_cm = 13
        self.magnet = ElectromagnetController(13)
        self.location = location
        self.delay = 0.001


    def get_directions(self,start_square, target_square):
        # Define a dictionary to map letters to column indices
        column_map = {chr(ord('A') + i): i for i in range(12)}

        # Parse the start and target squares to extract row and column
        start_column, start_row = column_map[start_square[0]], int(start_square[1])
        target_column, target_row = column_map[target_square[0]], int(target_square[1])

        # Calculate the horizontal and vertical distances in millimeters
        horizontal_distance = abs(target_column - start_column)
        vertical_distance = abs(target_row - start_row)

        # Determine the direction of movement
        
        if target_column > start_column:
            horizontal_direction = "right"
        elif target_column < start_column:
            horizontal_direction = "left"
        else:
            horizontal_direction = None

        if target_row > start_row:
            vertical_direction = "up"
        elif target_row < start_row:
            vertical_direction = "down"
        else:
            vertical_direction = None

        # Return the distance and direction
        return {
            "horizontal_distance": horizontal_distance,
            "vertical_distance": vertical_distance,
            "horizontal_direction": horizontal_direction,
            "vertical_direction": vertical_direction,
        }

    def move_to_square(self,start_square_directions,current,dest):


        horizontal_distance,vertical_distance,horizontal_direction,vertical_direction = start_square_directions["horizontal_distance"],start_square_directions["vertical_distance"],start_square_directions["horizontal_direction"],start_square_directions["vertical_direction"]
        horizontal_steps = horizontal_distance*self.steps_per_square
        vertical_steps = vertical_distance*self.steps_per_square

        if vertical_steps != 0:
            if current[0] == 'L':
                #move left
                self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"forward","backward")
            else:
                #move right
                self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"backward","forward")

            #move vertically
            if vertical_direction == "up":
                self.gantry.move(self.delay, vertical_steps, "forward","forward")
            else:
                self.gantry.move(self.delay, vertical_steps, "backward","backward")

            if horizontal_direction == None:

                if current[0] == 'L':
                    #move right to slot
                    self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"backward","forward")
                else:
                    #move left tp slot
                    self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"forward","backward")
            else:

                if dest[1] == '8':
                    #move down
                    self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"backward","backward")
                else:
                    #move up
                    self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"forward","forward")

                if current[0] == 'L':
                    #move right to slot
                    self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"backward","forward")
                else:
                    #move left tp slot
                    self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"forward","backward")



        if horizontal_steps != 0:

            if vertical_direction == None:
                if dest[1] == '8':
                    #move down
                    self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"backward","backward")
                else:
                    #move up
                    self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"forward","forward")

            if horizontal_direction == "left":
                self.gantry.move(self.delay, horizontal_steps, "forward","backward")
            else:
                self.gantry.move(self.delay, horizontal_steps, "backward","forward")

            if dest[1] == '8':
                #move up slot
                self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"forward","forward")
            else:
                #move down slot
                self.gantry.move(self.delay, math.ceil(self.steps_per_square/2),"backward","backward")


        time.sleep(2)

    def move_piece(self,start_square,end_square):

        start_square_directions = self.get_directions(self.location,start_square)
        self.move_to_square(start_square_directions,self.location,start_square)
     
        self.location = start_square
        self.magnet.turn_on()



        end_square_directions = self.get_directions(self.location,end_square)
        self.move_to_square(end_square_directions,self.location,end_square)


        self.magnet.turn_off()
        self.location = end_square

    def manual_control(self):
        direction = input("Enter a direction (up, down, left, right)")
        distance = float(input("Enter distance in cm"))
        user_input = input("Press '1' to toggle the electromagnet, 'q' to quit: ")

        if user_input == '1':
            self.magnet.toggle()

        steps = math.ceil(distance*self.steps_per_cm)


        if direction == "up":
            self.gantry.move(self.delay, steps, "forward","forward")
        elif direction == "down":
            self.gantry.move(self.delay, steps, "backward","backward")
        else:
            pass

        if direction == "right":
            self.gantry.move(self.delay, steps, "backward","forward")
        elif direction == "left":
            self.gantry.move(self.delay, steps,"forward","backward")
        else:
            pass

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":

    try:
        # Create instances for each motor with their respective pins

        driver = Driver("A1")
        choice = input("1 for manual 2 for test")
        if choice == "1":
            while True:
                driver.manual_control()
        else:
            driver.move_piece("L8","L4")
            driver.move_piece("A4","A1")


    except KeyboardInterrupt:
        pass
    finally:
        driver.cleanup()