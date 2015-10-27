# -*- coding: utf-8 -*-


from werkzeug.exceptions import BadRequest
from flask import session

from GradeServer.utils.utilProblemQuery import select_problem
from GradeServer.utils.utilSubmissionQuery import select_replies_on_code
from GradeServer.utils.utilArticleQuery import select_article
from GradeServer.utils.utilUserQuery import select_member
from GradeServer.utils.utilSubmissionQuery import select_data_of_submission_board

from GradeServer.resource.sessionResources import SessionResources
from GradeServer.resource.languageResources import LanguageResources

from GradeServer.GradeServer_logger import Log
'''
Request Bad Check
'''
def get_is_check_request(form, name, checkOnValue, checkOffValue):
    try:
        form[name]
        return checkOnValue
    except BadRequest:
        return checkOffValue
    
def get_request_value(form, name):
    try:
        data = form[name]
        
        if type(data) != int:
            data = data.strip()
            data = data.replace('\r', '')
            if not len(data):
                raise Exception
        
        return data
    except (BadRequest, Exception):
        return None 
    
 
from GradeServer.resource.setResources import SETResources
'''
return authority boolean
'''
def is_authority(authority):
    isAdministrator, isUser = None, None
    
    try:
        if SETResources().const.ADMINISTRATOR in authority:
            isAdministrator = True
        if SETResources().const.USER in authority:
            isUser = True
            
        return (isAdministrator, isUser)
    except Exception:
        return (None, None)



'''
Access Authority Check
'''
def access_authority_check(problemLevel = None, memberIdIndex = None,
                           submissionIndex = None, problemIndex = None, submissionReplyIndex = None,
                           articleIndex = None, boardReplyIndex = None,
                           isAdministrator = None, isWrite = None, isCode = None):
    
    try:
        # Zero Index Check
        if memberIdIndex == 0\
           or problemIndex == 0\
           or submissionReplyIndex == 0\
           or (articleIndex == 0 and not isWrite)\
           or boardReplyIndex == 0:
            return False
        
        # Get Authority type Turple
        authority = is_authority(session[SessionResources().const.AUTHORITY])
        
        # Get my Index
        thisMemberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]
        
        # Authority check authority is turple, size 3
        if isAdministrator and authority[0]:
            if problemLevel\
                 and problemLevel not in (LanguageResources().const.GoldLevel[1],
                                          LanguageResources().const.SilverLevel[1],
                                          LanguageResources().const.BronzeLevel[1]):
                return False
            
            return True
        elif isAdministrator and not authority[0]:
            return False
        else:
            # Division Index
            if submissionIndex:
                submissionIndex = select_data_of_submission_board(submissionIndex).first()
                memberIdIndex = submissionIndex.memberIdIndex
                problemIndex = submissionIndex.problemIndex
                
            # MemberIdIndex Check
            if memberIdIndex\
               and not select_member(memberIdIndex).first():
                return False
            
            if problemIndex\
               and not course_problem_check(isAdministrator,
                                            authority,
                                            memberIdIndex,
                                            problemIndex,
                                            thisMemberIdIndex,
                                            isCode):
                return False
                    
            # Submission Reply Index check
            if submissionReplyIndex:
                replySubmissionIndex = select_replies_on_code(submissionIndex = None,
                                                              submissionReplyIndex = submissionReplyIndex).first()
                replySubmissionIndex = select_data_of_submission_board(replySubmissionIndex.submissionIndex).first()
                if not course_problem_check(isAdministrator,
                                            authority,
                                            replySubmissionIndex.memberIdIndex,
                                            replySubmissionIndex.problemIndex,
                                            thisMemberIdIndex,
                                            isCode):
                    return False
    
            # Board Check
            if articleIndex:
                article = select_article(articleIndex).first()
                if isWrite\
                   and article.writerIdIndex != thisMemberIdIndex:
                    return False
        # All Pass Authority
        return True
    except Exception as e:
        Log.error(str(e)) 
        return False


# Course Administrator Check CourseIndex
def course_problem_check(isAdministrator, authority, memberIdIndex, problemIndex,
                         thisMemberIdIndex, isCode):
    
    # Problem in Course Check
    if problemIndex:
        if not select_problem(problemIndex).first():
            return False
        if isCode\
           and authority[1]\
           and thisMemberIdIndex != memberIdIndex:
            return False
        
    return True