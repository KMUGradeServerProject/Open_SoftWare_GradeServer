# -*- coding: utf-8 -*-
import os
import socket

from flask import request, session, render_template, url_for, redirect, flash, Response

from datetime import datetime

from GradeServer.utils.loginRequired import login_required
from GradeServer.utils.checkInvalidAccess import check_invalid_access

from GradeServer.utils.parameter.articleParameter import ArticleParameter

from GradeServer.utils.utilPaging import get_page_pointed, get_page_record
from GradeServer.utils.utilQuery import select_count
from GradeServer.utils.utilSubmissionQuery import submissions_sorted,\
                                                  select_last_submissions,\
                                                  select_all_submissions,\
                                                  select_submissions_result,\
                                                  select_submissions_peoples_counts,\
                                                  select_solved_peoples_counts,\
                                                  select_submitted_records_of_problem,\
                                                  select_problem_chart_submissions,\
                                                  select_solved_submissions,\
                                                  select_submitted_files,\
                                                  select_data_of_submission_board,\
                                                  select_code_is_like,\
                                                  insert_replies_on_code,\
                                                  update_code_view_reply_counting,\
                                                  select_replies_on_code,\
                                                  update_replies_on_code_delete,\
                                                  update_replies_on_code_modify,\
                                                  select_replies_on_code_like,\
                                                  insert_likes_on_code,\
                                                  update_code_is_like,\
                                                  update_code_like_counting,\
                                                  select_replies_on_code_is_like,\
                                                  insert_likes_on_reply_of_code,\
                                                  update_replies_on_code_is_like,\
                                                  update_replies_on_code_like_counting,\
                                                  select_failed_problems
from GradeServer.utils.utilProblemQuery import join_problems_name,\
                                               join_problem_lists_submissions,\
                                               select_problem,\
                                               select_all_problems
from GradeServer.utils.utilUserQuery import join_member_id
from GradeServer.utils.utilCodeSubmissionQuery import select_all_languages                                               
from GradeServer.utils.utils import is_authority,\
                                    get_request_value
from GradeServer.utils.utilMessages import unknown_error
from GradeServer.controller.codeSubmission import page_move

from GradeServer.resource.setResources import SETResources
from GradeServer.resource.htmlResources import HTMLResources
from GradeServer.resource.routeResources import RouteResources
from GradeServer.resource.otherResources import OtherResources
from GradeServer.resource.languageResources import LanguageResources
from GradeServer.resource.sessionResources import SessionResources
from GradeServer.resource.enumResources import ENUMResources

from GradeServer.database import dao

from GradeServer.GradeServer_logger import Log
from GradeServer import page_not_found
from GradeServer.GradeServer_blueprint import GradeServer


def make_wrong_test_case_path(problemPath, problemName, checkType, testCase):
    return '%s/%s_%s/%s_case%s_input.txt' %(problemPath, problemName, checkType, problemName, testCase)

@GradeServer.teardown_request
def close_db_session(exception = None):
    '''요청이 완료된 후에 db연결에 사용된 세션을 종료함'''
    try:
        dao.remove()
    except Exception as e:
        Log.error(str(e))


'''
Registered Problem list of course
'''
@GradeServer.route('/problem_list?page=<int:pageNum>')
@login_required
@check_invalid_access
def problem_list(pageNum):
    """ problem submitting page """
    try:
        # Get Last Submitted History
        lastSubmission = select_last_submissions(memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).subquery()
        
        # Current Submission                                      
        submissions = select_submissions_result(lastSubmission).subquery()

        # Get Problem Informations
        problems = select_all_problems().subquery()
        
        # Get ProblemList Count
        # Get ProblemListRecords OuterJoin
        try:
            count = select_count(problems.c.problemIndex).first().\
                                                          count
                                                      
            problemListRecords = get_page_record(join_problem_lists_submissions(problems,
                                                                                submissions),
                                                 pageNum = pageNum).all()
        
        except Exception:
            count = 0
            problemListRecords = []

        # Get Course Information
        
        browserName = request.user_agent.browser
        browserVersion = request.user_agent.version
        wrongTestCaseText = {}
        for problemListRecord in problemListRecords:
            if problemListRecord.wrongTestCaseNumber != 0:
                try:
                    f = open(make_wrong_test_case_path(str(problemListRecord.problemPath),
                                                   str(problemListRecord.problemName),
                                                   str(problemListRecord.solutionCheckType),
                                                   str(problemListRecord.wrongTestCaseNumber)), "r")
                    temp = {problemListRecord.problemName : f.read()}
                    wrongTestCaseText.update(temp)
                    f.close()
                except:
                    pass

        return render_template(HTMLResources().const.PROBLEM_LIST_HTML,
                               problemListRecords = problemListRecords,
                               wrongTestCaseText = wrongTestCaseText,
                               browserName = browserName,
                               browserVersion = browserVersion,
                               datetime = datetime.now(),
                               pages = get_page_pointed(pageNum = pageNum,
                                                        count = count))
    except Exception as e:
        return unknown_error(e)



