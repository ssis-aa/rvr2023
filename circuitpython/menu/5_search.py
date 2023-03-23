# drive a square drive_mode

DISTANCE = 25
TIMEOUT  = 7
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
WHITE = (255, 255, 255)

import board, busio, time
import adafruit_hcsr04              # ultrasonic for distance to be used later
from   sphero_rvr import RVRDrive

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)    # rp2040
rvr = RVRDrive(uart = busio.UART(board.GP4, board.GP5, baudrate=115200))     # rp2040
rgb = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=False)
rgb[0] = BLUE
rgb.show()

def leds(color):
    rvr.set_all_leds(color[0], color[1], color[2])
    rgb[0] = color
    rgb.show()

time.sleep(0.5)
print("Start square drive")
leds(BLUE) #set leds to blue
time.sleep(2)

colors = [RED, GREEN, BLUE]
pattern = [[90, 0.0, 0.3], [180, 0.3, 0.3], [ 270, 0.3, 0.0], [  0, 0.0, 0.0],
           [90, 0.4, 0.4], [ 0, 0.6, 0.4], [180, 0.6, 1.2]]
for i, point in enumerate(pattern):
    leds(colors[i%3])
    print(f"Drive to {pattern[i][0]}, {pattern[i][1]}")
    rvr.drive_to_position_si(pattern[i][0],pattern[i][1], pattern[i][2], 100)
    time.sleep(5)

rvr.drive_to_position_si(0, 0,   0.6, 100)
time.sleep(5)
rvr.drive_to_position_si(0, 0.6, 0.6, 100)
time.sleep(5)
rvr.drive_to_position_si(0, 0.6, 0  , 100)
time.sleep(5)
rvr.drive_to_position_si(0, 0,   0,   100)
time.sleep(5)

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

leds(WHITE)
while dist > DISTANCE:
    rvr.setMotors(100,100)
    try:
        dist = sonar.distance
    except RuntimeError:
        print("Retrying!")
    print("(",dist,")")
    rvr.setMotors(150,150)

leds(BLUE)
start = time.monotonic()
diff = 0

while time.monotonic() - start < TIMEOUT:
    rvr.setMotors(diff, diff)
    try:
        dist = sonar.distance
    except RuntimeError:
        print("Retrying!")
    diff = 12 * (dist - DISTANCE)
    if diff > 0:
        leds(GREEN)
    else:
        leds(RED)
    print("(",dist,")")


rvr.stop()
time.sleep(20)
