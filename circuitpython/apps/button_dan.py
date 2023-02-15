import time
import board
import digitalio

buttona = digitalio.DigitalInOut(board.GP15)


buttonb = digitalio.DigitalInOut(board.GP17)

print("Press button A or B")

while True:
    if buttona.value:
        print("You pressed button a!")
        time.sleep(0.5)
    if buttonb.value:
        print("You pressed button b!")
        time.sleep(0.5)
