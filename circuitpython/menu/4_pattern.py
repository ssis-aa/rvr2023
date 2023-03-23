# drive a square drive_mode
# if your rp2040 has no NEOPIXEL uncomment line 19, 22, 23

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
rgb = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=False)
def leds(color):
    rvr.set_all_leds(color[0], color[1], color[2])
    rgb[0] = color
    rgb.show()

leds(RED)
time.sleep(0.5)
print("Start square drive")
leds(BLUE) #set leds to blue
time.sleep(2)

rvr.reset_yaw()

pattern = [[270, 0.0, 0.3], [180, 0.3, 0.3], [ 90, 0.3, 0.0], [  0, 0.0, 0.0],
           [270, 0.4, 0.4], [  0, 0.6, 0.4], [180, 0.6, 1.2], [270, 0.0, 0.6],
           [180, 0.6, 0.6], [ 90, 0.6, 0.0], [  0, 0.0, 0.0]]

for i, point in enumerate(pattern):
    leds(colors[i%3])
    print(f"Drive to {pattern[i][0]}, {pattern[i][1]}")
    rvr.drive_to_position_si(pattern[i][0],pattern[i][1], pattern[i][2], 100)
    time.sleep(3)

leds(BLACK)
time.sleep(2)
for i in range(21):
    leds(colors[i%3])
    time.sleep(0.1)

print("Pattern finished")
leds(BLACK)
rvr.stop()
time.sleep(20)
