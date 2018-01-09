#for extensometer
#send data from 3 timestamps every 30 mins

from xbee import XBee, ZigBee
import serial
from time import sleep
import re
from datetime import datetime as dt
from ConfigParser import SafeConfigParser
from struct import *
import sys
import time
import MySQLdb



results=open('/home/pi/Server/results.txt')
resline=results.readlines()
#print resline

PORT = '/dev/xbeeusbport'
#PORT='COM3'
BAUD_RATE = 9600

#DEST_ADDR_LONG = "\x00\x13\xa2\x00\x40\xf6\x2f\x8a"
DEST_ADDR_LONG = "\x00\x00\x00\x00\x00\x00\x00\x00"

'''
a=resline[-3]
b=resline[-2]
c=resline[-1]

lag = a[0:-1]+b[0:-1]+c[0:-1]
'''

lastData=resline[-1]
print lastData

ser = serial.Serial(PORT, BAUD_RATE)
xbee = ZigBee(ser,escaped=True)

xbee.send("tx",data=lastData,dest_addr_long=DEST_ADDR_LONG,dest_addr="\xff\xfe")	
resp = xbee.wait_read_frame()
print resp

ser.close()



