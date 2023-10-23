import board
import busio
import busio as io
import sdcardio
import storage
from adafruit_cap1188.i2c import CAP1188_I2C
import time
import ulab.numpy as np
from audiomp3 import MP3Decoder
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!
from adafruit_onewire.bus import OneWireBus
import adafruit_ds18x20
class listener:
    def __init__(self):
        #setup sd card
        spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
        cs = board.GP15
        sd = sdcardio.SDCard(spi, cs)
        vfs = storage.VfsFat(sd)
        self.sd=1
        try:
            storage.mount(vfs, '/sd')
            with open("/sd/test.csv", "w") as f:
                f.write("")
            print("SD card found")
        except:
            print("No Sd card")
            self.sd=0
        self.audio = AudioOut(board.GP18)
        #setup bio-listener
        self.bio=1
        self.i2c = busio.I2C(board.GP9, board.GP8)
        try:
            self.cap = CAP1188_I2C(self.i2c)
        except:
            print("No bio-listener")
            self.bio=0
        self.calibrate()
        print("Device setup!")
        #setup temp
        ow_bus = OneWireBus(board.GP5)
        devices = ow_bus.scan()
        for device in devices:
            print("ROM = {} \tFamily = 0x{:02x}".format([hex(i) for i in device.rom], device.family_code))
        self.temp=1
        try:
            self.ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, devices[0])
        except:
            print("No Temperature device")
            self.temp=0
        #bandpass filter
        self.LP=self.step()
        self.HP=self.step()
    def testI2C(self):
        while not self.i2c.try_lock():
            pass
        print("I2C addresses found:",[hex(device_address) for device_address in self.i2c.scan()])
    def step(self):
        vals=np.zeros(8)
        if self.bio:
            t=time.time()
            for i in range(1,9):
                vals[i-1]=self.cap[i].raw_value
        else:
            print("No device for listening")
        return vals
        
    def filter(self,array,alpha=0.1):
        low_pass=(1-alpha)*self.LP +(alpha*array)
        highpass=alpha*self.HP + alpha*(low_pass-self.LP)
        self.LP=low_pass.copy()
        self.HP=highpass.copy()
        return highpass
    def calibrate(self):
        self.cap.recalibrate()
    def soil_temp(self):
        if self.temp:
            return self.ds18b20.temperature
        else:
            print("No device for temperature")
            return 0

l=listener()
#print(l.testI2C())
for i in range(200):
    v=l.filter(l.step())
    print([v[0],v[7],v[5]])
    time.sleep(0.1)
    
#print(dir(l.cap[1]))
