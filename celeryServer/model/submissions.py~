# -*- coding: utf-8 -*-
"""
사용자들의 제출 현황에 대한 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import TEXT, INTEGER, DATETIME, ENUM

from GradeServer.model import Base
from GradeServer.model.languages import Languages
from GradeServer.model.dataOfSubmissionBoard import DataOfSubmissionBoard

from GradeServer.resource.enumResources import ENUMResources

class Submissions(Base) :
    
    __tablename__ = 'Submissions'
    
    submissionIndex = Column(INTEGER(unsigned = True),
                             ForeignKey(DataOfSubmissionBoard.submissionIndex,
                                        onupdate = 'CASCADE',
                                        ondelete = 'NO ACTION'),
                             primary_key = True,
                             autoincrement = False,
                             nullable = False)
    submissionCount = Column(INTEGER(unsigned = True),
                             primary_key = True,
                             autoincrement = False,
                             default = 0,
                             nullable = False)
    solutionCheckCount = Column(INTEGER(unsigned = True),
                                default = 0,
                                nullable = False)
    status = Column(ENUM(ENUMResources().const.NEVER_SUBMITTED,
                         ENUMResources().const.JUDGING,
                         ENUMResources().const.SOLVED,
                         ENUMResources().const.TIME_OVER,
                         ENUMResources().const.MEMORY_OVERFLOW,
                         ENUMResources().const.WRONG_ANSWER,
                         ENUMResources().const.COMPILE_ERROR,
                         ENUMResources().const.RUNTIME_ERROR,
                         ENUMResources().const.SERVER_ERROR),
                    default = ENUMResources().const.NEVER_SUBMITTED,
                    nullable = False)
    score = Column(INTEGER(unsigned = True),
                   default = 0,
                   nullable = False)
    codeSubmissionDate = Column(DATETIME,
                                nullable = False)
    compileErrorMessage = Column(TEXT,
                                 default = None,
                                 nullable = True)
    wrongTestCaseNumber = Column(INTEGER(unsigned = True),
                                 default = None,
                                 nullable = True)
    runTime = Column(INTEGER(unsigned = True),
                     default = 0,
                     nullable = False)
    usedMemory = Column(INTEGER(unsigned = True),
                        default = 0,
                        nullable = False)
    usedLanguageIndex = Column(INTEGER(unsigned = True),
                               ForeignKey(Languages.languageIndex,
                                          onupdate = 'CASCADE',
                                          ondelete = 'NO ACTION'),
                               nullable = False)
    sumOfSubmittedFileSize = Column(INTEGER(unsigned = True),
                                    nullable = False) # Byte
    
