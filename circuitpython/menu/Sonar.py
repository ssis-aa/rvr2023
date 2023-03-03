# This is my sonar program
# Trigger pin: GP4
# Echo Pin:    GP5

import time
import board
import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)

while True:
    try:
        print("(",sonar.distance,")")
    except RuntimeError:
        print("Retrying!")
    time.sleep(0.2)
