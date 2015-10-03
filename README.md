# Open_SoftWare_GradeServer
2015 오픈소프트 개발자 대회 출품작 -GradeServer

##제약 사항

####DB의 Character Set을 utf8로 설정하여 한글이 깨지지 않도록 한다.

####Local에는 Redis와 MariaDB 또는 MySQL이 깔려 있어야 하며, 오픈소스 구동 전 Redis와 DB 서비스가 실행되고 있어야 한다.

####오픈 소스는 RedHat 계열의 리눅스에서만 실행 가능하며 Centos7에서 가장 효율성이 높다.

####runserver.py 실행시에는 python runserver.py DB_ID DB_PW 처럼 argv를 파일 이름 DB 접속 아이디 DB 접속 암호를 쓴다.
