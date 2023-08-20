import RPi.GPIO as GPIO
import time

class ElectromagnetController:
    def __init__(self, relay_pin):
        self.relay_pin = relay_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_pin, GPIO.OUT)
        self.electromagnet_state = False  # Initially turned off
        
    def turn_on(self):
        GPIO.output(self.relay_pin, GPIO.HIGH)
        self.electromagnet_state = True
        print("Relay ON")
        
    def turn_off(self):
        GPIO.output(self.relay_pin, GPIO.LOW)
        self.electromagnet_state = False
        print("Relay OFF")
        
    def toggle(self):
        if self.electromagnet_state:
            self.turn_off()
        else:
            self.turn_on()
        
    def cleanup(self):
        GPIO.cleanup()

try:
    relay_pin = 17
    magnet_controller = ElectromagnetController(relay_pin)
    
    while True:
        user_input = input("Press '1' to toggle the electromagnet, 'q' to quit: ")
        if user_input == '1':
            magnet_controller.toggle()
        elif user_input == 'q':
            break
    
except KeyboardInterrupt:
    pass
finally:
    magnet_controller.cleanup()
