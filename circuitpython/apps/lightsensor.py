# read the light sensor

import board, analogio, time

lightsensor = analogio.AnalogIn(board.A5)

while True:
    print(lightsensor.value())
    sleep(1)
