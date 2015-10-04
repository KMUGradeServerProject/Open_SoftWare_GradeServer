import os

MAX_CONTAINER_COUNT = 1

if len(sys.argv) < 2:
	print 'rm one container'
elif len(sys.argv) == 2:
	MAX_CONTAINER_COUNT = int(sys.argv[1])
else:
	print 'option error'
	os.exit()

for i in xrange(1, MAX_CONTAINER_COUNT):
	os.system("sudo docker stop grade_container"+str(i))
	os.system("sudo docker rm grade_container"+str(i))
