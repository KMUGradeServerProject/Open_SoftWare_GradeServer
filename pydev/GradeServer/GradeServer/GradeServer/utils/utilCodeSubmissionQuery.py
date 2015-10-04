from GradeServer.database import dao
from datetime import datetime
from GradeServer.model.problems import Problems
from GradeServer.model.dataOfSubmissionBoard import DataOfSubmissionBoard
from GradeServer.model.submittedFiles import SubmittedFiles
from GradeServer.model.submissions import Submissions
from GradeServer.model.languages import Languages

from GradeServer.utils.utilSubmissionQuery import select_last_submissions
from GradeServer.utils.utilProblemQuery import select_problem
from GradeServer.utils.utilUserQuery import select_member
        
from GradeServer.utils.utilMessages import unknown_error, get_message
from GradeServer.resource.enumResources import ENUMResources
from sqlalchemy import and_


'''
Get all languages
'''
def select_all_languages():
    return dao.query(Languages).all()              

def get_member_name(memberIdIndex):
    try:
        memberName = select_member(memberIdIndex = memberIdIndex).first().\
                                                                  memberName
        return memberName
    except:
        return unknown_error(get_message('dbError'))

def get_problem_name(problemIndex):
    try:
        problemName = select_problem(problemIndex = problemIndex).first().\
                                                                  problemName
                                                                                                      
        return problemName
    except:
        return unknown_error(get_message('dbError'))
    
def get_submission_info(memberIdIndex, problemIndex):
    try:
        submissionInfo = select_last_submissions(memberIdIndex = memberIdIndex,
                                                 problemIndex = problemIndex).first()
        
        submissionCount = submissionInfo.submissionCount + 1
        solutionCheckCount = submissionInfo.solutionCheckCount

    except:
        submissionCount = 1
        solutionCheckCount = 0

    return submissionCount, solutionCheckCount

def get_submission_index(memberIdIndex, problemIndex):
                              
    try:
        submissionIndex = dao.query(DataOfSubmissionBoard.submissionIndex).\
                          filter(and_(DataOfSubmissionBoard.memberIdIndex == memberIdIndex,
                                      DataOfSubmissionBoard.problemIndex == problemIndex)).first().\
                          submissionIndex
    except:
        dataOfSubmissionBoard = DataOfSubmissionBoard(memberIdIndex = memberIdIndex,
                                                      problemIndex = problemIndex)
        
        dao.add(dataOfSubmissionBoard)
        dao.commit()

        submissionIndex = dao.query(DataOfSubmissionBoard.submissionIndex).\
                              filter(and_(DataOfSubmissionBoard.memberIdIndex == memberIdIndex,
                                          DataOfSubmissionBoard.problemIndex == problemIndex)).first().\
                              submissionIndex
    return submissionIndex

def insert_submitted_files(submissionIndex, fileIndex, fileName, filePath, fileSize):
    submittedFiles = SubmittedFiles(submissionIndex = submissionIndex,
                                    fileIndex = fileIndex,
                                    fileName = fileName,
                                    filePath = filePath,
                                    fileSize = fileSize)                
    dao.add(submittedFiles)
    
def get_used_language_index(usedLanguageName, usedLanguageVersion = None):
    try:
        usedLanguageIndex = dao.query(Languages.languageIndex).\
                           filter(Languages.languageName == usedLanguageName,
                                  Languages.languageVersion == usedLanguageVersion).\
                           first().\
                           languageIndex
    except:
        return unknown_error(get_message('dbError'))
    return usedLanguageIndex

def get_problem_info(problemIndex, problemName):
    try:
        problemPath, limitedTime, limitedMemory, solutionCheckType, numberOfTestCase = dao.query(Problems.problemPath,
                                                                                                 Problems.limitedTime,
                                                                                                 Problems.limitedMemory,
                                                                                                 Problems.solutionCheckType,
                                                                                                 Problems.numberOfTestCase).\
                                                                                            filter(Problems.problemIndex == problemIndex).\
                                                                                            first()
    except:
        return unknown_error(get_message('dbError'))
    return problemPath, limitedTime, limitedMemory, solutionCheckType, numberOfTestCase

def get_used_language_version(usedLanguage):
    try:
        usedLanguageVersion = dao.query(Languages.languageVersion).\
                                  first().\
                                  languageVersion
    except:
        return unknown_error(get_message('dbError'))
    return usedLanguageVersion

def delete_submitted_files_data(submissionIndex):
    dao.query(SubmittedFiles).\
        filter(SubmittedFiles.submissionIndex == submissionIndex).\
        delete()
                     
def insert_to_submissions(submissionIndex, submissionCount, solutionCheckCount, usedLanguageIndex, sumOfSubmittedFileSize):
    submissions = Submissions(submissionIndex = submissionIndex,
                              submissionCount = submissionCount,
                              solutionCheckCount = solutionCheckCount,
                              status = ENUMResources().const.JUDGING,
                              codeSubmissionDate = datetime.now(),
                              sumOfSubmittedFileSize = sumOfSubmittedFileSize,
                              usedLanguageIndex = usedLanguageIndex)
    dao.add(submissions)