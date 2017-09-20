import matplotlib.pyplot as plt
import sys

f = open("months.txt")

data =[]

for item in f:
	#print(item.strip())
	data.append(int(item.strip()))
	
plt.plot(data)
plt.ylabel("data")
#plt.show()
plt.savefig('basefigure.png')
print "Done"
sys.exit()