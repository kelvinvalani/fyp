import RPi.GPIO as GPIO
import time
class LimitSwitch:
    def __init__(self, switch_pin):
        self.triggered = False
        self.pin = switch_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def detect(self):
        if GPIO.input(self.pin) == GPIO.HIGH:
            self.triggered = True
            print("Switch " +str(self.pin) +" is pressed")
        else:
            self.triggered = False
    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    switch1 = LimitSwitch(12)
    switch2 = LimitSwitch(16)

    try:
        while True:
            switch1.detect()
            switch2.detect()
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()