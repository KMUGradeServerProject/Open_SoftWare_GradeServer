
# -*- coding: utf-8 -*-

from sqlalchemy import func, and_, or_

from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.languageResources import LanguageResources


from GradeServer.utils.utilProblemQuery import join_problems_name
from GradeServer.utils.utilUserQuery import join_member_id

from GradeServer.database import dao
from GradeServer.model.dataOfSubmissionBoard import DataOfSubmissionBoard
from GradeServer.model.languages import Languages
from GradeServer.model.submittedFiles import SubmittedFiles
from GradeServer.model.submissions import Submissions
from GradeServer.model.submittedRecordsOfProblems import SubmittedRecordsOfProblems
from GradeServer.model.likesOnSubmission import LikesOnSubmission
from GradeServer.model.likesOnReplyOfSubmission import LikesOnReplyOfSubmission
from GradeServer.model.repliesOnSubmission import RepliesOnSubmission

'''
select SubmittedCodeOnBoard
'''
def select_data_of_submission_board(submissionIndex, memberIdIndex = None, problemIndex = None):
    # 어떤 소속의 특정 과목 또는 문제 또는 인원에 대하여
    return dao.query(DataOfSubmissionBoard).\
               filter(DataOfSubmissionBoard.submissionIndex == submissionIndex if submissionIndex
                      else (DataOfSubmissionBoard.problemIndex == problemIndex if problemIndex
                            else DataOfSubmissionBoard.problemIndex != None),
                           (DataOfSubmissionBoard.memberIdIndex == memberIdIndex if memberIdIndex
                            else DataOfSubmissionBoard.memberIdIndex != None))
                                       
                        
'''
Submissions to Last Submitted
'''
def select_last_submissions(memberIdIndex = None, problemIndex = None):
    
    # Submissions Table join Keys 
    dataOfSubmissionBoard = select_data_of_submission_board(None,
                                                            memberIdIndex,
                                                            problemIndex).subquery()
    
    submissions = dao.query(dataOfSubmissionBoard.c.memberIdIndex,
                            dataOfSubmissionBoard.c.problemIndex,
                            dataOfSubmissionBoard.c.viewCount,
                            dataOfSubmissionBoard.c.submissionReplyCount,
                            dataOfSubmissionBoard.c.sumOfLikeCount,
                            Submissions).\
                      join(Submissions,
                           dataOfSubmissionBoard.c.submissionIndex == Submissions.submissionIndex).subquery()

    return dao.query(dataOfSubmissionBoard,
                     submissions.c.codeSubmissionDate,
                     func.max(submissions.c.submissionCount).label('submissionCount'),
                     func.max(submissions.c.solutionCheckCount).label('solutionCheckCount')).\
               join(submissions,
                    dataOfSubmissionBoard.c.submissionIndex == submissions.c.submissionIndex).\
               group_by(submissions.c.submissionIndex)



               
'''
Submissions to Last Submitted between any days
'''
def select_between_days_last_submissions(submissions, submissionDatePeriod):
    return dao.query(submissions).\
               filter(submissions.c.codeSubmissionDate.\
                                    between(submissionDatePeriod['start'], 
                                            submissionDatePeriod['end']))
                   
                   
'''
All Submission Record
'''
def select_all_submissions(memberIdIndex = None, problemIndex = None, lastSubmission = None):
   
    if lastSubmission == None:
        # Submissions Table join Keys 
        dataOfSubmissionBoard = select_data_of_submission_board(None,
                                                                memberIdIndex,
                                                                problemIndex).subquery()
        submissions = dao.query(dataOfSubmissionBoard.c.memberIdIndex,
                                dataOfSubmissionBoard.c.problemIndex,
                                dataOfSubmissionBoard.c.viewCount,
                                dataOfSubmissionBoard.c.submissionReplyCount,
                                dataOfSubmissionBoard.c.sumOfLikeCount,
                                Submissions).\
                          join(Submissions, 
                               dataOfSubmissionBoard.c.submissionIndex == Submissions.submissionIndex).\
                          subquery()
    # lastSubmissions Not None Case (Problem Submitted Records)
    else:
        submissions = dao.query(lastSubmission.c.memberIdIndex,
                                lastSubmission.c.problemIndex,
                                lastSubmission.c.viewCount,
                                lastSubmission.c.submissionReplyCount,
                                lastSubmission.c.sumOfLikeCount,
                                Submissions).\
                      join(Submissions,
                           and_(lastSubmission.c.solutionCheckCount == Submissions.solutionCheckCount,
                                lastSubmission.c.submissionIndex == Submissions.submissionIndex)).\
                      group_by(Submissions.submissionIndex).\
                      subquery()
                          
    submissions = join_languages_name(submissions,
                                      submissions.c.usedLanguageIndex).subquery()
    submissions = join_problems_name(submissions,
                                     submissions.c.problemIndex).subquery()
    submissions = join_member_id(submissions,
                                 submissions.c.memberIdIndex)
                                         
    return submissions
  


