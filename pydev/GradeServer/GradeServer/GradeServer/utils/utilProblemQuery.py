# -*- coding: utf-8 -*-


from datetime import datetime
from sqlalchemy import and_, not_

from GradeServer.database import dao

from GradeServer.model.problems import Problems
from GradeServer.model.languages import Languages

from GradeServer.resource.languageResources import LanguageResources
from GradeServer.resource.enumResources import ENUMResources


'''
Get all problems
'''
def select_all_problems(isDeleted = ENUMResources().const.FALSE):
    return dao.query(Problems).\
               filter(Problems.isDeleted == isDeleted)

    
'''
Get Select Problems
case Gold, Silver, Bronze
'''
def select_problems(problemDifficulty = None, isDeleted = ENUMResources().const.FALSE):
    return dao.query(Problems).\
               filter((Problems.problemDifficulty == problemDifficulty if problemDifficulty
                       else Problems.problemDifficulty != problemDifficulty),
                      Problems.isDeleted == isDeleted).\
               order_by(Problems.problemIndex.asc())


'''
Get Problem Information
'''
def select_problem(problemIndex, problemName = None, isDeleted = ENUMResources().const.FALSE):
    return dao.query(Problems).\
               filter(and_((Problems.problemIndex == problemIndex if problemIndex
                           else Problems.problemName == problemName),
                           Problems.isDeleted == isDeleted))
               
               
               


'''
Get submit possible Registered Problems
'''
def select_submission_possilbe_registered_problems(problems):
    return dao.query(problems).\
               filter(problems.c.endDateOfSubmission >= datetime.now())


    
        
'''
Problems sorted
'''
def problems_sorted(problems, sortCondition = LanguageResources().const.Name[1]):
    if sortCondition == LanguageResources().const.Name[1]:
        problemRecords = dao.query(problems).\
                             order_by(problems.c.problemName.asc(),
                                      problems.c.problemDifficulty.asc())
    # Difficulty ProblemName 정렬
    elif sortCondition == LanguageResources().const.Difficulty[1]:
        problemRecords = dao.query(problems).\
                             order_by(problems.c.problemDifficulty.asc(),
                                      problems.c.problemName.asc())
                             
    return problemRecords


               
'''
Join Problem Names
'''
def join_problems_name(subquery, subProblemIndex, isDeleted = ENUMResources().const.FALSE):
    return dao.query(subquery,
                     Problems.problemName,
                     Problems.solutionCheckType,
                     Problems.problemPath).\
               outerjoin(Problems,
                         Problems.problemIndex == subProblemIndex)


    
'''
OuterJoin Problem List and submission_code
'''
def join_problem_lists_submissions(problems, submissions):
    return dao.query(problems,
                     submissions.c.score,
                     submissions.c.status,
                     submissions.c.submissionCount,
                     submissions.c.solutionCheckCount,
                     submissions.c.compileErrorMessage,
                     submissions.c.wrongTestCaseNumber).\
               outerjoin(submissions,
                         problems.c.problemIndex == submissions.c.problemIndex).\
               order_by(problems.c.problemName.asc())
               
               
'''
Insert Problems
'''
def insert_problem(problemName, problemDifficulty, solutionCheckType, limitedTime, limitedMemory, problemPath, isDeleted = ENUMResources().const.FALSE):
    return Problems(problemName = problemName,
                    problemDifficulty = problemDifficulty,
                    solutionCheckType = solutionCheckType,
                    limitedTime = limitedTime,
                    limitedMemory = limitedMemory,
                    problemPath = problemPath)


'''
Update Problem
'''
def update_problem(problemIndex, problemDifficulty, solutionCheckType, limitedTime, limitedMemory):
    dao.query(Problems).\
        filter(Problems.problemIndex == problemIndex).\
        update(dict(problemDifficulty = problemDifficulty,
                    solutionCheckType = solutionCheckType,
                    limitedTime = limitedTime,
                    limitedMemory = limitedMemory))
 
 
'''
update numberOfTestCase       
'''
def update_number_of_test_case(problemIndex, numberOfTestCase):
    dao.query(Problems).\
        filter(Problems.problemIndex == problemIndex).\
        update(dict(numberOfTestCase = numberOfTestCase))
    
    
        
''' 
Update Problem isDeleted
'''
def update_problem_deleted(problemIndex, isDeleted = ENUMResources().const.TRUE):
    dao.query(Problems).\
        filter(Problems.problemIndex == problemIndex).\
        update(dict(isDeleted = isDeleted))