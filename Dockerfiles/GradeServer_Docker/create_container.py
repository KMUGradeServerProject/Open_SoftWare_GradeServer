import os
import sys

MAX_CONTAINER_COUNT = 1

if len(sys.argv) < 2:
	print 'make one container'
elif len(sys.argv) == 2:
	MAX_CONTAINER_COUNT = int(sys.argv[1])
else:
	print 'option error'
	os.exit()

for i in range(1, MAX_CONTAINER_COUNT+1):
	os.system('sudo docker create --privileged -i -t --name grade_container' + str(i)
			  + ' --cpuset-cpus="' + str(i) + '" --memory="1g" -v /mnt/shared:/mnt/shared gradeserver:1.0 /bin/bash')
	os.system('sudo docker start grade_container'+str(i))
