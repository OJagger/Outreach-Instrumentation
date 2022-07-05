#!/usr/bin/python3
from re import I
import board
import busio
import time
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
# import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from hx711 import HX711

# fig = plt.figure(figsize = (16,9))
# Pax = fig.add_subplot(131)
# Tax = fig.add_subplot(132)
# Fax = fig.add_subplot(133)
# Pax.title.set_text('Pressure')
# Tax.title.set_text('Temperature')
# Fax.title.set_text('Thrust')
# mng = plt.get_current_fig_manager()
# mng.full_screen_toggle()
# fig.show()

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
p_chan = AnalogIn(ads, ADS.P0)
t_chan = AnalogIn(ads, ADS.P1)
hx = HX711(5,6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)
hx.reset()
hx.tare()

f = open("PT_calibration.txt", "w")


i = 0
x, Praw, Traw, Fraw = [], [], [], []

INTERVAL = 0.02
now = time.time()
last = now-1
next = now+INTERVAL
while True:
    #last = now
    now = time.time()
    #dt = now- last
    if now >= next:
        dt = now-last
        next = now+INTERVAL
        last = now
        x.append(i)
        Praw.append(p_chan.voltage)
        Traw.append(t_chan.voltage)
        Fraw.append(hx.get_weight(1))

        print('P: {}, T: {}, freq: {}'.format(Praw[-1],Traw[-1], 1/dt))

        f.write('{}, {}\n'.format(Praw[-1],Traw[-1]))

        
#        Pax.plot(x,Praw,'b')
#        Tax.plot(x,Traw,'b') 
#        Fax.plot(x,Fraw,'b')
#        Pax.set_xlim(left=max(0,i-50), right=max(i,50))
#        Tax.set_xlim(left=max(0,i-50), right=max(i,50))
#        Fax.set_xlim(left=max(0,i-50), right=max(i,50))
#
#        fig.canvas.draw()

        # hx.power_down()
        # hx.power_up()
        # time.sleep(0.1)

        i += 1



