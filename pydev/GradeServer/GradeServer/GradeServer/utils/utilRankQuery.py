
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from sqlalchemy import func, and_

from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.languageResources import LanguageResources

from GradeServer.database import dao
from GradeServer.model.members import Members
from GradeServer.model.submissions import Submissions

from GradeServer.utils.utilUserQuery import join_member_id
from GradeServer.utils.utilSubmissionQuery import select_between_days_last_submissions,\
                                                  select_last_submissions


'''
 DB Select basic rank
 '''
def select_ranks(submissions):
    # # Total Submission Count (Rank Page Server Error Exception)
    submissionCount = dao.query(submissions.c.memberIdIndex,
                                func.sum(submissions.c.solutionCheckCount).label('solutionCheckCount')).\
                          group_by(submissions.c.memberIdIndex).\
                          subquery()
                          
        # 중복 제거푼 문제숫
    sumOfSolvedProblemCount = dao.query(submissions.c.memberIdIndex).\
                                  join(Submissions,
                                       and_(Submissions.status == ENUMResources().const.SOLVED,
                                            Submissions.submissionIndex == submissions.c.submissionIndex)).\
                                  group_by(Submissions.submissionIndex).\
                                  subquery()
    sumOfSolvedProblemCount = dao.query(sumOfSolvedProblemCount,
                                        func.count(sumOfSolvedProblemCount.c.memberIdIndex).label('sumOfSolvedProblemCount')).\
                                        group_by(sumOfSolvedProblemCount.c.memberIdIndex).\
                                        subquery()
    
    #SubmitCount and SolvedCount Join
    return dao.query(submissionCount.c.memberIdIndex,
                     submissionCount.c.solutionCheckCount,
                     sumOfSolvedProblemCount.c.sumOfSolvedProblemCount,
                     (sumOfSolvedProblemCount.c.sumOfSolvedProblemCount / submissionCount.c.solutionCheckCount * 100).label('solvedRate')).\
               join(sumOfSolvedProblemCount,
                    and_(submissionCount.c.memberIdIndex == sumOfSolvedProblemCount.c.memberIdIndex))


'''
Rank Sorting Condition
'''
def ranks_sorted(ranks, sortCondition = LanguageResources().const.Rate[1]):
    # rate, Solved Problem, submissionCount 정렬
    if sortCondition == LanguageResources().const.Rate[1]:
        rankMemberRecords = dao.query(ranks,
                                      Members.comment).\
                                join(Members,
                                     and_(Members.memberIdIndex == ranks.c.memberIdIndex)).\
                                order_by(ranks.c.solvedRate.desc(),
                                         ranks.c.sumOfSolvedProblemCount.desc(),
                                         ranks.c.solutionCheckCount.asc())
    # Solved Problem, rate, submissionCount  Sorted
    elif sortCondition == LanguageResources().const.SolvedProblems[1]:
        rankMemberRecords = dao.query(ranks,
                                      Members.comment).\
                                join(Members,
                                     and_(Members.memberIdIndex == ranks.c.memberIdIndex)).\
                                order_by(ranks.c.sumOfSolvedProblemCount.desc(),
                                         ranks.c.solvedRate.desc(),
                                         ranks.c.solutionCheckCount.asc())
                                
    return rankMemberRecords

'''
Top Coder
'''
def select_top_coder():
    # Top Coder Layer
    try:
        # 오늘 요일 월1 ~ 일7
        dayOfWeekNum = datetime.now().isoweekday()
        # 요일 별 제출 기간 추려내기
        minusDays = {1: -1,
                                         2: -2,
                                         3: -3,
                                         4: -4,
                                         5: -5,
                                         6: -6,
                                         7: -0}
        addDays = {1: 5,
                                    2: 4,
                                    3: 3,
                                    4: 2,
                                    5: 1,
                                    6: 0,
                                    7: 6}
                # 금주의 시작일과 끝일 구함
        submissionDatePeriod = dayOfWeek(minusDays = minusDays[dayOfWeekNum],
                                         addDays = addDays[dayOfWeekNum])
                # 이번주에 낸 제출 목록 
        ranks = select_ranks(select_between_days_last_submissions(select_last_submissions(memberIdIndex = None,
                                                                                          problemIndex = None).subquery(),
                                                                  submissionDatePeriod).subquery()).subquery()
        ranks = join_member_id(ranks,
                               subMemberIdIndex = ranks.c.memberIdIndex).subquery()                                                   
                # 랭킹 동률 처리
        topCoders= ranks_sorted(rankTieProcess(ranks).subquery()).all()
                                         
    except Exception:
        topCoders = []
        
    return topCoders


'''
 요일 별로 금주 기간 지정
 '''
def dayOfWeek(minusDays, addDays, dateFormat = '%Y-%m-%d'):
    # 현재 날짜에서 addDays일후 날짜까지 구함
    startDate = (datetime.now() + timedelta(days = minusDays)).strftime(dateFormat)
    endDate = (datetime.now() + timedelta(days = addDays)).strftime(dateFormat) 
    submissionDatePeriod = {'start': startDate,
                            'end': endDate}
    
    return submissionDatePeriod


'''
랭킹 동률 처리
'''
def rankTieProcess(ranks):
    # High solvedRate
    solvedRate = dao.query(func.max(ranks.c.solvedRate).label('solvedRate')).subquery()
    ranks = dao.query(ranks).\
                filter(func.round(ranks.c.solvedRate, 4) == func.round(solvedRate.c.solvedRate, 4)).subquery()   
                     
    # High sumOfSolvedProblemCount
    solvedRate = dao.query(func.max(ranks.c.sumOfSolvedProblemCount).label('sumOfSolvedProblemCount')).subquery()
    ranks = dao.query(ranks).\
                filter(ranks.c.sumOfSolvedProblemCount == solvedRate.c.sumOfSolvedProblemCount).subquery()  
                      
    # Low solutionCheckCount
    solvedRate = dao.query(func.max(ranks.c.solutionCheckCount).label('solutionCheckCount')).subquery()
    ranks = dao.query(ranks).\
                filter(ranks.c.solutionCheckCount == solvedRate.c.solutionCheckCount)
                
    return ranks
