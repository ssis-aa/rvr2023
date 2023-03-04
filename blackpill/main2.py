# sonar example 2022-02-21
import board, busio, time, math, digitalio, adafruit_hcsr04
from ssis_rvr   import pin
from sphero_rvr import RVRDrive

rvr   = RVRDrive(uart = busio.UART(pin.TX, pin.RX, baudrate=115200))
sonar = adafruit_hcsr04.HCSR04(trigger_pin=pin.TRIGGER, echo_pin=pin.ECHO)

# ******************************************************************************

time.sleep(0.2)
rvr.set_all_leds(255,0,0) #set leds to red
time.sleep(0.2)

rvr.sensor_start()
print("starting up")
rvr.set_all_leds(0,255,0) #set leds to green
time.sleep(0.2)
setpoint = 40.0
MAX_SPEED = 100

rvr.update_sensors()
rvr.set_all_leds(255,255,255) #turn off leds or make them all white
time.sleep(0.2)

sensor_distance = sonar.distance
error = 0
tolerance = 3
k = 2
start_time = time.monotonic()
elapsed_time = time.monotonic() - start_time

def checkSonar():
    try:
        sensor_distance = sonar.distance
        print(sensor_distance)
        if sensor_distance < 10 :
            rvr.set_all_leds(255,0,0)
        else:
            rvr.set_all_leds(0,255,0)
        time.sleep(0.1)
        rvr.set_all_leds(0,0,0)
        time.sleep(sensor_distance / 200)

    except RuntimeError:
        print("Retrying!")
        rvr.set_all_leds(0,0,255) #set leds to blue
        pass
    time.sleep(0.2)

rvr.set_all_leds(255,255,255) #turn off leds or make them all white
time.sleep(0.2)

while(elapsed_time < 6.0):

    checkSonar()

    #rvr.setMotors(MAX_SPEED, MAX_SPEED)

    elapsed_time = time.monotonic() - start_time

    try:
        sensor_distance = sonar.distance

        # Add your proportional control code here.
        error = sensor_distance - setpoint
        output = error*k


        rvr.setMotors(output, output) #set the power of the motors for both the left and right track
            # Read the Sphero RVR library file to find the rvr.setMotors(left,right) command.
            # Use this command in the next line to send the output of your proportional
            # control to both the left and right motors.

    except RuntimeError:
        print("Retrying!")
        pass
    time.sleep(0.2)


rvr.stop()
