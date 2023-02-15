import time, board, busio, displayio, digitalio
import adafruit_displayio_sh1106

displayio.release_displays()

ButtonA = digitalio.DigitalInOut(board.GP15)
ButtonB = digitalio.DigitalInOut(board.GP17)

i2c = busio.I2C(board.GP1, board.GP0) # SCL SDA
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_sh1106.SH1106(display_bus, width=128, height=64, colstart=2)

while True:
    if buttonA.value:
        print("A")
        time.sleep(0.5)
    if buttonB.value:
        print("B")
        time.sleep(0.5)
