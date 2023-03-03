# LED lightshow Sphero RVR example 2023-03-03

import board, busio, time

import adafruit_hcsr04
from sphero_rvr import RVRDrive

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP7)    # M4 Metro express

rvr = RVRDrive(uart = busio.UART(board.GP4, board.GP5, baudrate=115200))       # M4 Metro express

# CODE BELOW THIS LINE WILL WORK FOR ANY BOARD ********************************************

time.sleep(0.5)

print("LEDs on")

for i in range(10):
    rvr.set_all_leds(255,0,0) #set leds to red
    time.sleep(0.5)
    rvr.set_all_leds(0,255,0) #set leds to green
    time.sleep(0.5)
    rvr.set_all_leds(0,0,255) #set leds to blue
    time.sleep(0.5) #turn off
    rvr.set_all_leds(255,255,255) #turn off leds or make them all black


#print("starting up")

rvr.sensor_start()
print("sensor_start")

time.sleep(10)
#rvr.drive_to_position_si(0, 0, 1, 1)

rvr.update_sensors()

rvr.stop()
print("Done")