@GradeServer.route('/problem?problemIndex=<int:problemIndex>&page=<int:pageNum>')
@login_required
@check_invalid_access
def problem(problemIndex, pageNum):
    """
    use db to get its problem page
    now, it moves to just default problem page
    """
    try :
        # are Not Access. conditions is an Administrator and endOfSubmission ago
        # languages of Course
        try:
            
            languageInfoRecords = select_all_languages()
        except Exception:
            languageInfoRecords = []

        try:
            problemInformation = select_problem(problemIndex = problemIndex).first()
        except Exception:
            problemInformation = []    

        problemName = problemInformation.problemName.replace(' ', '')
        pdfExists = os.path.exists(OtherResources().const.PDF_PATH %(problemName, problemName))
        browserName = request.user_agent.browser
        browserVersion = request.user_agent.version
        
        return render_template(HTMLResources().const.PROBLEM_HTML,
                               problemIndex = problemIndex,
                               problemInformation = problemInformation,
                               languageInfoRecords = languageInfoRecords,
                               pdfExists = pdfExists,
                               problemName = problemName,
                               pageNum = pageNum,
                               browserName = browserName,
                               datetime = datetime.now(),
                               browserVersion = browserVersion)
    
    except Exception as e:
        return unknown_error(e)
    
    

'''
problem Submitted Record of course
status is submitted result
'''
@GradeServer.route('/problem_record?problemIndex=<int:problemIndex>&status=<status>&sortCondition=<sortCondition>', methods = ['GET', 'POST'])
@login_required
@check_invalid_access
def problem_record(status, problemIndex, sortCondition, error = None):
    # Not Accept URL Check
    if sortCondition not in (LanguageResources().const.SubmissionDate[1],
                             LanguageResources().const.Memory[1],
                             LanguageResources().const.FileSize[1],
                             LanguageResources().const.Runtime[1]):
        return page_not_found()
    
    try:
        memberId = None
        # Request Post
        if request.method == 'POST':
            # Search Event
            if 'memberId' in request.form:
                memberId = get_request_value(form = request.form,
                                             name = 'memberId')
                        

        # Chart View Value Text
        chartSubmissionDescriptions = [LanguageResources().const.TriedPeople,
                                       LanguageResources().const.SolvedPeople,
                                       LanguageResources().const.Count,
                                       LanguageResources().const.Solved,
                                       LanguageResources().const.WrongAnswer,
                                       LanguageResources().const.TimeOver,
                                       LanguageResources().const.MemoryOverflow,
                                       LanguageResources().const.CompileError,
                                       LanguageResources().const.RuntimeError]
        
        # last Submissions of Problem Info
        lastSubmission = select_last_submissions(problemIndex = problemIndex).subquery()
        submissions = select_all_submissions(problemIndex = problemIndex,
                                             lastSubmission = lastSubmission).subquery()
        try:
            # Submitted Members Count
            sumOfSubmissionPeopleCount = select_submissions_peoples_counts(submissions).subquery()
            # Solved Members Count
            sumOfSolvedPeopleCount = select_solved_peoples_counts(submissions).subquery()
            # Problem Record
            problemSubmittedRecords = select_submitted_records_of_problem(problemIndex = problemIndex).subquery()
            # Chart SubmissionRecords
            chartSubmissionRecords = select_problem_chart_submissions(sumOfSubmissionPeopleCount,
                                                                      sumOfSolvedPeopleCount,
                                                                      problemSubmittedRecords).first()
        except Exception:
            chartSubmissionRecords = []
       
        # Problem Information (LimitedTime, LimitedMemory
        try:
            problemInformation = select_problem(problemIndex = problemIndex).first()
        except Exception:
            problemInformation = []
            
        # Problem Solved Users
        try:
            # Problem Solved Member
            problemSolvedMemberRecords = submissions_sorted(select_solved_submissions(submissions).subquery(),
                                                            sortCondition = sortCondition).all()
        except Exception:
            problemSolvedMemberRecords = []
        
        # Search Failed Problem
        if status != ENUMResources().const.SOLVED\
           and status != ENUMResources().const.JUDGING\
           and status != ENUMResources().const.SERVER_ERROR:
            try:
                # last Submissions of Problem Info
                lastSubmission = select_last_submissions(memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX],
                                                         problemIndex = problemIndex).subquery()
                submissions = select_all_submissions(memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX],
                                                     problemIndex = problemIndex,
                                                     lastSubmission = lastSubmission).subquery()
                # Current Failed Problem
                failedProblem = select_failed_problems(submissions).first()
            except Exception:
                failedProblem = []
        else:
            failedProblem = []

        return render_template(HTMLResources().const.PROBLEM_RECORD_HTML,
                               memberId = memberId,
                               status =  status,
                               problemSolvedMemberRecords = problemSolvedMemberRecords,
                               problemInformation = problemInformation,
                               chartSubmissionDescriptions = chartSubmissionDescriptions,
                               chartSubmissionRecords = chartSubmissionRecords,
                               failedProblem = failedProblem,
                               error = error)
    except Exception as e:
        return unknown_error(e)
    
 
