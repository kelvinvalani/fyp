import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the relay
relay_pin = 17

# Initialize the relay pin as an output pin
GPIO.setup(relay_pin, GPIO.OUT)

def turn_on_relay():
    GPIO.output(relay_pin, GPIO.HIGH)
    print("Relay ON")

def turn_off_relay():
    GPIO.output(relay_pin, GPIO.LOW)
    print("Relay OFF")

try:
    while True:
        turn_on_relay()
        time.sleep(20)  # Electromagnet ON for 2 seconds
        turn_off_relay()
        time.sleep(2)  # Electromagnet OFF for 2 seconds

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