'''
get Language Name
'''
def join_languages_name(subquery, subLanguageIndex, isDeleted = ENUMResources().const.FALSE):
    return dao.query(subquery,
                     Languages.languageName,
                     Languages.languageVersion).\
               outerjoin(Languages,
                         Languages.languageIndex == subLanguageIndex)
               
               
               
'''
Join Registrations in member Submissions
'''  
def join_registrations_submissions(members, submissions):
    submissions =  dao.query(members,
                             submissions.c.problemIndex,
                             submissions.c.status,
                             submissions.c.codeSubmissionDate,
                             submissions.c.runTime,
                             submissions.c.usedMemory,
                             submissions.c.sumOfSubmittedFileSize,
                             submissions.c.score).\
                        outerjoin(submissions,
                                  members.c.memberIdIndex == submissions.c.memberIdIndex).\
                        subquery()
    submissions = dao.query(submissions).\
                      order_by(submissions.c.memberId.asc())
    
    return submissions


               
'''
Submissions 검색
'''
def search_submissions(submissions, filterFindParameter):
    # condition은 All, courseName, problemName, memberId로 나누어서 검새
    if filterFindParameter.filterCondition == LanguageResources().const.All[1]: # Filters[0] is '모두'
        submissions = dao.query(submissions).\
                          filter(or_(submissions.c.problemName.like('%' + filterFindParameter.keyWord + '%'),
                                     submissions.c.memberId == filterFindParameter.keyWord))
    elif filterFindParameter.filterCondition == LanguageResources().const.Problem[1]: # Filters[2] is 'ProblemName'
        submissions = dao.query(submissions).\
                          filter(submissions.c.problemName.like('%' + filterFindParameter.keyWord + '%'))
    else: # Filters[3] is 'MembmerId'
        submissions = dao.query(submissions).\
                          filter(submissions.c.memberId == filterFindParameter.keyWord)

    return submissions
  
 
''' 
 Current Submissions
'''
def select_submissions_result(lastSubmission):
    return dao.query(Submissions.score,
                     Submissions.status,
                     Submissions.compileErrorMessage,
                     Submissions.wrongTestCaseNumber,
                     lastSubmission).\
               join(lastSubmission,
                    and_(Submissions.submissionIndex == lastSubmission.c.submissionIndex,
                         Submissions.submissionCount == lastSubmission.c.submissionCount))
                      
                                                       
'''
Get SubmittedFiles
'''
def select_submitted_files(submissionCodeOnBoard):
    return dao.query(SubmittedFiles).\
               filter(SubmittedFiles.submissionIndex == submissionCodeOnBoard.c.submissionIndex)
                                       
                                       
                                                                         
