import RPi.GPIO as GPIO
import time
from driver import *
class MotorController:
    def __init__(self, motor1_in1, motor1_in2, motor1_in3, motor1_in4,motor2_in1, motor2_in2, motor2_in3, motor2_in4):
        self.MOTOR1_IN1 = motor1_in1
        self.MOTOR1_IN2 = motor1_in2
        self.MOTOR1_IN3 = motor1_in3
        self.MOTOR1_IN4 = motor1_in4
        self.MOTOR2_IN1 = motor2_in1
        self.MOTOR2_IN2 = motor2_in2
        self.MOTOR2_IN3 = motor2_in3
        self.MOTOR2_IN4 = motor2_in4

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.MOTOR1_IN1, GPIO.OUT)
        GPIO.setup(self.MOTOR1_IN2, GPIO.OUT)
        GPIO.setup(self.MOTOR1_IN3, GPIO.OUT)
        GPIO.setup(self.MOTOR1_IN4, GPIO.OUT)
        GPIO.setup(self.MOTOR2_IN1, GPIO.OUT)
        GPIO.setup(self.MOTOR2_IN2, GPIO.OUT)
        GPIO.setup(self.MOTOR2_IN3, GPIO.OUT)
        GPIO.setup(self.MOTOR2_IN4, GPIO.OUT)
        
        self.sequence = [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]
    
    def set_step(self, motor1_w1, motor1_w2, motor1_w3, motor1_w4,motor2_w1, motor2_w2, motor2_w3, motor2_w4):

        if motor1_w1 != "none":
            GPIO.output(self.MOTOR1_IN1, motor1_w1)
            GPIO.output(self.MOTOR1_IN2, motor1_w2)
            GPIO.output(self.MOTOR1_IN3, motor1_w3)
            GPIO.output(self.MOTOR1_IN4, motor1_w4)

        if motor2_w1 != "none":
            GPIO.output(self.MOTOR2_IN1, motor2_w1)
            GPIO.output(self.MOTOR2_IN2, motor2_w2)
            GPIO.output(self.MOTOR2_IN3, motor2_w3)
            GPIO.output(self.MOTOR2_IN4, motor2_w4)
    
    def move(self, delay, steps, motor1_direction,motor2_direction):
        if motor1_direction == "forward":
            motor1_step_sequence = self.sequence
        elif motor1_direction == "backward":
            motor1_step_sequence = self.sequence[::-1]
        else:
            motor1_step_sequence = []

        if motor2_direction == "forward":
            motor2_step_sequence = self.sequence
        elif motor2_direction == "backward":
            motor2_step_sequence = self.sequence[::-1]
        else:
            motor2_step_sequence = []
        
        if len(motor1_step_sequence)>0 and len(motor2_step_sequence):
            for _ in range(steps):
                for i in range(len(motor1_step_sequence)):
                    self.set_step(*motor1_step_sequence[i],*motor2_step_sequence[i])
                    time.sleep(delay)
        elif len(motor1_step_sequence)>0:
            for _ in range(steps):
                for i in range(len(motor1_step_sequence)):
                    self.set_step(*motor1_step_sequence[i],"none","none","none","none")
                    time.sleep(delay)
        elif len(motor2_step_sequence)>0:
            for _ in range(steps):
                for i in range(len(motor2_step_sequence)):
                    self.set_step("none","none","none","none",*motor2_step_sequence[i])
                    time.sleep(delay)
        else:
            pass


    
    
    def cleanup(self):
        GPIO.cleanup()
if __name__ == "__main__":
    
    try:
        # Create instances for each motor with their respective pins
        gantry = MotorController(motor1_in1=2, motor1_in2=3, motor1_in3=4, motor1_in4=14,motor2_in1=19, motor2_in2=26, motor2_in3=16, motor2_in4=20)

        delay = 0.001
        steps = 100  # Number of steps to move the motor

        # 8cm = 100 steps when moveing in perpendicular

        # 5.67cm = 100 steps when moving diaganol
        
        gantry.move(delay, steps, "forward","forward")    # Move up
        time.sleep(1)
        gantry.move(delay, steps, "backward","backward") # Move down
        time.sleep(1)
        gantry.move(delay, steps, "forward","backward") # Move left
        time.sleep(1)
        gantry.move(delay, steps, "backward","forward") # Move right
        time.sleep(1)
        gantry.move(delay, steps, "forward","none") # move north west
        time.sleep(1)
        gantry.move(delay, steps, "none","forward") # move north east
        time.sleep(1)
        gantry.move(delay, steps, "backward","none") # move south east
        time.sleep(1)
        gantry.move(delay, steps, "none","backward") # move south west

        gantry.move(delay, steps, "none","none") # stationary







        time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        gantry.cleanup()
