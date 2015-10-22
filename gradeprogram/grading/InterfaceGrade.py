# -*- coding: utf-8 -*-
import sys
import logging
import CompileTools
from FileTools import FileTools
from grading import GradingTools
from grading import ExecutionTools
from grading import ParameterSetting
from Languages import C_Command
from Languages import CPP_Command
from Languages import JAVA_Command
from Languages import PYTHON2_Command
from Languages import PYTHON3_Command
from gradingResource.listResources import ListResources

"""
명령행 인수를 정리하고 메인에서 컴파일, 실행, 채점에 접근하기 위한 인터페이스 class
"""

class InterfaceGrade(object):
    def __init__(self, args):
        # 명령행 인수 정리 및 실행 파일명 설정
        self.parameter = ParameterSetting.ParameterSetting(args)
        
        # 언어별 객체 생성
        if self.parameter.usingLang == ListResources.const.Lang_C:
            self.command = C_Command.C_Command(self.parameter.runFileName)
        elif self.parameter.usingLang == ListResources.const.Lang_CPP:
            self.command = CPP_Command.CPP_Command(self.parameter.runFileName)
        elif self.parameter.usingLang == ListResources.const.Lang_JAVA:
            self.command = JAVA_Command.JAVA_Command(self.parameter.runFileName)
        else:
            if self.parameter.version == ListResources.const.PYTHON_VERSION_TWO:
                self.command = PYTHON2_Command.PYTHON2_Command(self.parameter.runFileName)
            else:
                self.command = PYTHON3_Command.PYTHON3_Command(self.parameter.runFileName)
        
        # 컴파일
    def compile(self):
        logging.debug(self.parameter.saveDirectoryName + ' compile start')
        
        # 컴파일 객체 생성 후 컴파일 진행
        _compile = CompileTools.CompileTools(self.parameter, self.command)
        success = _compile.compileCode()
        
        logging.debug(self.parameter.saveDirectoryName + ' compile end')
        
        return success
        
        # 실행 및 채점
    def evaluation(self):
        score = 0
        logging.debug(self.parameter.saveDirectoryName + ' execution start')
        
        # 프로그램 실행 객체 생성 후 프로그램 실행
        execution = ExecutionTools.ExecutionTools(self.parameter, self.command)
        success, runTime, usingMem = execution.execution()
        
        logging.debug(self.parameter.saveDirectoryName + ' execution end')
        
        # 정상적으로 시행된 경우
        if success == 'Grading':
            logging.debug(self.parameter.saveDirectoryName + ' grade start')
            #채점 객체 생성 후 채점
            evaluation = GradingTools.GradingTools(self.parameter, self.command)
            success, score = evaluation.grade()
            
            logging.debug(self.parameter.saveDirectoryName + ' grade end')
            
            #채점 완료 후 프로그램 종료
        FileTools.saveResult(success, score, runTime, usingMem)
