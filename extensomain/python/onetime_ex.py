from extensometer import *


changegain(3)
time.sleep(1)
changegain(4)
distance=0
base=readbase()

time.sleep(2)

sample=main(distance)	
xcor(sample,base,distance)
plotter(sample,base)


print "Done sampling"
resetgain()

sys.exit()