'''
Submissions Sorting Condition
'''
def submissions_sorted(submissions, sortCondition = LanguageResources().const.SubmissionDate[1], DESC = None):
    
        # 제출날짜, 실행 시간, 사용 메모리, 코드 길이 순 정렬
    if sortCondition == LanguageResources().const.SubmissionDate[1]:
        submissionRecords = dao.query(submissions).\
                                order_by((submissions.c.codeSubmissionDate.desc() if DESC
                                          else submissions.c.codeSubmissionDate.asc()),
                                         submissions.c.runTime.asc(),
                                         submissions.c.usedMemory.asc(),
                                         submissions.c.sumOfSubmittedFileSize.asc())
        # 실행 시간, 사용 메모리, 코드 길이, 제출날짜 순 정렬
    elif sortCondition == LanguageResources().const.Runtime[1]:
        submissionRecords = dao.query(submissions).\
                                order_by(submissions.c.runTime.asc(),
                                         submissions.c.usedMemory.asc(),
                                         submissions.c.sumOfSubmittedFileSize.asc(),
                                         (submissions.c.codeSubmissionDate.desc() if DESC
                                          else submissions.c.codeSubmissionDate.asc()))
        # 사용 메모리, 실행 시간, 코드 길이, 제출날짜 별 정렬
    elif sortCondition == LanguageResources().const.Memory[1]:
        submissionRecords = dao.query(submissions).\
                                order_by(submissions.c.usedMemory.asc(),
                                         submissions.c.runTime.asc(),
                                         submissions.c.sumOfSubmittedFileSize.asc(),
                                         (submissions.c.codeSubmissionDate.desc() if DESC
                                          else submissions.c.codeSubmissionDate.asc()))
        # 코드 길이, 사용 메모리, 실행 시간, 제출날짜 별 정렬         
    elif sortCondition == LanguageResources().const.FileSize[1]:
        submissionRecords = dao.query(submissions).\
                                order_by(submissions.c.sumOfSubmittedFileSize.asc(),
                                         submissions.c.runTime.asc(),
                                         submissions.c.usedMemory.asc(),
                                         (submissions.c.codeSubmissionDate.desc() if DESC
                                          else submissions.c.codeSubmissionDate.asc()))  
                                 
    return submissionRecords



'''
Solved Submissions
'''
def select_solved_submissions(submissions):
    return dao.query(submissions).\
               filter(submissions.c.status == ENUMResources().const.SOLVED)



'''
Submissions Count
'''
def select_submissions_counts(submissions):
    return dao.query(func.count(submissions.c.memberId).label('sumOfSubmissionCount'))

'''
Not Solved, Judging, ServerError
'''
def select_failed_problems(submissions):
    return dao.query(submissions).\
                      filter(submissions.c.status != ENUMResources().const.SOLVED,
                             submissions.c.status != ENUMResources().const.JUDGING,
                             submissions.c.status != ENUMResources().const.SERVER_ERROR).\
                      group_by(submissions.c.problemIndex)


'''
Solved Problem Counts
'''
def select_solved_problems_counts(submissions):
    submissions = dao.query(submissions).\
                      filter(submissions.c.status == ENUMResources().const.SOLVED).\
                      group_by(submissions.c.problemIndex).\
                      subquery()
                      
    return dao.query(func.count(submissions.c.memberId).label('sumOfSolvedProblemCount'))

'''
Solved Counts
'''
def select_solved_counts(submissions):
    return dao.query(func.count(submissions.c.memberId).label('sumOfSolvedCount')).\
               filter(submissions.c.status == ENUMResources().const.SOLVED)
               
'''
Wrong Answer Counts
'''
def select_wrong_answer_counts(submissions):
    return dao.query(func.count(submissions.c.memberId).label('sumOfWrongAnswerCount')).\
               filter(submissions.c.status == ENUMResources().const.WRONG_ANSWER)

'''
Time Over Counts
'''
def select_time_over_counts(submissions):
    return dao.query(func.count(submissions.c.memberId).label('sumOfTimeOverCount')).\
               filter(submissions.c.status == ENUMResources().const.TIME_OVER)

'''
Memory Over Flow Counts
'''
def select_memory_overflow_counts(submissions):
    return dao.query(func.count(submissions.c.memberId).label('sumOfMomoryOverflowCount')).\
               filter(submissions.c.status == ENUMResources().const.MEMORY_OVERFLOW)       
                       
'''
Compile Error Counts
'''
def select_compile_error_counts(submissions):
    return dao.query(func.count(submissions.c.memberId).label('sumOfCompileErrorCount')).\
               filter(submissions.c.status == ENUMResources().const.COMPILE_ERROR)
               
'''
RunTime Error Counts
'''
def select_runtime_error_counts(submissions):
    return dao.query(func.count(submissions.c.memberId).label('sumOfRunTimeErrorCount')).\
               filter(submissions.c.status == ENUMResources().const.RUNTIME_ERROR)

'''
Server Error Counts
'''
def select_server_error_counts(submissions):
    return dao.query(func.count(submissions.c.memberId).label('sumOfServerErrorCount')).\
               filter(submissions.c.status == ENUMResources().const.SERVER_ERROR)
               
