# PlantListener
Repo for development of a board that listens to the bioelectricity of plants and logs this data

## Build
You will need a device capable of running CircuiPython. We have used the Raspberry Pi Pico flashed with <a href="https://circuitpython.org/board/raspberry_pi_pico/">circuitpython</a>. We simplified the sd card and audio output by using a <a href="https://thepihut.com/products/maker-pi-pico-base-without-pico">cytron data logger board</a>. 
We make use ot teh CAP118 breakout sensor from Adafruit to provide the capacitive touch.

Further sensors such as humidity, temperature, moister can be added alongside a PCB. 

<img src="assets/pro-jCyufv6l.jpeg" width="30%">