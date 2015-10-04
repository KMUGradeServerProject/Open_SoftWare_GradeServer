# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .
    사용 프로그래밍 언어에 대한 정보
"""


from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER

from model import Base

class Languages(Base) :
    
    __tablename__ = 'Languages'
    
    languageIndex = Column(INTEGER
                           (unsigned = True),
                           primary_key = True,
                           autoincrement = True,
                           nullable = False)
    languageName = Column(VARCHAR(255), 
                          nullable = False,
                          unique = True)
    languageVersion = Column(VARCHAR(255),
                             nullable = True,
                             unique = True)
