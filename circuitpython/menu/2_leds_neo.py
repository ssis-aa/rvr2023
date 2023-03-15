# LED lightshow Sphero RVR example 2023-03-14
# v0.1 2023-03-03 general test of LED activation to test serial connection
# v0.2 2023-03-04 with text output about what to expect
# v0.3 2023-03-06 short ultrasonic test
# v0.4 2023-03-14 included neopixel led on YD-RP2040 board

#import board, busio, time, neopixel
import board, busio, time
import adafruit_hcsr04             # ultrasonic for distance to be used later
from sphero_rvr import RVRDrive

RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)    # rp2040
rvr = RVRDrive(uart = busio.UART(board.GP4, board.GP5, baudrate=115200))     # rp2040

#rgb = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=False)
#rgb[0] = BLUE
#rgb.show()
time.sleep(0.5)

def leds(color):
    rvr.set_all_leds(color[0], color[1], color[2])
    #rgb[0] = color
    #rgb.show()

print("LEDs on")

for i in range(3):
    leds(RED)
    print("RED")
    time.sleep(1)
    leds(GREEN)
    print("GREEN")
    time.sleep(1)
    leds(BLUE)
    print("BLUE")
    time.sleep(1) #turn off

rvr.set_all_leds(0,0,0) #turn off leds or make them all black

rvr.sensor_start()
print("RVR sensor_start")

dist = 0
for i in range(100):
    try:
        dist = sonar.distance
    except RuntimeError:
        print("Retrying!")
    if dist < 20:
        leds(RED)
    elif dist < 50:
        leds(GREEN)
    else:
        leds(BLUE)
    print("(",dist,")")
    time.sleep(0.1)

#rvr.drive_to_position_si(0, 0, 1, 1)

rvr.update_sensors()

rvr.stop()
print("Done")
