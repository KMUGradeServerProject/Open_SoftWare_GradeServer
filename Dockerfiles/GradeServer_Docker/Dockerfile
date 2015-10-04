FROM centos:6

MAINTAINER lee youngchan <y2y0c4@gmail.com>

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

RUN yum -y install tar

#install python2.7. &pip
RUN wget https://www.python.org/ftp/python/2.7.5/Python-2.7.5.tgz && tar xvfz Python-2.7.5.tgz && ./Python-2.7.5/configure && make && make altinstall && mv /usr/bin/python /usr/bin/python_old && cp /usr/local/bin/python2.7 /usr/bin/python
RUN curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python -;easy_install pip

#install python3.4
RUN cp /usr/bin/yum /usr/bin/yum_old && sed -i 's/\/usr\/bin\/python/\/usr\/bin\/python2.6/g' /usr/bin/yum
RUN wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz && tar xvfz Python-3.4.2.tgz 
RUN cd Python-3.4.2; ./configure ; make ; make install

#install nfs
RUN yum -y install nfs-utils

#add program

#install ptrace
RUN wget https://pypi.python.org/packages/source/p/ptrace/ptrace-1.0.1.tar.gz
RUN tar fxz ptrace-1.0.1.tar.gz
RUN cd ptrace-1.0.1; python setup.py build;python setup.py install

#etc
RUN mkdir /temp
RUN mkdir /container
RUN mkdir /mnt/shared
ADD gradeprogram.tar.gz /

VOLUME /tempdir
