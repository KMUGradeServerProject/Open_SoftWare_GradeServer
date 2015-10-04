# -*- coding: utf-8 -*-

from flask import request, redirect, url_for
from functools import wraps
from repoze.lru import lru_cache

from GradeServer.resource.routeResources import RouteResources
from GradeServer.resource.languageResources import LanguageResources

from GradeServer.utils.utilMessages import unknown_error
from __builtin__ import True

@lru_cache(maxsize=300)
def check_invalid_access(f):
    """
    Check invalid access through URL 
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            from GradeServer.utils.utils import access_authority_check,\
                                                get_request_value
            from GradeServer import page_not_found
            
            # Get URL Parameters
            problemLevel = get_request_value(kwargs,
                                             'problemLevel')
            memberIdIndex = get_request_value(kwargs,
                                              'memberIdIndex')
            submissionIndex = get_request_value(kwargs,
                                                'submissionIndex')
            problemIndex = get_request_value(kwargs,
                                             'problemIndex')
            submissionReplyIndex = get_request_value(kwargs,
                                                     'submissionReplyIndex')
            articleIndex = get_request_value(kwargs,
                                             'articleIndex')
            boardReplyIndex = get_request_value(kwargs,
                                                'boardReplyIndex')
            # unusual URL Access Check
            if not access_authority_check(problemLevel = (None if problemLevel == LanguageResources().const.All[1]
                                                          else problemLevel),
                                          memberIdIndex = (None if memberIdIndex == None
                                                           else int(memberIdIndex)),
                                          submissionIndex = (None if submissionIndex == None
                                                             else int(submissionIndex)),
                                          problemIndex = (None if problemIndex == None
                                                          else int(problemIndex)),
                                          submissionReplyIndex = (None if submissionReplyIndex == None
                                                                  else int(submissionReplyIndex)),
                                          articleIndex = (None if articleIndex == None
                                                          else int(articleIndex)),
                                          boardReplyIndex = (None if boardReplyIndex == None
                                                             else int(boardReplyIndex)),
                                          isAdministrator = 'manage' in request.endpoint,
                                          isWrite = (True if 'write' in request.endpoint
                                                     else None),
                                          isCode = (True if 'submission_code' in request.endpoint
                                                    else None)):
                
                return page_not_found()
    
            # URL direct access and manager case
            if not request.referrer and 'manage' in request.endpoint:
                return redirect(url_for(RouteResources().const.ID_CHECK,
                                        select = request.endpoint.split('.')[-1]))
            
            return f(*args, **kwargs)

        except Exception as e: 
            return unknown_error (e)

    return decorated_function
