# -*- coding: utf-8 -*-
"""
    photolog.database
    ~~~~~~~~~~~~~~~~~

    DB 연결 및 쿼리 사용을 위한 공통 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from model import Base
from celery.worker.control import pool_restart


fp = open('data.txt')
data = fp.readlines()
fp.close()

engine = create_engine("mysql+mysqlconnector://" + data[0].rstrip() + ":" + data[1].rstrip() +"@localhost/GradeServer", convert_unicode = True, pool_size=50, pool_recycle=3600)

global db_session
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.metadata.create_all(bind=engine)
