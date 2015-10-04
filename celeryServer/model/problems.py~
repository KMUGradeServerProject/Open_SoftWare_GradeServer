# -*- coding: utf-8 -*-
"""
 문제에 대한 정보 모듈
 ============================
 무결성이 깨지는 구조이기 때문에 조심히 작업할 것
"""


from sqlalchemy import Column 
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, TEXT, ENUM

from GradeServer.model import Base 

from GradeServer.resource.enumResources import ENUMResources

class Problems(Base) :
    
    __tablename__ = 'Problems'
    
    problemIndex = Column(INTEGER(unsigned = True),
                          primary_key = True,
                          autoincrement = True,
                          nullable = False)
    problemName = Column(VARCHAR(255),
                         nullable = False,
                         unique = True)
    problemDifficulty = Column(ENUM(ENUMResources().const.BRONZE,
                                    ENUMResources().const.SILVER,
                                    ENUMResources().const.GOLD),
                               default = ENUMResources().const.BRONZE,
                               nullable = False)
    solutionCheckType = Column(ENUM(ENUMResources().const.SOLUTION,
                                    ENUMResources().const.CHECKER),
                               default = ENUMResources().const.CHECKER,
                               nullable = False)
    numberOfTestCase = Column(INTEGER(unsigned = True),
                              default = 0,
                              nullable = False)
    limitedTime = Column(INTEGER(unsigned = True),
                         default = 3000,
                         nullable = False) #ms
    limitedMemory = Column(INTEGER(unsigned = True),
                           default = 1024,
                           nullable = False) #MB
    problemPath = Column(TEXT,
                         nullable = True)
    isDeleted = Column(ENUM (ENUMResources().const.TRUE,
                             ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE,
                       nullable = False)
