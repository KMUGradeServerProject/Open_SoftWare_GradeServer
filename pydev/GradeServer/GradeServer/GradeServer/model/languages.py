# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .
    사용 프로그래밍 언어에 대한 정보
"""


from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER

from GradeServer.model import Base
from sqlalchemy.sql.schema import UniqueConstraint

class Languages(Base) :
    
    __tablename__ = 'Languages'
    
    languageIndex = Column(INTEGER
                           (unsigned = True),
                           primary_key = True,
                           autoincrement = True,
                           nullable = False)
    languageName = Column(VARCHAR(255), 
                          nullable = False)
    languageVersion = Column(VARCHAR(255),
                             nullable = True)
    
    __table_args__ = (UniqueConstraint('languageName',
                                       'languageVersion'),)
