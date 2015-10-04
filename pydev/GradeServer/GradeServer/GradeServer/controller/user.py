# -*- coding: utf-8 -*-

from flask import request, render_template, url_for, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash

from GradeServer.utils.loginRequired import login_required
from GradeServer.utils.checkInvalidAccess import check_invalid_access

from GradeServer.utils.utilPaging import get_page_pointed, get_page_record
from GradeServer.utils.utilMessages import unknown_error
from GradeServer.utils.utilQuery import select_count
from GradeServer.utils.utilSubmissionQuery import submissions_sorted,\
                                                  select_all_submissions,\
                                                  select_member_chart_submissions
from GradeServer.utils.utilUserQuery import select_member,\
                                            update_members
from GradeServer.utils.utils import get_request_value

from GradeServer.resource.htmlResources import HTMLResources
from GradeServer.resource.routeResources import RouteResources
from GradeServer.resource.setResources import SETResources
from GradeServer.resource.sessionResources import SessionResources
from GradeServer.resource.languageResources import LanguageResources


from GradeServer.database import dao

from GradeServer import page_not_found
from GradeServer.GradeServer_logger import Log
from GradeServer.GradeServer_py3des import TripleDES
from GradeServer.GradeServer_blueprint import GradeServer


@GradeServer.teardown_request
def close_db_session(exception = None):
    """요청이 완료된 후에 db연결에 사용된 세션을 종료함"""
    try:
        dao.remove()
    except Exception as e:
        Log.error(str(e))
        
        
"""
로그인한 유저가 제출 했던 모든기록
"""
@GradeServer.route('/submission_record?memberIdIndex=<int:memberIdIndex>&page=<int:pageNum>&sortCondition=<sortCondition>')
@login_required
@check_invalid_access
def submission_record(memberIdIndex, sortCondition, pageNum):
    
    # Not Accept URL Check
    if sortCondition not in (LanguageResources().const.SubmissionDate[1],
                             LanguageResources().const.Memory[1],
                             LanguageResources().const.FileSize[1],
                             LanguageResources().const.Runtime[1]):
        return page_not_found()
    try:       
        # Get MemberId
        try:
            member = select_member(memberIdIndex).first()
        except Exception:
            member = []
            
                # 모든 제출 정보
        submissions = select_all_submissions(memberIdIndex).subquery()
         
        try:
                        # 차트 정보
            chartSubmissionRecords = select_member_chart_submissions(submissions).first()
        except Exception:
            #None Type Exception
            chartSubmissionRecords = []

        # Viiew Value Text
        chartSubmissionDescriptions = [LanguageResources().const.SolvedProblems,
                                       LanguageResources().const.Count,
                                       LanguageResources().const.Solved,
                                       LanguageResources().const.WrongAnswer,
                                       LanguageResources().const.TimeOver,
                                       LanguageResources().const.MemoryOverflow,
                                       LanguageResources().const.CompileError,
                                       LanguageResources().const.RuntimeError]
        
        try:                           
                        # 모든 제출 정보
            count = select_count(submissions.c.memberId).first().\
                                                         count  
            # Sorted
            submissionRecords = get_page_record(submissions_sorted(submissions,
                                                                   sortCondition = sortCondition,
                                                                   DESC = True),
                                                pageNum = pageNum).all()
        except Exception:
            count = 0
            submissionRecords = []

        return render_template(HTMLResources().const.SUBMISSION_RECORD_HTML,
                               memberIdIndex = memberIdIndex,
                               sortCondition = sortCondition,
                               member = member,
                               submissionRecords = submissionRecords,
                               chartSubmissionDescriptions = chartSubmissionDescriptions,
                               chartSubmissionRecords = chartSubmissionRecords,
                               pages = get_page_pointed(pageNum = pageNum,
                                                        count = count))
    except Exception as e:
        # Unknow Error
        return unknown_error(e)

