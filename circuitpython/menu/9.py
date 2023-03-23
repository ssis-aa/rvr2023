# distance drive_mode

DISTANCE = 20

import board, busio, time
import adafruit_hcsr04              # ultrasonic for distance to be used later
from sphero_rvr2 import RVRDrive

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)    # rp2040
rvr = RVRDrive(uart = busio.UART(board.GP4, board.GP5, baudrate=115200))     # rp2040


time.sleep(0.5)
print("Start ultrasonic distance drive")
rvr.set_all_leds(0,0,255) #set leds to blue
time.sleep(2)

dist = 450
rvr.reset_yaw()
rvr.set_all_leds(0,255,0)

while dist > DISTANCE + 15:
    rvr.setMotors(150,150)
    try:
        dist = sonar.distance
    except RuntimeError:
        print("Retrying!")
    print("(",dist,")")

rvr.set_all_leds(255,255,0)
while dist > DISTANCE:
    rvr.setMotors(100,100)
    try:
        dist = sonar.distance
    except RuntimeError:
        print("Retrying!")
    print("(",dist,")")
    rvr.setMotors(150,150)

rvr.set_all_leds(255,0,0)
start = time.monotonic()
diff = 0

while time.monotonic() - start < 5:
    rvr.setMotors(diff, diff)
    try:
        dist = sonar.distance
    except RuntimeError:
        print("Retrying!")
    diff = 15 * (dist - DISTANCE)
    print("(",dist,")")


rvr.stop()
time.sleep(20)
