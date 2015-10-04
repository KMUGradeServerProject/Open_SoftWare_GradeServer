# -*- coding: utf-8 -*-
"""
    문제별 제출 한 소스 코드 댓글의 좋아요 정보 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, ENUM

from model import Base
from model.repliesOnSubmission import RepliesOnSubmission
from model.members import Members
from gradingResource.enumResources import ENUMResources

class LikesOnReplyOfSubmission(Base) :
    
    __tablename__ = 'LikesOnReplyOfSubmission'
    
    submissionReplyIndex = Column(INTEGER(unsigned = True),
                                  ForeignKey(RepliesOnSubmission.submissionReplyIndex,
                                             onupdate = 'CASCADE',
                                             ondelete = 'CASCADE'),
                                  primary_key = True,
                                  autoincrement = False,
                                  nullable = False)
    codeReplyLikerIdIndex = Column(INTEGER(unsigned = True),
                                   ForeignKey(Members.memberIdIndex,
                                              onupdate = 'CASCADE',
                                              ondelete = 'CASCADE'),
                                   primary_key = True,
                                   autoincrement = False,
                                   nullable = False)
    isLikeCancelled = Column(ENUM(ENUMResources().const.TRUE,
                                  ENUMResources().const.FALSE),
                             default = ENUMResources().const.FALSE,
                             nullable = False)
    
