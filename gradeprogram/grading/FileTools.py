# -*- coding: utf-8 -*-
import os
import sys
import logging
from shutil import copyfile, copy
from gradingResource.enumResources import ENUMResources

"""
파일 관련 method들을 모아놓은 wrapping class
파일 복사, 입/출력에 관한 것들을 method로 정의
"""

class FileTools(object):
    # 파일에서 모든 라인 리스트로 반환
    @staticmethod
    def readFileLines(fileName):
        try:
            readFile = open(fileName, 'r')
        except Exception as e:
            logging.debug(e)
            logging.info('file error : ' + fileName + ' read error')
            
            saveResult(ENUMResources.const.SERVER_ERROR, 0, 0, 0)
            sys.exit()
        
        lines = readFile.readlines()
        readFile.close()
        
        return lines
    
    # 파일을 전체를 스트링으로 반환
    @staticmethod
    def readFileAll(fileName):
        try:
            readFile = open(fileName, 'r') # answer output open
        except Exception as e:
            logging.debug(e)
            logging.info('file error : ' + fileName + ' read error')
            
            saveResult(ENUMResources.const.SERVER_ERROR, 0, 0, 0)
            sys.exit()
        
        allFile = readFile.read()
        
        readFile.close()
        
        return allFile.strip('\r\n ')
    
    # 파일을 지정한 경로로 복사
    @staticmethod
    def copyFile(oldName, newName):
        try:
            if os.path.exists(newName):
                os.remove(newName)
            
            copyfile(oldName, newName)
        except Exception as e:
            logging.debug(e)
            logging.info('file error : ' + oldName + ' copy error')
            
            saveResult(ENUMResources.const.SERVER_ERROR, 0, 0, 0)
            sys.exit()
    
    # 리스트의 모든 파일을 지정한 경로로 복사    
    @staticmethod
    def copyAllFile(fileList, path):
        try:           
            for name in fileList:
                copy(name, path)
        except Exception as e:
            logging.debug(e)
            logging.info('file error : All file copy error')
            
            saveResult(ENUMResources.const.SERVER_ERROR, 0, 0, 0)
            sys.exit()

    # 결과 저장
    @staticmethod
    def saveResult(result, score, time, memory):
        try:
            fp = open('container.txt', 'w')
            fp.write(result + ' ' + str(score) + ' ' + str(time) + ' ' + str(memory))
            fp.close()
        except Exception:
            saveResult(ENUMResources.const.SERVER_ERROR, 0, 0, 0)
