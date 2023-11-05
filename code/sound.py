from listener import *
import board
from pwmio import PWMOut

l=listener()

beeper = PWMOut(board.GP18, variable_frequency=True)
while True:
    v=l.filter(l.step())
    beeper.duty_cycle = 2 ** 15
    try:
        beeper.frequency = abs(int(v[0]*40000))
    except:
        print("error",int(v[0]*40000))
        beeper.frequency = 1

