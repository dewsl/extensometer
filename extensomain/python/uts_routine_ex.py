from uts_extensometer import *

distance=0
base=readbase()

for x in range(40):	
	sample=main(distance)	
	xcor(sample,base,distance)
	distance=move1cm()
	time.sleep(4)

print "Done sampling the whole range"
backhome()

sys.exit()