import os
import sys
import time
import getpass

if getpass.getuser() != 'root':
    print "only run this program as 'root'"
    sys.exit(1)

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
    time.sleep(1)
    serverDir = root.replace('runserver.py', 'pydev/GradeServer/GradeServer')
    os.chdir(serverDir)
    os.execl('/usr/bin/python', '/usr/bin/python', 'runserver.py', dbUserName, dbPassword)

else:
    dockerDir = root.replace('runserver.py', 'Dockerfiles/GradeServer_Docker')

    os.system('python ' + dockerDir + '/create_container.py')

    celeryDir = root.replace('runserver.py', 'celeryServer')
    os.chdir(celeryDir)
    fp = open('data.txt', 'w')
    fp.write(dbUserName + '\n')
    fp.write(dbPassword + '\n')
    fp.close()
    #os.system('celery multi start celeryServer worker --loglevel=info --concurrency=1')
    #os.system('rm -rf data.txt')
