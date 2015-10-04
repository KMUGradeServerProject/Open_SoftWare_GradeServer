# -*- coding: utf-8 -*-
"""
   등록된 문제마다 제출 된 결과의 합산 정보 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from model import Base
from model.problems import Problems

class SubmittedRecordsOfProblems(Base) :
    
    __tablename__ = 'SubmittedRecordsOfProblems'
    
    problemIndex = Column(INTEGER(unsigned = True),
                       ForeignKey (Problems.problemIndex,
                                   onupdate = 'CASCADE',
                                   ondelete = 'CASCADE'),
                       primary_key = True,
                       autoincrement = False,
                       nullable = False)
    sumOfSubmissionCount = Column(INTEGER (unsigned = True),
                                  default = 0,
                                  nullable = False)
    sumOfSolvedCount = Column(INTEGER (unsigned = True),
                              default = 0,
                              nullable = False)
    sumOfWrongCount = Column(INTEGER (unsigned = True),
                             default = 0,
                             nullable = False)
    sumOfRuntimeErrorCount = Column(INTEGER (unsigned = True),
                                    default = 0,
                                    nullable = False)
    sumOfCompileErrorCount = Column(INTEGER (unsigned = True),
                                    default = 0,
                                    nullable = False)
    sumOfTimeOverCount = Column(INTEGER (unsigned = True),
                                default = 0,
                                nullable = False)
    sumOfMemoryOverFlowCount = Column(INTEGER (unsigned = True),
                                      default = 0,
                                      nullable = False)
