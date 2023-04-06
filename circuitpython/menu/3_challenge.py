# drive for the RVR Challenge 2023
# if your rp2040 has no NEOPIXEL write False below
HAVE_NEOPIXEL = True

DISTANCE = 25
TIMEOUT  = 7
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
WHITE = (255, 255, 255)
colors = [RED, GREEN, BLUE]

import board, busio, time
import adafruit_hcsr04              # ultrasonic for distance to be used later
from   sphero_rvr import RVRDrive

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)    # rp2040
rvr = RVRDrive(uart = busio.UART(board.GP4, board.GP5, baudrate=115200))     # rp2040
if HAVE_NEOPIXEL:
    rgb = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=False)
def leds(color):
    rvr.set_all_leds(color[0], color[1], color[2])
    if HAVE_NEOPIXEL:
        rgb[0] = color
        rgb.show()

leds(RED)
time.sleep(0.5)
print("Competition 2023")
leds(BLUE) #set leds to blue
time.sleep(2)

rvr.reset_yaw()

# The pattern array has 4 values: direction, x-coordinate, y-coordinate, seconds to execute
# As directions: 0 is forward, 270 is right, 180 is backward and 90 is left. coordinates in meters.
pattern = [[270, 0.0, 2.1, 6.5], [180, 1.1, 2.1, 3.5], [ 90, 1.0, 2.1, 2.8],
           [  0, 1.0, 2.0, 2.5], ]

for i, point in enumerate(pattern):
    leds(colors[i%3])
    print(f"Drive to {pattern[i][0]}, {pattern[i][1]}")
    rvr.drive_to_position_si(pattern[i][0],pattern[i][1], pattern[i][2], 100)
    time.sleep(pattern[i][3])

leds(BLACK)
time.sleep(2)
for i in range(21):
    leds(colors[i%3])
    time.sleep(0.1)
print("Pattern finished")
leds(BLACK)
rvr.stop()
time.sleep(20)
