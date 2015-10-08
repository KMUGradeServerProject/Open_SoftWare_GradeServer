# -*- coding: utf-8 -*-
import os
import sys
import signal
import string
import ptrace
import logging
import resource
from FileTools import FileTools
from gradingResource.enumResources import ENUMResources
from gradingResource.fileNameNPathResources import FileNameNPathResources
from gradingResource.listResources import ListResources

"""
프로그램 실행하고 성능을 측정하는 class
컴파일된 프로그램을 실행하고 사용 메모리, 시간을 체크
"""

class ExecutionTools(object):
    def __init__(self, parameter, command):
        self.usingLang = parameter.usingLang
        self.answerPath = parameter.answerPath
        self.runFileName = parameter.runFileName
        self.problemName = parameter.problemName
        self.caseCount = parameter.caseCount
        self.command = command
        self.limitTime = parameter.limitTime
        self.limitMemory = parameter.limitMemory
        
        if self.usingLang == ListResources.const.Lang_JAVA or\
        self.usingLang == ListResources.const.Lang_PYTHON:
            self.limitTime = self.limitTime << 1
            self.limitMemory = self.limitMemory << 1
        
        # 프로그램 실행
    def execution(self):
        # 전체 input case파일 복사
        if self.caseCount > 0:
            copyCommand = "%s%s%s" % (self.answerPath, self.problemName,
                                      FileNameNPathResources.const.DefaultInputTotalCaseFileName)
            FileTools.copyFile(copyCommand, FileNameNPathResources.const.InputCaseFileName)
        
        # 실행 명령어 설정
        runCommandList = self.command.ExecuteCommand()
        
        #자식 프로세스 생성 후 자식 프로세스는 프로그램 실행, 부모 프로세스는 자식 프로세스의 자원 사용을 체크
        logging.debug('execution')
        
        pid = os.fork()
        
        # 자식 프로세스
        if pid == 0:
            self.runProgram(runCommandList)
        
        # 부모 프로세스
        else:
            result, time, usingMem = self.watchRunProgram(pid)
        
        # ms 단위로 환산
        userTime = int(time * 1000)
        
        # 실행 후 런타임 에러 및 사용 시간 메모리 초과 확인
        if result == 'Grading':
            if os.path.isfile('run.err') and os.path.getsize('run.err') > 0:
                result = ENUMResources.const.RUNTIME_ERROR
            
            elif userTime > self.limitTime:
                result = ENUMResources.const.TIME_OVER
        
            elif (usingMem >> 10) > self.limitMemory:
                 result = ENUMResources.const.MEMORY_OVERFLOW
        
        elif not result:
            sys.stderr.write(ENUMResources.const.SERVER_ERROR + ' ' + str(0) + ' ' + str(0) + ' ' + str(0))
            sys.exit()
        
        return result, userTime, usingMem
    
    #프로그램 실행
    def runProgram(self, runCommandList):
        # 프로세스 우선순위 증가
        os.nice(19)
        
        # 프로그램 실행 결과 출력되는 stdout을 파일로 리다이렉션
        redirectionSTDOUT = os.open(FileNameNPathResources.const.OutputResultFileName,
                                    os.O_RDWR|os.O_CREAT)
        os.dup2(redirectionSTDOUT,1)
        
        # 프로세스 사용 자원 제한
        soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
        rlimTime = int(self.limitTime / 1000) + 1
        
        resource.setrlimit(resource.RLIMIT_CPU, (rlimTime,hard))
        
        # 파이썬 런타임 에러 메시지 리다이렉션
        if self.usingLang == ListResources.const.Lang_PYTHON:
            redirectionSTDERROR = os.open('run.err', os.O_RDWR|os.O_CREAT)
            os.dup2(redirectionSTDERROR, 2)
        
        if self.caseCount is not 0:
            redirectionSTDIN = os.open('input.txt', os.O_RDONLY)
            os.dup2(redirectionSTDIN, 0)
        
        # 프로세스 추적/실행
        ptrace.traceme()
            
        os.execl(runCommandList[0], runCommandList[1], runCommandList[2])
            
    # 자식 프로세스 추적
    def watchRunProgram(self, pid):
        usingMem = 0
        
        while True:
            wpid, status, res = os.wait4(pid,0)
            signal.signal(signal.SIGXCPU, self.sigHandler)
            
            # 정상 종료된 경우
            if os.WIFEXITED(status):
                return 'Grading', res[0], usingMem
            
            exitCode = os.WEXITSTATUS(status)
            
            # 종료 코드에 따라 return
            if  exitCode is 24:
                return ENUMResources.const.TIME_OVER, res[0], usingMem
            
            elif exitCode is not 5 and exitCode is not 0 and exitCode is not 17:
                return ENUMResources.const.RUNTIME_ERROR, 0, 0 
            
            elif os.WIFSIGNALED(status):
                try:
                    ptrace.kill(pid)
                except Exception as e:
                    pass
                
                return ENUMResources.const.RUNTIME_ERROR, 0, 0
            
            # 메모리 사용량 측정
            else:
                usingMem = self.getUsingMemory(pid, usingMem, res[6])
                
                ptrace.syscall(pid, 0)
                
    # 메모리 사용량 측정
    def getUsingMemory(self, pid, usingMem, minflt):
        # 프로세스 임시파일 접근
        procFileOpenCommand = "%s%i%s" % (FileNameNPathResources.const.ProcessDirName,
                                          pid,
                                          FileNameNPathResources.const.ProcessStatusFileName) 
        fileLines = FileTools.readFileLines(procFileOpenCommand)
        split = string.split

        # 물리 메모리 측정
        for i in xrange(14,19):
            index = fileLines[i].find('VmRSS')
            if index != -1:
                words = split(fileLines[i])
                temp = int(words[index+1])
                break;
        
        if temp > usingMem:
            usingMem = temp
        
        return usingMem
    
    def sigHandler(self, sig, f):
        pass
