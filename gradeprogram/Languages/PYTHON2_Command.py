# -*- coding: utf-8 -*-
from Language import Language

class PYTHON2_Command(Language):
    def __init__(self, runFileName):
        Language.__init__(self, runFileName)
        
    def CompileCommand(self):
        return 'PYTHON'
        
    def ExecuteCommand(self):
        runCommandList = []
        append = runCommandList.append
        
        append('/usr/bin/python')
        append('/usr/bin/python')
        append(self.runFileName)
            
        return runCommandList