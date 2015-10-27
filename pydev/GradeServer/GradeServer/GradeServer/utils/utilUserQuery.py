
# -*- coding: utf-8 -*-


from sqlalchemy import or_, and_

from GradeServer.database import dao

from GradeServer.model.members import Members

from GradeServer.resource.setResources import SETResources
from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.languageResources import LanguageResources



def select_all_members(isDeleted = ENUMResources().const.FALSE):
    return dao.query(Members).\
               filter(Members.isDeleted == isDeleted)


'''
Select match MemberId  
'''
def select_match_member_id(memberId, isDeleted = ENUMResources().const.FALSE):
    return dao.query(Members).\
               filter(Members.memberId == memberId,
                      Members.isDeleted == isDeleted)
              
               


'''
Search Members
'''
def search_members(members, filterFindParameter, isDeleted = ENUMResources().const.FALSE):
    # condition은 All, ID, Name로 나누어서 검새
    if filterFindParameter.filterCondition == LanguageResources().const.All[1]: # Filters[0] is '모두'
        members = dao.query(members).\
                      filter(or_(members.c.memberId == filterFindParameter.keyWord, 
                                 members.c.memberName.like('%' + filterFindParameter.keyWord + '%')),
                             members.c.isDeleted == isDeleted)
    elif filterFindParameter.filterCondition == LanguageResources().const.ID[1]: # Filters[1] is ID
        members = dao.query(members).\
                      filter(members.c.memberId == filterFindParameter.keyWord,
                             members.c.isDeleted == isDeleted)
    else: # Filters[2] is 'NAme'
        members = dao.query(members).\
                      filter(members.c.memberName.like('%'+ filterFindParameter.keyWord + '%'),
                             members.c.isDeleted == isDeleted)

    return members




'''
Select Member
'''
def select_member(memberIdIndex, isDeleted = ENUMResources().const.FALSE):
    return dao.query(Members).\
               filter(Members.memberIdIndex == memberIdIndex,
                      Members.isDeleted == isDeleted)
               
               
               
'''
DB Select All Members to User in Authority
'''
def select_members(Administrator = SETResources().const.ADMINISTRATOR,
                   User = SETResources().const.USER,
                   isDeleted = ENUMResources().const.FALSE):
    
        # 자동 완성을 위한 모든 유저기록
    members = dao.query(Members).\
                  filter(Members.authority == User,
                         Members.isDeleted == isDeleted)
    
    return members


'''
Users Sorted
'''
def members_sorted(members, sortCondition = LanguageResources().const.ID[1]): 
    # MEMBER ID, ORGANIZATION NAME, MEMBER NAME, LAST_ACCESS_DATE, END DATE 정렬
    if sortCondition == LanguageResources().const.ID[1]:
        memberRecords = dao.query(members).\
                            order_by(members.c.memberId.asc(),
                                     members.c.memberName.asc(),
                                     members.c.lastAccessDate.asc(),
                                     members.c.limitedUseDate.asc())
    # MEMBER NAME, ORGANIZATION NAME, MEMBER ID, LAST_ACCESS_DATE, END DATE 정렬
    elif sortCondition == LanguageResources().const.Name[1]:
        memberRecords = dao.query(members).\
                            order_by(members.c.memberName.asc(),
                                     members.c.memberId.asc(),
                                     members.c.lastAccessDate.asc(),
                                     members.c.limitedUseDate.asc())     
    # LAST_ACCESS_DATE, ORGANIZATION NAME, MEMBER ID, MEMBER NAME, END DATE 정렬                    
    elif sortCondition == LanguageResources().const.LastAccess[1]:
        memberRecords = dao.query(members).\
                            order_by(members.c.lastAccessDate.asc(),
                                     members.c.memberName.asc(),
                                     members.c.memberId.asc(),
                                     members.c.limitedUseDate.asc())     
    # END DATE, ORGANIZATION NAME, MEMBER ID, MEMBER NAME, LAST_ACCESS_DATE 정렬                    
    elif sortCondition == LanguageResources().const.FinishDate[1]:
        memberRecords = dao.query(members).\
                            order_by(members.c.limitedUseDate.asc(),
                                     members.c.memberId.asc(),
                                     members.c.memberName.asc(),
                                     members.c.lastAccessDate.asc())                     
                                
    return memberRecords 


               
def select_match_member_sub(members, memberIdIndex):
    # memberId Filterling
    return dao.query(members).\
               filter(members.c.memberIdIndex == memberIdIndex)
               


'''
get memberId
'''
def join_member_id(subquery, subMemberIdIndex, isDeleted = ENUMResources().const.FALSE):
    return dao.query(subquery,
                     Members.memberId).\
               join(Members,
                    and_(Members.memberIdIndex == subMemberIdIndex,
                         Members.isDeleted == isDeleted))

'''
Insert Members
'''
def insert_members(memberId, password, memberName, signedInDate, detailInformation = None, contactNumber = None, emailAddress = None, authority = SETResources().const.USER, comment = None):
    return Members(memberId = memberId,
                   password = password,
                   memberName = memberName,
                   contactNumber = contactNumber,
                   emailAddress = emailAddress,
                   detailInformation = detailInformation,
                   authority = authority,
                   signedInDate = signedInDate,
                   comment = comment)


    
''' 
Update Login Time
'''
def update_recent_access_date(memberIdIndex, lastAceesDate, isDeleted = ENUMResources().const.FALSE):
    ''' doesnt need to add exception handler here? '''
    dao.query(Members).\
        filter(and_(Members.memberIdIndex == memberIdIndex,
                    Members.isDeleted == isDeleted)).\
        update(dict(lastAccessDate = lastAceesDate))  
 
 
'''
 Update Member isDeleted
'''
def update_member_deleted(memberIdIndex, isDeleted = ENUMResources().const.TRUE): 
    dao.query(Members).\
        filter(Members.memberIdIndex == memberIdIndex).\
        update(dict(isDeleted = isDeleted))    
    
        

'''
Update Member Information
'''
def update_members(members, password, contactNumber = None, emailAddress = None, comment = None):
    members.update(dict(password = password,
                        contactNumber = contactNumber,
                        emailAddress = emailAddress,
                        comment = comment) if password 
                   else dict(contactNumber = contactNumber,
                        emailAddress = emailAddress,
                        comment = comment))
