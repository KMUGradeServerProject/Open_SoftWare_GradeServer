# -*- coding: utf-8 -*-
"""
   제출 된 파일 정보에 대한 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, TEXT

from model import Base
from model.dataOfSubmissionBoard import DataOfSubmissionBoard


class SubmittedFiles (Base) :
    
    __tablename__ = 'SubmittedFiles'
    
    submissionIndex = Column(INTEGER(unsigned = True),
                           ForeignKey(DataOfSubmissionBoard.submissionIndex,
                                      onupdate = 'CASCADE',
                                      ondelete = 'CASCADE'),
                           autoincrement = False,
                           primary_key = True,
                           nullable = False)
    fileIndex =Column(INTEGER(unsigned = True),
                      primary_key = True,
                      autoincrement = False,
                      nullable = False)
    fileName = Column(VARCHAR(1024),
                      nullable = False)
    filePath = Column(TEXT,
                      nullable = False)
    fileSize = Column(INTEGER(unsigned = True),
                      default = 0,
                      nullable = False) #Byte
