# -*- coding: utf-8 -*-
from Language import Language

class PYTHON3_Command(Language):
    def __init__(self, runFileName):
        Language.__init__(self, runFileName)
        
    def CompileCommand(self):
        return 'PYTHON'
        
    def ExecuteCommand(self):
        runCommandList = []
        append = runCommandList.append

        append('/usr/local/bin/python3')
        append('/usr/local/bin/python3')
        append(self.runFileName)
            
        return runCommandList