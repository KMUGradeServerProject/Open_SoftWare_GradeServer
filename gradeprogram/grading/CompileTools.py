# -*- coding: utf-8 -*-
import os
import sys
import glob
import logging
from subprocess import call
from FileTools import FileTools
from gradingResource.enumResources import ENUMResources
from gradingResource.listResources import ListResources
from gradingResource.fileNameNPathResources import FileNameNPathResources

"""
코드를 웹 서버로부터 복사한 후 컴파일 하는 class
파이썬 코드는 복사 후 컴파일을 하지 않음
"""

class CompileTools(object):
    def __init__(self, parameter, command):
        self.filePath = parameter.filePath
        self.runFileName = parameter.runFileName
        self.command = command
        self.usingLang = parameter.usingLang
        
        # 컴파일
    def compileCode(self):
        # 제출 파일 복사
        fileList = glob.glob(self.filePath + FileNameNPathResources.const.AllFile)
        
        if len(fileList) is 0:
            print ENUMResources.const.SERVER_ERROR, 0, 0, 0
            sys.exit()
            
        FileTools.copyAllFile(fileList, os.getcwd())
            
        # 컴파일 명령어 설정
        command = self.command.CompileCommand()
        
        if command == 'PYTHON':
            return True
        
        # 컴파일
        logging.debug('compile')
        call(command, shell = True)
        
        # 컴파일 에러 확인
        if os.path.exists(self.runFileName) or os.path.exists(self.runFileName + '.class'):
            return True
        
        elif os.path.getsize(FileNameNPathResources.const.MessageFile) > 0:
            print ENUMResources.const.COMPILE_ERROR, 0, 0, 0
            sys.exit()
        
        else:
            print ENUMResources.const.SERVER_ERROR, 0, 0, 0
            sys.exit()