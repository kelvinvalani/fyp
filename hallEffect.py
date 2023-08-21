import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the sensor's OUT pin
hall_sensor_pin = 17

# Set up the GPIO pin as input with internal pull-up resistor
GPIO.setup(hall_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # Read the state of the GPIO pin
        sensor_state = GPIO.input(hall_sensor_pin)
        
        if sensor_state == GPIO.HIGH:
            print("No magnetic field")
        else:
            print("Magnetic field detected!")
        
        time.sleep(0.5)  # Delay to avoid rapid reading

except KeyboardInterrupt:
    pass

# Clean up GPIO configuration
GPIO.cleanup()
