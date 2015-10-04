# -*- coding: utf-8 -*-
"""
    문제별 제출 한 소스 코드의 댓글 정보 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DATETIME, TEXT, ENUM

from GradeServer.model import Base
from GradeServer.model.members import Members
from GradeServer.model.dataOfSubmissionBoard import DataOfSubmissionBoard

from GradeServer.resource.enumResources import ENUMResources

class RepliesOnSubmission(Base) :
    
    __tablename__ = 'RepliesOnSubmission'
    
    submissionReplyIndex = Column(INTEGER(unsigned = True),
                                  primary_key = True,
                                  autoincrement = True,
                                  nullable = False)
    submissionIndex = Column(INTEGER(unsigned = True),
                             ForeignKey(DataOfSubmissionBoard.submissionIndex,
                                        onupdate = 'CASCADE',
                                        ondelete = 'CASCADE'),
                             nullable = False)
    codeReplierIdIndex = Column(INTEGER(unsigned = True),
                                ForeignKey(Members.memberIdIndex,
                                           onupdate = 'CASCADE',
                                           ondelete = 'CASCADE'),
                                nullable = False)
    codeReplyContent = Column(TEXT,
                              nullable = False)
    codeReplierIp = Column(VARCHAR (20),
                           nullable = False)
    codeRepliedDate = Column(DATETIME,
                             nullable = False)
    sumOfLikeCount = Column(INTEGER(unsigned = True),
                            default = 0,
                            nullable = False)
    isDeleted = Column(ENUM(ENUMResources().const.TRUE,
                            ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE,
                       nullable = False)    