'''
Member Chart Information
'''
def select_member_chart_submissions(submissions):
    return dao.query(select_solved_problems_counts(submissions).subquery(),# 중복 제거푼 문제숫
                     select_submissions_counts(submissions).subquery(),# 총 제출 횟수
                     select_solved_counts(submissions).subquery(),# 모든 맞춘 횟수
                     select_wrong_answer_counts(submissions).subquery(),# 틀린 횟수
                     select_time_over_counts(submissions).subquery(),# 타임 오버 횟수
                     select_memory_overflow_counts(submissions).subquery(),# 메모리 오버 플로우 횟수
                     select_compile_error_counts(submissions).subquery(),# 컴파일 에러 횟수
                     select_runtime_error_counts(submissions).subquery(),# 런타임 에러 횟수
                     select_server_error_counts(submissions).subquery())# 서버 에러 횟수
    
    
    
'''
Problem Chart Information
'''
def select_problem_chart_submissions(sumOfSubmissionPeopleCount, sumOfSolvedPeopleCount, problemSubmittedRecords):
    return dao.query(sumOfSubmissionPeopleCount,
                     sumOfSolvedPeopleCount,
                     problemSubmittedRecords.c.sumOfSubmissionCount,
                     problemSubmittedRecords.c.sumOfSolvedCount,
                     problemSubmittedRecords.c.sumOfWrongCount,
                     problemSubmittedRecords.c.sumOfTimeOverCount,
                     problemSubmittedRecords.c.sumOfMemoryOverFlowCount,
                     problemSubmittedRecords.c.sumOfCompileErrorCount,
                     problemSubmittedRecords.c.sumOfRuntimeErrorCount)
    
'''
Submitted Records Of problems
'''
def select_submitted_records_of_problem(problemIndex):
    return dao.query(SubmittedRecordsOfProblems).\
               filter(SubmittedRecordsOfProblems.problemIndex == problemIndex)
               
               
'''
Sum Of Submitted People Counts
'''
def select_submissions_peoples_counts(submissions):
    return dao.query(func.count(submissions.c.memberId).label('sumOfSubmissionPeopleCount'))
      
'''
Sum Of Solved People Counts
'''
def select_solved_peoples_counts(submissions):
    return dao.query(func.count(submissions.c.memberId).label('sumOfSolvedPeopleCount')).\
               filter(submissions.c.status == ENUMResources().const.SOLVED)



'''
 Code IsLike
'''
def select_code_is_like(submissionIndex, memberIdIndex):
    return dao.query(LikesOnSubmission).\
               filter(and_(LikesOnSubmission.submissionIndex == submissionIndex,
                           LikesOnSubmission.codeLikerIdIndex == memberIdIndex))
               
               
'''
Replies on Code isLike
'''
def select_replies_on_code_is_like(submissionReplyIndex, memberIdIndex):
    return dao.query(LikesOnReplyOfSubmission).\
               filter(and_(LikesOnReplyOfSubmission.submissionReplyIndex == submissionReplyIndex,
                           LikesOnReplyOfSubmission.codeReplyLikerIdIndex == memberIdIndex))
 

'''
Replies on Code isLike
'''
def select_replies_on_code_like(repliesOnSubmission, memberIdIndex):
    return dao.query(LikesOnReplyOfSubmission).\
               join(repliesOnSubmission,
                    and_(LikesOnReplyOfSubmission.submissionReplyIndex == repliesOnSubmission.c.submissionReplyIndex,
                         LikesOnReplyOfSubmission.codeReplyLikerIdIndex == memberIdIndex))
         
 
 
 
'''
Replies on Code
'''
def select_replies_on_code(submissionIndex, submissionReplyIndex = None, isDeleted = ENUMResources().const.FALSE):
    return dao.query(RepliesOnSubmission).\
               filter(and_((RepliesOnSubmission.submissionIndex == submissionIndex if submissionIndex
                            else RepliesOnSubmission.submissionReplyIndex == submissionReplyIndex),
                           RepliesOnSubmission.isDeleted == isDeleted)) 
 
 
