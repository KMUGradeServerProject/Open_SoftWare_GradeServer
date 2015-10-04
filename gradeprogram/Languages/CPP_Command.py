# -*- coding: utf-8 -*-
from Language import Language

class CPP_Command(Language):
    def __init__(self, runFileName):
        Language.__init__(self, runFileName)
        
    def CompileCommand(self):
        return 'g++ *.cpp -o main -lm -w 2>message.txt'
        
    def ExecuteCommand(self):
        runCommandList = []
        append = runCommandList.append
        
        append('./main')
        append('./main')
        append('')
            
        return runCommandList