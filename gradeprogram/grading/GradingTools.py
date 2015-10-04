# -*- coding: utf-8 -*-
import string
import logging
from FileTools import FileTools
from subprocess import call
from gradingResource.enumResources import ENUMResources
from gradingResource.fileNameNPathResources import FileNameNPathResources

"""
정상 실행되는 프로그램을 채점하는 class
채점 형태, input case에 따라 다른 방식으로 채점 진행.
"""

class GradingTools(object):
    def __init__(self, parameter, command):
        self.gradeMethod = parameter.gradeMethod
        self.caseCount = parameter.caseCount
        self.answerPath = parameter.answerPath
        self.problemName = parameter.problemName
        self.filePath = parameter.filePath
        self.command = command
        
    # 채점
    def grade(self):
        # 채점 방식 및 case 개수에 따라 다른 방식 적용
        if self.gradeMethod == ENUMResources.const.SOLUTION:   # solution
            if self.caseCount > 1:
                result, score = self.gradeSolutionMulti()
                
            else:
                result, score = self.gradeSolutionSingle()
            
        else:   # checker
            self.gradeChecker()
            
        return result, score

    # one case, soultion type        
    def gradeSolutionSingle(self):
        # 사용자 출력 파일과 정답 파일을 라인별로 비교, 일치율을 점수로 환산
        answerOpenCommand = "%s%s%s" % (self.answerPath, self.problemName,
                                        FileNameNPathResources.const.DefaultOutputTotalResultFileName)
        
        stdLines = FileTools.readFileLines(FileNameNPathResources.const.OutputResultFileName)
        answerLines = FileTools.readFileLines(answerOpenCommand)
        
        answerLineCount = len(answerLines)
        stdLineCount = len(stdLines)
        
        count = stdLineCount - answerLineCount
        
        _min = stdLineCount if count < 0 else answerLineCount
        count = abs(count)
        
        strip = string.rstrip
        logging.debug('single grade')
        
        for i in xrange(_min):
            stdLine = strip(stdLines[i], '\r\n ')
            answerLine = strip(answerLines[i], '\r\n ')
            
            if stdLine != answerLine:   # if not same each line
                count += 1
        
        return self.getSolutionScore(count, answerLineCount)
    
    # checker type
    def gradeChecker(self):
        # 별도의 채점 프로그램으로 채점
        copyCommand = "%s%s%s" % (self.answerPath, self.problemName, '_checker')
        FileTools.copyFile(copyCommand, 'checker')
        
        logging.debug('checker grade')
        
        call('./checker 1>result.txt', shell = True)
        
        score = self.getScore('result.txt')
        
        if score is 100:
            return ENUMResources.const.SOLVED, score
        else:
            return ENUMResources.const.WRONG_ANSWER, score
    
    # multi case, solution type
    def gradeSolutionMulti(self):
        # 사용자 출력 파일을 각 case별 출력을 순서대로 각 라인을 비교, 일치율을 점수로 환산 
        answerOpenCommand = "%s%s%s" % (self.answerPath, self.problemName,
                                        FileNameNPathResources.const.DefaultOutputTotalResultFileName)
        
        answerLines = FileTools.readFileLines(answerOpenCommand)
        stdLines = FileTools.readFileLines(FileNameNPathResources.const.OutputResultFileName)
        
        strip = string.rstrip
        
        totalCount = len(answerLines)
        loopCount = len(stdLines)
        caseCount = 1
        count = abs(loopCount - totalCount)
        i = 0
        appendFlag = True
        
        logging.debug('multi grade')
        if loopCount is 0:
            self.makeTestCase(1)
            return ENUMResources.const.WRONG_ANSWER, 0
            
        while i < loopCount:
            answerOpenCommand = "%s%s%s%i%s" % (self.answerPath,
                                                self.problemName,
                                                FileNameNPathResources.const.CaseFile,
                                                caseCount,
                                                FileNameNPathResources.const.OutputCaseName)
            answers = FileTools.readFileLines(answerOpenCommand)
            
            for answer in answers:
                stdLine = strip(stdLines[i], '\r\n ')
                answerLine = strip(answer, '\r\n ')
                
                if stdLine != answerLine:
                    count += 1
                    # 틀린 case는 한번만 저장 
                    if appendFlag:
                        self.makeTestCase(caseCount)
                        appendFlag = False
                    
                i += 1
                if i is loopCount:
                    break
                
            if caseCount is self.caseCount:
                count += loopCount - i
                break
            
            caseCount += 1
            
        if appendFlag and loopCount < totalCount:
            self.makeTestCase(caseCount)
                
        return self.getSolutionScore(count, loopCount)
    
    # 틀린 case를 저장
    def makeTestCase(self, caseNum):
        wf = open('message.txt', 'w')
            
        wf.writelines(str(caseNum))
                
        wf.close()
    
    # 점수 환산 method
    def getSolutionScore(self, count, lineCount):
        result = ENUMResources.const.SOLVED
        score = 100
        
        if count > 0:
            result = ENUMResources.const.WRONG_ANSWER
            score = int( ((lineCount - count) * 100) / lineCount )
            
        if score < 0:
            return ENUMResources.const.WRONG_ANSWER, 0
        
        return result, score
            
    def getScore(self, fileName):
        scores = FileTools.readFileLines('result.txt')
        
        return int(scores[0])