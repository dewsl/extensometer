import matplotlib.pyplot as plt
import serial
import sys
import numpy
import time
from scipy import signal
from scipy.signal import correlate
from numpy.fft import rfft,irfft
from numpy import fliplr
from timeit import default_timer as timer
from datetime import datetime as dt

'''
sample =[]
base =[]
buffer =[]
paddedbase=[]
corr=[]
distance=0
tts=0
'''
distance=0
sample=[]
base=[]
tts=0

#ser = serial.Serial('COM6', 115200)
ser = serial.Serial('/dev/samplingusbport', 115200)
#sergain = serial.Serial('/dev/gainusbport', 9600)

def getTemp():
	ser.write("AT+TMP\r\n")
	temp=ser.readline()
	temp=ser.readline()
	temp=temp[0:-4]
	print temp
	
	return temp
	

def readbase():
	#base=[]
	f=open("/home/pi/Server/newbase.txt")
	for item in f:
		base.append(int(item.strip()))
		
	#base=buffer[1137:4000]
	
	f.close() 
	
	return base

def xcor(sample,base,distance,temp):
	'''
	ave=numpy.mean(base)
	avebase=[]
	for i in base:
		avebase.append(i-ave)


	paddedbase=[0]*8000+avebase
	corr=numpy.correlate(sample,paddedbase,mode='full')
	'''
	
	sample=sample-numpy.mean(sample)
	base=base-numpy.mean(base)

	paddedbase=([0]*8000).append(base)
	corr=numpy.correlate(sample,base,mode='full')
	
	lag=numpy.argmax(corr)
	maxIndSample=numpy.argmax(sample)
	maxValSample=max(sample)
	
	
	print "Lag is", lag
	data=">>01/01#INAXA*l*la:"+str(lag)+','+"mx:"+str(maxValSample)+','+"mi:"+str(maxIndSample)+','+"tp:"+str(temp)+'*'+dt.today().strftime("%y%m%d%H%M%S")+"<<\n"
	payload=str(len(data))+data.upper()	
	print "Writing this data to file:", payload
	
	
	fresults = open("/home/pi/Server/results.txt","a")
	fresults.write(payload)
	fresults.close()
	
	lag=0
	
	'''
	plt.plot(corr)
	plt.xlabel("cross correlation")
	
	filename="crosscorrelation_"+str(distance)+"cm.png"
	plt.savefig(filename)
	plt.show()
	'''
	
	print "DONE: Write to text file"
	print "DONE: Compute cross correlation"
	#print "DONE: Save cross correlation image as", filename
	
	sample=[]
	
	return data

def plotter(sample,base):
	plt.figure()
	plt.plot(sample)
	plt.xlabel("sample")
	
	#plt.figure()
	#plt.plot(base)
	#plt.xlabel("base")
	
	plt.show()
	
	print "Done plotting"
	
	return
'''	
def move1cm():
	#sermove = serial.Serial('COM5', 9600)
	
	global distance
	
	time.sleep(0.25)
	sergain.write("at+utscm")
	distance +=1

	#print "Plus 1 cm. Next distance is",distance,"cm"
	#print ""
	
	#sermove.close()
	return distance
	
def movemax():
	#sermove = serial.Serial('COM5', 9600)

	time.sleep(0.5)
	sergain.write("at+max")
	time.sleep(0.5)

	#sermove.close()
	return
	
def movemid():
	#sermove = serial.Serial('COM5', 9600)

	time.sleep(0.5)
	sergain.write("at+mid")
	time.sleep(0.5)

	#sermove.close()
	return	
	
def movebackhome():
	#sermove = serial.Serial('COM5', 9600)

	time.sleep(0.5)
	sergain.write("at+home")
	time.sleep(0.5)

	#sermove.close()
	return
'''	
	
def changegain(gain):
	#ser = serial.Serial('COM5', 9600)

	time.sleep(1)
	command="at+gain"+str(gain)
	print command
	ser.write(command)
	
	#ser.close()
	return 
	
def resetgain():
	#ser = serial.Serial('COM5', 9600)
	
	time.sleep(1)
	
	ser.write("at+rgain")

	#ser.close()
	return 
	
def main(distance):
	global sample
	sample=[]
	
	print "Starting"
	#print "Sampling for "+str(distance)+" cm"
	
	
	
	ser.write("AT+PWR\r\n")
	#print ser.readline()
	time.sleep(1.5)
	
	start=timer()
	ser.write("AT+UTS\r\n")

	'''
	read_serial=ser.readline()		#first two data are trash
	read_serial=ser.readline()
	read_serial=ser.readline()
	'''
	
	for _ in xrange(40):
		num = ser.read(2)
		
	
	
	'''
	num = ser.read(2)
	num = ser.read(2)
	num = ser.read(2)
	num = ser.read(2)
	num = ser.read(2)
	num = ser.read(2)
	'''
	'''
	while read_serial != "DONE\r\n":
		sample.append(int(read_serial))
		read_serial=ser.readline()
	'''
	
	for _ in xrange(10000):
		num_int = ord(num[0])*256 + ord(num[1])
		sample.append(num_int)
		#print num_int
		num=ser.read(2)
	
	end=timer()
	tts=end-start
	
	#fbase = open("bbase.txt","a")
	#fbase.write(str(sample))
	#fbase.close()
	
	'''
	fresults = open("results.txt","a")
	fresults.write(str(distance)+","+str(tts)+",")
	fresults.close()
	'''
	
	print "Sampled in", tts, "seconds."
	print "Done sampling"
	
	return sample
'''
	
main()	
readbase()
xcor()
#plotter()
move1cm()

sys.exit()

		
	'''	
