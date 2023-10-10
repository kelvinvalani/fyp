import RPi.GPIO as GPIO
import time
class LimitSwitch:
    def __init__(self, switch_pin = None):
        self.triggered = False
        self.pin = switch_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def detect(self):
        if GPIO.input(self.pin) == GPIO.HIGH:
            self.triggered = True
            print("Switch pressed")
        else:
            self.triggered = False

if __name__ == "__main__":
    siwtch = LimitSwitch(0.1, switch_pin=10)
    while True:
        siwtch.detect()
        time.sleep(0.1)