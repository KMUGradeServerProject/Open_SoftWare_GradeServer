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
    time.sleep(1.5)
    
    if os.getgroups().count(1410) is 0:
        os.system('sudo groupadd -g docker')
        os.system('sudo gpasswd -a ${USER} docker')
        os.system('sudo service docker restart')
        os.system('newgrp docker')
    
    dockerDir = root.replace('runserver.py', 'Dockerfiles/GradeServer_Docker')
    os.system('sudo python ' + dockerDir + '/create_container.py')
    
    serverDir = root.replace('runserver.py', 'pydev/GradeServer/GradeServer')
    os.chdir(serverDir)
    os.execl('/usr/bin/sudo', '/usr/bin/sudo', 'python', 'runserver.py', dbUserName, dbPassword)

else:
    celeryDir = root.replace('runserver.py', 'celeryServer')
    os.chdir(celeryDir)
    
    fp = open('data.txt', 'w')
    fp.write(dbUserName + '\n')
    fp.write(dbPassword + '\n')
    fp.close()
    
    os.system('celery -A celeryServer worker -l info -c 1 --pidfile="./%n.pid" 1>celery.log')
    time.sleep(0.8)
    os.system('rm -rf data.txt')
