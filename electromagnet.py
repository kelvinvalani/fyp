import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin to which the base of the transistor is connected
electromagnet_pin = 17

# Set up the GPIO pin as an output pin
GPIO.setup(electromagnet_pin, GPIO.OUT)

# Function to turn ON the electromagnet
def turn_on_electromagnet():
    GPIO.output(electromagnet_pin, GPIO.HIGH)
    print("Electromagnet turned ON")

# Function to turn OFF the electromagnet
def turn_off_electromagnet():
    GPIO.output(electromagnet_pin, GPIO.LOW)
    print("Electromagnet turned OFF")

try:
    while True:
        user_input = input("Enter 'on' to turn ON the electromagnet, 'off' to turn OFF, or 'exit' to quit: ")

        if user_input.lower() == 'on':
            turn_on_electromagnet()
        elif user_input.lower() == 'off':
            turn_off_electromagnet()
        elif user_input.lower() == 'exit':
            break
        else:
            print("Invalid input. Please try again.")

except KeyboardInterrupt:
    # Cleanup GPIO on Ctrl+C
    GPIO.cleanup()
