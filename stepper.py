import RPi.GPIO as GPIO
import time

class MotorController:
    def __init__(self, in1, in2, in3, in4):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        
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
    
    def set_step(self, w1, w2, w3, w4):
        GPIO.output(self.IN1, w1)
        GPIO.output(self.IN2, w2)
        GPIO.output(self.IN3, w3)
        GPIO.output(self.IN4, w4)
    
    def move(self, delay, steps, direction):
        if direction == "forward":
            step_sequence = self.sequence
        elif direction == "backward":
            step_sequence = reversed(self.sequence)
        else:
            raise ValueError("Invalid direction")
        
        for _ in range(steps):
            for step in step_sequence:
                self.set_step(*step)
                time.sleep(delay)
    
    
    def cleanup(self):
        GPIO.cleanup()

try:
    # Create instances for each motor with their respective pins
    motor1 = MotorController(in1=17, in2=18, in3=27, in4=22)
    motor2 = MotorController(in1=23, in2=24, in3=25, in4=26)

    delay = 0.005
    steps = 150  # Number of steps to move the motor

    # Move the motors forward
    motor1.move(delay, steps, "forward")
    motor2.move(delay, steps, "forward")

    time.sleep(1)

    # Move the motors backward
    motor1.move(delay, steps, "backward")
    motor2.move(delay, steps, "backward")

    time.sleep(1)

    # Move the motors backward
    motor1.move(delay, steps, "forward")
    motor2.move(delay, steps, "backward")

    time.sleep(1)

    # Move the motors backward
    motor1.move(delay, steps, "backward")
    motor2.move(delay, steps, "forward")

    time.sleep(1)

    # Move the motors backward
    motor1.move(delay, steps, "forward")

    time.sleep(1)

    motor1.move(delay, steps, "backward")

    time.sleep(1)
    
    motor1.move(delay, steps, "forward")

    time.sleep(1)
    motor2.move(delay, steps, "backward")
except KeyboardInterrupt:
    pass
finally:
    motor1.cleanup()
    motor2.cleanup()
