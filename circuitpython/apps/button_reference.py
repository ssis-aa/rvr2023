# Input button A and B test code
# Button A: GP15
# Button B: GP17

# https://github.com/ssis-aa/rvr2023/blob/main/circuitpython/apps/button_reference.py

import time
import board
import digitalio

buttona = digitalio.DigitalInOut(board.GP15)
buttonb = digitalio.DigitalInOut(board.GP17)

print("Press button A or B")

while True:
    if buttona.value:
        print("You pressed button A")
        time.sleep(0.5)
    if buttonb.value:
        print("You pressed button B")
        time.sleep(0.5)
