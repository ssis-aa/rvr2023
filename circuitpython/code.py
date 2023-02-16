# Input button A and B test code
# Button A: GP15
# Button B: GP17

# start screen menu.py
# 2023/02/16



import time, os, sys
import board, displayio, terminalio, digitalio, busio
import adafruit_displayio_sh1106
from adafruit_debouncer import Debouncer
from adafruit_display_text import label


DISPLAY_ROWS = 5
color_menu   = 0xFFFFFF
color_select = 0x00FF55
long_press   = 0.5          # time in seconds for long press to start program

pin = digitalio.DigitalInOut(board.GP15)    # boot switch - choose and select
pin.direction = digitalio.Direction.INPUT
switch = Debouncer(pin, interval=0.05)

programs = os.listdir('apps')              # folder for programs
programs.sort()
number_programs = len(programs)            # number of installed programs


displayio.release_displays()
i2c = busio.I2C(board.GP1, board.GP0) # SCL SDA
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_sh1106.SH1106(display_bus, width=128, height=64, colstart=2)

menu = []                                  # first menu item:
menu.append("Menu/Settings [{} programs]".format(number_programs))
menu.append("REPL")                        # second menu item

for x in programs:
    menu.append(x[:-3])                    # remove the .py from program files

#font = bitmap_font.load_font("fonts/Helvetica-Bold-16.bdf")
#font = bitmap_font.load_font("fonts/SourceSerifPro-15.bdf")
#font = bitmap_font.load_font("fonts/SourceSansPro-15.pcf")

mainmenu = displayio.Group()
select = 0

def menu_create():
  for item in range(DISPLAY_ROWS):
    listitem = label.Label(terminalio.FONT, text="tbd", color=color_menu)
    listitem.x = 0
    listitem.y = 7 + 15 * item
    mainmenu.append(listitem)

def menu_fill(s):
  for item in range(DISPLAY_ROWS-1,-1,-1):
    mainmenu[item].text = menu[item + s]

def menu_select(x):
  mainmenu[x].color = color_select
  if (x == 0):
    x = DISPLAY_ROWS - 1
  else:
    x -= 1
  mainmenu[x].color = color_menu

# setup
menu_create()
menu_fill(0)
menu_select(0)
display.show(mainmenu)
pressed = time.monotonic()


while True:
  switch.update()
  if switch.fell:    # button pressed
    pressed = time.monotonic()
  if switch.rose:    # button released
    time_pressed = time.monotonic() - pressed
    if time_pressed > long_press:
      if select < 2:
        sys.exit()
      program = "apps/" + programs[select - 2]
      # displayio.release_displays() # return to REPL output - tbd
      pin.deinit()
      exec(open(program).read())
    select += 1
    if (select > number_programs + 1):
      select = 0
      menu_fill(0)
    if (select > DISPLAY_ROWS - 1):
      menu_fill(select - DISPLAY_ROWS + 1)
    else:
      menu_select(select)

#exec(open("apps/bouncy_balls1.py").read())