''' 
Insert Replies on Code
'''
def insert_replies_on_code(submissionIndex, memberIdIndex, articleParameter):
    return RepliesOnSubmission(submissionIndex = submissionIndex,
                               codeReplierIdIndex = memberIdIndex,
                               codeReplyContent = articleParameter.content,
                               codeReplierIp = articleParameter.updateIp,
                               codeRepliedDate = articleParameter.updateDate)
 
 
 
'''
Insert Language Init Data
'''
def insert_language(languageName, languageVersion = None):
    return Languages(languageName = languageName,
                     languageVersion = languageVersion)    
    
           
'''
Insert Code likes
'''
def insert_likes_on_code(submissionIndex, memberIdIndex):
    return LikesOnSubmission(submissionIndex = submissionIndex,
                             codeLikerIdIndex = memberIdIndex)
                        
                        
                        
'''
Insert LikesOnReplies Code
'''
def insert_likes_on_reply_of_code(submissionReplyIndex, memberIdIndex): 
    return LikesOnReplyOfSubmission(submissionReplyIndex = submissionReplyIndex,
                                    codeReplyLikerIdIndex = memberIdIndex)



'''
Insert Init Submitted RecordsOf Problems
'''
def insert_submitted_records_of_problems(problemIndex):
    return SubmittedRecordsOfProblems(problemIndex = problemIndex)
    
    
    
'''
Board Code Like Counting
'''
def update_code_like_counting(submissionIndex, LIKE_INCREASE = 1):
    dao.query(DataOfSubmissionBoard).\
        filter(DataOfSubmissionBoard.submissionIndex == submissionIndex).\
        update(dict(sumOfLikeCount = DataOfSubmissionBoard.sumOfLikeCount + LIKE_INCREASE))   

      
'''
Board Code isLike update
'''
def update_code_is_like(submissionIndex, memberIdIndex, isLikeCancelled = ENUMResources().const.FALSE):
    dao.query(LikesOnSubmission).\
        filter(and_(LikesOnSubmission.submissionIndex == submissionIndex,
                    LikesOnSubmission.codeLikerIdIndex == memberIdIndex)).\
        update(dict(isLikeCancelled = isLikeCancelled)) 
      


'''
Replies on Code Update
'''
def update_replies_on_code_modify(submissionReplyIndex, replyParameter):
    dao.query(RepliesOnSubmission).\
        filter(RepliesOnSubmission.submissionReplyIndex == submissionReplyIndex).\
        update(dict(codeReplyContent = replyParameter.content,
                    codeReplierIp = replyParameter.updateIp,
                    codeRepliedDate = replyParameter.updateDate))

  
'''
Repllies on Code Like Counting
'''
def update_replies_on_code_like_counting(submissionReplyIndex, LIKE_INCREASE = 1):
    dao.query(RepliesOnSubmission).\
        filter(RepliesOnSubmission.submissionReplyIndex == submissionReplyIndex).\
        update(dict(sumOfLikeCount = RepliesOnSubmission.sumOfLikeCount + LIKE_INCREASE)) 
  
      
'''
Replies on Code is Like
'''
def update_replies_on_code_is_like(submissionReplyIndex, memberIdIndex, isLikeCancelled = ENUMResources().const.FALSE):
    dao.query(LikesOnReplyOfSubmission).\
        filter(and_(LikesOnReplyOfSubmission.submissionReplyIndex == submissionReplyIndex,
                    LikesOnReplyOfSubmission.codeReplyLikerIdIndex == memberIdIndex)).\
        update(dict(isLikeCancelled = isLikeCancelled))
        


'''
Code reply, View Counting
'''
def update_code_view_reply_counting(submissionIndex, VIEW_INCREASE = 1, REPLY_INCREASE = 0):
    dao.query(DataOfSubmissionBoard).\
        filter(DataOfSubmissionBoard.submissionIndex == submissionIndex).\
        update(dict(viewCount = DataOfSubmissionBoard.viewCount + VIEW_INCREASE,
                    submissionReplyCount = DataOfSubmissionBoard.submissionReplyCount + REPLY_INCREASE))                    
                    
                                
'''
Repllies on Code delete
'''
def update_replies_on_code_delete(submissionReplyIndex, isDeleted = ENUMResources().const.TRUE):
    dao.query(RepliesOnSubmission).\
        filter(RepliesOnSubmission.submissionReplyIndex == submissionReplyIndex).\
        update(dict(isDeleted = isDeleted)) 