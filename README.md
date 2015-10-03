# Open_SoftWare_GradeServer
2015 오픈소프트 개발자 대회 출품작 -GradeServer

##제약 사항
###MariaDB직접 설치
###DB 접속 아이디 및 패스워드 설정 방법
####-mysqladmin -u ID -p PASSWORD
####-service mysqld restart
###DB CharacterSet utf-8
####-vi /etc/my.cnf
####-[client]
####//추가
####default-character-set = utf8
####[mysqld]
####//추가
####init_connect="SET collation_connection = utf8_general_ci"
####init_connect="SET NAMES utf8"
####default-character-set = utf8
####character-set-server = utf8
####collation-server = utf8_general_ci
####[mysqldump]
####//추가
####default-character-set = utf8
####[mysql]
####//추가
####default-character-set = utf8
####service mysqld restart
