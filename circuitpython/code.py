# Start menu for microcontroller with OLED display v0.4
# https://github.com/ssis-aa/rvr2023/blob/main/circuitpython/code.py
# 2023/02/23
# Button A: GP15 (left  - select)
# Button B: GP17 (right - confirm)

import time, os, sys
import board, displayio, terminalio, digitalio, busio
import adafruit_displayio_sh1106
from adafruit_debouncer    import Debouncer
from adafruit_display_text import label

DISPLAY_ROWS = 6
color_menu   = 0xFFFFFF
color_select = 0x000000   # 0x00FF55
long_press   = 0.5        # time in seconds for long press to start program

pin_select            = digitalio.DigitalInOut(board.GP15)
pin_select.direction  = digitalio.Direction.INPUT
switchA               = Debouncer(pin_select, interval=0.05)
pin_confirm           = digitalio.DigitalInOut(board.GP17)
pin_confirm.direction = digitalio.Direction.INPUT
switchB               = Debouncer(pin_confirm, interval=0.05)

programs = os.listdir("menu")  # folder for programs
programs.sort()
number_programs = len(programs)  # number of installed programs

displayio.release_displays()
i2c = busio.I2C(board.GP1, board.GP0)  # SCL SDA
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_sh1106.SH1106(
    display_bus, width=128, height=64, colstart=2
)

menu = []  # first menu item:
menu.append("Menu/Settings [{}]".format(number_programs))

for i, x in enumerate(programs):
    if x[:2] == "._":
        programs[i] = programs[i][2:]
        x = x[2:]
    menu.append(x[:-3])  # remove the .py from program files

mainmenu = displayio.Group()
select   = 0                  # item select on the list shown


def menu_create():
    for item in range(DISPLAY_ROWS):
        listitem = label.Label(terminalio.FONT, text="tbd")
        listitem.x = 0
        listitem.y = 4 + 11 * item
        mainmenu.append(listitem)


def menu_fill(s):
    for item in range(DISPLAY_ROWS - 1, -1, -1):
        mainmenu[item].text = menu[item + s]


def menu_select(x):
    mainmenu[x].color = color_select
    mainmenu[x].background_color = 0xFFFFFF
    if x == 0:
        x = DISPLAY_ROWS - 1
    else:
        x -= 1
    mainmenu[x].color = 0xFFFFFF
    mainmenu[x].background_color = 0x000000


# setup
menu_create()
menu_fill(0)
menu_select(0)
display.show(mainmenu)
pressed = time.monotonic()


while True:
    switchA.update()
    switchB.update()
    if switchA.rose:  # button pressed
        pressed = time.monotonic()
    if switchA.fell:  # button released
        time_pressed = time.monotonic() - pressed
        if time_pressed > long_press:  # alternative to press button B
            if select < 2:
                sys.exit()
            program = "menu/" + programs[select - 2]
            # displayio.release_displays() # return to REPL output - tbd
            pin_select.deinit()
            pin_confirm.deinit()
            exec(open(program).read())
            break
        select += 1
        if select > number_programs + 1:
            select = 0
            menu_fill(0)
        if select > DISPLAY_ROWS - 1:
            menu_fill(select - DISPLAY_ROWS + 1)
        else:
            menu_select(select)
    if switchB.fell:
        if select < 2:
            sys.exit()
        program = "menu/" + programs[select - 2]
        print("Selected: ", program)
        display.show(None)
        pin_select.deinit()
        pin_confirm.deinit()
        exec(open(program).read())
        break
