FROM centos:6

MAINTAINER Hwang Sek-Jin <dollking2000@gmail.com>

#install packages
RUN yum -y update
RUN yum -y groupinstall "Development Tools"
RUN yum -y install gcc
RUN yum -y install java-1.7.0-openjdk java-1.7.0-openjdk-devel
RUN yum -y install wget
RUN yum -y install zlib-devel openssl-devel

ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

#setting MariaDB.repo
RUN echo "[mariadb]">> /etc/yum.repos.d/MariaDB.repo&&echo "name=MariaDB" >> /etc/yum.repos.d/MariaDB.repo && echo "baseurl=http://yum.mariadb.org/10.0/centos6-amd64" >> /etc/yum.repos.d/MariaDB.repo &&echo "gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB" >> /etc/yum.repos.d/MariaDB.repo &&echo "gpgcheck=1" >> /etc/yum.repos.d/MariaDB.repo 

#install mariadb & tar
RUN yum -y install MariaDB-server MariaDB-client
RUN yum -y install tar

#install nfs
RUN yum -y install nfs-utils

#install python2.7. &pip
RUN wget https://www.python.org/ftp/python/2.7.5/Python-2.7.5.tgz && tar xvfz Python-2.7.5.tgz && ./Python-2.7.5/configure && make && make altinstall && mv /usr/bin/python /usr/bin/python_old && cp /usr/local/bin/python2.7 /usr/bin/python
RUN curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python -;easy_install pip

#install flask
RUN pip install flask

#install aqlalchemy
RUN pip install sqlalchemy
RUN /usr/local/bin/easy_install mysql-connector-python

#install wtforms
RUN pip install wtforms

#install celery
RUN pip install celery

#install redis
RUN pip install redis
RUN wget http://download.redis.io/releases/redis-2.6.16.tar.gz && tar xzf redis-2.6.16.tar.gz # && ./redis-2.6.16/make

RUN pip install tornado
RUN pip install sqlalchemy_utils
RUN easy_install repoze.lru

#service start
RUN service mysql start
RUN service rpcbind start

#etc
RUN mkdir /mnt/shared
ADD my.cnf /etc/
ADD webserver.tar.gz /
RUN service mysql start

VOLUME ["/mnt/shared", "/var/lib/mysql"]

#ENTRYPOINT python hello.py

EXPOSE 80 6379 3306
