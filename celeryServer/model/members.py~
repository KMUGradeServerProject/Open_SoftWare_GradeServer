# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    어플리케이션을 사용할 사용자 정보

"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import DATETIME, VARCHAR, INTEGER, TEXT, SET, ENUM

from GradeServer.model import Base

from GradeServer.resource.setResources import SETResources
from GradeServer.resource.enumResources import ENUMResources

class Members (Base) :
    
    __tablename__ ='Members'
    
    memberIdIndex = Column(INTEGER(unsigned = True),
                           primary_key =True,
                           autoincrement = True,
                           nullable = False)
    memberId = Column(VARCHAR(255),
                      nullable = False,
                      unique = True)
    password = Column(VARCHAR(1024),
                      nullable =False)
    memberName = Column(VARCHAR(1024),
                        nullable =False)
    contactNumber = Column(VARCHAR(20),
                           nullable =True)
    emailAddress = Column(VARCHAR(1024),
                          nullable =True)
    detailInformation = Column(VARCHAR(1024),
                               nullable = True)
    authority = Column(SET(SETResources().const.ADMINISTRATOR,
                           SETResources().const.USER),
                       default = SETResources().const.USER,
                       nullable = False)
    limitedUseDate = Column(DATETIME,
                            default = None,
                            nullable = True)
    signedInDate = Column(DATETIME,
                          nullable = False)
    lastAccessDate = Column(DATETIME,
                            nullable =True)
    comment = Column(TEXT,
                     nullable = True)   
    isDeleted = Column(ENUM(ENUMResources().const.TRUE, 
                            ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE,
                       nullable = False)
