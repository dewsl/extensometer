import numpy as np
import random, math
import matplotlib.pyplot as plt

a= np.array([math.sin(i*0.1) for i in range(8000)])
b= np.array([math.sin(i*0.1 +2*3.14) for i in range(1000)])
c=[100]*8000
base=[]


f=open("base.txt")
for item in f:
	base.append(int(item.strip()))

ave=np.mean(base)
print ave
avebase=[]
for i in base:
	avebase.append(i-ave)
	
	
paddedbase=[0]*8000+avebase
	
corr= np.correlate(base,paddedbase,mode='full')

#corr=np.absolute(corr)

imagcorr=np.imag(corr)

'''
for i in corr:
	if isinstance(x, complex):
		print "Yeah!"
'''
#print np.argmax(corr)
#print "pbase:", paddedbase

'''
plt.plot(a)
plt.xlabel("a")

plt.figure()
plt.plot(b)
plt.xlabel("b")
'''
'''
print corr[:100]
print abscorr[:100]

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.xcorr(base, base, maxlags=4000)
plt.show()
'''

plt.plot(base)
plt.xlabel("base")

plt.figure()
plt.plot(avebase)
plt.xlabel("avebase")


plt.figure()
plt.plot(paddedbase)
plt.xlabel("padded base")



plt.figure()
plt.plot(corr)
plt.xlabel("xcorr")

plt.figure()
plt.plot(imagcorr)
plt.xlabel("imagcorr")

plt.show()
