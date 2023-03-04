# LED lightshow Sphero RVR example 2023-03-04
# v0.1 2023-03-03 general test of LED activation to test serial connection
# v0.2 2023-03-04 with text output about what to expect

import board, busio, time

import adafruit_hcsr04             # ultrasonic for distance to be used later
from sphero_rvr import RVRDrive

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)    # rp2040

rvr = RVRDrive(uart = busio.UART(board.GP4, board.GP5, baudrate=115200))     # rp2040

# CODE BELOW THIS LINE WILL WORK FOR ANY BOARD ****************************************

time.sleep(0.5)

print("LEDs on")

for i in range(5):
    rvr.set_all_leds(255,0,0) #set leds to red
    print("RED")
    time.sleep(1)
    rvr.set_all_leds(0,255,0) #set leds to green
    print("GREEN")
    time.sleep(1)
    rvr.set_all_leds(0,0,255) #set leds to blue
    print("BLUE")
    time.sleep(1) #turn off

rvr.set_all_leds(0,0,0) #turn off leds or make them all black


#print("starting up")

rvr.sensor_start()
print("RVR sensor_start")

time.sleep(10)
#rvr.drive_to_position_si(0, 0, 1, 1)

rvr.update_sensors()

rvr.stop()
print("Done")
