import os
import sys

os.makedirs('/mnt/shared')
os.system('sudo docker create --privileged -i -t --name webserver -p 80:80 webserver:1.0 /bin/bash')
os.system('sudo docker start webserver')
