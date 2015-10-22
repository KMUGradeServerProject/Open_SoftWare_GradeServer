# -*- coding: utf-8 -*-
import os
import glob
import string
import logging
from FileTools import FileTools
from gradingResource.listResources import ListResources
from gradingResource.fileNameNPathResources import FileNameNPathResources

class ParameterSetting(object):
    def __init__(self, args):
        self.filePath = args[1]
        self.problemPath = args[2]
        self.saveDirectoryName = args[3]
        self.gradeMethod = args[4]
        self.caseCount = int(args[5])
        self.limitTime = int(args[6])
        self.limitMemory = int(args[7])
        self.usingLang = args[8]
        self.version = args[9]
        self.problemName = args[10]
        
        self.answerPath = "%s%s%s%s%s%s" % (self.problemPath,
                                            FileNameNPathResources.const.FileSeparator,
                                            self.problemName, '_',
                                            self.gradeMethod,
                                            FileNameNPathResources.const.FileSeparator)
        
        # make execution file name
        try:
            os.mkdir(self.saveDirectoryName)
        except Exception:
            FileTools.saveResult(ENUMResources.const.SERVER_ERROR, 0, 0, 0)
            sys.exit()
            
        self.filePath = "%s%s" % (self.filePath,
                                  FileNameNPathResources.const.FileSeparator)
        self.runFileName = self.makeRunFileName()
        
        os.chdir(self.saveDirectoryName)
        
        logging.debug(self.saveDirectoryName + ' parameter setting')
        
    def makeRunFileName(self):
        if self.usingLang != ListResources.const.Lang_PYTHON:
            return FileNameNPathResources.const.DefaultFileName
        
        fileExtention = ''
        if self.usingLang == ListResources.const.Lang_PYTHON:
            fileExtention = '.py'
            
        fileList = glob.glob(self.filePath + FileNameNPathResources.const.AllFile
                             + fileExtention)
        
        if len(fileList) > 1:
            return FileNameNPathResources.const.DefaultFileName + fileExtention
        
        split = string.split
        name = split(fileList[0], FileNameNPathResources.const.FileSeparator)
        return split(name[-1], FileNameNPathResources.const.Dot)[0] + fileExtention
