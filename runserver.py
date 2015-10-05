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

try:
    os.makedirs('/mnt/shared')
except Exception:
    pass

pid = os.fork()

if pid is not 0:
    time.sleep(2)
    serverDir = root.replace('runserver.py', 'pydev/GradeServer/GradeServer')
    os.chdir(serverDir)
    os.execl('/usr/bin/sudo', '/usr/bin/sudo', 'python', 'runserver.py', dbUserName, dbPassword)

else:
    dockerDir = root.replace('runserver.py', 'Dockerfiles/GradeServer_Docker')

    os.system('sudo python ' + dockerDir + '/create_container.py')

    celeryDir = root.replace('runserver.py', 'celeryServer')
    os.chdir(celeryDir)
    fp = open('data.txt', 'w')
    fp.write(dbUserName + '\n')
    fp.write(dbPassword + '\n')
    fp.close()
    os.system('celery multi start worker -A celeryServer -l info --concurrency=1')
    os.system('rm -rf data.txt')