'''
show submitted Code file 
status is submitted result
'''    
@GradeServer.route('/submission_code?memberIdIndex=<int:memberIdIndex>&problemIndex<int:problemIndex>&status=<status>', methods = ['GET', 'POST'])
@login_required
@check_invalid_access
def submission_code(memberIdIndex, status, problemIndex, error = None):
    try:
        # Get endDateOfSubmission of Problem
        # are Not Access. conditions is an Administrator and endOfSubmission ago
        if SETResources().const.ADMINISTRATOR in session[SessionResources().const.AUTHORITY]\
           or memberIdIndex == session[SessionResources().const.MEMBER_ID_INDEX]:
            
            # Get SubmissionIndex
            dataOfSubmissionBoard = select_data_of_submission_board(None,
                                                                    memberIdIndex,
                                                                    problemIndex)
            if dataOfSubmissionBoard.first():
                submissionIndex = dataOfSubmissionBoard.first().submissionIndex
                                # 내가 Code에 누른 좋아요 정보
                try:
                    isLikeCancelled = select_code_is_like(submissionIndex,
                                                          memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).first().\
                                                          isLikeCancelled
                except Exception:
                    # Non-Exist Case
                    isLikeCancelled = None
            
                if request.method == 'POST':
                    authorityCheck = is_authority(session[SessionResources().const.AUTHORITY])
                    
                    for form in request.form:
                                        # 댓글 달기
                        if form == 'writeCodeReply':
                                                # 새로운 댓글 정보articleParameter
                            codeReplyContent = get_request_value(form = request.form,
                                                                 name = 'writeCodeReply')
                            
                            if codeReplyContent:
                                dao.add(insert_replies_on_code(submissionIndex,
                                                               memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX],
                                                               articleParameter = ArticleParameter(title = None,
                                                                                                   content = codeReplyContent,
                                                                                                   updateIp = socket.gethostbyname(socket.gethostname()),
                                                                                                   updateDate = datetime.now())))
                                # remove duplicated read count
                                update_code_view_reply_counting(submissionIndex,
                                                                VIEW_INCREASE = -1,
                                                                REPLY_INCREASE = 1)
                                
                            break 
                                                # 댓글 삭제   
                        elif 'deleteCodeReply' in form:
                            # Get Reply Index
                            replyIndex = len('deleteCodeReply')
                            submissionReplyIndex = int(form[replyIndex:])
                                                  
                            try:
                                writerIndex = select_replies_on_code(submissionIndex = None,
                                                                     submissionReplyIndex = submissionReplyIndex).first()
                            except Exception:
                                writerIndex = None
                            if (authorityCheck[0] or authorityCheck[1])\
                               or writerIndex.codeReplierIdIndex == session['memberIdIndex']:
                                    
                                update_replies_on_code_delete(submissionReplyIndex,
                                                              isDeleted = ENUMResources().const.TRUE)
                                # remove duplicated read count
                                update_code_view_reply_counting(submissionIndex,
                                                                VIEW_INCREASE = -1,
                                                                REPLY_INCREASE = -1)
                            else:
                                error = LanguageResources().const.GetOutHere
                            
                            break 
                        # Commit Modify
                        elif 'modifyCodeReplyContent' in form:
                            replyIndex = len('modifyCodeReplyContent')
                            submissionReplyIndex = int(form[replyIndex:])
                            try:
                                writerIndex = select_replies_on_code(submissionIndex = None,
                                                                     submissionReplyIndex = submissionReplyIndex).first()
                            except Exception:
                                writerIndex = None
                            if writerIndex.codeReplierIdIndex == session['memberIdIndex']:
                                submissionReplyContent = get_request_value(form = request.form,
                                                                           name = 'modifyCodeReplyContent{0}'.format(form[replyIndex:]))
                                
                                if submissionReplyContent:
                                    #update comment
                                    update_replies_on_code_modify(submissionReplyIndex,
                                                                  ArticleParameter(title = None,
                                                                                   content = submissionReplyContent,
                                                                                   updateIp = socket.gethostbyname(socket.gethostname()),
                                                                                   updateDate = datetime.now()))
                                    # remove duplicated read count
                                    update_code_view_reply_counting(submissionIndex,
                                                                    VIEW_INCREASE = -1)
                            else:
                                error = LanguageResources().const.GetOutHere
                                
                            break
                    # end Loop
                    # Commit Exception
                    try:
                        dao.commit()
                    except Exception:
                        dao.rollback()
                        error = LanguageResources().const.DBFailed
                
                try:
                    # replies 정보
                    repliesOnSubmissionRecords = select_replies_on_code(submissionIndex).subquery()
                    repliesOnSubmissionRecords = join_member_id(repliesOnSubmissionRecords,
                                                                repliesOnSubmissionRecords.c.codeReplierIdIndex)
                                        # 내가 게시글 리플에 누른 좋아요 정보
                    repliesOnSubmissionIsLikeRecords = select_replies_on_code_like(repliesOnSubmissionRecords.subquery(),
                                                                                   session[SessionResources().const.MEMBER_ID_INDEX]).all()
                    repliesOnSubmissionRecords = repliesOnSubmissionRecords.all()  
                except Exception:
                    repliesOnSubmissionIsLikeRecords = []
                    repliesOnSubmissionRecords = []
                    
                                # 읽은 횟수 카운팅
                update_code_view_reply_counting(submissionIndex,
                                                VIEW_INCREASE = 1)
                
                # Commit Exception
                try:
                    dao.commit()
                except Exception:
                    dao.rollback()
                    
                # Problem Information (LimitedTime, LimitedMemory
                try:
                    problemName = select_problem(problemIndex = problemIndex).first().\
                                                                              problemName
                except Exception:
                    problemName = None
                    
                # Problem Solved Users
                try:
                    # last Submissions Info
                    lastSubmission = select_last_submissions(memberIdIndex = memberIdIndex,
                                                             problemIndex = problemIndex).subquery()
                    problemSolvedMemberRecords = select_all_submissions(memberIdIndex = memberIdIndex,
                                                                        problemIndex = problemIndex,
                                                                        lastSubmission = lastSubmission).first()
                except Exception:
                    problemSolvedMemberRecords = []
                    
                # Submitted Files Information
                import codecs
                try:
                    submittedFileRecords = select_submitted_files(dataOfSubmissionBoard.subquery()).all()
                    fileData = []
                    
                    for raw in submittedFileRecords:
                        # Open
                        filePath = '{0}/{1}'.format(raw.filePath,
                                                    raw.fileName)
                        # EUC_KR type
                        try:
                            with codecs.open(filePath,
                                             'r',
                                             encoding = 'cp949') as f:
                                # Read
                                data = f.read()
                                fileData.append(data)
                        # UTF-8 Type
                        except Exception:
                            with codecs.open(filePath,
                                             'r',
                                             encoding = 'utf8') as f:
                                # Read
                                data = f.read()
                                fileData.append(data)
                except Exception:
                    submittedFileRecords = []
                    fileData = []
                    
                return render_template(HTMLResources().const.SUBMISSION_CODE_HTML,
                                       memberIdIndex = memberIdIndex,
                                       submissionIndex = submissionIndex,
                                       submittedFileRecords = submittedFileRecords,
                                       fileData = fileData,
                                       problemName = problemName,
                                       problemSolvedMemberRecords = problemSolvedMemberRecords,
                                       isLikeCancelled = isLikeCancelled,
                                       sumOfLikeCount = dataOfSubmissionBoard.first().\
                                                                              sumOfLikeCount,
                                       repliesOnSubmissionIsLikeRecords = repliesOnSubmissionIsLikeRecords,
                                       repliesOnSubmissionRecords = repliesOnSubmissionRecords,
                                       browserName = request.user_agent.browser,
                                       browserVersion = request.user_agent.version,
                                       error = error)
        #Access Rejection
        else:
            return redirect(url_for(RouteResources().const.PROBLEM_RECORD,
                                    status = status,
                                    problemIndex = problemIndex,
                                    sortCondition = LanguageResources().const.SubmissionDate[1]))
    except Exception as e:
        return unknown_error(e)


