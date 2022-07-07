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
import math

def cal_pressure(pRaw):
    #return 1000*(pCal[0] + (pRaw-vCal[0])*(pCal[1]-pCal[0])/(vCal[1]-vCal[0]))
    return 1000*(pRaw*(pCal[1]-pCal[0])/(vCal[1]-vCal[0]))

def cal_temperature(tRaw):
    return (-tRaw+1.95)*200/1.65 - 50

def cal_force(fRaw):
    return fRaw*fCal[0]/fCal[1]

def mean(vec):
    return sum(vec)/len(vec)

cal_file = open('pressure-calibration.txt','r')
pCal = [float(x) for x in cal_file.readline().split(', ')]
vCal = [float(x) for x in cal_file.readline().split(', ')]
print(pCal, vCal)
cal_file.close()

cal_file = open('thrust-calibration.txt','r')
fCal = [float(x) for x in cal_file.readline().split(', ')]
print(fCal)
cal_file.close()

#plt.ion()
fig = plt.figure(figsize = (16,9))
Pax = fig.add_subplot(131)
Tax = fig.add_subplot(132)
Fax = fig.add_subplot(133)
Pax.set_ylabel('Pressure (Pa)')
Tax.set_ylabel('Temperature (C)')
Fax.set_ylabel('Thrust (N)')
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
fig.show()

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
p_chan = AnalogIn(ads, ADS.P0)
t_chan = AnalogIn(ads, ADS.P1)
hx = HX711(5,6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)
hx.reset()
hx.tare()



i = 0
x, Praw, Traw, Fraw = [], [], [], []
Praw = [0]*50
Traw = [20]*50
Fraw = [0]*50
x = range(1,51)
Pln, = Pax.plot(x,Praw,'b')
Tln, = Tax.plot(x,Traw,'b') 
Fln, = Fax.plot(x,Fraw,'b')

print(type(Pln))

p_tare_list = []

for i in range(20):
    p_tare_list.append(p_chan.voltage)
    time.sleep(0.05)

p_tare = sum(p_tare_list)/len(p_tare_list)

INTERVAL = 0.1
now = time.time()
next = now+INTERVAL
while True:
    now = time.time()
    if now >= next:
        next = next+INTERVAL
        #x.append(i)
        Praw.append(cal_pressure(p_chan.voltage)-p_tare)
        Traw.append(cal_temperature(t_chan.voltage))
        Fraw.append(cal_force(hx.get_weight(1)))

        Praw.pop(0)
        Traw.pop(0)
        Fraw.pop(0)

        print('P: {}, T: {}, F: {}'.format(Praw[-1],Traw[-1], Fraw[-1]))

        Pln.set_ydata(Praw)
        Tln.set_ydata(Traw)
        Fln.set_ydata(Fraw)
        Pax.set_ylim(min(Praw)-0.1*(abs(min(Praw))), max(Praw)+0.1*(abs(max(Praw))))
        Tax.set_ylim(min(Traw)-0.1*(abs(min(Traw))), max(Traw)+0.1*(abs(max(Traw))))
        Fax.set_ylim(min(Fraw)-0.1*(abs(min(Fraw))), max(Fraw)+0.1*(abs(max(Fraw))))
        Pax.set_title('Average: {:0.2f} Pa'.format(mean(Praw[-5:])))
        Tax.set_title('Average: {:0.2f} C'.format(mean(Traw[-5:])))
        Fax.set_title('Average: {:0.2f} N'.format(mean(Fraw[-5:])))
        fig.canvas.draw()
        fig.canvas.flush_events()
        
        # Pax.set_xlim(left=max(0,i-50), right=max(i,50))
        # Tax.set_xlim(left=max(0,i-50), right=max(i,50))
        # Fax.set_xlim(left=max(0,i-50), right=max(i,50))

        # hx.power_down()
        # hx.power_up()
        # time.sleep(0.1)

        i += 1



