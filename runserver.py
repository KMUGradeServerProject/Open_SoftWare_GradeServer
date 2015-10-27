import os
import sys
import time

if len(sys.argv) < 3:
    print 'add your username and password in database'
    sys.exit(1)

k = raw_input('did you run redis and database?(y/n):')

if k.lower() == 'n':
    print 'you need to run redis and database, first'
    sys.exit(1)

root = sys.argv[0]
dbUserName = sys.argv[1]
dbPassword = sys.argv[2]

pid = os.fork()

if pid is not 0:
    time.sleep(2.2)
    
    os.system('sudo python /mnt/shared/Dockerfiles/create_container.py')
    
    os.chdir('/mnt/shared/pydev/GradeServer/GradeServer')
    os.execl('/usr/bin/sudo', '/usr/bin/sudo', 'python', 'runserver.py', dbUserName, dbPassword)

else:
    os.chdir('celeryServer/')
    
    fp = open('data.txt', 'w')
    fp.write(dbUserName + '\n')
    fp.write(dbPassword + '\n')
    fp.close()
    
    os.system('celery multi start worker -A celeryServer -l info -c 1 --pidfile="./%n.pid" --logfile="./%n.log"')
    time.sleep(0.8)
    os.system('rm -rf data.txt')