'''
Submission Click Like
'''
@GradeServer.route('/code_like_click?submissionIndex=<int:submissionIndex>', methods = ['POST'])
@login_required
@check_invalid_access
def code_like_click(submissionIndex):
        # 게시글 좋아요  Push
        # 내가 게시글에 누른 좋아요 정보
    try:
        isLikeCancelled = select_code_is_like(submissionIndex,
                                              memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).first().\
                                              isLikeCancelled
    except Exception:
        # Non-Exist Case
        isLikeCancelled = None
            
        # 좋아요를 누른적 없을 때
    if not isLikeCancelled:
        # Insert Like
        dao.add(insert_likes_on_code(submissionIndex,
                                     memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]))
        # Counting +1
        LIKE_INCREASE = 1
    else:
                                # 다시 좋아요 누를 때
        if isLikeCancelled == ENUMResources().const.TRUE:
            # Counting +1
            LIKE_INCREASE = 1
            isLikeCancelled = ENUMResources().const.FALSE
                                # 좋아요 취소 할 때
        else:  # if it's already exist then change the value of 'pushedLike'
            # Counting -1
            LIKE_INCREASE = -1
            isLikeCancelled = ENUMResources().const.TRUE
            
        # Update Like
        update_code_is_like(submissionIndex,
                            memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX],
                            isLikeCancelled = isLikeCancelled)
    # Article 좋아요 갯수 올리기
    update_code_like_counting(submissionIndex,
                              LIKE_INCREASE = LIKE_INCREASE)
    
    try:
        dao.commit()
        # return like count
        try:
            count =  select_data_of_submission_board(submissionIndex,
                                                     memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).first().\
                                                     sumOfLikeCount
        except Exception:
            count = 0
        
        return Response(str(count))
    except Exception:
        dao.rollback()
        
    return Response()



    
