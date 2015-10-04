# -*- coding: utf-8 -*-
"""
    게시판 글 댓글의 좋아요 정보 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, ENUM

from GradeServer.model import Base
from GradeServer.model.repliesOnBoard import RepliesOnBoard
from GradeServer.model.members import Members
from GradeServer.resource.enumResources import ENUMResources

class LikesOnReplyOfBoard (Base) :
    
    __tablename__ = 'LikesOnReplyOfBoard'
    
    boardReplyIndex = Column(INTEGER(unsigned = True),
                             ForeignKey(RepliesOnBoard.boardReplyIndex,
                                        onupdate = 'CASCADE',
                                        ondelete = 'CASCADE'),
                             primary_key = True,
                             autoincrement = False,
                             nullable = False)
    boardReplyLikerIdIndex = Column(INTEGER(unsigned = True),
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
