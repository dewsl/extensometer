#! /usr/bin/python
#this version saves data on text file
#flexi number of sensors

from xbee import XBee, ZigBee
import serial
from time import sleep
import re
from datetime import datetime as dt
from ConfigParser import SafeConfigParser
from struct import *
import sys
from readtable import *
import time
import MySQLdb

sys.path.insert(0, '/home/pi/Server/')
config = SafeConfigParser()
config.read(sys.path[0]+ '/' + 'config.txt')

PORT = config.get('port', 'xb')
#PORT='COM3'
BAUD_RATE = 9600

DEST_ADDR_LONG = "\x00\x00\x00\x00\x00\x00\xff\xff"
gatename=config.options('gname')
#print gatename
#print routername

numconfig = SafeConfigParser()
numconfig.read(sys.path[0] + '/' + 'rpi-server-config.txt')

servernum = numconfig.get('gsmio','server')
setname = numconfig.get('coordinfo','name')

import pprint
rss=["","","",""]
parDB=0
rssdate=0
startTime=0


sys.path.insert(0, '/home/pi/rpiserver/')
import senslopedbio
import senslopeServer

def getRssi():
	ser = serial.Serial(PORT, BAUD_RATE)
	xbee = ZigBee(ser,escaped=True)
	
	global sc
	global rss
	
	i=0
	for data in routerdata:
		
		xbee.remote_at(							#remote_at RSSI
			dest_addr_long=data[2], 			
			command="DB", 
			frame_id="A")
		
		response=xbee.wait_read_frame()
		stat=response['status']
		stat=ord(stat)
		
		if stat is 0:
			parDB = response['parameter']
			parDB = ord(parDB)
			print data[0].upper(),"is alive. RSS is -",parDB,"dBm"
			data[3] = ","+data[0].upper()+","+str(ord(response['parameter']))
			data[3] = data[3].upper()
			data[3] = re.sub('[^A-Zbcxy0-9\,]',"",data[3])
		else:
			print "Can't connect to", data[0].upper()
			data[3] = ","+data[0].upper()+",,"
			data[3] = re.sub('[^A-Zbcxy0-9\,]',"",data[3])

		i=i+1
	
	ser.close()
	return


def wakeup():
	ser = serial.Serial(PORT, BAUD_RATE)
	xbee = ZigBee(ser,escaped=True)

	xbee.send("tx",data="Wake up and get data\n",dest_addr_long=DEST_ADDR_LONG,dest_addr="\xff\xfe")
	resp = xbee.wait_read_frame()
	print "Wake up"
	
	ser.close()
	return

	
def receive():
	ser = serial.Serial(PORT, BAUD_RATE)
	xbee = ZigBee(ser,escaped=True)
	
	paddr=""
	i=0
	sfin=[]
	fin=[]
	
	
	while True:
		try: 
			print "waiting"
			response = xbee.wait_read_frame()
			#print response
			rf = response['rf_data']
			print rf 
			rf=str(rf)
			datalen=len(rf)
			
			paddr = ""
			paddr = paddr + hex(int(ord(response['source_addr_long'][4])))
			paddr = paddr + hex(int(ord(response['source_addr_long'][5])))
			paddr = paddr + hex(int(ord(response['source_addr_long'][6])))
			paddr = paddr + hex(int(ord(response['source_addr_long'][7])))
			
			hashStart=rf.find('#')
			
			slashStart=rf.find("/")
			
			#pag may voltage na pinadala
			if rf.find('VOLTAGE') is not -1:
				for data in routerdata:
					if paddr in data:
						volt=rf[hashStart+1:-1]
						volt= re.sub('[^.0-9\*]',"",volt)
						print ">>Voltage from",data[0]
						data[3]=data[3]+","+volt
						print data[3]
						
					
			else:
				for data in routerdata:
					if paddr in data:
						if rf[slashStart+1] == rf[slashStart-1]:
							sfin.append(data[0])
						msg=rf[hashStart+1:-1]
						msg=re.sub('[^A-Zxyabc0-9\*]',"",msg)
						#data[-1]=data[-1]+msg
						if msg.find("ERROR") is not -1:
							msg=msg.replace("ERROR","NODATAPARSED")
						if rf.find("<") is not -1:
							if len(msg)+len(data[-1]) < 160:
								data[-1]=data[-1]+msg
								print data[-1]
								data[-1] = data[-1].replace(gatename[0].upper(),setname)
								senslopeServer.WriteOutboxMessageToDb(data[-1],servernum)
								data[-1]=""
								if data[0] in sfin:
									fin.append(data[0])
							else:
								print data[-1]
								data[-1] = data[-1].replace(gatename[0].upper(),setname)
								senslopeServer.WriteOutboxMessageToDb(data[-1],servernum)
								data[-1]=""
								data[-1]=msg
								senslopeServer.WriteOutboxMessageToDb(data[-1],servernum)
								data[-1]=""
						elif rf.find(">") is not -1:
							if len(data[-1]) is 0:
								data[-1]=msg
							elif len(data[-1]) <160:
								data[-1] = data[-1].replace(gatename[0].upper(),setname)
								senslopeServer.WriteOutboxMessageToDb(data[-1],servernum)
								data[-1]=""
								data[-1]=msg
						else:
							if len(msg)+len(data[-1]) < 160:
								data[-1]=data[-1]+msg
							else:
								print data[-1]
								data[-1] = data[-1].replace(gatename[0].upper(),setname)
								senslopeServer.WriteOutboxMessageToDb(data[-1],servernum)
								data[-1]=""
								data[-1]=msg
						print ">> Packet from",data[0]

				
			#print "len(fin):", len(fin)
			#print "len(routername):", len(routername)
			#tapos check dito kung nasa laman na ng list yung lahat ng names
			#if len(fin) == len(routername)+3:
			#	print "All data received. Terminating script."
			#	writeRssi()
			#	reset()
			#	sys.exit()
			
			
		except KeyboardInterrupt:
			break
			
	ser.close()		
	return

	
def writeRssi():
	ser = serial.Serial(PORT, BAUD_RATE)
	xbee = ZigBee(ser,escaped=True)

	gatetxt="GATEWAY*RSSI,"+gatename[0].upper()
	gatetxt=re.sub('[^A-Z0-9\,*]',"",gatetxt)
	
	for data in routerdata:
		gatetxt=gatetxt+data[3]
	gatetxt=gatetxt+"*"+dt.today().strftime("%y%m%d%H%M%S")
	gatetxt=gatetxt.replace(gatename[0].upper(),setname)
	senslopeServer.WriteOutboxMessageToDb(gatetxt,servernum)
	
	print "Done writing RSSI and voltage."
	ser.close()
	return
	
	
def reset():
	ser = serial.Serial(PORT, BAUD_RATE)
	xbee = ZigBee(ser,escaped=True)

	#poweroff
	xbee.remote_at(
	dest_addr_long=DEST_ADDR_LONG, 			
		command="D1",
		parameter='\x04')
		#frame_id="A")
		
	sleep(2)
	
	#poweron
	xbee.remote_at(
		dest_addr_long=DEST_ADDR_LONG, 			
		command="D1",
		parameter='\x00')
		#frame_id="A")
		
	print "Reset done"
	
	ser.close()
	return
	