'''
Submission Reply Click Like
'''
@GradeServer.route('/code_reply_like_click?submissionReplyIndex=<int:submissionReplyIndex>', methods = ['POST'])
@login_required
@check_invalid_access
def code_reply_like_click(submissionReplyIndex):
        # 댓글 좋아요
        # 내가 Reply에 누른 좋아요 정보
    try:
        isReplyLike = select_replies_on_code_is_like(submissionReplyIndex,
                                                     memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]).first().\
                                                                                                                                         isLikeCancelled
    except Exception:
        # Non-Exist Case
        isReplyLike = None
        
                        # 좋아요를 누른적 없을 때
    if not isReplyLike:
        # Insert Like
        dao.add(insert_likes_on_reply_of_code(submissionReplyIndex,
                                              memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX]))
        # Counting +1
        LIKE_INCREASE = 1
    else:
                                # 다시 좋아요 누를 때
        if isReplyLike == ENUMResources().const.TRUE:
            # Counting +1
            LIKE_INCREASE = 1
            isLikeCancelled = ENUMResources().const.FALSE
                                # 좋아요 취소 할 때
        else:  # if it's already exist then change the value of 'pushedLike'
            # Counting -1
            LIKE_INCREASE = -1
            isLikeCancelled = ENUMResources().const.TRUE
            
        # Update Like
        update_replies_on_code_is_like(submissionReplyIndex,
                                       memberIdIndex = session[SessionResources().const.MEMBER_ID_INDEX],
                                       isLikeCancelled = isLikeCancelled)
            
    # Like or UnLIke
    update_replies_on_code_like_counting(submissionReplyIndex,
                                         LIKE_INCREASE = LIKE_INCREASE)
    try:
        dao.commit()
        
        # return like count
        try:
            count = select_replies_on_code(submissionIndex = None,
                                           submissionReplyIndex = submissionReplyIndex).first().\
                                                                                        sumOfLikeCount
        except Exception:
            count = 0
        
        return Response(str(count))
    except Exception:
        dao.rollback()
        
    return Response()
