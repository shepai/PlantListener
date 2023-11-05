from listener import *
import board
from pwmio import PWMOut

l=listener()

beeper = PWMOut(board.GP18, variable_frequency=True)
while True:
    v=l.filter(l.step())
    beeper.duty_cycle = 2 ** 15
    freq=((int(v[0]*40000)) +  (int(v[4]*40000)))//2 +1000
    print(freq)
    try:
        beeper.frequency = freq
    except:
        print("error",freq)
        beeper.frequency = 1

