from listener import *
from pwmio import PWMOut
import board
l=listener()

# Generate one period of sine wav.
length = 10000

beeper = PWMOut(board.GP18, variable_frequency=True)
for i in range(length):
    v=l.filter(l.step())
    beeper.duty_cycle = 2 ** 15
    print(sine_wave[i])
    try:
        beeper.frequency = abs(int(v[0]*40000))
    except:
        print("error",int(v[0]*40000))
        beeper.frequency = 1

