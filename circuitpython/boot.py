# Start rp2040 and initiate the OLED display, execute the menu.py
# https://github.com/ssis-aa/rvr2023/blob/main/circuitpython/boot.py
# 2023/02/23 v0.3

import time, board, busio, displayio
import adafruit_displayio_sh1106

displayio.release_displays()

i2c = busio.I2C(board.GP1, board.GP0) # SCL SDA
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_sh1106.SH1106(display_bus, width=128, height=64, colstart=2)

print("Display activated.")
# exec(open("apps/menu.py").read())
# does not work
