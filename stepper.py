import RPi.GPIO as GPIO
import time

# Define the GPIO pins for the L289N driver
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Set the GPIO mode and pins as outputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Define the motor control sequence
# (You may need to adjust the sequence based on your motor and driver wiring)
sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

def set_step(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)

def forward(delay, steps):
    for _ in range(steps):
        for step in sequence:
            set_step(*step)
            time.sleep(delay)

def backward(delay, steps):
    for _ in range(steps):
        for step in reversed(sequence):
            set_step(*step)
            time.sleep(delay)

try:
    # You can adjust the delay and steps according to your motor and requirements
    delay = 0.005
    steps = 200  # Number of steps to move the motor

    # Move the motor forward
    forward(delay, steps)

    # Pause for a moment
    time.sleep(1)

    # Move the motor backward
    backward(delay, steps)

except KeyboardInterrupt:
    pass
finally:
    # Clean up the GPIO on exit
    GPIO.cleanup()