"""
로그인한 유저가 권한이 필요한 페이지에 접급하기전
본인인지 확인하기 위한 페이지
"""
@GradeServer.route('/id_check?select=<select>', methods = ['GET', 'POST'])
@login_required
def id_check(select, error = None):
    if request.method == 'POST':
        password = get_request_value(form = request.form,
                                    name = 'password')
        if password:
            check = select_member(memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).first()
                                        
                            # 암호가 일치 할 때
            #Checking Success
            if len(password) <= 20\
               and check_password_hash (check.password,
                                        TripleDES.encrypt(str(password))):
                # for all user
                if select == 'account':
                    return redirect(url_for(RouteResources().const.EDIT_PERSONAL))
                # server manager
                elif SETResources().const.ADMINISTRATOR in session[SessionResources().const.AUTHORITY]:
                    if select == 'user_submit':
                        return redirect(url_for('.user_submit',
                                                pageNum = int(1)))
                    elif select == 'manage_problem':
                        return redirect(url_for('.manage_problem',
                                                problemLevel = LanguageResources().const.All[1],
                                                pageNum = int(1)))
                    elif select == 'manage_problem_set':
                        return redirect(url_for('.manage_problem_set',
                                                activeTabIndex = LanguageResources().const.All[1],
                                                pageNum = int(1)))
                    elif select == 'manage_user':
                        return redirect(url_for('.manage_user',
                                                sortCondition = LanguageResources().const.ID[1],
                                                filterCondition = ' ',
                                                keyWord = ' ',
                                                pageNum = int(1)))
                    elif select == 'manage_service':
                        return redirect(url_for('.manage_service'))
                        # 암호가 일치 하지 않을 때
            else:
                error = LanguageResources().const.WrongPassword
        else:
            error = LanguageResources().const.WrongPassword
               
    return render_template(HTMLResources().const.ID_CHECK_HTML,
                           error = error)

"""
로그인한 유저가 자신의 암호, 연락처 등을 바꿀수 있고
자신의 장보를 확인 할 수 있는 페이지
"""
@GradeServer.route('/edit_personal', methods = ['GET', 'POST'])
@login_required
@check_invalid_access
def edit_personal(error = None):
    contactNumber, emailAddress, comment = None, None, None
    try:
        #Get User Information
        try:
            members = select_member(memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).subquery()
            memberInformation = select_member(memberIdIndex = members.c.memberIdIndex).first()
        except Exception:
            memberInformation = []
        
        #Get Post
        if request.method == 'POST':
            password = get_request_value(form = request.form,
                                         name = 'password')
            passwordConfirm = get_request_value(form = request.form,
                                                name = 'passwordConfirm')
            #Get Updating Data
            contactNumber = get_request_value(form = request.form,
                                              name = 'contactNumber')
            emailAddress = get_request_value(form = request.form,
                                             name = 'emailAddress') 
            comment = get_request_value(form = request.form,
                                        name = 'comment')
            #Password Same
            if(password and passwordConfirm) and password == passwordConfirm:
                #Generate Password
                encryPassword = TripleDES.encrypt(str(password))
                passwordConfirm = None

                password = generate_password_hash(encryPassword)
                #Update DB
                update_members(select_member(memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]),
                               password,
                               contactNumber,
                               emailAddress,
                               comment)
            #Password Different
            elif not password and not passwordConfirm:
                #Update DB
                update_members(members = select_member(memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]),
                               password = None,
                               contactNumber = contactNumber,
                               emailAddress = emailAddress,
                               comment = comment)
            # Commit Exception
            try:
                dao.commit()
                
                return redirect(url_for(RouteResources().const.SIGN_IN))
            except Exception:
                dao.rollback()
                error = LanguageResources().const.DBFailed
        
        return render_template(HTMLResources().const.EDIT_PERSONAL_HTML,
                               memberInformation = memberInformation,
                               contactNumber = contactNumber,
                               emailAddress = emailAddress,
                               comment = comment,
                               error = error)
    except Exception as e:
        return unknown_error(e)
