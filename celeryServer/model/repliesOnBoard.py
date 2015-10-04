# -*- coding: utf-8 -*-
"""
    게시판 글 댓글 정보 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DATETIME, TEXT, ENUM

from model import Base
from model.articlesOnBoard import ArticlesOnBoard
from model.members import Members

from gradingResource.enumResources import ENUMResources

class RepliesOnBoard(Base) :
    
    __tablename__ = 'RepliesOnBoard'
    
    boardReplyIndex = Column(INTEGER(unsigned = True),
                             primary_key = True,
                             autoincrement = True,
                             nullable = False)
    articleIndex = Column(INTEGER(unsigned = True),
                          ForeignKey(ArticlesOnBoard.articleIndex,
                                     onupdate = 'CASCADE',
                                     ondelete = 'CASCADE'),
                          nullable = False)
    boardReplierIdIndex = Column(INTEGER(unsigned = True),
                                 ForeignKey(Members.memberIdIndex,
                                            onupdate = 'CASCADE',
                                            ondelete = 'CASCADE'),
                                 nullable = False)
    boardReplyContent = Column(TEXT,
                               nullable = False)
    sumOfLikeCount = Column(INTEGER(unsigned = True),
                            default = 0,
                            nullable = False)
    boardReplierIp = Column(VARCHAR(20),
                            nullable = False)
    boardRepliedDate = Column(DATETIME,
                              nullable = False)
    isDeleted = Column(ENUM(ENUMResources().const.TRUE,
                             ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE,
                       nullable = False)
    
