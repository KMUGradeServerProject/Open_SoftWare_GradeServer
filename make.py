import os
import sys
import platform

if os.getuid is not 0:
    print "only run this program as 'root'"
    sys.exit(1)

if platform.system() == 'Windows':
    print 'cannot use this program in  Windows'
    sys.exit(1)


root  = sys.argv[0]

osInfo = platform.dist()

if osInfo[0] == 'centos':
    os.system('yum -y update')
    os.system('yum -y groupinstall "Development Tools"')
    os.system('yum -y install gcc')
    os.system('yum -y install wget')
    os.system('yum -y install zlib-devel openssl-devel')
    os.system('yum -y install docker')

    os.system('yum -y install tar')
    os.system('easy_install pip')

    os.system('pip install flask')
    os.system('pip install sqlalchemy')
    os.system('easy_install mysql-connector-python')
    os.system('pip install wtforms')
    os.system('pip install celery')

    os.system('pip install tornado')
    os.system('pip install sqlalchemy_utils')
    os.system('easy_install repoze.lru')
    os.system('pip install redis')

    os.system('service docker start')

    dockerDir = root.replace('make.py', '')
    
    if len(dockerDir) < 1:
	dockerDir = './'

    os.chdir(dockerDir)

    os.system('tar cvfz ./Dockerfiles/GradeServer_Docker/gradeprogram.tar.gz gradeprogram/')
    os.chdir('Dockerfiles/GradeServer_Docker')

    print 'start building gradeserver image'
    os.system('docker build -t gradeserver:1.0 .')

#if osInfo[0] == '':
