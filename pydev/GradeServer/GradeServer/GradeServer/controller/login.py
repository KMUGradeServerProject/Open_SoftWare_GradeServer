# -*- coding: utf-8 -*-
"""
    GradeSever.controller.login
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    로그인 확인 데코레이터와 로그인 처리 모듈.

    :copyright: (c) 2015 by KookminUniv

"""
"""
bug reporting

if path is a/b/c/d, it can't recognize any .css and .js file.
(a/b/c is okay)
"""
from flask import request, redirect, session, url_for, render_template
from datetime import datetime

from GradeServer.database import dao
from GradeServer.GradeServer_blueprint import GradeServer

from GradeServer.utils.utilArticleQuery import select_notices
from GradeServer.utils.utilUserQuery import select_match_member_id,\
                                            update_recent_access_date
from GradeServer.utils.utilRankQuery import select_top_coder
from GradeServer.utils.utils import get_request_value

from GradeServer.resource.htmlResources import HTMLResources
from GradeServer.resource.sessionResources import SessionResources
from GradeServer.resource.languageResources import LanguageResources

from werkzeug.security import check_password_hash
from GradeServer.GradeServer_py3des import TripleDES
                
@GradeServer.teardown_request
def close_db_session(exception = None):
    """요청이 완료된 후에 db연결에 사용된 세션을 종료함"""
    try:
        dao.remove()
    except Exception as e:
        from GradeServer.GradeServer_logger import Log
        Log.error(str(e))


def check_user_info(request_form, error = None):
    checker = True
    language = {'kr':0, # default
                'en':1}
        
    for form in request_form:
            if "language" in form:
                checker = False
                lang = get_request_value(form = request.form,
                                         name = 'language')
                session['language'] = language[lang]
                
    if checker: 
        try:
            """ DB Password check """
            memberId = get_request_value(form = request.form,
                                         name = 'memberId')
            password = get_request_value(form = request.form,
                                         name = 'password')
            
            check = select_match_member_id(memberId = memberId).first()
            
            #Checking Success
            if memberId == memberId\
               and check_password_hash(check.password,
                                       TripleDES.encrypt(str(password))):
                #push Session Cache 
                session[SessionResources().const.MEMBER_ID_INDEX] = check.memberIdIndex
                session[SessionResources().const.MEMBER_ID] = memberId
                session[SessionResources().const.MEMBER_NAME] = check.memberName
                session[SessionResources().const.AUTHORITY] = list(check.authority)
                session[SessionResources().const.LAST_ACCESS_DATE] = datetime.now()
                
                # set default language
                session['language'] = language['kr']
                                            
                # Commit Exception
                try:
                    update_recent_access_date(session[SessionResources().const.MEMBER_ID_INDEX],
                                              datetime.now())
                    dao.commit()
                except Exception:
                    dao.rollback()
                    error = LanguageResources().const.DBFailed
            else:
                error = LanguageResources().const.WrongPassword
        # Not Exist MemberId
        except Exception:
            error = LanguageResources().const.WrongPassword
        # Return Login Page
        return error
        
"""
메인 페이지 및 로그인 관리 
"""
@GradeServer.route('/', methods = ['GET', 'POST'])
def sign_in():
    '''
    @@ Success sign in flash
    
    When the page redirected from sign up page,
    It display flash message.    
    '''
        
    """ main page before sign in"""
    error = None
    if request.method == 'POST':       
        error = check_user_info(request.form)
                    
    isLogin = len(session._get_current_object())
    if isLogin:
        isLogin = session[SessionResources().const.MEMBER_ID_INDEX]
        memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]
    else:
        memberIdIndex = None
        
    return render_template(HTMLResources().const.MAIN_HTML,
                           noticeRecords = select_notices(memberIdIndex,
                                                          isLogin),
                           topCoders = select_top_coder(),
                           error = error)
               
        
"""   
로그아웃
"""
from GradeServer.utils.loginRequired import login_required
@GradeServer.route ('/signout')
@login_required
def sign_out():
    """ Log Out """
    # 세션 클리어
    session.clear()
    # 메인 페이지로 옮기기
    from GradeServer.resource.routeResources import RouteResources
    return redirect(url_for(RouteResources().const.SIGN_IN))

"""
새 페이지에서 로그인
"""
@GradeServer.route("/sign_in?to=<to>&params=<params>", methods=["GET", "POST"])
def sign_in_newPage(to, params, error = None):

    if request.method == "POST":        
        error = check_user_info(request.form)
                    
    isLogin = len(session._get_current_object())
    if isLogin:
        isLogin = session[SessionResources().const.MEMBER_ID_INDEX]
    else:
        return render_template("signin.html")
    
    # params = {a:b, c:d}
    params = params[1:-1].encode('utf8').split(', ')
    tmp_params = params
    params = []
    
    for i in tmp_params:
        key, value = i.split(':')
        key = key.replace('\'', '')
        value = value.lstrip()
        
        if key == 'pageNum': key = 'page'
        
        params.append(key+'='+value)
    
    def getkey(item):
        return item.split('=')[0]
    
    params = sorted(params, key=getkey)
    params = '%26'.join(params) # %26 == &
    params = params.replace('u\'', '')
    params = params.replace('\'', '')
    
    return redirect(request.url_root+to+"%3F"+params) # %3F == ?