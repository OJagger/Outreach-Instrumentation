#!/usr/bin/python3
from re import I
import board
import busio
import time
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
from hx711 import HX711
from multiprocessing import Process, Pipe

fig = plt.figure(figsize = (16,9))
Pax = fig.add_subplot(131)
Tax = fig.add_subplot(132)
Fax = fig.add_subplot(133)
Pax.title.set_text('Pressure')
Tax.title.set_text('Temperature')
Fax.title.set_text('Thrust')
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
fig.show()


pltconn, daqconn = Pipe(duplex=True)


def get_readings(hx711, adc, conn):
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    p_chan = AnalogIn(ads, ADS.P0)
    t_chan = AnalogIn(ads, ADS.P1)
    hx = HX711(5,6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(1)
    hx.reset()
    hx.tare()
    conn.send(1)
    try:
        while True:
        
    


i = 0
x, Praw, Traw, Fraw = [], [], [], []

INTERVAL = 0.1
now = time.time()
next = now+INTERVAL
while True:
    now = time.time()
    if now >= next:
        next = next+INTERVAL
        x.append(i)
        Praw.append(p_chan.voltage)
        Traw.append(t_chan.voltage)
        Fraw.append(hx.get_weight(5))

        print('P: {}, T: {}, F: {}'.format(Praw[-1],Traw[-1], Fraw[-1]))

        Pax.plot(x,Praw,'b')
        Tax.plot(x,Traw,'b') 
        Fax.plot(x,Fraw,'b')
        Pax.set_xlim(left=max(0,i-50), right=max(i,50))
        Tax.set_xlim(left=max(0,i-50), right=max(i,50))
        Fax.set_xlim(left=max(0,i-50), right=max(i,50))

        fig.canvas.draw()

        # hx.power_down()
        # hx.power_up()
        # time.sleep(0.1)

        i += 1



