from gradingResource.enumResources import ENUMResources
from gradingResource.listResources import ListResources
from model.submissions import Submissions
from model.submittedRecordsOfProblems import SubmittedRecordsOfProblems

class DBUpdate(object):
    def __init__(self, submissionIndex, submissionCount, problemIndex):
        self.submissionIndex = submissionIndex
        self.submissionCount = submissionCount
        self.problemIndex = problemIndex
        
    def UpdateResutl(self, messageParaList, db_session, text):
        compileError = ''
        testCase = 0
        
        try:
            if len(messageParaList) != 4:
                return False
                
            else:
                result = messageParaList[0]
                score = messageParaList[1]
                runTime = messageParaList[2]
                usingMem = messageParaList[3]
            
                if result == ENUMResources.const.WRONG_ANSWER:
                    testCase = int(text)
                    self.UpdateTable_SubmittedRecordsOfProblems_WrongAnswer(db_session)
                
                elif result == ENUMResources.const.TIME_OVER:
                    self.UpdateTable_SubmittedRecordsOfProblems_TimbeOver(db_session)
                
                elif result == ENUMResources.const.SOLVED:
                    self.UpdateTable_SubmittedRecordsOfProblems_Solved(db_session)
                    
                elif result == ENUMResources.const.RUNTIME_ERROR:
                    self.UpdateTable_SubmittedRecordsOfProblems_RunTimeError(db_session)
                    
                elif result == ENUMResources.const.COMPILE_ERROR:
                    compileError = text
                    self.UpdateTable_SubmittedRecordsOfProblems_CompileError(db_session)
                
                elif result == ENUMResources.const.MEMORY_OVERFLOW:
                    self.UpdateTable_SubmittedRecordsOfProblems_MemoryOverflow(db_session)
                
                else:
                    return False
                
                self.UpdateTableSubmissions(result, score, runTime, usingMem,
                                            db_session, compileError, testCase)
                
                db_session.commit()
                return True
        except Exception as e:
            print e
            db_session.rollback()
            return False
            
    
    def UpdateTableSubmissions(self, result, score, runTime, usingMem,
                               db_session, compileError, testCase):
        try:
            db_session.query(Submissions).\
                filter_by(submissionIndex = self.submissionIndex,
                          submissionCount = self.submissionCount).\
                update(dict(status = ListResources.const.GRADERESULT_List.index(result),
                            score = score,
                            runTime = runTime,
                            usedMemory = usingMem,
                            solutionCheckCount = Submissions.solutionCheckCount+1,
                            compileErrorMessage = compileError,
                            wrongTestCaseNumber = testCase))
        except Exception as e:
            raise e
    
    def UpdateTable_SubmittedRecordsOfProblems_CompileError(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                filter_by(problemIndex = self.problemIndex).\
                          update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                      sumOfCompileErrorCount = SubmittedRecordsOfProblems.sumOfCompileErrorCount + 1))
        except Exception as e:
            raise e
            
    def UpdateTable_SubmittedRecordsOfProblems_Solved(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemIndex = self.problemIndex).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfSolvedCount = SubmittedRecordsOfProblems.sumOfSolvedCount + 1))
        except Exception as e:
            raise e
            
    def UpdateTable_SubmittedRecordsOfProblems_WrongAnswer(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemIndex = self.problemIndex).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfWrongCount = SubmittedRecordsOfProblems.sumOfWrongCount + 1))
        except Exception as e:
            raise e
            
    def UpdateTable_SubmittedRecordsOfProblems_TimbeOver(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemIndex = self.problemIndex).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfTimeOverCount = SubmittedRecordsOfProblems.sumOfTimeOverCount + 1))
        except Exception as e:
            raise e
            
    def UpdateTable_SubmittedRecordsOfProblems_RunTimeError(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemIndex = self.problemIndex).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfRuntimeErrorCount = SubmittedRecordsOfProblems.sumOfRuntimeErrorCount + 1))
        except Exception as e:
            raise e
        
    def UpdateTable_SubmittedRecordsOfProblems_MemoryOverflow(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemIndex = self.problemIndex).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfRuntimeErrorCount = SubmittedRecordsOfProblems.sumOfMemoryOverFlowCount + 1))
        except Exception as e:
            raise e
   
    @staticmethod
    def UpdateServerError(submissionIndex, submissionCount, db_session):
        try :
            db_session.query(Submissions).\
                filter_by(submissionIndex = submissionIndex,
                          submissionCount = submissionCount).\
                update(dict(status = 9,
                            score = 0,
                            runTime = 0,
                            usedMemory = 0))
            db_session.commit()
            print '...server error...'
        except Exception as e:
            raise e
