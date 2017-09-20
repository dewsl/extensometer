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

ser = serial.Serial('COM6', 115200)
sergain = serial.Serial('COM5', 9600)

def readbase():
	#base=[]
	f=open("newbase.txt")
	for item in f:
		base.append(int(item.strip()))
		
	#base=buffer[1137:4000]
	
	f.close() 
	
	return base

def xcor(sample,base,distance):
	
	ave=numpy.mean(base)
	avebase=[]
	for i in base:
		avebase.append(i-ave)


	paddedbase=[0]*8000+avebase
	corr=numpy.correlate(sample,paddedbase,mode='full')
	
	lag=numpy.argmax(corr)
	
	print "Lag is", lag
	fresults = open("results.txt","a")
	fresults.write(str(lag)+'\n')
	fresults.close()
	
	lag=0
	
	plt.plot(corr)
	plt.xlabel("cross correlation")
	
	filename="crosscorrelation_"+str(distance)+"cm.png"
	plt.savefig(filename)
	plt.show()
	
	print "DONE: Write to text file"
	print "DONE: Compute cross correlation"
	#print "DONE: Save cross correlation image as", filename
	
	sample=[]
	
	return

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
	
def backhome():
	#sermove = serial.Serial('COM5', 9600)

	time.sleep(0.5)
	sergain.write("at+home")
	time.sleep(0.5)

	#sermove.close()
	return
	
	
def changegain(gain):
	#sergain = serial.Serial('COM5', 9600)

	time.sleep(1)
	command="at+gain"+str(gain)
	print command
	sergain.write(command)
	
	#sergain.close()
	return 
	
def resetgain():
	#sergain = serial.Serial('COM5', 9600)
	
	time.sleep(1)
	
	sergain.write("at+rgain")

	#sergain.close()
	return 
	
def main(distance):
	global sample
	sample=[]
	
	print "Starting"
	#print "Sampling for "+str(distance)+" cm"
	
	start=timer()
	
	ser.write("AT+UTS\r\n")

	'''
	read_serial=ser.readline()		#first two data are trash
	read_serial=ser.readline()
	read_serial=ser.readline()
	'''
	
	num = ser.read(2)
	num = ser.read(2)
	num = ser.read(2)
	num = ser.read(2)
	num = ser.read(2)
	num = ser.read(2)
	
	'''
	while read_serial != "DONE\r\n":
		sample.append(int(read_serial))
		read_serial=ser.readline()
	'''
	
	for _ in xrange(7998):
		num_int = ord(num[0])*256 + ord(num[1])
		sample.append(num_int)
		#print num_int
		num=ser.read(2)
	
	end=timer()
	tts=end-start
	
	
	fresults = open("results.txt","a")
	fresults.write(str(distance)+","+str(tts)+",")
	fresults.close()
	
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
